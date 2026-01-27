import { MetadataRoute } from 'next';
import { getSiteUrl } from '@/lib/config';

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = getSiteUrl();
    const currentDate = new Date();

    // Categorías principales de productos
    const categories = [
        { slug: 'tiendas-campana', priority: 0.9 },
        { slug: 'sacos-dormir', priority: 0.9 },
        { slug: 'mochilas', priority: 0.85 },
        { slug: 'cocina-camping', priority: 0.8 },
        { slug: 'iluminacion', priority: 0.8 },
        { slug: 'mobiliario', priority: 0.8 },
        { slug: 'colchones-esterillas', priority: 0.8 },
        { slug: 'herramientas', priority: 0.75 },
        { slug: 'accesorios', priority: 0.7 },
    ];

    // URLs de categorías
    const categoryUrls = categories.map((cat) => ({
        url: `${baseUrl}/ofertas/${cat.slug}`,
        lastModified: currentDate,
        changeFrequency: 'daily' as const,
        priority: cat.priority,
    }));

    // Guías y contenido SEO (artículos evergreen)
    const guides = [
        { slug: 'mejores-tiendas-campana-2026', priority: 0.7 },
        { slug: 'mejores-sacos-dormir-2026', priority: 0.7 },
        { slug: 'guia-camping-principiantes', priority: 0.65 },
        { slug: 'como-elegir-tienda-campana', priority: 0.65 },
        { slug: 'mejores-mochilas-trekking', priority: 0.65 },
        { slug: 'equipamiento-camping-esencial', priority: 0.6 },
        { slug: 'camping-con-ninos', priority: 0.6 },
        { slug: 'camping-invierno-guia', priority: 0.6 },
    ];

    const guideUrls = guides.map((guide) => ({
        url: `${baseUrl}/guias/${guide.slug}`,
        lastModified: currentDate,
        changeFrequency: 'weekly' as const,
        priority: guide.priority,
    }));

    // Páginas legales
    const legalPages = [
        'politica-privacidad',
        'aviso-legal',
        'politica-cookies',
        'sobre-nosotros',
        'contacto',
    ];

    const legalUrls = legalPages.map((page) => ({
        url: `${baseUrl}/${page}`,
        lastModified: new Date('2024-01-01'),
        changeFrequency: 'yearly' as const,
        priority: 0.3,
    }));

    return [
        // Página principal - máxima prioridad
        {
            url: baseUrl,
            lastModified: currentDate,
            changeFrequency: 'hourly',
            priority: 1.0,
        },
        // Página de todas las ofertas
        {
            url: `${baseUrl}/ofertas`,
            lastModified: currentDate,
            changeFrequency: 'hourly',
            priority: 0.95,
        },
        // Black Friday y ofertas especiales
        {
            url: `${baseUrl}/black-friday-camping`,
            lastModified: currentDate,
            changeFrequency: 'daily',
            priority: 0.85,
        },
        {
            url: `${baseUrl}/prime-day-camping`,
            lastModified: currentDate,
            changeFrequency: 'daily',
            priority: 0.85,
        },
        // Categorías
        ...categoryUrls,
        // Guías
        ...guideUrls,
        // Legal
        ...legalUrls,
    ];
}
