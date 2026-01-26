import { NextResponse } from 'next/server';
import { generateMarketingContentAdvanced } from '@/lib/openrouter';
import { generateMarketingContent } from '@/lib/gemini';

/**
 * Genera contenido optimizado específicamente para TikTok Shop
 */
export async function POST(request: Request) {
    const body = await request.json();
    const { productTitle, productUrl, productData } = body;

    try {
        let content;

        // Priorizar Gemini (gratuito) o usar OpenRouter con modelos gratuitos
        if (process.env.GOOGLE_API_KEY) {
            try {
                const fullContent = await generateMarketingContent(productTitle, productUrl);
                // Adaptar formato de Gemini a TikTok Shop
                content = {
                    title: productTitle.slice(0, 60),
                    description: fullContent.telegram.content.replace(/\*\*/g, '').slice(0, 500),
                    tags: ['camping', 'ofertas', 'descuento', 'outdoor', 'amazon'],
                    cta: '¡Compra ahora con enlace en bio! 🔗',
                };
            } catch (geminiError) {
                // Fallback a OpenRouter con modelos gratuitos
                if (process.env.OPENROUTER_API_KEY) {
                    const fullContent = await generateMarketingContentAdvanced(
                        productTitle,
                        productUrl,
                        productData,
                        { useBestModel: false } // Usar modelos gratuitos
                    );
                    content = fullContent.tiktokshop;
                } else {
                    throw geminiError;
                }
            }
        } else if (process.env.OPENROUTER_API_KEY) {
            // Si no hay Gemini, usar OpenRouter con modelos gratuitos
            const fullContent = await generateMarketingContentAdvanced(
                productTitle,
                productUrl,
                productData,
                { useBestModel: false } // Usar modelos gratuitos
            );
            content = fullContent.tiktokshop;
        } else {
            // Fallback a Gemini
            const fullContent = await generateMarketingContent(productTitle, productUrl);
            // Adaptar formato de Gemini a TikTok Shop
            content = {
                title: productTitle.slice(0, 60),
                description: fullContent.telegram.content.replace(/\*\*/g, '').slice(0, 500),
                tags: ['camping', 'ofertas', 'descuento', 'outdoor', 'amazon'],
                cta: '¡Compra ahora con enlace en bio! 🔗',
            };
        } else {
            return NextResponse.json(
                { error: 'No AI provider configured. Set OPENROUTER_API_KEY or GOOGLE_API_KEY' },
                { status: 500 }
            );
        }

        return NextResponse.json({
            success: true,
            tiktokshop: content,
            tips: {
                posting: 'Publica en horarios de máxima audiencia: 19:00-21:00 y 12:00-14:00',
                hashtags: 'Usa 5-7 hashtags relevantes, mezcla populares y nicho',
                engagement: 'Responde a los primeros 10 comentarios en la primera hora',
                video: 'Añade video del producto en uso para mejor conversión',
            },
        });
    } catch (error) {
        console.error('TikTok Shop generation error:', error);
        return NextResponse.json(
            {
                error: error instanceof Error ? error.message : 'Failed to generate TikTok Shop content',
            },
            { status: 500 }
        );
    }
}
