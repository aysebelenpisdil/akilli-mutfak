import React, { useState } from 'react';

const DIETARY_PREFIXES = [
    'vegan-', 'glutensiz-', 'sut-urunsuz-', 'vejetaryen-', 'laktozsuz-', 'kuruyemissiz-',
];

function buildFallbackChain(imageName: string): string[] {
    const primary = `images/recipies/${imageName}.jpg`;
    for (const prefix of DIETARY_PREFIXES) {
        if (imageName.startsWith(prefix)) {
            const base = imageName.slice(prefix.length);
            return [primary, `images/recipies/${base}.jpg`];
        }
    }
    return [primary];
}

interface RecipeImageProps {
    imageName: string;
    alt: string;
    className?: string;
    size?: 'card' | 'hero';
}

const RecipeImage: React.FC<RecipeImageProps> = ({ imageName, alt, className = '', size = 'card' }) => {
    const [urlIndex, setUrlIndex] = useState(0);
    const [loaded, setLoaded] = useState(false);
    const [failed, setFailed] = useState(false);

    const urls = buildFallbackChain(imageName);
    const sizeClasses = size === 'hero' ? 'h-80 sm:h-96' : 'h-48';

    const handleError = () => {
        if (urlIndex < urls.length - 1) {
            setUrlIndex(prev => prev + 1);
            setLoaded(false);
        } else {
            setFailed(true);
        }
    };

    return (
        <div className={`relative w-full ${sizeClasses} overflow-hidden bg-gray-100 ${className}`}>
            {!loaded && !failed && (
                <div className="absolute inset-0 animate-shimmer" />
            )}

            {failed && (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100">
                    <span className="text-5xl mb-2">🍽️</span>
                    <span className="text-sm text-gray-400">Görsel Yüklenemedi</span>
                </div>
            )}

            {!failed && (
                <img
                    src={urls[urlIndex]}
                    alt={alt}
                    loading="lazy"
                    onLoad={() => setLoaded(true)}
                    onError={handleError}
                    className={`w-full h-full object-cover transition-opacity duration-500 ${loaded ? 'opacity-100' : 'opacity-0'}`}
                />
            )}
        </div>
    );
};

export default RecipeImage;
