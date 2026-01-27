'use client';

import Script from 'next/script';

interface AdSenseProps {
    clientId: string;
    slot: string;
    format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal';
    style?: React.CSSProperties;
    className?: string;
}

/**
 * Componente de Google AdSense optimizado
 */
export default function AdSense({ clientId, slot, format = 'auto', style, className }: AdSenseProps) {
    if (!clientId || !slot) {
        return null;
    }

    return (
        <>
            <Script
                async
                src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${clientId}`}
                crossOrigin="anonymous"
                strategy="lazyOnload"
            />
            <ins
                className={`adsbygoogle ${className || ''}`}
                style={{
                    display: 'block',
                    ...style,
                }}
                data-ad-client={clientId}
                data-ad-slot={slot}
                data-ad-format={format}
                data-full-width-responsive="true"
            />
            <Script id={`adsense-${slot}`} strategy="afterInteractive">
                {`(adsbygoogle = window.adsbygoogle || []).push({});`}
            </Script>
        </>
    );
}
