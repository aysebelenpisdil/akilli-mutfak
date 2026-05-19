import { describe, it, expect } from 'vitest';
import { filterRecipes, getActiveFilterLabels } from '../utils/recipeFilter';
import type { RecipeWithMatch } from '../types';

const noPref = {
    vegan: false, vegetarian: false, glutenFree: false, dairyFree: false, nutAllergy: false,
};

function makeRecipe(overrides: Partial<RecipeWithMatch> = {}): RecipeWithMatch {
    return {
        Title: 'Test Tarif',
        Ingredients: "['domates', 'soğan']",
        Instructions: 'test',
        Image_Name: 'test',
        Cleaned_Ingredients: "['domates', 'soğan']",
        matchingCount: 1,
        matchingIngredients: ['domates'],
        ...overrides,
    };
}

// ── filterRecipes ─────────────────────────────────────────────────────────────

describe('filterRecipes', () => {
    it('tercih yok → tüm tarifler döner', () => {
        const recipes = [makeRecipe(), makeRecipe({ Title: 'Tarif 2' })];
        expect(filterRecipes(recipes, noPref, [], undefined)).toHaveLength(2);
    });

    it('boş liste ile boş liste döner', () => {
        expect(filterRecipes([], noPref, [], undefined)).toHaveLength(0);
    });

    it('vegan filtresi et içeren tarifi kaldırır', () => {
        const etliTarif = makeRecipe({
            Title: 'Etli Tarif',
            Cleaned_Ingredients: "['kıyma', 'soğan']",
        });
        const result = filterRecipes([etliTarif], { ...noPref, vegan: true }, [], undefined);
        expect(result).toHaveLength(0);
    });

    it('vegan filtresi et içermeyen tarifi bırakır', () => {
        const vegTarif = makeRecipe({
            Title: 'Vegan Tarif',
            Cleaned_Ingredients: "['nohut', 'domates']",
        });
        const result = filterRecipes([vegTarif], { ...noPref, vegan: true }, [], undefined);
        expect(result).toHaveLength(1);
    });

    it('hariç tutulan malzeme tarifi kaldırır', () => {
        const recipe = makeRecipe({ Cleaned_Ingredients: "['fıstık', 'domates']" });
        const result = filterRecipes([recipe], noPref, ['fıstık'], undefined);
        expect(result).toHaveLength(0);
    });

    it('hariç tutulan malzeme ilgisiz tarifi kaldırmaz', () => {
        const recipe = makeRecipe({ Cleaned_Ingredients: "['domates', 'soğan']" });
        const result = filterRecipes([recipe], noPref, ['fıstık'], undefined);
        expect(result).toHaveLength(1);
    });

    it('kalori max filtresi yüksek kalorili tarifi kaldırır', () => {
        const recipe = makeRecipe({ estimatedCalories: 900 });
        const result = filterRecipes([recipe], noPref, [], { max: 400 });
        expect(result).toHaveLength(0);
    });

    it('kalori max filtresi düşük kalorili tarifi bırakır', () => {
        const recipe = makeRecipe({ estimatedCalories: 300 });
        const result = filterRecipes([recipe], noPref, [], { max: 400 });
        expect(result).toHaveLength(1);
    });

    it('estimatedCalories yoksa kalori filtresi uygulanmaz', () => {
        const recipe = makeRecipe(); // no estimatedCalories
        const result = filterRecipes([recipe], noPref, [], { max: 100 });
        expect(result).toHaveLength(1);
    });

    it('glutenFree filtresi buğday içeren tarifi kaldırır', () => {
        const recipe = makeRecipe({ Cleaned_Ingredients: "['buğday unu', 'su']" });
        const result = filterRecipes([recipe], { ...noPref, glutenFree: true }, [], undefined);
        expect(result).toHaveLength(0);
    });

    it('nutAllergy filtresi fındık içeren tarifi kaldırır', () => {
        const recipe = makeRecipe({ Cleaned_Ingredients: "['fındık', 'şeker']" });
        const result = filterRecipes([recipe], { ...noPref, nutAllergy: true }, [], undefined);
        expect(result).toHaveLength(0);
    });
});

// ── getActiveFilterLabels ─────────────────────────────────────────────────────

describe('getActiveFilterLabels', () => {
    it('tercih yok → boş liste', () => {
        expect(getActiveFilterLabels(noPref, [], undefined)).toHaveLength(0);
    });

    it('vegan aktif → "Vegan" etiketi çıkar', () => {
        const labels = getActiveFilterLabels({ ...noPref, vegan: true }, [], undefined);
        expect(labels).toContain('Vegan');
    });

    it('glutenFree aktif → etiket çıkar', () => {
        const labels = getActiveFilterLabels({ ...noPref, glutenFree: true }, [], undefined);
        expect(labels.some(l => l.toLowerCase().includes('gluten'))).toBe(true);
    });

    it('vegan true iken vegetarian etiketi çıkmaz', () => {
        const labels = getActiveFilterLabels(
            { ...noPref, vegan: true, vegetarian: true }, [], undefined
        );
        expect(labels).toContain('Vegan');
        expect(labels).not.toContain('Vejetaryen');
    });

    it('hariç malzeme → ilk 3 görünür', () => {
        const labels = getActiveFilterLabels(noPref, ['a', 'b', 'c'], undefined);
        expect(labels.some(l => l.includes('hariç'))).toBe(true);
    });

    it('3\'ten fazla hariç malzeme → +N daha gösterilir', () => {
        const labels = getActiveFilterLabels(noPref, ['a', 'b', 'c', 'd', 'e'], undefined);
        expect(labels.some(l => l.includes('+'))).toBe(true);
    });
});
