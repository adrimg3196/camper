import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://camperdeals.es';

    const categories = [
        'tiendas-campana',
        'sacos-dormir',
        'mochilas',
        'cocina-camping',
        'iluminacion',
        'mobiliario',
        'herramientas',
        'accesorios'
    ];

    const categoryUrls = categories.map((cat) => ({
        url: `${baseUrl}/ofertas/${cat}`,
        lastModified: new Date(),
        changeFrequency: 'hourly' as const,
        priority: 0.8,
    }));

    return [
        {
            url: baseUrl,
            lastModified: new Date(),
            changeFrequency: 'hourly',
            priority: 1,
        },
        ...categoryUrls,
    ];
}
