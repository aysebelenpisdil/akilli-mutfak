import React, { createContext, useContext, useState, useEffect, useRef, useCallback, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { getFridgeIngredients, saveFridgeIngredients, getPreferences, savePreferences } from '../utils/api';

export interface DietaryPreferences {
    glutenFree: boolean;
    vegetarian: boolean;
    vegan: boolean;
    dairyFree: boolean;
    nutAllergy: boolean;
    [key: string]: boolean;
}

interface FridgeContextType {
    fridgeIngredients: string[];
    addIngredient: (ingredient: string) => void;
    removeIngredient: (ingredient: string) => void;
    dietaryPreferences: DietaryPreferences;
    setDietaryPreferences: (prefs: DietaryPreferences) => void;
    excludedIngredients: string[];
    toggleExcludedIngredient: (ingredient: string) => void;
}

const FridgeContext = createContext<FridgeContextType | undefined>(undefined);

export const FridgeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { user } = useAuth();
    const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const prefSaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    // Prevent save-on-fetch race: set true before setFridgeIngredients/setPrefs calls
    const skipFridgeSaveRef = useRef(false);
    const skipPrefsSaveRef = useRef(false);

    const DEFAULT_DIETARY: DietaryPreferences = {
        glutenFree: false, vegetarian: false, vegan: false,
        dairyFree: false, nutAllergy: false,
    };

    const [fridgeIngredients, setFridgeIngredients] = useState<string[]>(() => {
        const saved = localStorage.getItem('fridgeIngredients');
        return saved ? JSON.parse(saved) : [];
    });

    const [dietaryPreferences, setDietaryPreferencesState] = useState<DietaryPreferences>(() => {
        const saved = localStorage.getItem('dietaryPreferences');
        return saved ? JSON.parse(saved) : DEFAULT_DIETARY;
    });

    const [excludedIngredients, setExcludedIngredients] = useState<string[]>(() => {
        const saved = localStorage.getItem('excludedIngredients');
        return saved ? JSON.parse(saved) : [];
    });

    const fetchFridgeFromApi = useCallback(async () => {
        skipFridgeSaveRef.current = true; // set BEFORE state update so save effect skips
        try {
            const { ingredients } = await getFridgeIngredients();
            setFridgeIngredients(ingredients);
        } catch {
            skipFridgeSaveRef.current = false;
            setFridgeIngredients([]);
        }
    }, []);

    const fetchPreferencesFromApi = useCallback(async () => {
        skipPrefsSaveRef.current = true;
        try {
            const { dietary, excluded } = await getPreferences();
            if (Object.keys(dietary).length > 0) {
                setDietaryPreferencesState({ ...DEFAULT_DIETARY, ...dietary } as DietaryPreferences);
            }
            setExcludedIngredients(excluded);
        } catch {
            skipPrefsSaveRef.current = false;
        }
    }, []);

    useEffect(() => {
        if (user) {
            fetchFridgeFromApi();
            fetchPreferencesFromApi();
        } else {
            const saved = localStorage.getItem('fridgeIngredients');
            setFridgeIngredients(saved ? JSON.parse(saved) : []);
        }
    }, [user?.id, fetchFridgeFromApi, fetchPreferencesFromApi]);

    useEffect(() => {
        if (!user) {
            localStorage.setItem('fridgeIngredients', JSON.stringify(fridgeIngredients));
            return;
        }
        if (skipFridgeSaveRef.current) {
            skipFridgeSaveRef.current = false;
            return; // data just fetched from DB — no need to write it back
        }
        if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
        saveTimeoutRef.current = setTimeout(() => {
            saveFridgeIngredients(fridgeIngredients).catch(() => {});
            saveTimeoutRef.current = null;
        }, 500);
        return () => {
            if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
        };
    }, [user?.id, fridgeIngredients]);

    useEffect(() => {
        if (!user) {
            localStorage.setItem('dietaryPreferences', JSON.stringify(dietaryPreferences));
            localStorage.setItem('excludedIngredients', JSON.stringify(excludedIngredients));
            return;
        }
        if (skipPrefsSaveRef.current) {
            skipPrefsSaveRef.current = false;
            return;
        }
        if (prefSaveTimeoutRef.current) clearTimeout(prefSaveTimeoutRef.current);
        prefSaveTimeoutRef.current = setTimeout(() => {
            savePreferences({ dietary: dietaryPreferences, excluded: excludedIngredients }).catch(() => {});
            prefSaveTimeoutRef.current = null;
        }, 500);
        return () => {
            if (prefSaveTimeoutRef.current) clearTimeout(prefSaveTimeoutRef.current);
        };
    }, [user?.id, dietaryPreferences, excludedIngredients]);

    const addIngredient = (ingredient: string) => {
        if (!fridgeIngredients.includes(ingredient)) {
            setFridgeIngredients([...fridgeIngredients, ingredient]);
        }
    };

    const removeIngredient = (ingredient: string) => {
        setFridgeIngredients(fridgeIngredients.filter(i => i !== ingredient));
    };

    const setDietaryPreferences = (prefs: DietaryPreferences) => {
        setDietaryPreferencesState(prefs);
    };

    const toggleExcludedIngredient = (ingredient: string) => {
        if (excludedIngredients.includes(ingredient)) {
            setExcludedIngredients(excludedIngredients.filter(i => i !== ingredient));
        } else {
            setExcludedIngredients([...excludedIngredients, ingredient]);
        }
    };

    return (
        <FridgeContext.Provider value={{ 
            fridgeIngredients, 
            addIngredient, 
            removeIngredient,
            dietaryPreferences,
            setDietaryPreferences,
            excludedIngredients,
            toggleExcludedIngredient
        }}>
            {children}
        </FridgeContext.Provider>
    );
};

export const useFridge = () => {
    const context = useContext(FridgeContext);
    if (!context) {
        throw new Error('useFridge must be used within a FridgeProvider');
    }
    return context;
};
