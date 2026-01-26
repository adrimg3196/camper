import { MetadataRoute } from 'next';
import { getSiteUrl } from '@/lib/config';

export default function robots(): MetadataRoute.Robots {
    const baseUrl = getSiteUrl();

    return {
        rules: [
            {
                // Reglas para todos los bots
                userAgent: '*',
                allow: '/',
                disallow: [
                    '/api/',
                    '/admin/',
                    '/_next/',
                    '/private/',
                    '/*.json$',
                ],
            },
            {
                // Reglas específicas para Googlebot
                userAgent: 'Googlebot',
                allow: '/',
                disallow: ['/api/', '/admin/'],
            },
            {
                // Reglas para Googlebot-Image (permitir todas las imágenes)
                userAgent: 'Googlebot-Image',
                allow: '/',
            },
            {
                // Reglas para Bingbot
                userAgent: 'Bingbot',
                allow: '/',
                disallow: ['/api/', '/admin/'],
            },
            {
                // Bloquear bots de IA que copian contenido
                userAgent: 'GPTBot',
                disallow: '/',
            },
            {
                userAgent: 'ChatGPT-User',
                disallow: '/',
            },
            {
                userAgent: 'CCBot',
                disallow: '/',
            },
            {
                userAgent: 'anthropic-ai',
                disallow: '/',
            },
        ],
        sitemap: `${baseUrl}/sitemap.xml`,
        host: baseUrl,
    };
}
