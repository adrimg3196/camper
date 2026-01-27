/**
 * Hugging Face Integration - Modelos Gratuitos
 * Acceso a modelos open source de alta calidad
 */

// Mejores modelos gratuitos de Hugging Face Inference API
export const HF_MODELS = {
    // Generación de texto
    TEXT: {
        mistral: 'mistralai/Mistral-7B-Instruct-v0.3',
        llama: 'meta-llama/Meta-Llama-3-8B-Instruct',
        zephyr: 'HuggingFaceH4/zephyr-7b-beta',
        phi3: 'microsoft/Phi-3-mini-4k-instruct',
    },
    // Traducción
    TRANSLATION: {
        marian: 'Helsinki-NLP/opus-mt-en-es',
    },
    // Resumen
    SUMMARIZATION: {
        bart: 'facebook/bart-large-cnn',
    },
    // Clasificación de sentimiento
    SENTIMENT: {
        roberta: 'cardiffnlp/twitter-roberta-base-sentiment-latest',
    },
} as const;

interface HuggingFaceOptions {
    model?: string;
    maxTokens?: number;
    temperature?: number;
    waitForModel?: boolean;
}

/**
 * Genera texto usando Hugging Face Inference API (GRATUITO)
 */
export async function generateWithHuggingFace(
    prompt: string,
    options: HuggingFaceOptions = {}
): Promise<string> {
    const apiKey = process.env.HUGGINGFACE_API_KEY;

    if (!apiKey) {
        throw new Error('HUGGINGFACE_API_KEY is not configured');
    }

    const model = options.model || HF_MODELS.TEXT.mistral;

    try {
        const response = await fetch(
            `https://api-inference.huggingface.co/models/${model}`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    inputs: prompt,
                    parameters: {
                        max_new_tokens: options.maxTokens || 500,
                        temperature: options.temperature || 0.7,
                        return_full_text: false,
                        do_sample: true,
                    },
                    options: {
                        wait_for_model: options.waitForModel ?? true,
                    },
                }),
            }
        );

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`HuggingFace API error: ${response.status} - ${error}`);
        }

        const data = await response.json();

        // La respuesta puede venir en diferentes formatos
        if (Array.isArray(data) && data[0]?.generated_text) {
            return data[0].generated_text;
        }
        if (data.generated_text) {
            return data.generated_text;
        }
        if (typeof data === 'string') {
            return data;
        }

        throw new Error('Unexpected response format from HuggingFace');
    } catch (error) {
        console.error('HuggingFace generation error:', error);
        throw error;
    }
}

/**
 * Genera contenido de marketing usando HuggingFace (Gratuito)
 */
export async function generateMarketingWithHF(
    productTitle: string,
    productUrl: string,
    discount: number
): Promise<{
    telegram: string;
    tiktok: string;
    instagram: string;
}> {
    const prompt = `<s>[INST] Eres un experto en marketing de productos de camping. Genera contenido promocional en español para:

Producto: ${productTitle}
URL: ${productUrl}
Descuento: ${discount}%

Genera 3 versiones cortas (máximo 200 caracteres cada una):
1. Para TELEGRAM (con emojis y urgencia)
2. Para TIKTOK (gancho viral)
3. Para INSTAGRAM (con hashtags)

Responde SOLO el contenido, sin explicaciones. [/INST]`;

    const response = await generateWithHuggingFace(prompt, {
        model: HF_MODELS.TEXT.mistral,
        maxTokens: 400,
        temperature: 0.8,
    });

    // Parsear la respuesta
    const lines = response.split('\n').filter(l => l.trim());

    return {
        telegram: lines[0] || `🏕️ ¡OFERTA -${discount}%! ${productTitle.slice(0, 50)}... 🔥 ${productUrl}`,
        tiktok: lines[1] || `POV: Encontraste ${productTitle.slice(0, 30)} con -${discount}% 🤯`,
        instagram: lines[2] || `${productTitle.slice(0, 50)} con descuento increíble 🏕️ #camping #ofertas #outdoor`,
    };
}

/**
 * Analiza sentimiento de reviews (útil para seleccionar productos)
 */
export async function analyzeSentiment(text: string): Promise<{
    label: string;
    score: number;
}> {
    const apiKey = process.env.HUGGINGFACE_API_KEY;

    if (!apiKey) {
        return { label: 'neutral', score: 0.5 };
    }

    try {
        const response = await fetch(
            `https://api-inference.huggingface.co/models/${HF_MODELS.SENTIMENT.roberta}`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputs: text }),
            }
        );

        if (!response.ok) {
            return { label: 'neutral', score: 0.5 };
        }

        const data = await response.json();

        if (Array.isArray(data) && Array.isArray(data[0])) {
            // Encontrar el label con mayor score
            const sorted = data[0].sort((a: any, b: any) => b.score - a.score);
            return {
                label: sorted[0].label,
                score: sorted[0].score,
            };
        }

        return { label: 'neutral', score: 0.5 };
    } catch (error) {
        console.error('Sentiment analysis error:', error);
        return { label: 'neutral', score: 0.5 };
    }
}

/**
 * Traduce texto de inglés a español
 */
export async function translateToSpanish(text: string): Promise<string> {
    const apiKey = process.env.HUGGINGFACE_API_KEY;

    if (!apiKey) {
        return text;
    }

    try {
        const response = await fetch(
            `https://api-inference.huggingface.co/models/${HF_MODELS.TRANSLATION.marian}`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputs: text }),
            }
        );

        if (!response.ok) {
            return text;
        }

        const data = await response.json();

        if (Array.isArray(data) && data[0]?.translation_text) {
            return data[0].translation_text;
        }

        return text;
    } catch (error) {
        console.error('Translation error:', error);
        return text;
    }
}
