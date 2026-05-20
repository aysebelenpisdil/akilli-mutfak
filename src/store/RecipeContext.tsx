import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useFridge } from './FridgeContext';
import { getRAGRecommendations, ApiError } from '../utils/api';
import { RecipeWithMatch } from '../types';
import { estimateRecipeCalories } from '../utils/calorieEstimator';
import type { CalorieRange } from '../utils/recipeFilter';

export type CalorieFilterKey = 'all' | 'low' | 'medium' | 'high';

export const CALORIE_RANGES: Record<CalorieFilterKey, CalorieRange | undefined> = {
    all: undefined,
    low: { max: 400 },
    medium: { min: 400, max: 700 },
    high: { min: 700 },
};

export const CALORIE_FILTER_LABELS: Record<CalorieFilterKey, string> = {
    all: 'Tümü',
    low: 'Düşük (<400)',
    medium: 'Orta (400-700)',
    high: 'Yüksek (>700)',
};

function enrichWithCalories(recipes: RecipeWithMatch[]): RecipeWithMatch[] {
    return recipes.map(r => ({
        ...r,
        estimatedCalories: r.estimatedCalories ?? estimateRecipeCalories(r.Cleaned_Ingredients),
    }));
}

interface RecipeContextType {
    rawRecipes: RecipeWithMatch[];
    loading: boolean;
    error: string | null;
    explanation: string | null;
    metadata: Record<string, unknown> | null;
    responseTime: number | null;
    calorieFilter: CalorieFilterKey;
    setCalorieFilter: (v: CalorieFilterKey) => void;
    page: number;
    loadMore: () => void;
    fetchRecipes: () => Promise<void>;
    hasSearched: boolean;
}

const RecipeContext = createContext<RecipeContextType | undefined>(undefined);

export const RecipeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { fridgeIngredients, dietaryPreferences, excludedIngredients } = useFridge();

    const [rawRecipes, setRawRecipes] = useState<RecipeWithMatch[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [explanation, setExplanation] = useState<string | null>(null);
    const [metadata, setMetadata] = useState<Record<string, unknown> | null>(null);
    const [responseTime, setResponseTime] = useState<number | null>(null);
    const [calorieFilter, setCalorieFilter] = useState<CalorieFilterKey>('all');
    const [page, setPage] = useState(1);
    const [hasSearched, setHasSearched] = useState(false);

    const fetchRecipes = async () => {
        setHasSearched(true);
        setPage(1);

        if (fridgeIngredients.length === 0) {
            setRawRecipes([]);
            setExplanation(null);
            setMetadata(null);
            return;
        }

        setLoading(true);
        setError(null);
        setResponseTime(null);
        setExplanation(null);
        setMetadata(null);

        try {
            const startTime = performance.now();
            const ragResponse = await getRAGRecommendations({
                ingredients: fridgeIngredients,
                preferences: dietaryPreferences,
                excluded_ingredients: excludedIngredients,
                explain: true,
                top_k: 50,
                retrieval_top_k: 100,
            });
            setResponseTime(Math.round(performance.now() - startTime));
            setRawRecipes(enrichWithCalories(ragResponse.recipes || []));
            setExplanation(ragResponse.explanation || null);
            setMetadata((ragResponse.metadata as unknown as Record<string, unknown>) || null);
        } catch (err) {
            setError((err as ApiError).message || 'Bir hata oluştu');
            setRawRecipes([]);
        } finally {
            setLoading(false);
        }
    };

    const loadMore = () => setPage(p => p + 1);

    return (
        <RecipeContext.Provider value={{
            rawRecipes, loading, error, explanation, metadata, responseTime,
            calorieFilter, setCalorieFilter,
            page, loadMore,
            fetchRecipes, hasSearched,
        }}>
            {children}
        </RecipeContext.Provider>
    );
};

export const useRecipes = () => {
    const ctx = useContext(RecipeContext);
    if (!ctx) throw new Error('useRecipes must be used within a RecipeProvider');
    return ctx;
};
