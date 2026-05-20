import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useShoppingList } from '../store/ShoppingListContext';
import { useFridge } from '../store/FridgeContext';
import { useIngredientSearch } from '../hooks/useIngredientSearch';
import type { ShoppingListItem } from '../utils/api';

const ShoppingListPage: React.FC = () => {
    const { items, addItem, removeItem, togglePurchased, clearPurchased, clearAll, pendingCount } = useShoppingList();
    const { addIngredient } = useFridge();
    const [query, setQuery] = useState('');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [isAdding, setIsAdding] = useState(false);
    const { suggestions } = useIngredientSearch(query, { maxResults: 8, minQueryLength: 1 });

    const pending = items.filter(i => !i.purchased);
    const purchased = items.filter(i => i.purchased);

    const handleSelectSuggestion = (name: string) => {
        addItem(name);
        setQuery('');
        setShowSuggestions(false);
    };

    const handleManualAdd = () => {
        if (query.trim() && !isAdding) {
            setIsAdding(true);
            addItem(query.trim(), query.trim());
            setQuery('');
            setShowSuggestions(false);
            setTimeout(() => setIsAdding(false), 400);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') handleManualAdd();
        if (e.key === 'Escape') setShowSuggestions(false);
    };

    const transferPurchasedToFridge = () => {
        purchased.forEach(p => addIngredient(p.display_name));
        clearPurchased();
    };

    const handleClearAll = () => {
        if (window.confirm('Alışveriş listesini tamamen temizlemek istediğinizden emin misiniz?')) {
            clearAll();
        }
    };

    return (
        <div className="max-w-2xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-1">Alışveriş Listesi</h1>
                <p className="text-sm text-gray-500">
                    {pendingCount > 0 ? `${pendingCount} alınacak` : 'Liste boş'}
                    {purchased.length > 0 && ` · ${purchased.length} alındı`}
                </p>
            </div>

            {/* Manual add search */}
            <div className="relative mb-6">
                <div className="flex gap-2">
                    <div className="relative flex-1">
                        <input
                            type="text"
                            value={query}
                            onChange={e => { setQuery(e.target.value); setShowSuggestions(true); }}
                            onFocus={() => setShowSuggestions(true)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ürün ara veya ekle..."
                            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                        />
                        {showSuggestions && query.trim().length > 0 && suggestions.length > 0 && (
                            <ul className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-52 overflow-y-auto">
                                {suggestions.map(s => (
                                    <li key={s.name}>
                                        <button
                                            onMouseDown={() => handleSelectSuggestion(s.name)}
                                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-primary transition-colors"
                                        >
                                            {s.name}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    <button
                        onClick={handleManualAdd}
                        disabled={!query.trim() || isAdding}
                        className="px-4 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-secondary disabled:opacity-40 disabled:cursor-not-allowed transition-colors min-w-[4.5rem] flex items-center justify-center"
                    >
                        {isAdding ? (
                            <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                        ) : 'Ekle'}
                    </button>
                </div>
            </div>

            {/* Action bar */}
            {items.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-6">
                    {purchased.length > 0 && (
                        <button
                            onClick={transferPurchasedToFridge}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-green-100 text-green-800 hover:bg-green-200 rounded-lg transition-colors"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                            Satın alınanları buzdolabıma aktar
                        </button>
                    )}
                    {purchased.length > 0 && (
                        <button
                            onClick={clearPurchased}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-lg transition-colors"
                        >
                            Satın alınanları temizle
                        </button>
                    )}
                    <button
                        onClick={handleClearAll}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                    >
                        Tümünü temizle
                    </button>
                </div>
            )}

            {/* Empty state */}
            {items.length === 0 && (
                <div className="text-center py-16 text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <p className="text-sm font-medium">Liste boş</p>
                    <p className="text-xs mt-1">
                        Tarif kartlarındaki sepet ikonuna veya tarif detayındaki butona tıklayarak eksik malzemeleri ekleyin.
                    </p>
                    <Link to="/recipes" className="mt-4 inline-block text-sm text-primary hover:underline">
                        Tariflere git →
                    </Link>
                </div>
            )}

            {/* Pending items */}
            {pending.length > 0 && (
                <section className="mb-6">
                    <h2 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-3">
                        Alınacaklar ({pending.length})
                    </h2>
                    <ul className="space-y-2">
                        {pending.map(item => (
                            <ShoppingRow key={item.name} item={item} onToggle={togglePurchased} onRemove={removeItem} />
                        ))}
                    </ul>
                </section>
            )}

            {/* Purchased items */}
            {purchased.length > 0 && (
                <section>
                    <h2 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-3">
                        Alındı ({purchased.length})
                    </h2>
                    <ul className="space-y-2">
                        {purchased.map(item => (
                            <ShoppingRow key={item.name} item={item} onToggle={togglePurchased} onRemove={removeItem} />
                        ))}
                    </ul>
                </section>
            )}
        </div>
    );
};

interface RowProps {
    item: ShoppingListItem;
    onToggle: (name: string) => void;
    onRemove: (name: string) => void;
}

const ShoppingRow: React.FC<RowProps> = ({ item, onToggle, onRemove }) => (
    <li className={`flex items-start gap-3 p-3 rounded-lg border transition-opacity ${
        item.purchased ? 'bg-gray-50 border-gray-200 opacity-60' : 'bg-white border-gray-200'
    }`}>
        <input
            type="checkbox"
            checked={item.purchased}
            onChange={() => onToggle(item.name)}
            className="mt-0.5 h-5 w-5 rounded border-gray-300 text-primary focus:ring-primary cursor-pointer"
        />
        <div className="flex-1 min-w-0">
            <span className={`font-medium text-sm ${item.purchased ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {item.display_name}
            </span>
            {item.from_recipes.length > 0 && (
                <div className="mt-1 flex flex-wrap gap-1">
                    {item.from_recipes.map(r => (
                        <Link
                            key={r}
                            to={`/recipe/${encodeURIComponent(r)}`}
                            className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors"
                        >
                            {r}
                        </Link>
                    ))}
                </div>
            )}
        </div>
        <button
            onClick={() => onRemove(item.name)}
            className="flex-shrink-0 text-gray-300 hover:text-red-500 transition-colors text-lg leading-none"
            title="Listeden kaldır"
        >
            ×
        </button>
    </li>
);

export default ShoppingListPage;
