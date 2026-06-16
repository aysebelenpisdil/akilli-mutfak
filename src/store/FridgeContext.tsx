import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo, ReactNode } from 'react';
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

function safeParseStringList(key: string): string[] {
    try {
        const raw = localStorage.getItem(key);
        const parsed: unknown = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed.filter((i): i is string => typeof i === 'string') : [];
    } catch {
        return [];
    }
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

    const [fridgeIngredients, setFridgeIngredients] = useState<string[]>(() =>
        safeParseStringList('fridgeIngredients')
    );

    const [dietaryPreferences, setDietaryPreferencesState] = useState<DietaryPreferences>(() => {
        try {
            const raw = localStorage.getItem('dietaryPreferences');
            const parsed: unknown = raw ? JSON.parse(raw) : null;
            if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return DEFAULT_DIETARY;
            return { ...DEFAULT_DIETARY, ...Object.fromEntries(Object.entries(parsed as Record<string, unknown>).map(([k, v]) => [k, Boolean(v)])) } as DietaryPreferences;
        } catch {
            return DEFAULT_DIETARY;
        }
    });

    const [excludedIngredients, setExcludedIngredients] = useState<string[]>(() =>
        safeParseStringList('excludedIngredients')
    );

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
            setFridgeIngredients(safeParseStringList('fridgeIngredients'));
        }
    }, [user?.id, fetchFridgeFromApi, fetchPreferencesFromApi]);

    useEffect(() => {
        if (!user) {
            const sanitized = Array.isArray(fridgeIngredients) ? fridgeIngredients.filter(i => typeof i === 'string') : [];
            localStorage.setItem('fridgeIngredients', JSON.stringify(sanitized));
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
            const safeDietary = Object.fromEntries(Object.entries(dietaryPreferences).map(([k, v]) => [String(k), Boolean(v)]));
            localStorage.setItem('dietaryPreferences', JSON.stringify(safeDietary));
            const sanitizedExcluded = Array.isArray(excludedIngredients) ? excludedIngredients.filter(i => typeof i === 'string') : [];
            localStorage.setItem('excludedIngredients', JSON.stringify(sanitizedExcluded));
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

    const addIngredient = useCallback((ingredient: string) => {
        if (!fridgeIngredients.includes(ingredient)) {
            setFridgeIngredients([...fridgeIngredients, ingredient]);
        }
    }, [fridgeIngredients]);

    const removeIngredient = useCallback((ingredient: string) => {
        setFridgeIngredients(fridgeIngredients.filter(i => i !== ingredient));
    }, [fridgeIngredients]);

    const setDietaryPreferences = useCallback((prefs: DietaryPreferences) => {
        setDietaryPreferencesState(prefs);
    }, []);

    const toggleExcludedIngredient = useCallback((ingredient: string) => {
        if (excludedIngredients.includes(ingredient)) {
            setExcludedIngredients(excludedIngredients.filter(i => i !== ingredient));
        } else {
            setExcludedIngredients([...excludedIngredients, ingredient]);
        }
    }, [excludedIngredients]);

    const contextValue = useMemo(() => ({
        fridgeIngredients,
        addIngredient,
        removeIngredient,
        dietaryPreferences,
        setDietaryPreferences,
        excludedIngredients,
        toggleExcludedIngredient,
    }), [fridgeIngredients, addIngredient, removeIngredient, dietaryPreferences,
        setDietaryPreferences, excludedIngredients, toggleExcludedIngredient]);

    return (
        <FridgeContext.Provider value={contextValue}>
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
