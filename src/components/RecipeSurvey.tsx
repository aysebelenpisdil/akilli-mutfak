import React, { useState } from 'react';
import { submitSurvey } from '../utils/api';

interface RecipeSurveyProps {
    contextIngredients: string[];
    recipeTitles: string[];
    onComplete: () => void;
}

const RecipeSurvey: React.FC<RecipeSurveyProps> = ({ contextIngredients, recipeTitles, onComplete }) => {
    const [rating, setRating] = useState(0);
    const [hovered, setHovered] = useState(0);
    const [cookIntent, setCookIntent] = useState<'yes' | 'maybe' | 'no' | ''>('');
    const [comment, setComment] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [submitted, setSubmitted] = useState(false);

    const handleSubmit = async () => {
        if (!rating || !cookIntent) return;
        setSubmitting(true);
        setError(null);
        try {
            await submitSurvey({
                rating,
                cook_intent: cookIntent as 'yes' | 'maybe' | 'no',
                comment: comment.trim() || undefined,
                context_ingredients: contextIngredients,
                recipe_titles: recipeTitles,
            });
            setSubmitted(true);
            setTimeout(onComplete, 3000);
        } catch (e: unknown) {
            const msg = e && typeof e === 'object' && 'message' in e ? (e as { message: string }).message : 'Gönderilemedi. Tekrar deneyin.';
            setError(msg);
            setSubmitting(false);
        }
    };

    if (submitted) {
        return (
            <div className="mt-4 bg-gradient-to-r from-green-50 to-teal-50 border-l-4 border-green-400 rounded-lg p-4 shadow-sm">
                <div className="flex items-center gap-2">
                    <svg className="h-5 w-5 text-green-600" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <p className="text-sm font-semibold text-green-800">Teşekkürler! Geri bildiriminiz alındı.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="mt-4 bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-amber-400 rounded-lg p-4 shadow-sm">
            <div className="flex items-start justify-between mb-3">
                <h3 className="text-sm font-semibold text-gray-900">Öneriler Nasıldı?</h3>
                <button
                    onClick={onComplete}
                    className="text-gray-400 hover:text-gray-600 text-xs leading-none"
                    aria-label="Atla"
                >
                    Atla ✕
                </button>
            </div>

            <div className="mb-3">
                <p className="text-xs text-gray-600 mb-1">Önerilerin yararlılığı:</p>
                <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map(star => (
                        <button
                            key={star}
                            onClick={() => setRating(star)}
                            onMouseEnter={() => setHovered(star)}
                            onMouseLeave={() => setHovered(0)}
                            className="text-2xl transition-transform hover:scale-110 leading-none"
                            aria-label={`${star} yıldız`}
                        >
                            <span className={star <= (hovered || rating) ? 'text-amber-400' : 'text-gray-300'}>
                                {star <= (hovered || rating) ? '★' : '☆'}
                            </span>
                        </button>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <p className="text-xs text-gray-600 mb-1">Bir tarifi pişirmeyi düşünüyor musun?</p>
                <div className="flex gap-4">
                    {(['yes', 'maybe', 'no'] as const).map(v => (
                        <label key={v} className="flex items-center gap-1.5 cursor-pointer text-sm text-gray-700">
                            <input
                                type="radio"
                                name="cook_intent"
                                value={v}
                                checked={cookIntent === v}
                                onChange={() => setCookIntent(v)}
                                className="accent-amber-500"
                            />
                            {({'yes': 'Evet', 'maybe': 'Belki', 'no': 'Hayır'} as const)[v]}
                        </label>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <textarea
                    value={comment}
                    onChange={e => setComment(e.target.value.slice(0, 500))}
                    placeholder="Yorum (opsiyonel)"
                    rows={2}
                    className="w-full text-sm border border-gray-200 rounded p-2 resize-none focus:outline-none focus:border-amber-400"
                />
                <p className="text-xs text-gray-400 text-right -mt-1">{comment.length}/500</p>
            </div>

            {error && <p className="text-xs text-red-600 mb-2">{error}</p>}

            <button
                onClick={handleSubmit}
                disabled={!rating || !cookIntent || submitting}
                className="bg-amber-500 text-white text-sm px-4 py-1.5 rounded-md hover:bg-amber-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
                {submitting ? 'Gönderiliyor…' : 'Gönder'}
            </button>
        </div>
    );
};

export default RecipeSurvey;
