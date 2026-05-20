import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useFridge } from '../store/FridgeContext';
import { useAuth } from '../store/AuthContext';
import { useShoppingList } from '../store/ShoppingListContext';

const Navbar: React.FC = () => {
    const location = useLocation();
    const { fridgeIngredients } = useFridge();
    const { user, logout, logoutLoading } = useAuth();
    const { pendingCount } = useShoppingList();
    const [menuOpen, setMenuOpen] = useState(false);

    const isActive = (path: string) =>
        location.pathname === path
            ? 'text-primary font-bold bg-green-50'
            : 'text-gray-600 hover:text-primary hover:bg-green-50';

    const closeMenu = () => setMenuOpen(false);

    return (
        <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2 flex-shrink-0" onClick={closeMenu}>
                        <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold text-lg">
                            F
                        </div>
                        <span className="font-bold text-xl tracking-tight text-gray-900">Buzdolabı Şefi</span>
                    </Link>

                    {/* Desktop links */}
                    <div className="hidden md:flex items-center space-x-2">
                        <Link to="/" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/')}`}>
                            Buzdolabım
                            <span className="ml-2 bg-gray-100 text-gray-600 py-0.5 px-2 rounded-full text-xs">
                                {fridgeIngredients.length}
                            </span>
                        </Link>
                        <Link to="/recipes" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/recipes')}`}>
                            Tarifler
                        </Link>
                        <Link to="/preferences" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/preferences')}`}>
                            Tercihler
                        </Link>
                        <Link to="/shopping-list" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/shopping-list')}`}>
                            Alışveriş Listesi
                            {pendingCount > 0 && (
                                <span className="ml-2 bg-amber-100 text-amber-700 py-0.5 px-2 rounded-full text-xs">
                                    {pendingCount}
                                </span>
                            )}
                        </Link>
                        <div className="h-6 w-px bg-gray-200" />
                        {user ? (
                            <>
                                <Link to="/profile" className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${isActive('/profile')}`}>
                                    Profilim
                                </Link>
                                <button
                                    onClick={logout}
                                    disabled={logoutLoading}
                                    className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {logoutLoading && <svg className="animate-spin h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>}
                                    Çıkış
                                </button>
                            </>
                        ) : (
                            <Link to="/login" className="px-4 py-1.5 text-sm font-medium text-white bg-primary hover:bg-secondary rounded-md transition-colors">
                                Giriş Yap
                            </Link>
                        )}
                    </div>

                    {/* Mobile hamburger button */}
                    <button
                        className="md:hidden flex flex-col justify-center items-center w-10 h-10 gap-1.5 rounded-md hover:bg-gray-100 transition-colors"
                        onClick={() => setMenuOpen(!menuOpen)}
                        aria-label="Menü"
                    >
                        <span className={`block w-6 h-0.5 bg-gray-700 transition-transform ${menuOpen ? 'rotate-45 translate-y-2' : ''}`} />
                        <span className={`block w-6 h-0.5 bg-gray-700 transition-opacity ${menuOpen ? 'opacity-0' : ''}`} />
                        <span className={`block w-6 h-0.5 bg-gray-700 transition-transform ${menuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
                    </button>
                </div>
            </div>

            {/* Mobile dropdown menu */}
            {menuOpen && (
                <div className="md:hidden bg-white border-t border-gray-100 shadow-lg">
                    <div className="px-4 py-3 flex flex-col gap-1">
                        <Link to="/" onClick={closeMenu} className={`flex items-center justify-between px-3 py-3 rounded-md text-sm font-medium transition-colors ${isActive('/')}`}>
                            <span>Buzdolabım</span>
                            <span className="bg-gray-100 text-gray-600 py-0.5 px-2 rounded-full text-xs">
                                {fridgeIngredients.length}
                            </span>
                        </Link>
                        <Link to="/recipes" onClick={closeMenu} className={`px-3 py-3 rounded-md text-sm font-medium transition-colors ${isActive('/recipes')}`}>
                            Tarifler
                        </Link>
                        <Link to="/preferences" onClick={closeMenu} className={`px-3 py-3 rounded-md text-sm font-medium transition-colors ${isActive('/preferences')}`}>
                            Tercihler
                        </Link>
                        <Link to="/shopping-list" onClick={closeMenu} className={`flex items-center justify-between px-3 py-3 rounded-md text-sm font-medium transition-colors ${isActive('/shopping-list')}`}>
                            <span>Alışveriş Listesi</span>
                            {pendingCount > 0 && (
                                <span className="bg-amber-100 text-amber-700 py-0.5 px-2 rounded-full text-xs">
                                    {pendingCount}
                                </span>
                            )}
                        </Link>
                        <div className="border-t border-gray-100 my-1" />
                        {user ? (
                            <>
                                <Link to="/profile" onClick={closeMenu} className={`px-3 py-3 rounded-md text-sm font-medium transition-colors ${isActive('/profile')}`}>
                                    Profilim
                                </Link>
                                <button
                                    onClick={() => { logout(); closeMenu(); }}
                                    disabled={logoutLoading}
                                    className="inline-flex items-center gap-2 text-left px-3 py-3 text-sm font-medium text-red-600 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {logoutLoading && <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>}
                                    Çıkış
                                </button>
                            </>
                        ) : (
                            <Link to="/login" onClick={closeMenu} className="px-3 py-3 text-sm font-medium text-white bg-primary hover:bg-secondary rounded-md transition-colors text-center">
                                Giriş Yap
                            </Link>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
