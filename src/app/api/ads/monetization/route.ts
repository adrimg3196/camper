import { NextResponse } from 'next/server';

/**
 * Sistema de monetización con múltiples fuentes de ingresos
 * - Google AdSense
 * - Media.net
 * - Amazon Native Ads
 * - Affiliate links optimizados
 */

interface MonetizationConfig {
    adsense: {
        enabled: boolean;
        clientId?: string;
        slots: {
            sidebar: string;
            content: string;
            footer: string;
        };
    };
    medianet: {
        enabled: boolean;
        siteId?: string;
    };
    amazon: {
        enabled: boolean;
        tag?: string;
    };
}

export async function GET() {
    const config: MonetizationConfig = {
        adsense: {
            enabled: !!process.env.GOOGLE_ADSENSE_CLIENT_ID,
            clientId: process.env.GOOGLE_ADSENSE_CLIENT_ID,
            slots: {
                sidebar: process.env.ADSENSE_SLOT_SIDEBAR || '',
                content: process.env.ADSENSE_SLOT_CONTENT || '',
                footer: process.env.ADSENSE_SLOT_FOOTER || '',
            },
        },
        medianet: {
            enabled: !!process.env.MEDIANET_SITE_ID,
            siteId: process.env.MEDIANET_SITE_ID,
        },
        amazon: {
            enabled: !!process.env.AMAZON_PARTNER_TAG,
            tag: process.env.AMAZON_PARTNER_TAG,
        },
    };

    return NextResponse.json({
        success: true,
        config,
        recommendations: generateRecommendations(config),
    });
}

function generateRecommendations(config: MonetizationConfig): string[] {
    const recommendations: string[] = [];

    if (!config.adsense.enabled) {
        recommendations.push('Configura Google AdSense para monetización inmediata');
    }

    if (!config.medianet.enabled) {
        recommendations.push('Considera Media.net como alternativa/complemento a AdSense');
    }

    if (!config.amazon.enabled) {
        recommendations.push('Asegúrate de tener AMAZON_PARTNER_TAG configurado');
    }

    if (config.adsense.enabled && !config.medianet.enabled) {
        recommendations.push('Combinar AdSense + Media.net puede aumentar ingresos un 20-30%');
    }

    return recommendations;
}
