import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { exec } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';
import { promisify } from 'util';

const execAsync = promisify(exec);
const SCRAPER_COMMAND = 'python3 scraper/professional_amazon_scraper.py';
const SCRAPER_TIMEOUT_MS = 180_000;
const SCRAPER_RESULTS_FILE = 'test_results.json';

export const runtime = 'nodejs';

interface DealRecord {
    asin: string;
    title: string;
    description: string;
    price: number;
    original_price: number;
    discount: number;
    image_url: string;
    url: string;
    affiliate_url: string;
    category: string;
    rating: number | null;
    review_count: number | null;
    is_active: boolean;
}

const SAMPLE_CAMPING_DEALS: DealRecord[] = [
    {
        asin: 'B09SAMPLE01',
        title: 'Tienda de Campaña Coleman 4 Personas - Impermeable 3000mm',
        description: 'Tienda familiar con tecnología WeatherTec. Montaje en 10 minutos.',
        price: 89.99,
        original_price: 149.99,
        discount: 40,
        image_url: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400',
        url: 'https://www.amazon.es/dp/B09SAMPLE01',
        affiliate_url: 'https://www.amazon.es/dp/B09SAMPLE01?tag=camperdeals07-21',
        category: 'tiendas-campana',
        rating: 4.5,
        review_count: 234,
        is_active: true,
    },
    {
        asin: 'B09SAMPLE02',
        title: 'Saco de Dormir Mammut -15C - Pluma de Ganso',
        description: 'Saco profesional para montaña. Relleno 90/10 pluma.',
        price: 129,
        original_price: 219,
        discount: 41,
        image_url: 'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=400',
        url: 'https://www.amazon.es/dp/B09SAMPLE02',
        affiliate_url: 'https://www.amazon.es/dp/B09SAMPLE02?tag=camperdeals07-21',
        category: 'sacos-dormir',
        rating: 4.8,
        review_count: 156,
        is_active: true,
    },
    {
        asin: 'B09SAMPLE03',
        title: 'Mochila Trekking Deuter 65L - Con Funda Lluvia',
        description: 'Sistema de ventilación Aircontact. Ideal rutas largas.',
        price: 149.99,
        original_price: 249.99,
        discount: 40,
        image_url: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
        url: 'https://www.amazon.es/dp/B09SAMPLE03',
        affiliate_url: 'https://www.amazon.es/dp/B09SAMPLE03?tag=camperdeals07-21',
        category: 'mochilas',
        rating: 4.7,
        review_count: 89,
        is_active: true,
    },
    {
        asin: 'B09SAMPLE04',
        title: 'Hornillo Gas Jetboil Flash - Hervidor Integrado',
        description: 'Hierve 500ml en 100 segundos. Sistema FluxRing.',
        price: 99.99,
        original_price: 159.99,
        discount: 37,
        image_url: 'https://images.unsplash.com/photo-1536746803623-cef87080bfc8?w=400',
        url: 'https://www.amazon.es/dp/B09SAMPLE04',
        affiliate_url: 'https://www.amazon.es/dp/B09SAMPLE04?tag=camperdeals07-21',
        category: 'cocina-camping',
        rating: 4.9,
        review_count: 312,
        is_active: true,
    },
    {
        asin: 'B09SAMPLE05',
        title: 'Linterna Frontal Petzl Actik Core - 450 Lumens',
        description: 'Recargable USB. Modo rojo para visión nocturna.',
        price: 44.99,
        original_price: 74.99,
        discount: 40,
        image_url: 'https://images.unsplash.com/photo-1567653418876-5bb0e566e1c2?w=400',
        url: 'https://www.amazon.es/dp/B09SAMPLE05',
        affiliate_url: 'https://www.amazon.es/dp/B09SAMPLE05?tag=camperdeals07-21',
        category: 'iluminacion',
        rating: 4.6,
        review_count: 567,
        is_active: true,
    },
];

// Verificar que es una llamada de CRON legítima o del dashboard
function isValidCronRequest(request: Request): boolean {
    if (process.env.NODE_ENV === 'development') return true;

    const authHeader = request.headers.get('authorization');
    if (authHeader === `Bearer ${process.env.CRON_SECRET}`) return true;

    const referer = request.headers.get('referer');
    const host = request.headers.get('host');
    if (referer && host && referer.includes(host)) return true;

    return false;
}

function toNumber(value: unknown): number | null {
    if (typeof value === 'number' && Number.isFinite(value)) return value;
    if (typeof value === 'string' && value.trim() !== '') {
        const parsed = Number(value);
        return Number.isFinite(parsed) ? parsed : null;
    }
    return null;
}

function normalizeAsin(rawAsin: unknown, rawUrl: unknown): string | null {
    if (typeof rawAsin === 'string' && /^[A-Z0-9]{10}$/i.test(rawAsin.trim())) {
        return rawAsin.trim().toUpperCase();
    }

    if (typeof rawUrl === 'string') {
        const match = rawUrl.match(/\/dp\/([A-Z0-9]{10})/i);
        if (match?.[1]) {
            return match[1].toUpperCase();
        }
    }

    return null;
}

function normalizeScrapedDeal(product: Record<string, unknown>): DealRecord | null {
    const asin = normalizeAsin(product.asin, product.url);
    const title = typeof product.title === 'string' ? product.title.trim() : '';
    const url = typeof product.url === 'string' ? product.url.trim() : '';

    const price = toNumber(product.current_price) ?? toNumber(product.price);
    const originalPrice = toNumber(product.original_price);
    const discount = toNumber(product.discount);

    if (!asin || !title || !url || price === null || originalPrice === null || discount === null) {
        return null;
    }

    const category = typeof product.category === 'string' && product.category.trim() ? product.category.trim() : 'camping';
    const affiliateUrl =
        typeof product.affiliate_url === 'string' && product.affiliate_url.trim()
            ? product.affiliate_url.trim()
            : `${url}${url.includes('?') ? '&' : '?'}tag=${process.env.AMAZON_PARTNER_TAG || 'camperdeals-21'}`;

    const description =
        typeof product.description === 'string' && product.description.trim()
            ? product.description.trim()
            : `${title} - Oferta destacada de camping`;

    return {
        asin,
        title,
        description,
        price,
        original_price: originalPrice,
        discount,
        image_url:
            typeof product.image_url === 'string' && product.image_url.trim()
                ? product.image_url.trim()
                : 'https://via.placeholder.com/400x400?text=Camping+Deal',
        url,
        affiliate_url: affiliateUrl,
        category,
        rating: toNumber(product.rating),
        review_count: toNumber(product.review_count),
        is_active: true,
    };
}

function extractSummaryJsonFromStdout(stdout: string): Record<string, unknown> | null {
    const lines = stdout
        .split('\n')
        .map((line) => line.trimEnd())
        .filter(Boolean);

    for (let index = lines.length - 1; index >= 0; index--) {
        const candidate = lines.slice(index).join('\n').trim();
        if (!candidate.startsWith('{')) continue;

        try {
            const parsed = JSON.parse(candidate);
            if (parsed && typeof parsed === 'object') {
                return parsed as Record<string, unknown>;
            }
        } catch {
            // Seguir buscando hacia arriba hasta encontrar el bloque JSON válido.
        }
    }

    return null;
}

async function runProfessionalScraper(): Promise<DealRecord[]> {
    const now = new Date();
    const env = {
        ...process.env,
        SCRAPE_TIME: now.toISOString(),
        AMAZON_PARTNER_TAG: process.env.AMAZON_PARTNER_TAG || 'camperdeals-21',
    };

    const { stdout, stderr } = await execAsync(SCRAPER_COMMAND, {
        cwd: process.cwd(),
        env,
        timeout: SCRAPER_TIMEOUT_MS,
        maxBuffer: 10 * 1024 * 1024,
    });

    if (stderr?.trim()) {
        console.warn('⚠️ Advertencias del scraper:', stderr.trim());
    }

    const summary = extractSummaryJsonFromStdout(stdout);
    if (!summary || summary.success !== true) {
        throw new Error('El scraper profesional no devolvió un resumen de éxito válido');
    }

    const resultsFilePath = path.join(process.cwd(), SCRAPER_RESULTS_FILE);
    const rawResults = await fs.readFile(resultsFilePath, 'utf8');
    const parsedResults = JSON.parse(rawResults) as { products?: Record<string, unknown>[] };

    const normalizedDeals = (parsedResults.products ?? [])
        .map((product) => normalizeScrapedDeal(product))
        .filter((deal): deal is DealRecord => deal !== null);

    if (normalizedDeals.length === 0) {
        throw new Error('El scraper profesional no generó productos normalizados');
    }

    return normalizedDeals;
}

// Upsert ofertas en Supabase
async function upsertDeals(deals: DealRecord[]) {
    const results = {
        inserted: 0,
        updated: 0,
        errors: 0,
    };

    for (const deal of deals) {
        const { error } = await supabase
            .from('deals')
            .upsert(
                {
                    ...deal,
                    updated_at: new Date().toISOString(),
                },
                {
                    onConflict: 'asin',
                }
            );

        if (error) {
            console.error(`Error upserting ${deal.asin}:`, error);
            results.errors++;
        } else {
            results.inserted++;
        }
    }

    return results;
}

// Desactivar ofertas antiguas (más de 7 días sin actualizar)
async function deactivateOldDeals() {
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const { data, error } = await supabase
        .from('deals')
        .update({ is_active: false })
        .lt('updated_at', sevenDaysAgo.toISOString())
        .eq('is_active', true)
        .select('asin');

    if (error) {
        console.error('Error desactivando ofertas antiguas:', error);
        return 0;
    }

    return data?.length || 0;
}

export async function GET(request: Request) {
    if (!isValidCronRequest(request)) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🔍 CRON: Iniciando scraping de ofertas...');

    try {
        let deals: DealRecord[] = [];
        let scraperUsed = 'professional_python';
        let note: string | undefined;

        try {
            console.log('🚀 Ejecutando scraper profesional...');
            deals = await runProfessionalScraper();
            console.log(`✅ Scraper profesional devolvió ${deals.length} ofertas válidas`);
        } catch (scraperError) {
            console.error('❌ Error ejecutando scraper profesional:', scraperError);
            deals = SAMPLE_CAMPING_DEALS;
            scraperUsed = 'sample_data';
            note = 'Python scraper failed, using sample data as fallback';
        }

        console.log(`📦 Procesando ${deals.length} ofertas...`);

        const upsertResults = await upsertDeals(deals);
        const deactivated = await deactivateOldDeals();

        console.log('✅ Scraping completado:');
        console.log(`   - Fuente: ${scraperUsed}`);
        console.log(`   - Insertadas/Actualizadas: ${upsertResults.inserted}`);
        console.log(`   - Errores: ${upsertResults.errors}`);
        console.log(`   - Desactivadas (antiguas): ${deactivated}`);

        return NextResponse.json({
            success: true,
            message:
                scraperUsed === 'professional_python'
                    ? 'Professional scraping completed'
                    : 'Scraping completed (fallback mode)',
            results: {
                processed: deals.length,
                ...upsertResults,
                deactivated,
            },
            timestamp: new Date().toISOString(),
            scraper_used: scraperUsed,
            ...(note ? { note } : {}),
        });
    } catch (error) {
        console.error('❌ Error en CRON scrape-deals:', error);
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
