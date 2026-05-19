/**
 * Shopping list core logic tests.
 * Tests the pure merge/normalize/dedupe functions without React dependencies.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

// ── Normalize helper (mirrors ShoppingListContext) ────────────────────────────
const normalize = (s: string) => s.trim().toLowerCase();

// ── Merge logic (mirrors ShoppingListContext.mergeItems) ──────────────────────
interface Item {
    name: string;
    display_name: string;
    purchased: boolean;
    from_recipes: string[];
}

function mergeItems(a: Item[], b: Item[]): Item[] {
    const map = new Map<string, Item>();
    [...a, ...b].forEach(it => {
        const key = normalize(it.name);
        const existing = map.get(key);
        if (existing) {
            existing.from_recipes = Array.from(new Set([...existing.from_recipes, ...it.from_recipes]));
            existing.purchased = existing.purchased && it.purchased;
        } else {
            map.set(key, { ...it, name: key });
        }
    });
    return Array.from(map.values());
}

function addItemsFromRecipe(prev: Item[], recipeTitle: string, missingIngredients: string[]): Item[] {
    const next = [...prev];
    missingIngredients.forEach(ing => {
        const key = normalize(ing);
        const idx = next.findIndex(i => i.name === key);
        if (idx >= 0) {
            if (!next[idx].from_recipes.includes(recipeTitle)) {
                next[idx] = { ...next[idx], from_recipes: [...next[idx].from_recipes, recipeTitle] };
            }
        } else {
            next.push({ name: key, display_name: ing.trim(), purchased: false, from_recipes: [recipeTitle] });
        }
    });
    return next;
}

// ── normalize ─────────────────────────────────────────────────────────────────

describe('normalize', () => {
    it('küçük harfe çevirir', () => expect(normalize('DOMATES')).toBe('domates'));
    it('baştaki ve sondaki boşlukları temizler', () => expect(normalize('  soğan  ')).toBe('soğan'));
    it('boş string boş kalır', () => expect(normalize('')).toBe(''));
});

// ── mergeItems ────────────────────────────────────────────────────────────────

describe('mergeItems', () => {
    it('farklı malzemeler birleşir', () => {
        const a: Item[] = [{ name: 'domates', display_name: 'Domates', purchased: false, from_recipes: [] }];
        const b: Item[] = [{ name: 'biber', display_name: 'Biber', purchased: false, from_recipes: [] }];
        const result = mergeItems(a, b);
        expect(result).toHaveLength(2);
    });

    it('aynı isimli malzeme tek satıra indirilir', () => {
        const a: Item[] = [{ name: 'soğan', display_name: 'Soğan', purchased: false, from_recipes: ['Tarif A'] }];
        const b: Item[] = [{ name: 'soğan', display_name: 'Soğan', purchased: false, from_recipes: ['Tarif B'] }];
        const result = mergeItems(a, b);
        expect(result).toHaveLength(1);
        expect(result[0].from_recipes).toContain('Tarif A');
        expect(result[0].from_recipes).toContain('Tarif B');
    });

    it('from_recipes duplicate recipe tag oluşmaz', () => {
        const a: Item[] = [{ name: 'tuz', display_name: 'Tuz', purchased: false, from_recipes: ['Tarif X'] }];
        const b: Item[] = [{ name: 'tuz', display_name: 'Tuz', purchased: false, from_recipes: ['Tarif X'] }];
        const result = mergeItems(a, b);
        expect(result[0].from_recipes.filter(r => r === 'Tarif X')).toHaveLength(1);
    });

    it('purchased sadece ikisi de true ise true kalır', () => {
        const a: Item[] = [{ name: 'un', display_name: 'Un', purchased: true, from_recipes: [] }];
        const b: Item[] = [{ name: 'un', display_name: 'Un', purchased: false, from_recipes: [] }];
        const result = mergeItems(a, b);
        expect(result[0].purchased).toBe(false);
    });

    it('her iki tarafta da purchased=true ise true kalır', () => {
        const a: Item[] = [{ name: 'seker', display_name: 'Şeker', purchased: true, from_recipes: [] }];
        const b: Item[] = [{ name: 'seker', display_name: 'Şeker', purchased: true, from_recipes: [] }];
        const result = mergeItems(a, b);
        expect(result[0].purchased).toBe(true);
    });

    it('büyük harf isimler normalize edilerek birleştirilir', () => {
        const a: Item[] = [{ name: 'DOMATES', display_name: 'Domates', purchased: false, from_recipes: ['A'] }];
        const b: Item[] = [{ name: 'domates', display_name: 'Domates', purchased: false, from_recipes: ['B'] }];
        const result = mergeItems(a, b);
        expect(result).toHaveLength(1);
        expect(result[0].name).toBe('domates');
    });

    it('boş listeler birleştirilirse boş liste döner', () => {
        expect(mergeItems([], [])).toHaveLength(0);
    });
});

// ── addItemsFromRecipe ────────────────────────────────────────────────────────

describe('addItemsFromRecipe', () => {
    it('yeni malzemeler eklenir', () => {
        const result = addItemsFromRecipe([], 'Karnıyarık', ['patlıcan', 'kıyma']);
        expect(result).toHaveLength(2);
        expect(result[0].from_recipes).toContain('Karnıyarık');
    });

    it('mevcut malzemeye yeni tarif tag\'i eklenir', () => {
        const prev: Item[] = [{ name: 'soğan', display_name: 'Soğan', purchased: false, from_recipes: ['Tarif A'] }];
        const result = addItemsFromRecipe(prev, 'Tarif B', ['soğan']);
        expect(result).toHaveLength(1);
        expect(result[0].from_recipes).toContain('Tarif A');
        expect(result[0].from_recipes).toContain('Tarif B');
    });

    it('aynı tariften ikinci kez ekleme idempotent', () => {
        const prev: Item[] = [{ name: 'tuz', display_name: 'Tuz', purchased: false, from_recipes: ['Tarif X'] }];
        const result = addItemsFromRecipe(prev, 'Tarif X', ['tuz']);
        expect(result[0].from_recipes.filter(r => r === 'Tarif X')).toHaveLength(1);
    });

    it('birden fazla malzeme aynı anda eklenebilir', () => {
        const result = addItemsFromRecipe([], 'Tarif', ['a', 'b', 'c']);
        expect(result).toHaveLength(3);
    });

    it('malzeme adı normalize edilir (büyük harf)', () => {
        const result = addItemsFromRecipe([], 'Tarif', ['PATLICAN']);
        expect(result[0].name).toBe('patlican');
    });

    it('boş malzeme listesi ile prev değişmez', () => {
        const prev: Item[] = [{ name: 'tuz', display_name: 'Tuz', purchased: false, from_recipes: [] }];
        const result = addItemsFromRecipe(prev, 'Tarif', []);
        expect(result).toHaveLength(1);
    });
});

// ── localStorage behaviour (simulated with in-memory mock) ───────────────────

describe('localStorage shopping list persistence', () => {
    const STORAGE_KEY = 'shoppingListItems';
    const store: Record<string, string> = {};

    const mockStorage = {
        getItem: (key: string) => store[key] ?? null,
        setItem: (key: string, val: string) => { store[key] = val; },
        removeItem: (key: string) => { delete store[key]; },
        clear: () => Object.keys(store).forEach(k => delete store[k]),
    };

    beforeEach(() => {
        vi.stubGlobal('localStorage', mockStorage);
        mockStorage.clear();
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it('liste localStorage\'a yazılır ve okunur', () => {
        const items: Item[] = [
            { name: 'domates', display_name: 'Domates', purchased: false, from_recipes: [] }
        ];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
        const read = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') as Item[];
        expect(read).toHaveLength(1);
        expect(read[0].name).toBe('domates');
    });

    it('liste silinince boş dizi döner', () => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify([{ name: 'tuz' }]));
        localStorage.removeItem(STORAGE_KEY);
        const read = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        expect(read).toHaveLength(0);
    });
});
