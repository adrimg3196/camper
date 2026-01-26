import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

// Verificar que es una llamada de CRON legítima de Vercel
function isValidCronRequest(request: Request): boolean {
    const authHeader = request.headers.get('authorization');
    // En producción, Vercel añade un header de autorización
    // En desarrollo, permitimos todas las llamadas
    if (process.env.NODE_ENV === 'development') return true;
    return authHeader === `Bearer ${process.env.CRON_SECRET}`;
}

// Formatear oferta para Telegram
function formatTelegramMessage(deal: any): string {
    const categoryEmojis: Record<string, string> = {
        'tiendas-campana': '⛺',
        'sacos-dormir': '🛏️',
        'mochilas': '🎒',
        'cocina-camping': '🍳',
        'iluminacion': '🔦',
        'mobiliario': '🪑',
        'colchones': '🛋️',
        'herramientas': '🔧',
    };

    const emoji = categoryEmojis[deal.category] || '🏕️';
    const savings = deal.original_price - deal.price;

    return `
${emoji} *¡OFERTA -${deal.discount}%!*

📦 ${deal.title.slice(0, 100)}${deal.title.length > 100 ? '...' : ''}

💰 ~${deal.original_price.toFixed(2)}€~ → *${deal.price.toFixed(2)}€*
💵 Ahorras: ${savings.toFixed(2)}€

${deal.rating ? `⭐ ${deal.rating}/5` : ''}

🔗 [Ver en Amazon](${deal.affiliate_url || deal.url})

_Enlace de afiliado. Los precios pueden variar._
`.trim();
}

// Enviar mensaje a Telegram
async function sendTelegramMessage(message: string, imageUrl?: string): Promise<boolean> {
    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const channelId = process.env.TELEGRAM_CHANNEL_ID || '@camperdeals';

    if (!botToken) {
        console.warn('TELEGRAM_BOT_TOKEN no configurado');
        return false;
    }

    try {
        const baseUrl = `https://api.telegram.org/bot${botToken}`;

        if (imageUrl && !imageUrl.includes('placeholder')) {
            // Enviar con foto
            const response = await fetch(`${baseUrl}/sendPhoto`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: channelId,
                    photo: imageUrl,
                    caption: message,
                    parse_mode: 'Markdown',
                }),
            });
            return response.ok;
        } else {
            // Enviar solo texto
            const response = await fetch(`${baseUrl}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: channelId,
                    text: message,
                    parse_mode: 'Markdown',
                    disable_web_page_preview: false,
                }),
            });
            return response.ok;
        }
    } catch (error) {
        console.error('Error enviando mensaje Telegram:', error);
        return false;
    }
}

// Obtener las mejores ofertas del día
async function getBestDeals(limit: number = 5) {
    const { data, error } = await supabase
        .from('deals')
        .select('*')
        .eq('is_active', true)
        .gte('discount', 30)
        .order('discount', { ascending: false })
        .limit(limit);

    if (error) {
        console.error('Error obteniendo ofertas:', error);
        return [];
    }

    return data || [];
}

// Log de publicación en Supabase
async function logPublication(dealId: string, platform: string, success: boolean) {
    try {
        await supabase.from('publication_logs').insert({
            deal_id: dealId,
            platform,
            success,
            published_at: new Date().toISOString(),
        });
    } catch (e) {
        // Silenciar si la tabla no existe
        console.log('No se pudo registrar log (tabla puede no existir)');
    }
}

export async function GET(request: Request) {
    // Verificar autorización
    if (!isValidCronRequest(request)) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🤖 CRON: Iniciando publicación diaria...');

    try {
        // Obtener mejores ofertas
        const deals = await getBestDeals(3); // 3 ofertas por día

        if (deals.length === 0) {
            console.log('⚠️ No hay ofertas para publicar');
            return NextResponse.json({
                success: true,
                message: 'No deals to publish',
                published: 0,
            });
        }

        let published = 0;
        const results: any[] = [];

        for (const deal of deals) {
            const message = formatTelegramMessage(deal);
            const success = await sendTelegramMessage(message, deal.image_url);

            if (success) {
                published++;
                console.log(`✅ Publicado: ${deal.title.slice(0, 50)}...`);
            } else {
                console.log(`❌ Error: ${deal.title.slice(0, 50)}...`);
            }

            results.push({
                id: deal.asin || deal.id,
                title: deal.title.slice(0, 50),
                success,
            });

            // Log en DB
            await logPublication(deal.asin || deal.id, 'telegram', success);

            // Rate limiting: esperar 3 segundos entre mensajes
            if (deals.indexOf(deal) < deals.length - 1) {
                await new Promise((resolve) => setTimeout(resolve, 3000));
            }
        }

        console.log(`📊 Publicación completada: ${published}/${deals.length}`);

        return NextResponse.json({
            success: true,
            message: `Published ${published} of ${deals.length} deals`,
            published,
            total: deals.length,
            results,
            timestamp: new Date().toISOString(),
        });
    } catch (error) {
        console.error('❌ Error en CRON daily-publish:', error);
        return NextResponse.json(
            {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error',
            },
            { status: 500 }
        );
    }
}

// También permitir POST para testing manual
export async function POST(request: Request) {
    return GET(request);
}
