import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import type { User } from '../types';
import { supabase } from '../lib/supabase';
import { getCurrentUser, logoutUser } from '../utils/api';

const API_BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/api$/, '') ?? 'http://localhost:8000';

interface AuthContextType {
    user: User | null;
    loading: boolean;
    logoutLoading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

async function bridgeToBackend(accessToken: string): Promise<User> {
    const response = await fetch(`${API_BASE}/api/auth/supabase-session`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken }),
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail ?? 'Backend oturumu oluşturulamadı.');
    }
    const session = await response.json();
    return session.user as User;
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [logoutLoading, setLogoutLoading] = useState(false);

    const checkSession = useCallback(async () => {
        try {
            const session = await getCurrentUser();
            setUser(session?.user ?? null);
        } catch {
            setUser(null);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        checkSession();
    }, [checkSession]);

    const login = async (email: string, password: string) => {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw new Error(error.message);

        if (!data.session?.access_token) throw new Error('Login succeeded but no session was returned');
        const localUser = await bridgeToBackend(data.session.access_token);
        setUser(localUser);
    };

    const signup = async (email: string, password: string) => {
        const { data, error } = await supabase.auth.signUp({ email, password });
        if (error) throw new Error(error.message);
        if (!data.session) {
            throw new Error('Kayıt başarılı! Supabase Dashboard\'dan "Confirm email" kapalı olduğunu doğrulayın.');
        }
        const localUser = await bridgeToBackend(data.session.access_token);
        setUser(localUser);
    };

    const logout = async () => {
        if (logoutLoading) return;
        setLogoutLoading(true);
        try {
            await supabase.auth.signOut();
            await logoutUser().catch(() => { /* ignore */ });
            setUser(null);
        } finally {
            setLogoutLoading(false);
        }
    };

    return (
        <AuthContext.Provider value={{ user, loading, logoutLoading, login, signup, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within an AuthProvider');
    return context;
};
