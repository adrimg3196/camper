import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/deals';
import Link from 'next/link';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Black Friday Camping 2026 | Ofertas Amazon hasta -70% | CampingDeals España",
    description: "🛒 Las MEJORES ofertas de camping en Black Friday 2026. Tiendas de campaña, sacos de dormir y mochilas con descuentos históricos. No te pierdas los chollos del año.",
    alternates: {
        canonical: `${getSiteUrl()}/black-friday-camping`,
    },
    openGraph: {
        title: "🛒 Black Friday Camping 2026 - Hasta 70% Descuento",
        description: "Los mejores descuentos del año en equipamiento de camping. ¡Prepárate para el Black Friday con las mejores ofertas en Amazon España!",
        images: [{
            url: "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&q=80&w=1200&h=630",
            width: 1200,
            height: 630,
        }],
    },
};

const BF_CATEGORIES = [
    { emoji: "⛺", name: "Tiendas de Campaña", slug: "tiendas-campana", deal: "hasta -65%" },
    { emoji: "🛏️", name: "Sacos de Dormir", slug: "sacos-dormir", deal: "hasta -55%" },
    { emoji: "🎒", name: "Mochilas Trekking", slug: "mochilas", deal: "hasta -50%" },
    { emoji: "🍳", name: "Cocina Camping", slug: "cocina-camping", deal: "hasta -45%" },
    { emoji: "💡", name: "Iluminación", slug: "iluminacion", deal: "hasta -60%" },
    { emoji: "🪑", name: "Mobiliario", slug: "mobiliario", deal: "hasta -40%" },
];

const BF_TIPS = [
    {
        icon: "📋",
        title: "Prepara tu lista antes",
        desc: "Añade a favoritos los productos que quieres. Los precios pueden cambiar en minutos."
    },
    {
        icon: "⏰",
        title: "Las mejores ofertas duran poco",
        desc: "Los primeros 30 minutos del Black Friday concentran el 60% de los mejores descuentos."
    },
    {
        icon: "📱",
        title: "Activa alertas en Telegram",
        desc: "Suscríbete a nuestro canal para recibir notificaciones al instante cuando empiece el Black Friday."
    },
    {
        icon: "🔍",
        title: "Compara el precio histórico",
        desc: "No todas las 'ofertas' son reales. Comprueba el precio habitual antes de comprar."
    },
];

export default async function BlackFridayCamping() {
    const allProducts = await getProducts();
    const products = [...allProducts]
        .sort((a, b) => (b.discount || 0) - (a.discount || 0))
        .slice(0, 12);

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": "Black Friday Camping 2026",
        "description": "Las mejores ofertas de camping en Black Friday 2026 con descuentos de hasta el 70%",
        "startDate": "2026-11-27",
        "endDate": "2026-11-30",
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
            "url": `${getSiteUrl()}/black-friday-camping`
        }
    };

    // FAQ Schema para SEO
    const faqSchema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "¿Cuándo es el Black Friday 2026?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "El Black Friday 2026 es el viernes 27 de noviembre. Sin embargo, Amazon suele empezar las ofertas una semana antes con la 'Semana del Black Friday', y el Cyber Monday cierra el evento el lunes 30 de noviembre."
                }
            },
            {
                "@type": "Question",
                "name": "¿Merece la pena esperar al Black Friday para comprar material de camping?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Sí, el Black Friday es uno de los mejores momentos para comprar equipamiento de camping. Las tiendas de campaña, sacos de dormir y mochilas suelen tener descuentos históricos de hasta el 65-70%, superando incluso al Prime Day."
                }
            },
            {
                "@type": "Question",
                "name": "¿Cómo saber si una oferta de Black Friday es real?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Compara el precio con el histórico del producto. En CampingDeals solo mostramos ofertas con descuentos verificados de más del 30% sobre el precio habitual del producto."
                }
            }
        ]
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />

            <main className="flex-grow">
                {/* HERO */}
                <section className="relative min-h-[450px] flex items-center justify-center overflow-hidden pt-16 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900">
                    <div
                        className="absolute inset-0 opacity-15"
                        style={{
                            backgroundImage: 'url("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&q=80&w=1600")',
                            backgroundSize: 'cover',
                            backgroundPosition: 'center'
                        }}
                    />
                    <div className="absolute top-20 left-10 w-72 h-72 bg-slate-500/20 rounded-full blur-3xl" />
                    <div className="absolute bottom-20 right-10 w-96 h-96 bg-green-500/10 rounded-full blur-3xl" />

                    <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
                        <span className="inline-flex items-center gap-2 py-1.5 px-4 rounded-full bg-white/10 text-white text-sm font-semibold mb-4 border border-white/20 uppercase tracking-wider">
                            <span className="w-2 h-2 bg-white rounded-full animate-pulse" />
                            Black Friday Camping 2026
                        </span>
                        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-4 leading-tight">
                            🛒 Black Friday Camping
                            <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-slate-300 to-green-400">
                                Hasta -70% Descuento
                            </span>
                        </h1>
                        <p className="text-lg sm:text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
                            Los mejores descuentos del año en equipamiento outdoor.
                            <strong className="text-white"> ¡Prepara tu lista ahora!</strong>
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <a
                                href="#ofertas-bf"
                                className="px-8 py-4 rounded-xl bg-white text-slate-900 hover:bg-slate-100 font-bold shadow-lg transition-all duration-300 hover:scale-105 text-lg"
                            >
                                Ver Ofertas Actuales →
                            </a>
                            <a
                                href="https://t.me/camperdeals"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 text-white font-medium transition-all duration-300"
                            >
                                📱 Alertas Black Friday Telegram
                            </a>
                        </div>
                    </div>
                </section>

                {/* COUNTDOWN BANNER */}
                <section className="bg-gradient-to-r from-slate-800 to-slate-700 border-y border-slate-600/50 py-5">
                    <div className="max-w-4xl mx-auto px-4 text-center">
                        <p className="text-white font-bold text-base sm:text-lg">
                            🔔 Suscríbete para recibir alertas al INSTANTE cuando empiece el Black Friday
                        </p>
                        <a
                            href="https://t.me/camperdeals"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block mt-3 px-6 py-2 bg-green-500 text-white font-bold rounded-full hover:bg-green-400 transition-colors"
                        >
                            Activar alertas gratis →
                        </a>
                    </div>
                </section>

                {/* CATEGORÍAS */}
                <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16">
                    <h2 className="text-2xl sm:text-3xl font-bold text-white mb-8 text-center">
                        Categorías con Mejores Descuentos en Black Friday
                    </h2>
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                        {BF_CATEGORIES.map((cat) => (
                            <Link
                                key={cat.slug}
                                href={`/ofertas/${cat.slug}`}
                                className="flex flex-col items-center gap-2 p-5 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-green-500/50 hover:bg-slate-800 transition-all duration-300 group text-center"
                            >
                                <span className="text-3xl group-hover:scale-110 transition-transform">{cat.emoji}</span>
                                <span className="text-sm text-slate-300 group-hover:text-white font-medium">{cat.name}</span>
                                <span className="text-xs text-green-400 font-bold">{cat.deal}</span>
                            </Link>
                        ))}
                    </div>
                </section>

                {/* TIPS BLACK FRIDAY */}
                <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
                    <h2 className="text-2xl font-bold text-white mb-8 text-center">Estrategia para el Black Friday</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {BF_TIPS.map((tip) => (
                            <div key={tip.title} className="p-5 rounded-xl bg-slate-800/40 border border-slate-700/50">
                                <span className="text-3xl mb-3 block">{tip.icon}</span>
                                <h3 className="font-bold text-white mb-2">{tip.title}</h3>
                                <p className="text-sm text-slate-400">{tip.desc}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* OFERTAS ACTUALES */}
                <section id="ofertas-bf" className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-10">
                        <div>
                            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">
                                🔥 Mejores Ofertas de Camping Ahora
                            </h2>
                            <p className="text-slate-400">Las mejores ofertas activas hoy — actualizado diariamente</p>
                        </div>
                        <span className="inline-flex items-center gap-2 text-sm text-green-400 font-semibold">
                            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
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
                            <span className="text-6xl mb-6 block">⏳</span>
                            <h3 className="text-xl font-bold text-white mb-2">Preparando las mejores ofertas...</h3>
                            <p className="text-slate-400">Suscríbete a Telegram para ser el primero en recibir las ofertas del Black Friday.</p>
                            <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="inline-block mt-6 px-6 py-3 bg-green-500 text-white font-bold rounded-xl hover:bg-green-400 transition-colors">
                                Activar alertas →
                            </a>
                        </div>
                    )}
                </section>

                {/* SEO CONTENT - FAQ */}
                <section className="max-w-4xl mx-auto px-4 sm:px-6 pb-20">
                    <div className="bg-slate-800/30 rounded-3xl border border-slate-700/50 p-8">
                        <h2 className="text-2xl font-bold text-white mb-6">
                            Preguntas Frecuentes: Black Friday Camping 2026
                        </h2>
                        <div className="space-y-6">
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-2">¿Cuándo es el Black Friday 2026?</h3>
                                <p className="text-slate-400">
                                    El Black Friday 2026 es el <strong className="text-white">viernes 27 de noviembre</strong>. Amazon suele adelantar las ofertas con la "Semana del Black Friday" desde el 23 de noviembre, y el Cyber Monday cierra el evento el 30 de noviembre.
                                </p>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-2">¿Qué productos de camping bajan más en Black Friday?</h3>
                                <ul className="space-y-2 text-slate-400 list-disc list-inside">
                                    <li><strong className="text-white">Tiendas de campaña</strong> — Descuentos históricos de hasta el 65%, las más convenientes para renovar</li>
                                    <li><strong className="text-white">Sacos de dormir</strong> — Hasta el 55% de descuento en marcas premium como Deuter, Marmot</li>
                                    <li><strong className="text-white">Linternas frontales</strong> — Petzl, Black Diamond con hasta el 60% de descuento</li>
                                    <li><strong className="text-white">Mochilas de trekking</strong> — Excelente momento para renovar tu mochila principal</li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-2">¿Cómo recibir alertas de Black Friday en camping?</h3>
                                <p className="text-slate-400">
                                    La forma más rápida es suscribirte a nuestro{' '}
                                    <a href="https://t.me/camperdeals" className="text-green-400 hover:underline">canal de Telegram</a>.
                                    Recibirás notificaciones al instante cuando encontremos una oferta de camping con descuento superior al 30%.
                                </p>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white mb-2">¿Black Friday o Prime Day: cuándo comprar material de camping?</h3>
                                <p className="text-slate-400">
                                    Históricamente, el <strong className="text-white">Black Friday ofrece mejores descuentos</strong> en equipamiento de camping que el Prime Day, especialmente en tiendas de campaña y sacos de dormir. El Prime Day es mejor para electrónica y cocina de camping. Si puedes elegir solo uno, elige Black Friday.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}
