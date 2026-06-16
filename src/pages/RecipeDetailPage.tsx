import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import recipes from '../data/recipes';
import { parseIngredientList, computeRecipeAvailability } from '../utils/helpers';
import { SubstitutionResponse, Recipe } from '../types';
import type { MealType } from '../types';
import RecipeImage from '../components/RecipeImage';
import { estimateRecipeCalories, getCalorieLabel, getIngredientCalories } from '../utils/calorieEstimator';
import { useFridge } from '../store/FridgeContext';
import { useAuth } from '../store/AuthContext';
import { useShoppingList } from '../store/ShoppingListContext';
import { getSubstitutions, recordInteraction, deleteInteractionByRecipe, logConsumption, getRecipeStatus, getRecipeByTitle, type ApiError } from '../utils/api';

function calorieLabelBadgeClass(label: string | null): string {
    if (label === 'Düşük') return 'bg-green-500 text-white';
    if (label === 'Orta') return 'bg-orange-400 text-white';
    return 'bg-red-500 text-white';
}

function CookButtonContent({ cookLoading, cookLogged }: Readonly<{ cookLoading: boolean; cookLogged: boolean }>) {
    if (cookLoading) {
        return (
            <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Kaydediliyor...
            </>
        );
    }
    if (cookLogged) {
        return (
            <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Kaydedildi
            </>
        );
    }
    return (
        <>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Pişirdim - Kaydet
        </>
    );
}

const MEAL_OPTIONS: { value: MealType; label: string }[] = [
    { value: 'breakfast', label: 'Kahvaltı' },
    { value: 'lunch', label: 'Öğle' },
    { value: 'dinner', label: 'Akşam' },
    { value: 'snack', label: 'Atıştırmalık' },
];

const PORTION_OPTIONS = [0.5, 1, 1.5, 2];

interface IngredientSidebarProps {
    ingredientsList: string[];
    cleanedList: string[];
    missingIngredients: string[];
    allMatchingIngredients: string[];
    substitutions: Record<string, string[]> | null;
    subExplanation: string | null;
    subLoading: boolean;
    subError: string | null;
    recipeTitle: string;
    addItemsFromRecipe: (title: string, items: string[]) => void;
    onSubstitute: () => void;
}

function RecipeIngredientSidebar({
    ingredientsList, cleanedList, missingIngredients, allMatchingIngredients,
    substitutions, subExplanation, subLoading, subError,
    recipeTitle, addItemsFromRecipe, onSubstitute,
}: Readonly<IngredientSidebarProps>) {
    return (
        <div className="bg-green-50 rounded-2xl p-6 sm:p-8 sticky top-24">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Malzemeler
            </h2>
            {allMatchingIngredients.length > 0 && (
                <div className="mb-6 pb-4 border-b border-green-200">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">Eşleşen Malzemeleriniz:</h3>
                    <ul className="flex flex-wrap gap-2">
                        {allMatchingIngredients.map((ing) => (
                            <li key={ing} className="bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm">{ing}</li>
                        ))}
                    </ul>
                </div>
            )}
            <ul className="space-y-4">
                {ingredientsList.map((ing, idx) => {
                    const cleanName = cleanedList[idx] || '';
                    const kcal = getIngredientCalories(cleanName);
                    const isMissing = missingIngredients.some(m => m.toLowerCase() === cleanName.toLowerCase());
                    const subsKey = substitutions
                        ? Object.keys(substitutions).find(k => k.toLowerCase() === cleanName.toLowerCase())
                        : undefined;
                    const subs: string[] | undefined = subsKey ? substitutions![subsKey] : undefined;
                    return (
                        <li key={ing}>
                            <div className="flex items-start">
                                <div className={`flex-shrink-0 h-6 w-6 rounded-full border flex items-center justify-center mr-3 mt-0.5 text-xs ${isMissing ? 'border-amber-300 text-amber-600 bg-amber-50' : 'border-green-200 text-green-600 bg-white'}`}>
                                    {idx + 1}
                                </div>
                                <div className="flex-1">
                                    <span className={`leading-relaxed ${isMissing ? 'text-amber-700' : 'text-gray-700'}`}>{ing}</span>
                                    {kcal !== undefined && <span className="ml-2 text-xs text-gray-400">{kcal} kcal</span>}
                                    {isMissing && <span className="ml-2 text-xs font-medium text-amber-600">(eksik)</span>}
                                </div>
                            </div>
                            {subs && subs.length > 0 && (
                                <div className="ml-9 mt-1 flex flex-wrap gap-1">
                                    {subs.map((sub) => (
                                        <span key={sub} className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-blue-50 text-blue-700 border border-blue-200">{sub}</span>
                                    ))}
                                </div>
                            )}
                        </li>
                    );
                })}
            </ul>
            {missingIngredients.length > 0 && (
                <div className="mt-6 pt-4 border-t border-green-200">
                    <button
                        onClick={() => addItemsFromRecipe(recipeTitle, missingIngredients)}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium bg-amber-500 text-white hover:bg-amber-600 transition-colors mb-3"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        {missingIngredients.length} eksik malzemeyi alışveriş listesine ekle
                    </button>
                </div>
            )}
            {missingIngredients.length > 0 && substitutions === null && (
                <div className="mt-6 pt-4 border-t border-green-200">
                    <button
                        onClick={onSubstitute}
                        disabled={subLoading}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {subLoading ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                                İkame önerileri yükleniyor...
                            </>
                        ) : (
                            <>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                                </svg>
                                {missingIngredients.length} eksik malzeme için ikame öner
                            </>
                        )}
                    </button>
                    {subError && <p className="mt-2 text-xs text-red-600">{subError}</p>}
                </div>
            )}
            {missingIngredients.length > 0 && substitutions !== null && Object.keys(substitutions).length === 0 && (
                <div className="mt-6 pt-4 border-t border-green-200">
                    <p className="text-xs text-amber-600">İkame önerileri şu an yüklenemiyor. Lütfen daha sonra tekrar deneyin.</p>
                </div>
            )}
            {subExplanation && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                    <p className="text-xs text-blue-700 leading-relaxed">{subExplanation}</p>
                </div>
            )}
        </div>
    );
}

interface FeedbackPanelProps {
    user: object | null;
    interactionStatus: string | null;
    interactionLoading: boolean;
    cookLoading: boolean;
    cookLogged: boolean;
    selectedMeal: MealType;
    selectedPortion: number;
    setSelectedMeal: (m: MealType) => void;
    setSelectedPortion: (p: number) => void;
    handleInteraction: (type: 'like' | 'skip') => void;
    handleCook: () => void;
}

function RecipeFeedbackPanel({
    user, interactionStatus, interactionLoading,
    cookLoading, cookLogged, selectedMeal, selectedPortion,
    setSelectedMeal, setSelectedPortion, handleInteraction, handleCook,
}: Readonly<FeedbackPanelProps>) {
    if (!user) {
        return (
            <div className="bg-gray-50 rounded-xl p-5 text-center">
                <p className="text-sm text-gray-600 mb-3">Beğeni ve pişirme kaydı için giriş yapın</p>
                <Link to="/login" className="inline-flex items-center px-4 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-secondary transition-colors">
                    Giriş Yap
                </Link>
            </div>
        );
    }
    const likeSpinner = interactionLoading && interactionStatus !== 'skip';
    const skipSpinner = interactionLoading && interactionStatus !== 'like';
    return (
        <div className="space-y-6">
            <div className="flex items-center gap-3">
                <button
                    onClick={() => handleInteraction('like')}
                    disabled={interactionLoading}
                    className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium border transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${interactionStatus === 'like' ? 'bg-red-50 border-red-300 text-red-600' : 'bg-white border-gray-200 text-gray-600 hover:border-red-300 hover:text-red-500'}`}
                >
                    {likeSpinner ? (
                        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill={interactionStatus === 'like' ? 'currentColor' : 'none'} stroke="currentColor"><path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" /></svg>
                    )}
                    Beğen
                </button>
                <button
                    onClick={() => handleInteraction('skip')}
                    disabled={interactionLoading}
                    className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium border transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${interactionStatus === 'skip' ? 'bg-gray-100 border-gray-400 text-gray-700' : 'bg-white border-gray-200 text-gray-600 hover:border-gray-400 hover:text-gray-700'}`}
                >
                    {skipSpinner ? (
                        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>
                    )}
                    Atla
                </button>
            </div>
            <div className="bg-gray-50 rounded-xl p-5 space-y-4">
                <h4 className="text-sm font-semibold text-gray-800">Bunu pişirdim</h4>
                <div className="flex flex-wrap items-center gap-3">
                    <div>
                        <span className="block text-xs text-gray-500 mb-1">Öğün</span>
                        <div className="flex gap-1">
                            {MEAL_OPTIONS.map(opt => (
                                <button key={opt.value} onClick={() => setSelectedMeal(opt.value)} className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${selectedMeal === opt.value ? 'bg-primary text-white' : 'bg-white border border-gray-200 text-gray-600 hover:border-primary'}`}>
                                    {opt.label}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div>
                        <span className="block text-xs text-gray-500 mb-1">Porsiyon</span>
                        <div className="flex gap-1">
                            {PORTION_OPTIONS.map(p => (
                                <button key={p} onClick={() => setSelectedPortion(p)} className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${selectedPortion === p ? 'bg-primary text-white' : 'bg-white border border-gray-200 text-gray-600 hover:border-primary'}`}>
                                    {p}x
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
                <button
                    onClick={handleCook}
                    disabled={cookLogged || cookLoading}
                    className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-colors disabled:cursor-not-allowed ${cookLogged ? 'bg-green-100 text-green-700 border border-green-300' : 'bg-primary text-white hover:bg-secondary disabled:opacity-70'}`}
                >
                    <CookButtonContent cookLoading={cookLoading} cookLogged={cookLogged} />
                </button>
            </div>
        </div>
    );
}

const RecipeDetailPage: React.FC = () => {
    const { title } = useParams<{ title: string }>();
    const location = useLocation();
    const locationState = location.state as { matchingIngredients?: string[]; recipe?: Recipe } | null;
    const matchingIngredients = locationState?.matchingIngredients ?? [];
    const { fridgeIngredients } = useFridge();
    const { user, logout } = useAuth();
    const { addItemsFromRecipe } = useShoppingList();

    const [recipe, setRecipe] = useState<Recipe | undefined>(
        locationState?.recipe ?? recipes.find(r => r.Title === decodeURIComponent(title || ''))
    );
    const [recipeLoading, setRecipeLoading] = useState(!recipe);
    const [recipeError, setRecipeError] = useState(false);

    const [substitutions, setSubstitutions] = useState<Record<string, string[]> | null>(null);
    const [subExplanation, setSubExplanation] = useState<string | null>(null);
    const [subLoading, setSubLoading] = useState(false);
    const [subError, setSubError] = useState<string | null>(null);

    const [interactionStatus, setInteractionStatus] = useState<string | null>(null);
    const [interactionLoading, setInteractionLoading] = useState(false);
    const [cookLoading, setCookLoading] = useState(false);
    const [selectedMeal, setSelectedMeal] = useState<MealType>('lunch');
    const [selectedPortion, setSelectedPortion] = useState(1);
    const [cookLogged, setCookLogged] = useState(false);

    const recipeTitle = recipe?.Title ?? decodeURIComponent(title || '');

    useEffect(() => {
        if (recipe) return;
        const decodedTitle = decodeURIComponent(title || '');
        setRecipeLoading(true);
        setRecipeError(false);
        getRecipeByTitle(decodedTitle)
            .then((data: Recipe) => setRecipe(data))
            .catch(() => {
                const local = recipes.find(r => r.Title === decodedTitle);
                if (local) setRecipe(local);
                else setRecipeError(true);
            })
            .finally(() => setRecipeLoading(false));
    }, [title]);

    useEffect(() => {
        if (user && recipeTitle) {
            // view kaydı kritik değil; 401'da logout yapma
            recordInteraction({ recipe_title: recipeTitle, interaction_type: 'view', context_ingredients: fridgeIngredients }).catch(() => {});
            getRecipeStatus(recipeTitle).then(res => setInteractionStatus(res.status)).catch(() => {});
        }
    }, [user, recipeTitle, fridgeIngredients]);

    const handleInteraction = useCallback(async (type: 'like' | 'skip') => {
        if (!user || !recipeTitle || interactionLoading) return;
        const previousStatus = interactionStatus;
        const isToggleOff = previousStatus === type;
        setInteractionStatus(isToggleOff ? null : type);
        setInteractionLoading(true);
        try {
            if (isToggleOff) {
                await deleteInteractionByRecipe(recipeTitle, type);
            } else {
                await recordInteraction({ recipe_title: recipeTitle, interaction_type: type, context_ingredients: fridgeIngredients });
            }
        } catch (err) {
            setInteractionStatus(previousStatus);
            if ((err as ApiError)?.status === 401) await logout();
        } finally {
            setInteractionLoading(false);
        }
    }, [user, recipeTitle, fridgeIngredients, logout, interactionStatus, interactionLoading]);

    const handleCook = useCallback(async () => {
        if (!user || !recipeTitle || cookLoading || cookLogged) return;
        setCookLoading(true);
        try {
            await recordInteraction({ recipe_title: recipeTitle, interaction_type: 'cook' });
            await logConsumption({ recipe_title: recipeTitle, meal_type: selectedMeal, portion_size: selectedPortion });
            setCookLogged(true);
        } catch (err) {
            if ((err as ApiError)?.status === 401) await logout();
        } finally {
            setCookLoading(false);
        }
    }, [user, recipeTitle, selectedMeal, selectedPortion, logout, cookLoading, cookLogged]);

    if (recipeLoading) {
        return (
            <div className="min-h-[50vh] flex flex-col items-center justify-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mb-4"></div>
                <p className="text-gray-600">Tarif yükleniyor...</p>
            </div>
        );
    }

    if (recipeError || !recipe) {
        return (
            <div className="min-h-[50vh] flex flex-col items-center justify-center">
                <h2 className="text-2xl font-bold text-gray-800">Tarif bulunamadı</h2>
                <Link to="/recipes" className="mt-4 text-primary hover:underline">Tariflere dön</Link>
            </div>
        );
    }

    const ingredientsList = parseIngredientList(recipe.Ingredients);
    const cleanedList = parseIngredientList(recipe.Cleaned_Ingredients);
    const instructionsList = recipe.Instructions.split('\n').filter(i => i.trim().length > 0);

    const totalCalories = estimateRecipeCalories(recipe.Cleaned_Ingredients);
    const calorieLabel = totalCalories == null ? null : getCalorieLabel(totalCalories);

    const availability = computeRecipeAvailability(cleanedList, fridgeIngredients, matchingIngredients);
    const missingIngredients = availability.missing;
    const allMatchingIngredients = availability.allMatching;

    const handleSubstitution = async () => {
        if (missingIngredients.length === 0) return;
        setSubLoading(true);
        setSubError(null);
        try {
            const response: SubstitutionResponse = await getSubstitutions({
                recipe_title: recipe.Title,
                missing_ingredients: missingIngredients,
                available_ingredients: fridgeIngredients,
            });
            setSubstitutions(response.substitutions);
            setSubExplanation(response.explanation);
        } catch {
            setSubError('İkame önerileri alınamadı. Lütfen tekrar deneyin.');
        } finally {
            setSubLoading(false);
        }
    };

    return (
        <div className="bg-white min-h-screen">
            {/* Hero Section */}
            <div className="relative w-full">
                <RecipeImage
                    imageName={recipe.Image_Name}
                    alt={recipe.Title}
                    size="hero"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8 sm:pb-12">
                     <Link to="/recipes" className="inline-flex items-center text-white/80 hover:text-white mb-4 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
                        </svg>
                        Sonuçlara Dön
                    </Link>
                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white leading-tight shadow-sm">
                        {recipe.Title}
                    </h1>
                    {totalCalories != null && (
                        <div className="mt-3 flex items-center gap-3">
                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold shadow ${calorieLabelBadgeClass(calorieLabel)}`}>
                                ~{totalCalories} kcal
                            </span>
                            <span className="text-white/70 text-sm">{calorieLabel} kalorili</span>
                        </div>
                    )}
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">

                    {/* Sidebar: Ingredients */}
                    <div className="lg:col-span-1">
                        <RecipeIngredientSidebar
                            ingredientsList={ingredientsList}
                            cleanedList={cleanedList}
                            missingIngredients={missingIngredients}
                            allMatchingIngredients={allMatchingIngredients}
                            substitutions={substitutions}
                            subExplanation={subExplanation}
                            subLoading={subLoading}
                            subError={subError}
                            recipeTitle={recipe.Title}
                            addItemsFromRecipe={addItemsFromRecipe}
                            onSubstitute={handleSubstitution}
                        />
                    </div>

                    {/* Main Content: Instructions + Feedback */}
                    <div className="lg:col-span-2">
                        <h2 className="text-2xl font-bold text-gray-900 mb-8 pb-2 border-b border-gray-100">Talimatlar</h2>
                        <div className="space-y-10">
                            {instructionsList.map((step, idx) => (
                                <div key={step} className="flex">
                                    <div className="flex-shrink-0 mr-6">
                                        <span className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white font-bold text-lg">
                                            {idx + 1}
                                        </span>
                                    </div>
                                    <div className="pt-1">
                                        <p className="text-lg text-gray-700 leading-relaxed">{step}</p>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Feedback Panel */}
                        <div className="mt-12 pt-8 border-t border-gray-200">
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Bu tarif hakkında</h3>
                            <RecipeFeedbackPanel
                                user={user}
                                interactionStatus={interactionStatus}
                                interactionLoading={interactionLoading}
                                cookLoading={cookLoading}
                                cookLogged={cookLogged}
                                selectedMeal={selectedMeal}
                                selectedPortion={selectedPortion}
                                setSelectedMeal={setSelectedMeal}
                                setSelectedPortion={setSelectedPortion}
                                handleInteraction={handleInteraction}
                                handleCook={handleCook}
                            />
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default RecipeDetailPage;
