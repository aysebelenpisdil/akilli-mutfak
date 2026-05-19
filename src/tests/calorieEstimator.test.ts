import { describe, it, expect } from 'vitest';
import { estimateRecipeCalories, getCalorieLabel } from '../utils/calorieEstimator';

describe('getCalorieLabel', () => {
    it('300 kcal → Düşük', () => expect(getCalorieLabel(300)).toBe('Düşük'));
    it('500 kcal → Orta', () => expect(getCalorieLabel(500)).toBe('Orta'));
    it('800 kcal → Yüksek', () => expect(getCalorieLabel(800)).toBe('Yüksek'));

    it('sınır değer — Düşük/Orta geçiş', () => {
        // Etiketlerin hangi aralıkta olduğunu kalorimetreden öğreniyoruz
        const low = getCalorieLabel(1);
        const high = getCalorieLabel(10000);
        expect(low).toBe('Düşük');
        expect(high).toBe('Yüksek');
    });
});

describe('estimateRecipeCalories', () => {
    it('bilinen malzemelerden pozitif kalori döner', () => {
        const cal = estimateRecipeCalories("['tavuk', 'domates', 'soğan']");
        expect(cal).toBeGreaterThan(0);
    });

    it('boş liste ile null veya 0 döner', () => {
        const cal = estimateRecipeCalories("[]");
        expect(cal === null || cal === 0).toBe(true);
    });

    it('bilinmeyen malzeme ile null veya 0 döner', () => {
        const cal = estimateRecipeCalories("['xyz_bilinmeyen_malzeme_123']");
        expect(cal === null || cal === 0).toBe(true);
    });

    it('geçersiz string ile hata fırlatmaz', () => {
        expect(() => estimateRecipeCalories('GEÇERSIZ')).not.toThrow();
    });
});
