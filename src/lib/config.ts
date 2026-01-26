/**
 * Configuración centralizada del sitio
 * Usa variables de entorno o valores por defecto
 */

export const SITE_CONFIG = {
    url: process.env.NEXT_PUBLIC_SITE_URL || 'https://camper-omega.vercel.app',
    name: 'CampingDeals España',
    description: 'Las mejores ofertas de camping con más del 30% de descuento',
    email: process.env.SITE_EMAIL || 'info@ofertascamping.es',
    twitter: '@campingdeals_es',
} as const;

/**
 * Obtiene la URL base del sitio
 */
export function getSiteUrl(): string {
    return SITE_CONFIG.url;
}

/**
 * Construye una URL completa desde una ruta relativa
 */
export function getAbsoluteUrl(path: string): string {
    const baseUrl = getSiteUrl();
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${baseUrl}${cleanPath}`;
}
