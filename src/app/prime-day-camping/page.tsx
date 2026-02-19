import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/deals';
import Link from 'next/link';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Prime Day Camping 2026 | Ofertas Amazon hasta -70% | CampingDeals España",
    description: "🔥 Las MEJORES ofertas de camping en Amazon Prime Day 2026. Tiendas de campaña, sacos de dormir y mochilas con descuentos de hasta el 70%. Ahorra antes de tu próxima aventura.",
    alternates: {
        canonical: `${getSiteUrl()}/prime-day-camping`,
    },
    openGraph: {
        title: "🔥 Prime Day Camping 2026 - Hasta 70% Descuento",
        description: "Las mejores ofertas de camping del año. ¡No te pierdas el Amazon Prime Day con descuentos increíbles en equipamiento outdoor!",
        images: [{
            url: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1200&h=630",
            width: 1200,
            height: 630,
        }],
    },
};

const PRIME_DAY_CATEGORIES = [
    { emoji: "⛺", name: "Tiendas de Campaña", slug: "tiendas-campana", deal: "hasta -60%" },
    { emoji: "🛏️", name: "Sacos de Dormir", slug: "sacos-dormir", deal: "hasta -50%" },
    { emoji: "🎒", name: "Mochilas Trekking", slug: "mochilas", deal: "hasta -45%" },
    { emoji: "🍳", name: "Cocina Camping", slug: "cocina-camping", deal: "hasta -40%" },
    { emoji: "💡", name: "Iluminación", slug: "iluminacion", deal: "hasta -55%" },
    { emoji: "🪑", name: "Mobiliario", slug: "mobiliario", deal: "hasta -35%" },
];

export default async function PrimeDayCamping() {
    const allProducts = await getProducts();
    // Priorizar productos con mayor descuento para esta página
    const products = [...allProducts]
        .sort((a, b) => (b.discount || 0) - (a.discount || 0))
        .slice(0, 12);

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": "Amazon Prime Day Camping 2026",
        "description": "Las mejores ofertas de camping en Amazon Prime Day 2026 con descuentos de hasta el 70%",
        "startDate": "2026-07-01",
        "endDate": "2026-07-02",
        "location": {
            "@type": "VirtualLocation",
            "url": "https://www.amazon.es"
        },
        "organizer": {
            "@type": "Organization",
            "name": "Amazon España",
            "url": "https://www.amazon.es"
        },
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "priceCurrency": "EUR",
            "url": `${getSiteUrl()}/prime-day-camping`
        }
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

            <main className="flex-grow">
                {/* HERO */}
                <section className="relative min-h-[450px] flex items-center justify-center overflow-hidden pt-16 bg-gradient-to-br from-orange-950 via-slate-900 to-slate-900">
                    <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1600")', backgroundSize: 'cover', backgroundPosition: 'center' }} />
                    <div className="absolute top-20 left-10 w-72 h-72 bg-orange-500/20 rounded-full blur-3xl" />
                    <div className="absolute bottom-20 right-10 w-96 h-96 bg-yellow-500/10 rounded-full blur-3xl" />

                    <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
                        <span className="inline-flex items-center gap-2 py-1.5 px-4 rounded-full bg-orange-500/20 text-orange-300 text-sm font-semibold mb-4 border border-orange-500/30 uppercase tracking-wider">
                            <span className="w-2 h-2 bg-orange-400 rounded-full animate-pulse" />
                            Prime Day Camping 2026
                        </span>
                        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-4 leading-tight">
                            🔥 Prime Day Camping
                            <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-yellow-400">
                                Hasta -70% Descuento
                            </span>
                        </h1>
                        <p className="text-lg sm:text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
                            Las mejores ofertas del año en equipamiento de camping.
                            <strong className="text-white"> ¡Prepárate para el verano!</strong>
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <a href="#ofertas-prime" className="px-8 py-4 rounded-xl bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-400 hover:to-yellow-400 text-white font-bold shadow-lg shadow-orange-500/30 transition-all duration-300 hover:scale-105 text-lg">
                                Ver Ofertas Prime Day →
                            </a>
                            <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 text-white font-medium transition-all duration-300">
                                📱 Alertas Prime Day Telegram
                            </a>
                        </div>
                    </div>
                </section>

                {/* COUNTDOWN / AVISO */}
                <section className="bg-gradient-to-r from-orange-600 to-yellow-600 py-6">
                    <div className="max-w-4xl mx-auto px-4 text-center">
                        <p className="text-white font-bold text-lg">
                            🔔 Suscríbete a nuestro canal de Telegram para recibir alertas al INSTANTE cuando empiecen las ofertas
                        </p>
                        <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="inline-block mt-3 px-6 py-2 bg-white text-orange-600 font-bold rounded-full hover:bg-orange-50 transition-colors">
                            Unirse gratis →
                        </a>
                    </div>
                </section>

                {/* CATEGORÍAS */}
                <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16">
                    <h2 className="text-2xl sm:text-3xl font-bold text-white mb-8 text-center">
                        Categorías con Mejores Descuentos
                    </h2>
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                        {PRIME_DAY_CATEGORIES.map((cat) => (
                            <Link
                                key={cat.slug}
                                href={`/ofertas/${cat.slug}`}
                                className="flex flex-col items-center gap-2 p-5 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-orange-500/50 hover:bg-slate-800 transition-all duration-300 group text-center"
                            >
                                <span className="text-3xl group-hover:scale-110 transition-transform">{cat.emoji}</span>
                                <span className="text-sm text-slate-300 group-hover:text-white font-medium">{cat.name}</span>
                                <span className="text-xs text-orange-400 font-bold">{cat.deal}</span>
                            </Link>
                        ))}
                    </div>
                </section>

                {/* OFERTAS ACTUALES */}
                <section id="ofertas-prime" className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-10">
                        <div>
                            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">
                                🔥 Mejores Ofertas Camping Ahora
                            </h2>
                            <p className="text-slate-400">Preparando el Prime Day — estas son las ofertas activas hoy</p>
                        </div>
                        <span className="inline-flex items-center gap-2 text-sm text-orange-400 font-semibold">
                            <span className="w-2 h-2 bg-orange-400 rounded-full animate-pulse" />
                            {products.length} chollos activos
                        </span>
                    </div>

                    {products.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {products.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-slate-800/30 rounded-3xl border border-slate-700/50">
                            <span className="text-6xl mb-6 block">🔍</span>
                            <h3 className="text-xl font-bold text-white mb-2">Buscando las mejores ofertas...</h3>
                            <p className="text-slate-400">Vuelve pronto o suscríbete a Telegram para ser el primero en saberlo.</p>
                        </div>
                    )}
                </section>

                {/* SEO CONTENT */}
                <section className="max-w-4xl mx-auto px-4 sm:px-6 pb-20">
                    <div className="bg-slate-800/30 rounded-3xl border border-slate-700/50 p-8">
                        <h2 className="text-2xl font-bold text-white mb-6">
                            Guía Prime Day Camping 2026: Todo lo que necesitas saber
                        </h2>
                        <div className="prose prose-invert max-w-none text-slate-300 space-y-4">
                            <p>
                                El <strong className="text-white">Amazon Prime Day</strong> es el evento de ofertas más grande del año para los amantes del camping y el outdoor. En 2026, esperamos descuentos de hasta el <strong className="text-orange-400">70%</strong> en equipamiento de aventura.
                            </p>
                            <h3 className="text-lg font-semibold text-white">¿Qué productos bajan más en Prime Day?</h3>
                            <ul className="space-y-2 text-slate-400 list-disc list-inside">
                                <li><strong className="text-white">Tiendas de campaña</strong> — Descuentos históricos de hasta el 60%</li>
                                <li><strong className="text-white">Sacos de dormir</strong> — Hasta el 50% de descuento en marcas premium</li>
                                <li><strong className="text-white">Mochilas de trekking</strong> — Excelente momento para renovar tu mochila</li>
                                <li><strong className="text-white">Linternas frontales</strong> — Ofertas flash con hasta el 55% de descuento</li>
                            </ul>
                            <h3 className="text-lg font-semibold text-white">Consejos para el Prime Day</h3>
                            <ul className="space-y-2 text-slate-400 list-disc list-inside">
                                <li>Añade a tu lista de deseos los productos que quieres antes del evento</li>
                                <li>Suscríbete a nuestro <a href="https://t.me/camperdeals" className="text-blue-400 hover:underline">canal de Telegram</a> para alertas instantáneas</li>
                                <li>Las mejores ofertas suelen aparecer en las primeras 2 horas del evento</li>
                                <li>Compara precios antes de comprar — no todas las "ofertas" son reales</li>
                            </ul>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}
