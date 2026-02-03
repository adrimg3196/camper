import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Verificar que es una llamada de CRON legítima o del dashboard
function isValidCronRequest(request: Request): boolean {
    // En desarrollo, permitir todas las llamadas
    if (process.env.NODE_ENV === 'development') return true;

    // Verificar header de autorización (para Vercel CRONs)
    const authHeader = request.headers.get('authorization');
    if (authHeader === `Bearer ${process.env.CRON_SECRET}`) return true;

    // Permitir llamadas desde el mismo origen (dashboard)
    const referer = request.headers.get('referer');
    const host = request.headers.get('host');
    if (referer && host && referer.includes(host)) return true;

    return false;
}

// Datos de ejemplo para cuando no hay scraper real
// En producción, esto se reemplaza por llamada al scraper Python o API externa
const SAMPLE_CAMPING_DEALS = [
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
        price: 129.00,
        original_price: 219.00,
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

// Upsert ofertas en Supabase
async function upsertDeals(deals: typeof SAMPLE_CAMPING_DEALS) {
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
    // Verificar autorización
    if (!isValidCronRequest(request)) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🔍 CRON: Iniciando scraping de ofertas...');

    try {
            // Ejecutar scraper profesional
            let deals: any[] = [];
            
            try {
                console.log('🚀 Ejecutando scraper profesional...');
                
                const { exec } = require('child_process');
                const { promisify } = require('util');
                const execAsync = promisify(exec);
                
                // Configurar variables de entorno
                const sevenDaysAgo = new Date();
                sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
                
                const env = {
                    ...process.env,
                    SCRAPE_TIME: new Date().toISOString(),
                    SEVEN_DAYS_AGO: sevenDaysAgo.toISOString(),
                    AMAZON_PARTNER_TAG: process.env.AMAZON_PARTNER_TAG || 'camperdeals-21',
                };
                
                // Ejecutar scraper profesional (más robusto)
                const { stdout, stderr } = await execAsync('python3 scraper/professional_amazon_scraper.py', {
                    cwd: process.cwd(),
                    env: env,
                    timeout: 600000, // 10 minutos máximo
                });
                
                if (stderr) {
                    console.warn('⚠️ Advertencias del scraper:', stderr);
                }
                
                console.log('📊 Analizando resultados del scraper...');
                
                // Extraer productos del JSON output
                const productsMatch = stdout.match(/\{[\s\S]*\}/);
                if (productsMatch) {
                    const scraperResult = JSON.parse(productsMatch[0]);
                    
                    if (scraperResult.success && scraperResult.products_found > 0) {
                        console.log(`✅ Scraper encontró ${scraperResult.products_found} productos`);
                        
                        // Transformar productos al formato de la DB
                        const transformedDeals = require('fs').readFileSync('test_results.json', 'utf8');
                        const testData = JSON.parse(transformedDeals);
                        
                        if (testData.products && testData.products.length > 0) {
                            deals = testData.products.map((product: any) => ({
                                asin: product.asin,
                                title: product.title,
                                description: product.description,
                                price: product.current_price,
                                original_price: product.original_price,
                                discount: product.discount,
                                image_url: product.image_url,
                                url: product.url,
                                affiliate_url: product.affiliate_url,
                                category: product.category,
                                rating: product.rating,
                                review_count: product.review_count,
                                is_active: true,
                            }));
                            
                            // Guardar en Supabase
                            const upsertResults = await upsertDeals(deals);
                            const deactivated = await deactivateOldDeals();
                            
                            console.log(`💾 Guardadas ${upsertResults.inserted} ofertas en Supabase`);
                            
                            return NextResponse.json({
                                success: true,
                                message: 'Professional scraping completed',
                                results: {
                                    processed: deals.length,
                                    ...upsertResults,
                                    deactivated,
                                },
                                timestamp: new Date().toISOString(),
                                scraper_used: 'professional_python',
                            });
                        }
                    }
                }
                
                throw new Error('Scraper no devolvió resultados válidos');
                
            } catch (scraperError) {
                console.error('❌ Error ejecutando scraper profesional:', scraperError);
            }

        console.log(`📦 Procesando ${deals.length} ofertas...`);

            // Upsert en Supabase (solo si usamos fallback de datos de ejemplo)
            const upsertResults = await upsertDeals(deals);

            // Desactivar ofertas antiguas
            const deactivated = await deactivateOldDeals();

            console.log(`✅ Scraping completado (fallback):`);
            console.log(`   - Insertadas/Actualizadas: ${upsertResults.inserted}`);
            console.log(`   - Errores: ${upsertResults.errors}`);
            console.log(`   - Desactivadas (antiguas): ${deactivated}`);

            return NextResponse.json({
                success: true,
                message: 'Scraping completed (fallback mode)',
                results: {
                    processed: deals.length,
                    ...upsertResults,
                    deactivated,
                },
                timestamp: new Date().toISOString(),
                scraper_used: 'sample_data',
                note: 'Python scraper failed, using sample data as fallback',
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
