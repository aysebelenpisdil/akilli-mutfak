import React, { createContext, useContext, useState, useEffect, useRef, useCallback, useMemo, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { getShoppingList, saveShoppingList, ShoppingListItem } from '../utils/api';

interface ShoppingListContextType {
    items: ShoppingListItem[];
    addItem: (name: string, displayName?: string, fromRecipe?: string) => void;
    addItemsFromRecipe: (recipeTitle: string, missingIngredients: string[]) => number;
    removeItem: (name: string) => void;
    togglePurchased: (name: string) => void;
    clearPurchased: () => void;
    clearAll: () => void;
    totalCount: number;
    pendingCount: number;
    isItemInList: (name: string) => boolean;
}

const STORAGE_KEY = 'shoppingListItems';
const normalize = (s: string) => s.trim().toLowerCase();

function safeParseItems(raw: string | null): ShoppingListItem[] {
    if (!raw) return [];
    try {
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    } catch {
        return [];
    }
}

function _applyIngredient(next: ShoppingListItem[], ing: string, recipeTitle: string): boolean {
    const key = normalize(ing);
    const idx = next.findIndex(i => i.name === key);
    if (idx >= 0) {
        if (!next[idx].from_recipes.includes(recipeTitle)) {
            next[idx] = { ...next[idx], from_recipes: [...next[idx].from_recipes, recipeTitle] };
        }
        return false;
    }
    next.push({ name: key, display_name: ing.trim(), purchased: false, from_recipes: [recipeTitle] });
    return true;
}

const ShoppingListContext = createContext<ShoppingListContextType | undefined>(undefined);

export const ShoppingListProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { user } = useAuth();
    const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const skipSaveRef = useRef(false);

    const [items, setItems] = useState<ShoppingListItem[]>(() =>
        safeParseItems(localStorage.getItem(STORAGE_KEY))
    );

    const mergeItems = (a: ShoppingListItem[], b: ShoppingListItem[]): ShoppingListItem[] => {
        const map = new Map<string, ShoppingListItem>();
        [...a, ...b].forEach(it => {
            const key = normalize(it.name);
            const existing = map.get(key);
            if (existing) {
                existing.from_recipes = Array.from(new Set([...existing.from_recipes, ...it.from_recipes]));
                // purchased=true only if both sides agree
                existing.purchased = existing.purchased && it.purchased;
            } else {
                map.set(key, { ...it, name: key });
            }
        });
        return Array.from(map.values());
    };

    // Login: merge anonymous localStorage list with remote DB list
    useEffect(() => {
        if (user) {
            (async () => {
                const local = safeParseItems(localStorage.getItem(STORAGE_KEY));
                const { items: remote } = await getShoppingList();
                const merged = mergeItems(local, remote);
                setItems(merged);
                localStorage.removeItem(STORAGE_KEY);
                // merged result intentionally written back to DB (skipSaveRef stays false)
            })().catch(() => {});
        } else {
            const saved = localStorage.getItem(STORAGE_KEY);
            // Login sırasında localStorage temizlenir; çıkışta boş localStorage
            // görünce setItems([]) çağırmak DB listesini sıfırlar — bu yüzden
            // sadece localStorage'da veri varsa yükle, yoksa state'i koru.
            if (saved) setItems(safeParseItems(saved));
        }
    }, [user?.id]);

    // Persist: localStorage for anonymous, debounced API for logged-in
    useEffect(() => {
        if (!user) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
            return;
        }
        if (skipSaveRef.current) {
            skipSaveRef.current = false;
            return;
        }
        if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
        saveTimeoutRef.current = setTimeout(() => {
            saveShoppingList(items).catch(() => {});
        }, 500);
        return () => { if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current); };
    }, [user?.id, items]);

    const addItem = useCallback((name: string, displayName?: string, fromRecipe?: string) => {
        const key = normalize(name);
        if (!key) return;
        setItems(prev => {
            const idx = prev.findIndex(i => i.name === key);
            if (idx >= 0) {
                if (!fromRecipe || prev[idx].from_recipes.includes(fromRecipe)) return prev;
                const next = [...prev];
                next[idx] = { ...next[idx], from_recipes: [...next[idx].from_recipes, fromRecipe] };
                return next;
            }
            return [...prev, {
                name: key,
                display_name: displayName ?? name.trim(),
                purchased: false,
                from_recipes: fromRecipe ? [fromRecipe] : [],
            }];
        });
    }, []);

    // Single setItems call to avoid race conditions with multiple ingredients
    const addItemsFromRecipe = useCallback((recipeTitle: string, missingIngredients: string[]): number => {
        let added = 0;
        setItems(prev => {
            const next = [...prev];
            missingIngredients.forEach(ing => {
                if (_applyIngredient(next, ing, recipeTitle)) added++;
            });
            return next;
        });
        return added;
    }, []);

    const removeItem = useCallback((name: string) =>
        setItems(prev => prev.filter(i => i.name !== normalize(name))), []);

    const togglePurchased = useCallback((name: string) =>
        setItems(prev => prev.map(i => i.name === normalize(name) ? { ...i, purchased: !i.purchased } : i)), []);

    const clearPurchased = useCallback(() => setItems(prev => prev.filter(i => !i.purchased)), []);
    const clearAll = useCallback(() => setItems([]), []);

    const isItemInList = useCallback((name: string) => items.some(i => i.name === normalize(name)), [items]);
    const pendingCount = items.filter(i => !i.purchased).length;

    const contextValue = useMemo(() => ({
        items,
        addItem,
        addItemsFromRecipe,
        removeItem,
        togglePurchased,
        clearPurchased,
        clearAll,
        totalCount: items.length,
        pendingCount,
        isItemInList,
    }), [items, addItem, addItemsFromRecipe, removeItem, togglePurchased,
        clearPurchased, clearAll, pendingCount, isItemInList]);

    return (
        <ShoppingListContext.Provider value={contextValue}>
            {children}
        </ShoppingListContext.Provider>
    );
};

export const useShoppingList = () => {
    const ctx = useContext(ShoppingListContext);
    if (!ctx) throw new Error('useShoppingList must be used within ShoppingListProvider');
    return ctx;
};
