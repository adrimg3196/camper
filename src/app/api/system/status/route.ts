import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

interface SystemStatus {
    database: {
        connected: boolean;
        dealsCount: number;
        activeDeals: number;
    };
    apis: {
        gemini: boolean;
        telegram: boolean;
        supabase: boolean;
    };
    crons: {
        dailyPublish: string;
        scrapeDeals: string;
    };
    lastActivity: {
        lastScrape: string | null;
        lastPublish: string | null;
    };
}

export async function GET() {
    const status: SystemStatus = {
        database: {
            connected: false,
            dealsCount: 0,
            activeDeals: 0,
        },
        apis: {
            gemini: !!process.env.GOOGLE_API_KEY,
            telegram: !!process.env.TELEGRAM_BOT_TOKEN,
            supabase: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
        },
        crons: {
            dailyPublish: '09:00 UTC',
            scrapeDeals: '07:00 UTC',
        },
        lastActivity: {
            lastScrape: null,
            lastPublish: null,
        },
    };

    try {
        // Test conexión a Supabase
        const { count: totalCount, error: countError } = await supabase
            .from('deals')
            .select('*', { count: 'exact', head: true });

        if (!countError) {
            status.database.connected = true;
            status.database.dealsCount = totalCount || 0;

            // Contar ofertas activas
            const { count: activeCount } = await supabase
                .from('deals')
                .select('*', { count: 'exact', head: true })
                .eq('is_active', true);

            status.database.activeDeals = activeCount || 0;
        }

        // Intentar obtener última actividad
        try {
            const { data: lastDeal } = await supabase
                .from('deals')
                .select('updated_at')
                .order('updated_at', { ascending: false })
                .limit(1)
                .single();

            if (lastDeal) {
                status.lastActivity.lastScrape = lastDeal.updated_at;
            }
        } catch {
            // Silenciar error si no hay datos
        }

        // Intentar obtener último log de publicación
        try {
            const { data: lastLog } = await supabase
                .from('publication_logs')
                .select('published_at')
                .order('published_at', { ascending: false })
                .limit(1)
                .single();

            if (lastLog) {
                status.lastActivity.lastPublish = lastLog.published_at;
            }
        } catch {
            // Tabla puede no existir
        }
    } catch (error) {
        console.error('Error checking system status:', error);
    }

    return NextResponse.json({
        status,
        healthy:
            status.database.connected &&
            status.apis.supabase,
        timestamp: new Date().toISOString(),
    });
}
