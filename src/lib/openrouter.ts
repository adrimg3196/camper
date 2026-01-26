/**
 * OpenRouter Integration - Multi-AI Content Generation
 * Supports: GPT-4, Claude, Gemini, Llama, and more
 */

interface OpenRouterModel {
    id: string;
    name: string;
    description?: string;
}

interface OpenRouterResponse {
    id: string;
    model: string;
    choices: Array<{
        message: {
            role: string;
            content: string;
        };
        finish_reason: string;
    }>;
    usage?: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
}

// Modelos recomendados por caso de uso
export const MODELS = {
    // Mejor calidad - Marketing y copywriting
    PREMIUM: {
        gpt4: 'openai/gpt-4-turbo-preview',
        claude: 'anthropic/claude-3.5-sonnet', // Claude 3.5 Sonnet (disponible y potente)
        gemini: 'google/gemini-pro-1.5',
    },
    // Balance calidad/precio - Contenido general
    BALANCED: {
        gpt4: 'openai/gpt-4o',
        claude: 'anthropic/claude-3.5-sonnet',
        gemini: 'google/gemini-pro',
    },
    // Gratuitos - Modelos sin costo
    FREE: {
        llama: 'meta-llama/llama-3-8b-instruct:free',
        mistral: 'mistralai/mistral-7b-instruct:free',
        gemma: 'google/gemma-7b-it:free',
        qwen: 'qwen/qwen-2-7b-instruct:free',
    },
    // Económico - Generación masiva
    ECONOMY: {
        gpt: 'openai/gpt-3.5-turbo',
        claude: 'anthropic/claude-3-haiku',
        llama: 'meta-llama/llama-3-70b-instruct',
    },
    // Especializados
    SPECIALIZED: {
        tiktok: 'openai/gpt-4-turbo-preview', // Mejor para scripts creativos
        seo: 'anthropic/claude-3.5-sonnet', // Mejor para SEO
        ads: 'google/gemini-pro-1.5', // Mejor para copy de ads
    },
} as const;

export interface ContentGenerationOptions {
    model?: string;
    temperature?: number;
    maxTokens?: number;
    useBestModel?: boolean; // Auto-select best model for task
}

/**
 * Genera contenido de marketing usando OpenRouter
 */
export async function generateWithOpenRouter(
    prompt: string,
    options: ContentGenerationOptions = {}
): Promise<string> {
    const apiKey = process.env.OPENROUTER_API_KEY;
    
    if (!apiKey) {
        throw new Error('OPENROUTER_API_KEY is not configured');
    }

    // Seleccionar modelo - Priorizar gratuitos si no se especifica
    let model = options.model;
    if (!model && options.useBestModel) {
        // Intentar primero con modelo gratuito
        model = MODELS.FREE.llama; // Llama 3.8B gratuito
    }
    if (!model) {
        model = MODELS.FREE.llama; // Default: modelo gratuito
    }

    try {
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': process.env.NEXT_PUBLIC_SITE_URL || 'https://camper-omega.vercel.app',
                'X-Title': 'Camper Deals - AI Marketing',
            },
            body: JSON.stringify({
                model,
                messages: [
                    {
                        role: 'system',
                        content: 'You are an expert social media marketer and copywriter specializing in outdoor and camping products. Always respond in Spanish unless specified otherwise.',
                    },
                    {
                        role: 'user',
                        content: prompt,
                    },
                ],
                temperature: options.temperature ?? 0.8,
                max_tokens: options.maxTokens ?? 1000, // Reducido para ahorrar créditos
            }),
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`OpenRouter API error: ${response.status} - ${error}`);
        }

        const data: OpenRouterResponse = await response.json();
        
        if (!data.choices || data.choices.length === 0) {
            throw new Error('No response from OpenRouter');
        }

        return data.choices[0].message.content;
    } catch (error) {
        console.error('OpenRouter generation error:', error);
        throw error;
    }
}

/**
 * Genera contenido de marketing multi-plataforma optimizado
 */
export async function generateMarketingContentAdvanced(
    topic: string,
    productUrl: string,
    productData?: {
        price?: number;
        originalPrice?: number;
        discount?: number;
        category?: string;
        rating?: number;
    },
    options: ContentGenerationOptions = {}
): Promise<{
    telegram: { content: string };
    tiktok: { script: string; visualSettings: string; hooks: string[] };
    tiktokshop: { title: string; description: string; tags: string[]; cta: string };
    instagram: { caption: string; hashtags: string[] };
    seo: { title: string; metaDescription: string; keywords: string[] };
    ads: { headline: string; description: string; cta: string };
}> {
    const discount = productData?.discount || 0;
    const price = productData?.price || 0;
    const originalPrice = productData?.originalPrice || 0;

    const prompt = `Eres un experto en marketing digital y generación de contenido viral. 

PRODUCTO: ${topic}
URL: ${productUrl}
${productData ? `
PRECIO: ${price}€ (antes ${originalPrice}€) - Descuento: ${discount}%
CATEGORÍA: ${productData.category || 'camping'}
RATING: ${productData.rating || 'N/A'}/5
` : ''}

Genera contenido de marketing optimizado para MÚLTIPLES plataformas. Responde SOLO con un JSON válido con esta estructura exacta:

{
  "telegram": {
    "content": "Copy para Telegram con emojis, precio, descuento destacado, y enlace de afiliado. Máximo 400 caracteres. Debe ser URGENTE y crear FOMO."
  },
  "tiktok": {
    "script": "Guion completo con timecodes (0:00, 0:03, 0:07, etc.) para video de 15-30 segundos. Debe tener HOOK potente en los primeros 3 segundos, mostrar beneficios, y CTA claro.",
    "visualSettings": "Descripción detallada de cómo debe verse el video: colores, estilo, transiciones, efectos",
    "hooks": ["Hook 1 (primeros 3 seg)", "Hook 2 alternativo", "Hook 3 alternativo"]
  },
  "tiktokshop": {
    "title": "Título optimizado para TikTok Shop (máx 60 caracteres) con keywords",
    "description": "Descripción completa del producto para TikTok Shop con beneficios, características, y llamadas a la acción. Incluye emojis estratégicos.",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "cta": "Call to action específico para TikTok Shop"
  },
  "instagram": {
    "caption": "Caption completo para Instagram con storytelling, emojis, y llamada a la acción",
    "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5", "#hashtag6", "#hashtag7", "#hashtag8", "#hashtag9", "#hashtag10"]
  },
  "seo": {
    "title": "Título SEO optimizado (50-60 caracteres) con keyword principal",
    "metaDescription": "Meta descripción SEO (150-160 caracteres) con keywords y CTA",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
  },
  "ads": {
    "headline": "Headline para anuncios (máx 30 caracteres) que capture atención",
    "description": "Descripción para anuncios (máx 90 caracteres) con beneficio principal",
    "cta": "Call to action para botón de anuncio"
  }
}

IMPORTANTE:
- Todo en ESPAÑOL
- Usa técnicas de copywriting avanzadas (FOMO, urgencia, prueba social)
- Optimiza para conversión (que compren)
- Incluye números y datos específicos cuando sea posible
- Crea urgencia y escasez
- Usa emojis estratégicamente (no en exceso)
- Responde SOLO con JSON válido, sin markdown, sin explicaciones`;

    const response = await generateWithOpenRouter(prompt, {
        ...options,
        useBestModel: true, // Usar mejor modelo para marketing
        temperature: 0.9, // Más creatividad
    });

    // Limpiar respuesta
    let jsonString = response.trim();
    jsonString = jsonString.replace(/```json/g, '').replace(/```/g, '').trim();
    
    // Si empieza con texto antes del JSON, extraer solo el JSON
    const jsonMatch = jsonString.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
        jsonString = jsonMatch[0];
    }

    try {
        return JSON.parse(jsonString);
    } catch (e) {
        console.error('Failed to parse OpenRouter response:', response);
        throw new Error(`Invalid JSON from OpenRouter: ${e}`);
    }
}

/**
 * Genera contenido SEO optimizado
 */
export async function generateSEOContent(
    topic: string,
    keywords: string[],
    options: ContentGenerationOptions = {}
): Promise<{
    title: string;
    metaDescription: string;
    h1: string;
    introduction: string;
    sections: Array<{ heading: string; content: string }>;
    faq: Array<{ question: string; answer: string }>;
}> {
    const prompt = `Genera contenido SEO optimizado para el tema: "${topic}"

Keywords objetivo: ${keywords.join(', ')}

Responde SOLO con JSON válido:
{
  "title": "Título SEO (50-60 caracteres) con keyword principal",
  "metaDescription": "Meta descripción (150-160 caracteres) con keywords y CTA",
  "h1": "H1 principal optimizado",
  "introduction": "Introducción de 2-3 párrafos que enganche y contenga keywords",
  "sections": [
    {
      "heading": "H2 con keyword",
      "content": "Contenido de 2-3 párrafos con keywords naturales"
    }
  ],
  "faq": [
    {
      "question": "Pregunta frecuente con keyword",
      "answer": "Respuesta completa y útil"
    }
  ]
}

Todo en ESPAÑOL. Optimizado para posicionamiento en Google.`;

    const response = await generateWithOpenRouter(prompt, {
        model: MODELS.SPECIALIZED.seo,
        ...options,
    });

    let jsonString = response.trim();
    jsonString = jsonString.replace(/```json/g, '').replace(/```/g, '').trim();
    const jsonMatch = jsonString.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
        jsonString = jsonMatch[0];
    }

    return JSON.parse(jsonString);
}

/**
 * Lista modelos disponibles en OpenRouter
 */
export async function listAvailableModels(): Promise<OpenRouterModel[]> {
    const apiKey = process.env.OPENROUTER_API_KEY;
    
    if (!apiKey) {
        return [];
    }

    try {
        const response = await fetch('https://openrouter.ai/api/v1/models', {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
            },
        });

        if (!response.ok) {
            return [];
        }

        const data = await response.json();
        return data.data || [];
    } catch (error) {
        console.error('Error fetching OpenRouter models:', error);
        return [];
    }
}
