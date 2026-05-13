import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';

type Mode = 'signin' | 'signup';

const LoginPage: React.FC = () => {
    const { user, login, signup } = useAuth();
    const navigate = useNavigate();

    const [mode, setMode] = useState<Mode>('signin');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (user) navigate('/', { replace: true });
    }, [user, navigate]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        if (mode === 'signup' && password.length < 6) {
            setError('Şifre en az 6 karakter olmalıdır.');
            return;
        }

        setLoading(true);
        try {
            if (mode === 'signin') {
                await login(email, password);
            } else {
                await signup(email, password);
            }
            navigate('/', { replace: true });
        } catch (err: unknown) {
            const msg = (err as { message?: string })?.message ?? '';
            if (msg.includes('Invalid login credentials') || msg.includes('invalid_credentials')) {
                setError('E-posta veya şifre hatalı.');
            } else if (msg.includes('User already registered') || msg.includes('already registered')) {
                setError('Bu e-posta adresi zaten kayıtlı. Giriş yapmayı deneyin.');
                setMode('signin');
            } else if (msg.includes('Email not confirmed')) {
                setError('E-posta doğrulanmamış. Supabase Dashboard\'dan "Confirm email" seçeneğini kapatın.');
            } else if (msg) {
                setError(msg);
            } else {
                setError('Bir hata oluştu. Lütfen tekrar deneyin.');
            }
        } finally {
            setLoading(false);
        }
    };

    const switchMode = () => {
        setMode(m => m === 'signin' ? 'signup' : 'signin');
        setError(null);
    };

    return (
        <div className="min-h-[70vh] flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
                    {/* Logo */}
                    <div className="text-center mb-8">
                        <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4">
                            F
                        </div>
                        <h1 className="text-2xl font-bold text-gray-900">Buzdolabı Şefi</h1>
                        <p className="mt-2 text-gray-500">
                            {mode === 'signin' ? 'Hesabınıza giriş yapın' : 'Yeni hesap oluşturun'}
                        </p>
                    </div>

                    {/* Mode tabs */}
                    <div className="flex rounded-lg border border-gray-200 mb-6 overflow-hidden">
                        <button
                            type="button"
                            onClick={() => { setMode('signin'); setError(null); }}
                            className={`flex-1 py-2 text-sm font-medium transition-colors ${
                                mode === 'signin'
                                    ? 'bg-primary text-white'
                                    : 'bg-white text-gray-600 hover:bg-gray-50'
                            }`}
                        >
                            Giriş Yap
                        </button>
                        <button
                            type="button"
                            onClick={() => { setMode('signup'); setError(null); }}
                            className={`flex-1 py-2 text-sm font-medium transition-colors ${
                                mode === 'signup'
                                    ? 'bg-primary text-white'
                                    : 'bg-white text-gray-600 hover:bg-gray-50'
                            }`}
                        >
                            Kayıt Ol
                        </button>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                                E-posta
                            </label>
                            <input
                                id="email"
                                type="email"
                                required
                                autoComplete="email"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                placeholder="ornek@email.com"
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-colors"
                            />
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                                Şifre
                                {mode === 'signup' && (
                                    <span className="ml-1 text-xs text-gray-400">(en az 6 karakter)</span>
                                )}
                            </label>
                            <input
                                id="password"
                                type="password"
                                required
                                autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="••••••••"
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-colors"
                            />
                        </div>

                        {error && (
                            <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">{error}</p>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3 px-4 bg-primary text-white font-medium rounded-lg hover:bg-secondary transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading
                                ? (mode === 'signin' ? 'Giriş yapılıyor...' : 'Kayıt olunuyor...')
                                : (mode === 'signin' ? 'Giriş Yap' : 'Kayıt Ol')
                            }
                        </button>
                    </form>

                    {/* Switch mode link */}
                    <p className="mt-4 text-center text-sm text-gray-500">
                        {mode === 'signin' ? 'Hesabınız yok mu?' : 'Zaten hesabınız var mı?'}{' '}
                        <button
                            type="button"
                            onClick={switchMode}
                            className="text-primary hover:underline font-medium"
                        >
                            {mode === 'signin' ? 'Kayıt Ol' : 'Giriş Yap'}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
