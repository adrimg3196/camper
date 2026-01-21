import { supabase } from './supabase';
import { Product } from './types';

// Mock data con productos reales de Amazon España
const MOCK_PRODUCTS: Product[] = [
    {
        id: '1',
        asin: 'B0BKJNXH8K',
        title: 'Coleman Coastline 3 Plus - Tienda de Campaña 3 Personas',
        price: 89.99,
        original_price: 169.99,
        discount: 47,
        rating: 4.5,
        review_count: 1250,
        image_url: 'https://m.media-amazon.com/images/I/81Zt42ioCgL._AC_SL1500_.jpg',
        category: 'tiendas-campana',
        url: 'https://www.amazon.es/dp/B0BKJNXH8K',
        affiliate_url: 'https://www.amazon.es/dp/B0BKJNXH8K?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '2',
        asin: 'B07WRZG371',
        title: 'Forceatt Saco de Dormir Ultraligero -10°C a 15°C',
        price: 39.99,
        original_price: 69.99,
        discount: 43,
        rating: 4.4,
        review_count: 3420,
        image_url: 'https://m.media-amazon.com/images/I/71nR8rQxKBL._AC_SL1500_.jpg',
        category: 'sacos-dormir',
        url: 'https://www.amazon.es/dp/B07WRZG371',
        affiliate_url: 'https://www.amazon.es/dp/B07WRZG371?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '3',
        asin: 'B08CXNK7YD',
        title: 'HOMIEE Mochila Senderismo 50L Impermeable con Cubierta Lluvia',
        price: 35.99,
        original_price: 59.99,
        discount: 40,
        rating: 4.6,
        review_count: 2890,
        image_url: 'https://m.media-amazon.com/images/I/71ypXKsLmhL._AC_SL1500_.jpg',
        category: 'mochilas',
        url: 'https://www.amazon.es/dp/B08CXNK7YD',
        affiliate_url: 'https://www.amazon.es/dp/B08CXNK7YD?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '4',
        asin: 'B08P54LYVS',
        title: 'Odoland Kit Utensilios Cocina Camping 15 Piezas',
        price: 29.99,
        original_price: 49.99,
        discount: 40,
        rating: 4.5,
        review_count: 1567,
        image_url: 'https://m.media-amazon.com/images/I/81lRHHLHpZL._AC_SL1500_.jpg',
        category: 'cocina-camping',
        url: 'https://www.amazon.es/dp/B08P54LYVS',
        affiliate_url: 'https://www.amazon.es/dp/B08P54LYVS?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '5',
        asin: 'B07RJB5VHH',
        title: 'LE Linterna Frontal LED Recargable USB 2000 Lúmenes',
        price: 19.99,
        original_price: 35.99,
        discount: 44,
        rating: 4.7,
        review_count: 8920,
        image_url: 'https://m.media-amazon.com/images/I/61kHvL+kSQL._AC_SL1500_.jpg',
        category: 'iluminacion',
        url: 'https://www.amazon.es/dp/B07RJB5VHH',
        affiliate_url: 'https://www.amazon.es/dp/B07RJB5VHH?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '6',
        asin: 'B0875L5N4V',
        title: 'KingCamp Silla Camping Plegable con Reposabrazos y Portavasos',
        price: 42.99,
        original_price: 74.99,
        discount: 43,
        rating: 4.4,
        review_count: 2134,
        image_url: 'https://m.media-amazon.com/images/I/71BqCqPq8SL._AC_SL1500_.jpg',
        category: 'mobiliario',
        url: 'https://www.amazon.es/dp/B0875L5N4V',
        affiliate_url: 'https://www.amazon.es/dp/B0875L5N4V?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '7',
        asin: 'B07MGPXN5W',
        title: 'Leatherman FREE P4 - Multiherramienta 21 Funciones',
        price: 129.99,
        original_price: 219.99,
        discount: 41,
        rating: 4.8,
        review_count: 567,
        image_url: 'https://m.media-amazon.com/images/I/61YaD2Pj9EL._AC_SL1500_.jpg',
        category: 'herramientas',
        url: 'https://www.amazon.es/dp/B07MGPXN5W',
        affiliate_url: 'https://www.amazon.es/dp/B07MGPXN5W?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '8',
        asin: 'B07N2BLG4Q',
        title: 'Garmin eTrex 32x GPS de Mano con Brújula y Altímetro',
        price: 199.99,
        original_price: 299.99,
        discount: 33,
        rating: 4.6,
        review_count: 1823,
        image_url: 'https://m.media-amazon.com/images/I/71Rsd16PFZL._AC_SL1500_.jpg',
        category: 'accesorios',
        url: 'https://www.amazon.es/dp/B07N2BLG4Q',
        affiliate_url: 'https://www.amazon.es/dp/B07N2BLG4Q?tag=camperdeals07-21',
        isPrime: true
    }
];

export async function getProducts(): Promise<Product[]> {
    try {
        const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
        const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

        console.log("🔍 [PROD DEBUG] Intentando conectar a Supabase...");
        console.log("🔍 [PROD DEBUG] Config URL:", url ? url.substring(0, 20) + "..." : "Faltante");
        console.log("🔍 [PROD DEBUG] Config KEY:", key ? "Presente (Longitud: " + key.length + ")" : "Faltante");

        if (url && key && !url.includes('placeholder')) {
            const { data, error } = await supabase
                .from('deals')
                .select('*')
                .eq('is_active', true)
                .order('id', { ascending: false });

            if (error) {
                console.error("❌ Error de Supabase:", error.message);
                throw error;
            }

            if (data && data.length > 0) {
                console.log(`✅ ${data.length} ofertas recuperadas de DB.`);
                return data.map((item: any): Product => ({
                    id: item.id.toString(),
                    asin: item.asin || `DB-${item.id}`,
                    title: item.marketing_title || item.title,
                    marketing_title: item.marketing_title,
                    marketing_description: item.marketing_description,
                    description: item.description,
                    price: item.price,
                    original_price: item.original_price,
                    discount: item.discount,
                    image_url: item.image_url,
                    category: item.category,
                    url: item.url,
                    affiliate_url: item.affiliate_url || item.url,
                    created_at: item.created_at,
                    rating: item.rating || 4.5,
                    review_count: item.review_count || 0,
                    isPrime: true
                }));
            } else {
                console.warn("⚠️ Supabase respondió vacío.");
            }
        } else {
            console.warn("⚠️ Variable NEXT_PUBLIC_SUPABASE_URL no configurada correctamente.");
        }
    } catch (e: any) {
        console.error('❌ [PROD ERROR] Error crítico en getProducts:', e.message || e);
    }

    console.warn("⚠️ [PROD WARNING] Usando MOCK_PRODUCTS como fallback.");
    return MOCK_PRODUCTS;
}
