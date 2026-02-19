import { supabase } from './supabase';
import { Product } from './types';

// Mock data con productos reales verificados en Amazon España
const MOCK_PRODUCTS: Product[] = [
    {
        id: '1',
        asin: 'B019N9W7WC',
        title: 'Coleman Tienda de Campaña Sundome 2 Personas',
        price: 200.13,
        original_price: 200.13,
        discount: 0,
        rating: 4.7,
        review_count: 11359,
        image_url: 'https://m.media-amazon.com/images/I/71AIHD5lPvL._AC_SL1500_.jpg',
        category: 'tiendas-campana',
        url: 'https://www.amazon.es/dp/B019N9W7WC',
        affiliate_url: 'https://www.amazon.es/dp/B019N9W7WC?tag=camperdeals07-21',
        isPrime: false
    },
    {
        id: '2',
        asin: 'B077XQDZW4',
        title: 'MalloMe Saco de Dormir para Adulto, Invierno y Verano',
        price: 31.58,
        original_price: 34.99,
        discount: 10,
        rating: 4.6,
        review_count: 15548,
        image_url: 'https://m.media-amazon.com/images/I/81D0F56EvDL._AC_SL1500_.jpg',
        category: 'sacos-dormir',
        url: 'https://www.amazon.es/dp/B077XQDZW4',
        affiliate_url: 'https://www.amazon.es/dp/B077XQDZW4?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '3',
        asin: 'B07DWCJ3DP',
        title: 'Bseash Mochila de Senderismo Impermeable 60L',
        price: 46.99,
        original_price: 46.99,
        discount: 0,
        rating: 4.2,
        review_count: 5052,
        image_url: 'https://m.media-amazon.com/images/I/51x6Pw1S+0L._AC_SL1500_.jpg',
        category: 'mochilas',
        url: 'https://www.amazon.es/dp/B07DWCJ3DP',
        affiliate_url: 'https://www.amazon.es/dp/B07DWCJ3DP?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '4',
        asin: 'B00MR34RCA',
        title: 'Hornillo de Gas con Maletín + 16 Cartuchos de Gas',
        price: 54.80,
        original_price: 54.80,
        discount: 0,
        rating: 4.6,
        review_count: 6149,
        image_url: 'https://m.media-amazon.com/images/I/81uAeCpBPCL._AC_SL1500_.jpg',
        category: 'cocina-camping',
        url: 'https://www.amazon.es/dp/B00MR34RCA',
        affiliate_url: 'https://www.amazon.es/dp/B00MR34RCA?tag=camperdeals07-21',
        isPrime: false
    },
    {
        id: '5',
        asin: 'B0F1F6LZG3',
        title: 'Lepro Linterna Frontal LED Recargable 2000 Lux',
        price: 11.99,
        original_price: 11.99,
        discount: 0,
        rating: 4.6,
        review_count: 20038,
        image_url: 'https://m.media-amazon.com/images/I/51p7Ch4eppL._AC_SL1500_.jpg',
        category: 'iluminacion',
        url: 'https://www.amazon.es/dp/B0F1F6LZG3',
        affiliate_url: 'https://www.amazon.es/dp/B0F1F6LZG3?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '6',
        asin: 'B09TDGG6KH',
        title: 'GCI Outdoor Freestyle Rocker Mecedora Portátil Camping',
        price: 326.16,
        original_price: 326.16,
        discount: 0,
        rating: 4.7,
        review_count: 22910,
        image_url: 'https://m.media-amazon.com/images/I/81BpeFnB1UL._AC_SL1500_.jpg',
        category: 'mobiliario',
        url: 'https://www.amazon.es/dp/B09TDGG6KH',
        affiliate_url: 'https://www.amazon.es/dp/B09TDGG6KH?tag=camperdeals07-21',
        isPrime: false
    },
    {
        id: '7',
        asin: 'B000IAZDEU',
        title: 'Victorinox Navaja Cazador 15 Funciones Camping',
        price: 31.52,
        original_price: 45.00,
        discount: 30,
        rating: 4.8,
        review_count: 26378,
        image_url: 'https://m.media-amazon.com/images/I/61PHPBMzXPL._AC_SL1500_.jpg',
        category: 'herramientas',
        url: 'https://www.amazon.es/dp/B000IAZDEU',
        affiliate_url: 'https://www.amazon.es/dp/B000IAZDEU?tag=camperdeals07-21',
        isPrime: true
    },
    {
        id: '8',
        asin: 'B07CK8B3R3',
        title: 'Brújula de Orientación para Senderismo y Montaña',
        price: 31.45,
        original_price: 31.45,
        discount: 0,
        rating: 4.5,
        review_count: 8309,
        image_url: 'https://m.media-amazon.com/images/I/81RqOPaCk4L._AC_SL1500_.jpg',
        category: 'accesorios',
        url: 'https://www.amazon.es/dp/B07CK8B3R3',
        affiliate_url: 'https://www.amazon.es/dp/B07CK8B3R3?tag=camperdeals07-21',
        isPrime: false
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
