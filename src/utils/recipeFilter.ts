/**
 * Recipe Filtering Utility
 * Filters recipes based on dietary preferences, excluded ingredients, and calorie range
 */

import { RecipeWithMatch } from '../types';
import { getAllForbiddenIngredients, DietaryPreferences } from './dietaryRules';
import { matchesExcludedIngredient } from './ingredientNormalizer';

export interface CalorieRange {
    min?: number;
    max?: number;
}

function _isCalorieOutOfRange(calories: number, range: CalorieRange): boolean {
    if (range.min !== undefined && calories < range.min) return true;
    if (range.max !== undefined && calories > range.max) return true;
    return false;
}

function _getCalorieLabel(range: CalorieRange): string | null {
    if (range.max !== undefined && range.max <= 400) return 'Düşük Kalorili';
    if (range.min !== undefined && range.min >= 400 && range.max !== undefined && range.max <= 700) return 'Orta Kalorili';
    if (range.min !== undefined && range.min > 700) return 'Yüksek Kalorili';
    return null;
}

function _buildExcludedLabels(excludedIngredients: string[]): string[] {
    const labels = excludedIngredients
        .slice(0, 3)
        .map(ing => `${ing.charAt(0).toUpperCase()}${ing.slice(1)} hariç`);
    if (excludedIngredients.length > 3) {
        labels.push(`+${excludedIngredients.length - 3} daha`);
    }
    return labels;
}

/**
 * Filter recipes based on dietary preferences, excluded ingredients, and calorie range
 */
export function filterRecipes(
    recipes: RecipeWithMatch[],
    dietaryPreferences: DietaryPreferences,
    excludedIngredients: string[],
    calorieRange?: CalorieRange
): RecipeWithMatch[] {
    const forbiddenIngredients = getAllForbiddenIngredients(dietaryPreferences, excludedIngredients);

    return recipes.filter(recipe => {
        const ingredientsString = recipe.Cleaned_Ingredients || recipe.Ingredients;

        if (excludedIngredients.length > 0 && matchesExcludedIngredient(ingredientsString, excludedIngredients)) {
            return false;
        }

        if (forbiddenIngredients.length > 0 && matchesExcludedIngredient(ingredientsString, forbiddenIngredients)) {
            return false;
        }

        if (calorieRange && recipe.estimatedCalories != null && _isCalorieOutOfRange(recipe.estimatedCalories, calorieRange)) {
            return false;
        }

        return true;
    });
}

/**
 * Get active filter labels for display
 */
export function getActiveFilterLabels(
    dietaryPreferences: DietaryPreferences,
    excludedIngredients: string[],
    calorieRange?: CalorieRange
): string[] {
    const labels: string[] = [];

    if (dietaryPreferences.vegan) labels.push('Vegan');
    if (dietaryPreferences.vegetarian && !dietaryPreferences.vegan) labels.push('Vejetaryen');
    if (dietaryPreferences.glutenFree) labels.push('Glutensiz');
    if (dietaryPreferences.dairyFree) labels.push('Süt Ürünü İçermez');
    if (dietaryPreferences.nutAllergy) labels.push('Kuruyemiş İçermez');

    if (calorieRange) {
        const calorieLabel = _getCalorieLabel(calorieRange);
        if (calorieLabel) labels.push(calorieLabel);
    }

    if (excludedIngredients.length > 0) {
        labels.push(..._buildExcludedLabels(excludedIngredients));
    }

    return labels;
}
