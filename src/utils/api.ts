import type {
    RAGRecommendRequest, RAGRecommendResponse,
    SubstitutionRequest, SubstitutionResponse,
    SessionInfo, InteractionCreate, ConsumptionCreate, UserFeatures, InteractionResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export class ApiError extends Error {
    status: number;
    constructor(message: string, status: number) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
    }
}

/**
 * Helper function to handle API errors
 */
const handleApiError = async (response: Response): Promise<never> => {
    let errorMessage = 'Bir hata oluştu';

    try {
        const data = await response.json();
        errorMessage = data.detail || data.message || errorMessage;
    } catch {
        errorMessage = `Sunucu hatası: ${response.status} ${response.statusText}`;
    }

    throw new ApiError(errorMessage, response.status);
};

/**
 * Get all recipes with optional filtering
 */
export const getRecipes = async (params?: {
    ingredients?: string[];
    q?: string;
    limit?: number;
    offset?: number;
}) => {
    try {
        const queryParams = new URLSearchParams();

        if (params?.ingredients && params.ingredients.length > 0) {
            queryParams.append('ingredients', params.ingredients.join(','));
        }
        if (params?.q) {
            queryParams.append('q', params.q);
        }
        if (params?.limit) {
            queryParams.append('limit', params.limit.toString());
        }
        if (params?.offset) {
            queryParams.append('offset', params.offset.toString());
        }

        const url = `${API_BASE_URL}/recipes/?${queryParams}`;
        const response = await fetch(url, { credentials: 'include' });

        if (!response.ok) {
            await handleApiError(response);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Ağ hatası. Sunucunun çalıştığından emin olun.', 0);
    }
};

/**
 * Get a specific recipe by title
 */
export const getRecipeByTitle = async (title: string) => {
    try {
        const response = await fetch(
            `${API_BASE_URL}/recipes/${encodeURIComponent(title)}`,
            { credentials: 'include' }
        );

        if (!response.ok) {
            await handleApiError(response);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Ağ hatası. Sunucunun çalıştığından emin olun.', 0);
    }
};

/**
 * Get recipe recommendations based on ingredients
 */
export const getRecommendations = async (ingredients: string[]) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipes/recommend`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ingredients }),
        });

        if (!response.ok) {
            await handleApiError(response);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Ağ hatası. Sunucunun çalıştığından emin olun.', 0);
    }
};

/**
 * Get RAG-based recipe recommendations with explanations
 *
 * Complete pipeline: Retrieve (FAISS) → Rerank (Cross-encoder) → Generate (Gemini LLM)
 *
 * @example
 * ```typescript
 * const response = await getRAGRecommendations({
 *   ingredients: ['chicken', 'pasta', 'tomato'],
 *   preferences: { vegan: false, glutenFree: false },
 *   excluded_ingredients: ['mushroom'],
 *   explain: true,
 *   top_k: 10
 * });
 *
 * console.log(response.recipes); // Top-k reranked recipes
 * console.log(response.explanation); // LLM-generated explanation
 * console.log(response.metadata); // Pipeline execution details
 * ```
 *
 * @param request - RAG recommendation request with ingredients, preferences, etc.
 * @returns RAG recommendation response with recipes, explanation, and metadata
 */
export const getRAGRecommendations = async (
    request: RAGRecommendRequest
): Promise<RAGRecommendResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipes/rag-recommend`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ingredients: request.ingredients,
                preferences: request.preferences,
                excluded_ingredients: request.excluded_ingredients,
                explain: request.explain ?? true,
                top_k: request.top_k ?? 10,
                retrieval_top_k: request.retrieval_top_k ?? 50,
            }),
        });

        if (!response.ok) {
            await handleApiError(response);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Ağ hatası. Sunucunun çalıştığından emin olun.', 0);
    }
};

/**
 * Get ingredient substitution suggestions from LLM
 */
export const getSubstitutions = async (
    request: SubstitutionRequest
): Promise<SubstitutionResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipes/substitutions`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            await handleApiError(response);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Ağ hatası. Sunucunun çalıştığından emin olun.', 0);
    }
};

/**
 * Health check - test if backend is running
 */
export const checkHealth = async () => {
    try {
        const response = await fetch(`${AUTH_BASE}/health`);
        return response.ok;
    } catch {
        return false;
    }
};

// ── Auth API ──

const AUTH_BASE = API_BASE_URL.replace('/api', '');

export const signupUser = async (email: string, password: string): Promise<SessionInfo> => {
    const response = await fetch(`${AUTH_BASE}/api/auth/signup`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const signinUser = async (email: string, password: string): Promise<SessionInfo> => {
    const response = await fetch(`${AUTH_BASE}/api/auth/signin`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const requestMagicLink = async (email: string): Promise<{ message: string; dev_token?: string }> => {
    const response = await fetch(`${AUTH_BASE}/api/auth/magic-link`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const verifyMagicLink = async (token: string): Promise<SessionInfo> => {
    const response = await fetch(`${AUTH_BASE}/api/auth/verify`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const getCurrentUser = async (): Promise<SessionInfo | null> => {
    try {
        const response = await fetch(`${AUTH_BASE}/api/auth/me`, {
            credentials: 'include',
        });
        if (response.status === 401) return null;
        if (!response.ok) return null;
        return response.json();
    } catch {
        return null;
    }
};

export const logoutUser = async (): Promise<void> => {
    await fetch(`${AUTH_BASE}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include',
    });
};

// ── Feedback API ──

export const recordInteraction = async (data: InteractionCreate): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/feedback/interaction`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        if (response.status === 401) {
            throw new ApiError('Oturum süresi doldu. Lütfen tekrar giriş yapın.', 401);
        }
        await handleApiError(response);
    }
};

export const logConsumption = async (data: ConsumptionCreate): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/feedback/consumption`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        if (response.status === 401) {
            throw new ApiError('Oturum süresi doldu. Lütfen tekrar giriş yapın.', 401);
        }
        await handleApiError(response);
    }
};

export const getUserFeatures = async (): Promise<UserFeatures> => {
    const response = await fetch(`${API_BASE_URL}/feedback/features`, {
        credentials: 'include',
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const getFridgeIngredients = async (): Promise<{ ingredients: string[] }> => {
    const response = await fetch(`${API_BASE_URL}/fridge/ingredients`, {
        credentials: 'include',
    });
    if (response.status === 401) return { ingredients: [] };
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export interface ShoppingListItem {
    name: string;
    display_name: string;
    purchased: boolean;
    from_recipes: string[];
}

export const getShoppingList = async (): Promise<{ items: ShoppingListItem[] }> => {
    const response = await fetch(`${API_BASE_URL}/shopping-list/items`, {
        credentials: 'include',
    });
    if (response.status === 401) return { items: [] };
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const saveShoppingList = async (items: ShoppingListItem[]): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/shopping-list/items`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items }),
    });
    if (!response.ok && response.status !== 401) await handleApiError(response);
};

export const saveFridgeIngredients = async (ingredients: string[]): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/fridge/ingredients`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients }),
    });
    if (!response.ok) {
        if (response.status === 401) {
            throw new ApiError('Oturum süresi doldu. Lütfen tekrar giriş yapın.', 401);
        }
        await handleApiError(response);
    }
};

export const getRecipeStatus = async (recipeTitle: string): Promise<{ status: string | null }> => {
    const response = await fetch(
        `${API_BASE_URL}/feedback/recipe-status/${encodeURIComponent(recipeTitle)}`,
        { credentials: 'include' }
    );
    if (response.status === 401) return { status: null };
    if (!response.ok) return { status: null };
    return response.json();
};

export const deleteInteractionByRecipe = async (
    recipe_title: string,
    interaction_type: 'like' | 'skip' | 'save' | 'cook'
): Promise<{ deleted: number }> => {
    const response = await fetch(`${API_BASE_URL}/feedback/interaction`, {
        method: 'DELETE',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe_title, interaction_type }),
    });
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const deleteInteraction = async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/feedback/interaction/${encodeURIComponent(id)}`, {
        method: 'DELETE',
        credentials: 'include',
    });
    if (!response.ok && response.status !== 404) await handleApiError(response);
};

export interface SurveyPayload {
    rating: number;
    cook_intent: 'yes' | 'maybe' | 'no';
    comment?: string;
    context_ingredients?: string[];
    recipe_titles?: string[];
}

export const submitSurvey = async (data: SurveyPayload): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/feedback/survey`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!response.ok) await handleApiError(response);
};

export const getInteractionHistory = async (
    limit = 50, offset = 0
): Promise<{ interactions: InteractionResponse[]; count: number }> => {
    const response = await fetch(
        `${API_BASE_URL}/feedback/history?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`,
        { credentials: 'include' }
    );
    if (!response.ok) await handleApiError(response);
    return response.json();
};

// ── User Preferences API ──

export interface PreferencesPayload {
    dietary: Record<string, boolean>;
    excluded: string[];
}

export const getPreferences = async (): Promise<PreferencesPayload> => {
    const response = await fetch(`${API_BASE_URL}/user/preferences`, {
        credentials: 'include',
    });
    if (response.status === 401) return { dietary: {}, excluded: [] };
    if (!response.ok) await handleApiError(response);
    return response.json();
};

export const savePreferences = async (payload: PreferencesPayload): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/user/preferences`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    if (!response.ok && response.status !== 401) await handleApiError(response);
};
