import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Link from 'next/link';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Guías de Camping 2026 | Análisis y Consejos de Expertos | CampingDeals",
    description: "Guías completas para comprar material de camping. Tiendas de campaña, sacos de dormir, mochilas y más. Análisis honestos con precios y comparativas actualizadas para 2026.",
    alternates: {
        canonical: `${getSiteUrl()}/guias`,
    },
};

const GUIDES = [
    {
        slug: "mejores-tiendas-campana-2026",
        title: "Las 7 Mejores Tiendas de Campaña 2026",
        description: "Comparativa completa de tiendas de campaña para todas las situaciones: senderismo, camping familiar y expediciones. Con precios actualizados y dónde comprar más barato.",
        image: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=800",
        category: "Tiendas de Campaña",
        readTime: "8 min",
        intent: "🛒 Guía de compra"
    },
    {
        slug: "mejores-sacos-dormir-2026",
        title: "Mejores Sacos de Dormir 2026: Guía Completa",
        description: "¿Plumas o fibra? ¿Qué temperatura necesitas? Todo lo que debes saber para elegir el saco de dormir perfecto. Comparativa de los mejores modelos con ofertas actuales.",
        image: "https://images.unsplash.com/photo-1517175782509-deef2807f66e?auto=format&fit=crop&q=80&w=800",
        category: "Sacos de Dormir",
        readTime: "7 min",
        intent: "🛒 Guía de compra"
    },
    {
        slug: "mejores-mochilas-trekking",
        title: "Mejores Mochilas de Trekking: Cuál Elegir",
        description: "De 30 a 80 litros, con o sin marco, para todos los presupuestos. Analizamos las mejores mochilas de montaña y dónde encontrarlas más baratas en Amazon.",
        image: "https://images.unsplash.com/photo-1527437285024-f38aafff3f68?auto=format&fit=crop&q=80&w=800",
        category: "Mochilas",
        readTime: "6 min",
        intent: "🛒 Guía de compra"
    },
    {
        slug: "guia-camping-principiantes",
        title: "Guía de Camping para Principiantes 2026",
        description: "Todo lo que necesitas para tu primera noche de camping. Lista completa de material, consejos prácticos y los productos mejor valorados para empezar bien.",
        image: "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&q=80&w=800",
        category: "Principiantes",
        readTime: "10 min",
        intent: "📚 Guía educativa"
    },
    {
        slug: "equipamiento-camping-esencial",
        title: "Equipamiento de Camping Esencial: La Lista Definitiva",
        description: "Qué llevar al camping sin olvidar nada. La checklist más completa con los 30 artículos imprescindibles, organizados por presupuesto y tipo de aventura.",
        image: "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&q=80&w=800",
        category: "Equipamiento",
        readTime: "9 min",
        intent: "📚 Guía educativa"
    },
    {
        slug: "como-elegir-tienda-campana",
        title: "Cómo Elegir una Tienda de Campaña: Todo lo que Necesitas Saber",
        description: "Capacidad, temporadas, peso, materiales... Explicamos cada característica para que tomes la mejor decisión de compra. Con ejemplos y precios reales.",
        image: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=800",
        category: "Tiendas de Campaña",
        readTime: "8 min",
        intent: "📚 Guía educativa"
    },
    {
        slug: "camping-con-ninos",
        title: "Camping con Niños: Qué Llevar y Cómo Prepararse",
        description: "Consejos prácticos y lista de material imprescindible para ir de camping con niños. Seguridad, entretenimiento y los productos más recomendados en Amazon.",
        image: "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&q=80&w=800",
        category: "Familia",
        readTime: "7 min",
        intent: "🛒 Guía de compra"
    },
    {
        slug: "camping-invierno-guia",
        title: "Camping en Invierno: Equipo Específico y Consejos",
        description: "El camping de invierno requiere material específico. Sacos de frío extremo, capas térmicas y tiendas para nieve. Todo lo que necesitas para no pasar frío.",
        image: "https://images.unsplash.com/photo-1486496572940-2bb2341fdbdf?auto=format&fit=crop&q=80&w=800",
        category: "Invierno",
        readTime: "8 min",
        intent: "🛒 Guía de compra"
    },
];

export default function GuiasPage() {
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Guías de Camping 2026",
        "description": "Guías completas de compra para material de camping con análisis honestos y precios actualizados",
        "url": `${getSiteUrl()}/guias`,
        "hasPart": GUIDES.map((guide) => ({
            "@type": "Article",
            "name": guide.title,
            "url": `${getSiteUrl()}/guias/${guide.slug}`,
            "description": guide.description,
        }))
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6">
                    {/* Header */}
                    <div className="text-center mb-16">
                        <span className="inline-block py-1 px-3 rounded-full bg-green-500/20 text-green-300 text-xs font-semibold mb-4 border border-green-500/30 uppercase tracking-wider">
                            Guías de Expertos
                        </span>
                        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">
                            Guías de Camping 2026
                        </h1>
                        <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                            Análisis honestos y guías de compra para que elijas el mejor equipamiento de camping al mejor precio.
                        </p>
                    </div>

                    {/* Guides Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-16">
                        {GUIDES.map((guide) => (
                            <Link
                                key={guide.slug}
                                href={`/guias/${guide.slug}`}
                                className="group flex flex-col bg-slate-800/50 rounded-2xl overflow-hidden border border-slate-700/50 hover:border-green-500/50 transition-all duration-300 hover:-translate-y-1"
                            >
                                <div className="relative h-44 overflow-hidden">
                                    <img
                                        src={guide.image}
                                        alt={guide.title}
                                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                        loading="lazy"
                                    />
                                    <div className="absolute top-3 left-3">
                                        <span className="text-xs font-semibold px-2 py-1 rounded-full bg-slate-900/80 backdrop-blur-sm text-green-400 border border-green-500/30">
                                            {guide.category}
                                        </span>
                                    </div>
                                </div>

                                <div className="flex-grow p-5 flex flex-col">
                                    <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
                                        <span>{guide.intent}</span>
                                        <span>•</span>
                                        <span>{guide.readTime} lectura</span>
                                    </div>
                                    <h2 className="text-base font-bold text-white mb-2 leading-snug group-hover:text-green-400 transition-colors line-clamp-2">
                                        {guide.title}
                                    </h2>
                                    <p className="text-sm text-slate-400 flex-grow line-clamp-3">
                                        {guide.description}
                                    </p>
                                    <div className="mt-4 text-sm font-semibold text-green-400 group-hover:text-green-300 transition-colors">
                                        Leer guía →
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>

                    {/* CTA Banner */}
                    <div className="bg-gradient-to-r from-slate-800 to-slate-700 rounded-2xl border border-slate-600/50 p-8 text-center">
                        <h2 className="text-xl font-bold text-white mb-3">¿Buscas las mejores ofertas ahora mismo?</h2>
                        <p className="text-slate-400 mb-6">Consulta las ofertas activas del día en camping y outdoor con más del 30% de descuento.</p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link
                                href="/"
                                className="px-6 py-3 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold transition-all duration-300 hover:scale-105"
                            >
                                Ver ofertas del día →
                            </Link>
                            <a
                                href="https://t.me/camperdeals"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-6 py-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-white font-medium border border-slate-600 transition-all duration-300"
                            >
                                📱 Alertas en Telegram
                            </a>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
