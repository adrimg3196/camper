// Tipos para el sistema de ofertas de Amazon

export interface AmazonProduct {
    asin: string;
    title: string;
    description?: string;
    imageUrl: string;
    category: ProductCategory;
    originalPrice: number;
    discountedPrice: number;
    discountPercentage: number;
    affiliateUrl: string;
    rating?: number;
    reviewCount?: number;
    isPrime?: boolean;
    lastUpdated: Date;
}

export type ProductCategory =
    | 'tiendas-campana'
    | 'sacos-dormir'
    | 'mochilas'
    | 'cocina-camping'
    | 'iluminacion'
    | 'mobiliario'
    | 'herramientas'
    | 'accesorios';

export interface CategoryInfo {
    slug: ProductCategory;
    name: string;
    icon: string;
    description: string;
    amazonSearchIndex: string;
    keywords: string[];
}

export const CATEGORIES: CategoryInfo[] = [
    {
        slug: 'tiendas-campana',
        name: 'Tiendas de Campaña',
        icon: '⛺',
        description: 'Tiendas para camping, trekking y festivales',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['tienda campaña', 'tienda camping', 'carpa', 'tienda iglu'],
    },
    {
        slug: 'sacos-dormir',
        name: 'Sacos de Dormir',
        icon: '🛏️',
        description: 'Sacos para todas las temperaturas',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['saco dormir', 'saco monta', 'sleeping bag'],
    },
    {
        slug: 'mochilas',
        name: 'Mochilas',
        icon: '🎒',
        description: 'Mochilas de trekking y senderismo',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['mochila trekking', 'mochila senderismo', 'mochila 50l', 'mochila 60l'],
    },
    {
        slug: 'cocina-camping',
        name: 'Cocina Camping',
        icon: '🍳',
        description: 'Hornillos, utensilios y menaje',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['hornillo camping', 'cocina gas', 'utensilios camping'],
    },
    {
        slug: 'iluminacion',
        name: 'Iluminación',
        icon: '🔦',
        description: 'Linternas, frontales y farolillos',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['linterna led', 'frontal led', 'farolillo camping'],
    },
    {
        slug: 'mobiliario',
        name: 'Mobiliario',
        icon: '🪑',
        description: 'Mesas, sillas y hamacas',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['silla camping', 'mesa camping', 'hamaca'],
    },
    {
        slug: 'herramientas',
        name: 'Herramientas',
        icon: '🔧',
        description: 'Navajas, multiherramientas y kits',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['navaja suiza', 'multiherramienta', 'kit supervivencia'],
    },
    {
        slug: 'accesorios',
        name: 'Accesorios',
        icon: '🧭',
        description: 'Brújulas, GPS y complementos',
        amazonSearchIndex: 'SportingGoods',
        keywords: ['brujula', 'gps senderismo', 'botiquin camping'],
    },
];

export interface DealStats {
    totalDeals: number;
    avgDiscount: number;
    maxDiscount: number;
    lastUpdate: Date;
}
