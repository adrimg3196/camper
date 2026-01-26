import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Script from "next/script";
import { getSiteUrl } from "@/lib/config";

const inter = Inter({ subsets: ["latin"] });

// SEO Ultra Optimizado para máximo posicionamiento
export const metadata: Metadata = {
    // Metadatos básicos
    title: {
        default: "Ofertas Camping 2026 | Chollos +30% Descuento | CampingDeals España",
        template: "%s | CampingDeals España"
    },
    description: "🏕️ Las MEJORES ofertas de camping con +30% descuento. Tiendas de campaña, sacos de dormir, mochilas trekking y equipamiento outdoor. ✓ Actualizado diariamente ✓ Envío Prime ✓ Precios más bajos garantizados.",

    // Keywords SEO (long-tail incluidas)
    keywords: [
        // Principales
        "ofertas camping",
        "chollos camping",
        "descuentos camping",
        "ofertas tiendas campaña",
        "sacos dormir baratos",

        // Long-tail
        "ofertas camping amazon",
        "chollos material camping",
        "descuentos equipamiento outdoor",
        "tiendas campaña baratas amazon",
        "sacos dormir oferta prime",
        "mochilas trekking descuento",
        "ofertas camping 2026",
        "black friday camping",

        // Geolocalización
        "ofertas camping españa",
        "tiendas campaña madrid",
        "camping barato barcelona",

        // Intención de compra
        "comprar tienda campaña barata",
        "mejor precio saco dormir",
        "donde comprar material camping"
    ],

    // Autores y creadores
    authors: [{ name: "CampingDeals España", url: "https://ofertascamping.es" }],
    creator: "CampingDeals España",
    publisher: "CampingDeals España",

    // Configuración de indexación
    robots: {
        index: true,
        follow: true,
        nocache: false,
        googleBot: {
            index: true,
            follow: true,
            noimageindex: false,
            "max-video-preview": -1,
            "max-image-preview": "large",
            "max-snippet": -1,
        },
    },

    // Open Graph (Facebook, LinkedIn, WhatsApp)
    openGraph: {
        title: "🏕️ Ofertas Camping +30% Descuento | CampingDeals España",
        description: "Las mejores ofertas de camping y outdoor con más del 30% de descuento. Tiendas, sacos, mochilas y más. Actualizado diariamente.",
        url: process.env.NEXT_PUBLIC_SITE_URL || "https://camper-omega.vercel.app",
        siteName: "CampingDeals España",
        images: [
            {
                url: "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=630&fit=crop",
                width: 1200,
                height: 630,
                alt: "Ofertas Camping España - Mejores descuentos en equipamiento outdoor",
            },
        ],
        locale: "es_ES",
        type: "website",
    },

    // Twitter Card
    twitter: {
        card: "summary_large_image",
        title: "🏕️ Ofertas Camping +30% Descuento",
        description: "Las mejores ofertas de camping y outdoor. Tiendas, sacos, mochilas con descuentos increíbles.",
        images: ["https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=630&fit=crop"],
        creator: "@campingdeals_es",
        site: "@campingdeals_es",
    },

    // Verificación de propiedad
    verification: {
        google: "tu-codigo-google-search-console",
        // yandex: "tu-codigo-yandex",
        // bing: "tu-codigo-bing",
    },

    // Alternates para idiomas y canonical
    alternates: {
        canonical: process.env.NEXT_PUBLIC_SITE_URL || "https://camper-omega.vercel.app",
        languages: {
            "es-ES": process.env.NEXT_PUBLIC_SITE_URL || "https://camper-omega.vercel.app",
            "es": process.env.NEXT_PUBLIC_SITE_URL || "https://camper-omega.vercel.app",
        },
    },

    // Categoría del sitio
    category: "shopping",

    // Otros metadatos
    applicationName: "CampingDeals España",
    referrer: "origin-when-cross-origin",
    formatDetection: {
        email: false,
        address: false,
        telephone: false,
    },

    // Metadatos adicionales
    other: {
        "google-site-verification": "tu-codigo-verificacion",
        "msvalidate.01": "tu-codigo-bing",
        "apple-mobile-web-app-title": "CampingDeals",
        "application-name": "CampingDeals España",
        "theme-color": "#1e293b",
        "color-scheme": "dark",
    },
};

// Viewport optimizado para móviles
export const viewport: Viewport = {
    themeColor: [
        { media: "(prefers-color-scheme: light)", color: "#f8fafc" },
        { media: "(prefers-color-scheme: dark)", color: "#1e293b" },
    ],
    width: "device-width",
    initialScale: 1,
    maximumScale: 5,
    userScalable: true,
    colorScheme: "dark",
};

// Schema.org JSON-LD para Rich Snippets (se genera dinámicamente)
function getJsonLd() {
    const siteUrl = getSiteUrl();
    return {
        "@context": "https://schema.org",
        "@graph": [
            // Organization Schema
            {
                "@type": "Organization",
                "@id": `${siteUrl}/#organization`,
                "name": "CampingDeals España",
                "url": siteUrl,
                "logo": {
                    "@type": "ImageObject",
                    "url": `${siteUrl}/logo.png`,
                    "width": 512,
                    "height": 512
                },
                "description": "Las mejores ofertas de camping y outdoor con más del 30% de descuento",
                "sameAs": [
                    "https://twitter.com/campingdeals_es",
                    "https://facebook.com/campingdeals.es",
                    "https://instagram.com/campingdeals_es"
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "customer service",
                    "availableLanguage": ["Spanish"]
                }
            },
            // WebSite Schema con SearchAction
            {
                "@type": "WebSite",
                "@id": `${siteUrl}/#website`,
                "url": siteUrl,
                "name": "CampingDeals España - Ofertas Camping",
                "description": "Encuentra las mejores ofertas de camping con descuentos de más del 30%",
                "publisher": { "@id": `${siteUrl}/#organization` },
                "inLanguage": "es-ES",
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": `${siteUrl}/buscar?q={search_term_string}`
                    },
                    "query-input": "required name=search_term_string"
                }
            },
            // WebPage Schema
            {
                "@type": "WebPage",
                "@id": `${siteUrl}/#webpage`,
                "url": siteUrl,
                "name": "Ofertas Camping 2026 | Chollos +30% Descuento",
                "isPartOf": { "@id": `${siteUrl}/#website` },
                "about": { "@id": `${siteUrl}/#organization` },
                "description": "Las mejores ofertas de camping con más del 30% de descuento",
                "inLanguage": "es-ES",
                "datePublished": "2024-01-01",
                "dateModified": new Date().toISOString().split('T')[0],
                "breadcrumb": { "@id": `${siteUrl}/#breadcrumb` }
            },
            // BreadcrumbList Schema
            {
                "@type": "BreadcrumbList",
                "@id": `${siteUrl}/#breadcrumb`,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Inicio",
                        "item": siteUrl
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Ofertas del Día",
                        "item": `${siteUrl}/#ofertas`
                    }
                ]
            },
            // ItemList Schema para productos (Rich Snippets de productos)
            {
                "@type": "ItemList",
                "@id": `${siteUrl}/#productlist`,
                "name": "Ofertas de Camping Destacadas",
                "description": "Las mejores ofertas de equipamiento de camping con descuentos superiores al 30%",
                "numberOfItems": 4,
                "itemListOrder": "https://schema.org/ItemListOrderDescending"
            },
        // FAQPage Schema
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "¿Con qué frecuencia se actualizan las ofertas de camping?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Nuestras ofertas de camping se actualizan diariamente. Escaneamos Amazon y otras tiendas cada 24 horas para encontrar los mejores descuentos en tiendas de campaña, sacos de dormir, mochilas y más equipamiento outdoor."
                    }
                },
                {
                    "@type": "Question",
                    "name": "¿Cuánto descuento puedo encontrar en material de camping?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Todas nuestras ofertas tienen un mínimo del 30% de descuento. Algunos productos de camping pueden llegar a tener descuentos del 50-70% en épocas especiales como Black Friday o Prime Day."
                    }
                },
                {
                    "@type": "Question",
                    "name": "¿Son seguras las compras a través de vuestros enlaces?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Sí, todos nuestros enlaces dirigen a Amazon España, una plataforma 100% segura. Somos afiliados de Amazon, lo que significa que recibimos una pequeña comisión sin coste adicional para ti."
                    }
                }
            ]
        }
    ]
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="es" className="dark">
            <head>
                {/* Preconnect para optimizar carga */}
                <link rel="preconnect" href="https://images.unsplash.com" />
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://www.amazon.es" />

                {/* DNS Prefetch */}
                <link rel="dns-prefetch" href="https://www.google-analytics.com" />
                <link rel="dns-prefetch" href="https://www.googletagmanager.com" />

                {/* Favicon y PWA */}
                <link rel="icon" href="/favicon.ico" sizes="any" />
                <link rel="icon" href="/icon.svg" type="image/svg+xml" />
                <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
                <link rel="manifest" href="/manifest.json" />

                {/* Schema.org JSON-LD */}
                <script
                    type="application/ld+json"
                    dangerouslySetInnerHTML={{ __html: JSON.stringify(getJsonLd()) }}
                />
            </head>
            <body className={`${inter.className} antialiased min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900`}>
                {children}

                {/* Google Analytics 4 - Reemplazar con tu ID */}
                <Script
                    src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
                    strategy="afterInteractive"
                />
                <Script id="google-analytics" strategy="afterInteractive">
                    {`
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());
                        gtag('config', 'G-XXXXXXXXXX');
                    `}
                </Script>
            </body>
        </html>
    );
}
