import { describe, it, expect } from 'vitest';
import {
    parseIngredientList,
    ingredientMatches,
    computeRecipeAvailability,
    getRecipeImageUrl,
} from '../utils/helpers';

// ── parseIngredientList ───────────────────────────────────────────────────────

describe('parseIngredientList', () => {
    it('boş string boş dizi döner', () => {
        expect(parseIngredientList('')).toEqual([]);
    });

    it('Python-stili tek tırnaklı liste parse edilir', () => {
        const result = parseIngredientList("['domates', 'soğan', 'biber']");
        expect(result).toEqual(['domates', 'soğan', 'biber']);
    });

    it('tek elemanlı liste çalışır', () => {
        expect(parseIngredientList("['tuz']")).toEqual(['tuz']);
    });

    it('geçersiz string boş dizi döner', () => {
        expect(parseIngredientList('geçersiz json {{{')).toEqual([]);
    });

    it('boşluklu malzeme isimlerini korur', () => {
        const result = parseIngredientList("['zeytinyağı', 'domates salçası']");
        expect(result).toContain('zeytinyağı');
        expect(result).toContain('domates salçası');
    });
});

// ── ingredientMatches ─────────────────────────────────────────────────────────

describe('ingredientMatches', () => {
    it('tam eşleşme döner true', () => {
        expect(ingredientMatches('domates', 'domates')).toBe(true);
    });

    it('büyük-küçük harf farkına duyarsız', () => {
        expect(ingredientMatches('Domates', 'domates')).toBe(true);
        expect(ingredientMatches('SOĞAN', 'soğan')).toBe(true);
    });

    it('Türkçe çekim eki toleransı (salçası → salça)', () => {
        expect(ingredientMatches('domates salçası', 'salça')).toBe(true);
    });

    it('Türkçe çekim eki toleransı (unu → un)', () => {
        expect(ingredientMatches('mısır unu', 'un')).toBe(true);
    });

    it('Türkçe çekim eki toleransı (eti → et)', () => {
        expect(ingredientMatches('kıyma eti', 'et')).toBe(true);
    });

    it('dolap malzemesi tarifi kapsamıyorsa false', () => {
        expect(ingredientMatches('domates', 'patlıcan')).toBe(false);
    });

    it('4+ harf fark yanlış eşleşme yaratmaz', () => {
        // "sut" (recipe) vs "sarımsak" (fridge) — startsWith yok ama yakın değil
        expect(ingredientMatches('sarımsak', 'süt')).toBe(false);
    });

    it('başında boşluk olan stringleri trim eder', () => {
        expect(ingredientMatches('  domates ', '  domates')).toBe(true);
    });
});

// ── computeRecipeAvailability ─────────────────────────────────────────────────

describe('computeRecipeAvailability', () => {
    const cleaned = ['domates', 'soğan', 'biber', 'patlıcan'];
    const fridge = ['domates', 'soğan'];

    it('eksik malzemeleri doğru hesaplar', () => {
        const result = computeRecipeAvailability(cleaned, fridge, []);
        expect(result.missing).toContain('biber');
        expect(result.missing).toContain('patlıcan');
        expect(result.missing).not.toContain('domates');
        expect(result.missing).not.toContain('soğan');
    });

    it('coveredCount ve totalCount doğru', () => {
        const result = computeRecipeAvailability(cleaned, fridge, []);
        expect(result.totalCount).toBe(4);
        expect(result.coveredCount).toBe(2);
    });

    it('isFullyAvailable tüm malzemeler mevcut ise true', () => {
        const result = computeRecipeAvailability(['tuz'], ['tuz'], []);
        expect(result.isFullyAvailable).toBe(true);
    });

    it('isFullyAvailable eksik varsa false', () => {
        const result = computeRecipeAvailability(['tuz', 'biber'], ['tuz'], []);
        expect(result.isFullyAvailable).toBe(false);
    });

    it('backendMatchingIngredients allMatching içine dahil edilir', () => {
        const result = computeRecipeAvailability(['domates'], ['domates'], ['backend-match']);
        expect(result.allMatching).toContain('backend-match');
    });

    it('boş tarif malzemeleri ile isFullyAvailable true döner', () => {
        const result = computeRecipeAvailability([], [], []);
        expect(result.isFullyAvailable).toBe(true);
        expect(result.missing).toHaveLength(0);
    });

    it('Türkçe ek toleransı missing hesaplamasında çalışır', () => {
        // Dolap: "domates salçası", Tarif: "salça" → eşleşmeli, missing olmamalı
        const result = computeRecipeAvailability(['salça'], ['domates salçası'], []);
        expect(result.missing).not.toContain('salça');
        expect(result.isFullyAvailable).toBe(true);
    });
});

// ── getRecipeImageUrl ─────────────────────────────────────────────────────────

describe('getRecipeImageUrl', () => {
    it('doğru URL formatı döner', () => {
        expect(getRecipeImageUrl('karniyarik')).toBe('images/recipies/karniyarik.jpg');
    });
});
