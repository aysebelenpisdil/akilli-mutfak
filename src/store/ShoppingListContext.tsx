import React, { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
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

const ShoppingListContext = createContext<ShoppingListContextType | undefined>(undefined);

export const ShoppingListProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { user } = useAuth();
    const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const skipSaveRef = useRef(false);

    const [items, setItems] = useState<ShoppingListItem[]>(() => {
        const saved = localStorage.getItem(STORAGE_KEY);
        return saved ? JSON.parse(saved) : [];
    });

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
                const local = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') as ShoppingListItem[];
                const { items: remote } = await getShoppingList();
                const merged = mergeItems(local, remote);
                setItems(merged);
                localStorage.removeItem(STORAGE_KEY);
                // merged result intentionally written back to DB (skipSaveRef stays false)
            })().catch(() => {});
        } else {
            const saved = localStorage.getItem(STORAGE_KEY);
            setItems(saved ? JSON.parse(saved) : []);
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

    const addItem = (name: string, displayName?: string, fromRecipe?: string) => {
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
    };

    // Single setItems call to avoid race conditions with multiple ingredients
    const addItemsFromRecipe = (recipeTitle: string, missingIngredients: string[]): number => {
        let added = 0;
        setItems(prev => {
            const next = [...prev];
            missingIngredients.forEach(ing => {
                const key = normalize(ing);
                const idx = next.findIndex(i => i.name === key);
                if (idx >= 0) {
                    if (!next[idx].from_recipes.includes(recipeTitle)) {
                        next[idx] = { ...next[idx], from_recipes: [...next[idx].from_recipes, recipeTitle] };
                    }
                } else {
                    added++;
                    next.push({ name: key, display_name: ing.trim(), purchased: false, from_recipes: [recipeTitle] });
                }
            });
            return next;
        });
        return added;
    };

    const removeItem = (name: string) =>
        setItems(prev => prev.filter(i => i.name !== normalize(name)));

    const togglePurchased = (name: string) =>
        setItems(prev => prev.map(i => i.name === normalize(name) ? { ...i, purchased: !i.purchased } : i));

    const clearPurchased = () => setItems(prev => prev.filter(i => !i.purchased));
    const clearAll = () => setItems([]);

    const isItemInList = (name: string) => items.some(i => i.name === normalize(name));
    const pendingCount = items.filter(i => !i.purchased).length;

    return (
        <ShoppingListContext.Provider value={{
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
        }}>
            {children}
        </ShoppingListContext.Provider>
    );
};

export const useShoppingList = () => {
    const ctx = useContext(ShoppingListContext);
    if (!ctx) throw new Error('useShoppingList must be used within ShoppingListProvider');
    return ctx;
};
