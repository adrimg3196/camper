import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

/**
 * Sistema de captación masiva de suscriptores para Telegram
 * Incluye: Landing pages, giveaways, incentivos, tracking
 */

interface TelegramCaptureData {
    email?: string;
    name?: string;
    source?: string; // 'landing', 'giveaway', 'popup', etc.
    utm_source?: string;
    utm_campaign?: string;
    utm_medium?: string;
}

// Guardar lead en Supabase
async function saveLead(data: TelegramCaptureData) {
    try {
        const { error } = await supabase.from('telegram_leads').insert({
            email: data.email,
            name: data.name,
            source: data.source || 'unknown',
            utm_source: data.utm_source,
            utm_campaign: data.utm_campaign,
            utm_medium: data.utm_medium,
            created_at: new Date().toISOString(),
            subscribed: false, // Se marca como true cuando se suscribe
        });

        if (error) {
            console.error('Error saving lead:', error);
            return false;
        }
        return true;
    } catch (error) {
        console.error('Error in saveLead:', error);
        return false;
    }
}

// Enviar mensaje de bienvenida automático
async function sendWelcomeMessage(email: string, channelId: string) {
    // Esto se puede hacer con un webhook o bot de Telegram
    // Por ahora solo registramos
    console.log(`Welcome message queued for: ${email} -> ${channelId}`);
    return true;
}

export async function POST(request: Request) {
    const body = await request.json();
    const { email, name, source, utm_source, utm_campaign, utm_medium } = body;

    try {
        // Validar email
        if (!email || !email.includes('@')) {
            return NextResponse.json(
                { error: 'Email inválido' },
                { status: 400 }
            );
        }

        // Guardar lead
        const saved = await saveLead({
            email,
            name,
            source,
            utm_source,
            utm_campaign,
            utm_medium,
        });

        if (!saved) {
            return NextResponse.json(
                { error: 'Error al guardar lead' },
                { status: 500 }
            );
        }

        // Obtener canal de Telegram
        const channelId = process.env.TELEGRAM_CHANNEL_ID || '@camperdeals';

        // Enviar mensaje de bienvenida (si está configurado)
        if (process.env.TELEGRAM_BOT_TOKEN) {
            await sendWelcomeMessage(email, channelId);
        }

        return NextResponse.json({
            success: true,
            message: 'Lead capturado correctamente',
            channel: channelId,
            nextSteps: [
                'Recibirás un email con el enlace al canal',
                'Únete al canal para recibir ofertas exclusivas',
                'Participa en nuestros giveaways semanales',
            ],
        });
    } catch (error) {
        console.error('Telegram capture error:', error);
        return NextResponse.json(
            {
                error: error instanceof Error ? error.message : 'Error al procesar solicitud',
            },
            { status: 500 }
        );
    }
}

// GET para obtener estadísticas de captación
export async function GET() {
    try {
        const { count, error } = await supabase
            .from('telegram_leads')
            .select('*', { count: 'exact', head: true });

        if (error) {
            return NextResponse.json(
                { error: 'Error al obtener estadísticas' },
                { status: 500 }
            );
        }

        // Obtener leads por fuente
        const { data: bySource } = await supabase
            .from('telegram_leads')
            .select('source')
            .eq('subscribed', true);

        const stats = {
            total: count || 0,
            subscribed: bySource?.length || 0,
            conversionRate: count ? ((bySource?.length || 0) / count) * 100 : 0,
            sources: {} as Record<string, number>,
        };

        // Contar por fuente
        bySource?.forEach((lead) => {
            const source = lead.source || 'unknown';
            stats.sources[source] = (stats.sources[source] || 0) + 1;
        });

        return NextResponse.json({
            success: true,
            stats,
        });
    } catch (error) {
        return NextResponse.json(
            {
                error: error instanceof Error ? error.message : 'Error al obtener estadísticas',
            },
            { status: 500 }
        );
    }
}
