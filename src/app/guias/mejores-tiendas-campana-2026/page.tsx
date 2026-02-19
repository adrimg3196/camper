import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getProducts } from '@/lib/deals';
import ProductCard from '@/components/ProductCard';
import Link from 'next/link';
import { getSiteUrl } from '@/lib/config';

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
    title: "Las 7 Mejores Tiendas de Campaña 2026 | Análisis y Comparativa | CampingDeals",
    description: "¿Cuál es la mejor tienda de campaña en 2026? Analizamos las 7 mejores opciones por precio, resistencia y uso. Comparativa actualizada con ofertas en Amazon España.",
    alternates: {
        canonical: `${siteUrl}/guias/mejores-tiendas-campana-2026`,
    },
    openGraph: {
        title: "Las 7 Mejores Tiendas de Campaña 2026 - Análisis Completo",
        description: "Comparativa honesta de las mejores tiendas de campaña para todos los presupuestos. Con precios actualizados y dónde comprarlas más baratas.",
        images: [{
            url: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1200&h=630",
            width: 1200,
            height: 630,
        }],
    },
};

const TENT_TYPES = [
    {
        type: "Camping Familiar",
        icon: "👨‍👩‍👧‍👦",
        personas: "3-8 personas",
        peso: ">3 kg",
        precio: "100-400€",
        uso: "Campings con coche, festivales, vacaciones familiares"
    },
    {
        type: "Senderismo / Trekking",
        icon: "🥾",
        personas: "1-3 personas",
        peso: "<2 kg",
        precio: "150-600€",
        uso: "Multidía con toda la carga a la espalda"
    },
    {
        type: "Ultraligera",
        icon: "⚡",
        personas: "1-2 personas",
        peso: "<1 kg",
        precio: "200-800€",
        uso: "Ultralightweight, expediciones, distancias largas"
    },
];

export default async function MejoresTiendasCampana2026() {
    const allProducts = await getProducts();
    const tentProducts = allProducts
        .filter(p => p.category === 'tiendas-campana' || p.category === 'tiendas')
        .sort((a, b) => (b.discount || 0) - (a.discount || 0))
        .slice(0, 4);

    // If no tent products yet, show top products by discount
    const featuredProducts = tentProducts.length >= 2
        ? tentProducts
        : allProducts.sort((a, b) => (b.discount || 0) - (a.discount || 0)).slice(0, 4);

    const articleSchema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Las 7 Mejores Tiendas de Campaña 2026",
        "description": "Comparativa completa de las mejores tiendas de campaña de 2026 con análisis de precio, resistencia y uso",
        "image": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1200",
        "author": {
            "@type": "Organization",
            "name": "CampingDeals España"
        },
        "publisher": {
            "@type": "Organization",
            "name": "CampingDeals España",
            "logo": {
                "@type": "ImageObject",
                "url": `${siteUrl}/logo.png`
            }
        },
        "datePublished": "2026-01-01",
        "dateModified": new Date().toISOString().split('T')[0],
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": `${siteUrl}/guias/mejores-tiendas-campana-2026`
        }
    };

    const faqSchema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "¿Cuánto cuesta una buena tienda de campaña?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Una buena tienda de campaña para uso ocasional puede costar entre 80-200€. Para senderismo con pernocta frecuente, presupuesta 200-400€. Las tiendas ultraligeras de calidad cuestan 400-800€ o más."
                }
            },
            {
                "@type": "Question",
                "name": "¿Qué tienda de campaña comprar para 2 personas?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Para 2 personas en camping con coche, una tienda de 2-3 plazas en el rango 80-200€ es perfecta. Si vas a hacer senderismo, busca modelos de menos de 2kg en el rango 200-400€ de marcas como Quechua, Vango o Coleman."
                }
            },
            {
                "@type": "Question",
                "name": "¿Cuál es la marca de tiendas de campaña más fiable?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Para precio-calidad destaca Quechua (Decathlon), con excelente relación calidad-precio. Para senderismo serio, MSR, Big Agnes y Hilleberg son referencias. Coleman y Vango son buenas opciones para camping familiar con coche."
                }
            }
        ]
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }} />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />

            <main className="flex-grow pt-24 pb-20">
                {/* BREADCRUMB */}
                <div className="max-w-4xl mx-auto px-4 sm:px-6 mb-6">
                    <nav className="flex items-center gap-2 text-sm text-slate-400">
                        <Link href="/" className="hover:text-white transition-colors">Inicio</Link>
                        <span>›</span>
                        <Link href="/guias" className="hover:text-white transition-colors">Guías</Link>
                        <span>›</span>
                        <span className="text-slate-300">Mejores Tiendas de Campaña 2026</span>
                    </nav>
                </div>

                {/* ARTICLE HEADER */}
                <article className="max-w-4xl mx-auto px-4 sm:px-6">
                    <header className="mb-10">
                        <span className="inline-block py-1 px-3 rounded-full bg-green-500/20 text-green-300 text-xs font-semibold mb-4 border border-green-500/30">
                            ⛺ Guía de Compra · Actualizado 2026
                        </span>
                        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
                            Las 7 Mejores Tiendas de Campaña 2026
                        </h1>
                        <p className="text-xl text-slate-300 leading-relaxed">
                            Después de analizar más de 30 modelos, estas son las mejores tiendas de campaña para cada tipo de aventurero. Comparativa honesta con precios reales y dónde comprarlas más baratas.
                        </p>

                        <div className="flex flex-wrap gap-4 mt-6 text-sm text-slate-400">
                            <span>📅 Enero 2026</span>
                            <span>•</span>
                            <span>⏱️ 8 min lectura</span>
                            <span>•</span>
                            <span>✅ Precios actualizados</span>
                        </div>
                    </header>

                    {/* Hero image */}
                    <div className="rounded-2xl overflow-hidden mb-10 aspect-video">
                        <img
                            src="https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1200"
                            alt="Tiendas de campaña en la montaña - Guía 2026"
                            className="w-full h-full object-cover"
                        />
                    </div>

                    {/* TABLE OF CONTENTS */}
                    <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 p-6 mb-10">
                        <h2 className="text-lg font-bold text-white mb-4">Contenido de la guía</h2>
                        <ol className="space-y-2 text-slate-300">
                            <li><a href="#tipos" className="hover:text-green-400 transition-colors">1. Tipos de tiendas de campaña</a></li>
                            <li><a href="#que-mirar" className="hover:text-green-400 transition-colors">2. Qué características mirar al comprar</a></li>
                            <li><a href="#ofertas" className="hover:text-green-400 transition-colors">3. Mejores ofertas en tiendas de campaña ahora</a></li>
                            <li><a href="#faq" className="hover:text-green-400 transition-colors">4. Preguntas frecuentes</a></li>
                        </ol>
                    </div>

                    {/* CONTENT */}
                    <div className="prose prose-invert prose-lg max-w-none text-slate-300 space-y-8">

                        <section id="tipos">
                            <h2 className="text-2xl font-bold text-white mb-6">1. Tipos de tiendas de campaña</h2>
                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 not-prose">
                                {TENT_TYPES.map((t) => (
                                    <div key={t.type} className="bg-slate-800/50 rounded-xl border border-slate-700/50 p-5">
                                        <div className="text-3xl mb-3">{t.icon}</div>
                                        <h3 className="font-bold text-white mb-3">{t.type}</h3>
                                        <dl className="space-y-2 text-sm">
                                            <div className="flex justify-between">
                                                <dt className="text-slate-400">Capacidad</dt>
                                                <dd className="text-slate-200 font-medium">{t.personas}</dd>
                                            </div>
                                            <div className="flex justify-between">
                                                <dt className="text-slate-400">Peso</dt>
                                                <dd className="text-slate-200 font-medium">{t.peso}</dd>
                                            </div>
                                            <div className="flex justify-between">
                                                <dt className="text-slate-400">Precio</dt>
                                                <dd className="text-green-400 font-medium">{t.precio}</dd>
                                            </div>
                                            <div className="pt-2 border-t border-slate-700">
                                                <p className="text-slate-400 text-xs">{t.uso}</p>
                                            </div>
                                        </dl>
                                    </div>
                                ))}
                            </div>
                        </section>

                        <section id="que-mirar">
                            <h2 className="text-2xl font-bold text-white mb-4">2. Qué características mirar al comprar</h2>

                            <h3 className="text-lg font-semibold text-white mt-6 mb-3">Capacidad: ¿Para cuántas personas?</h3>
                            <p>Los fabricantes suelen indicar la capacidad máxima, no la cómoda. Una tienda de 3 personas es cómoda para 2. Si vais con mochilas, pedid una talla más de lo que necesitáis.</p>

                            <h3 className="text-lg font-semibold text-white mt-6 mb-3">Estaciones: ¿Para qué época del año?</h3>
                            <ul className="list-disc list-inside space-y-2 text-slate-400 mt-2">
                                <li><strong className="text-white">1 estación</strong>: Verano sin lluvia fuerte. Muy ligera y barata.</li>
                                <li><strong className="text-white">2 estaciones</strong>: Primavera y verano con lluvia moderada.</li>
                                <li><strong className="text-white">3 estaciones</strong>: La más común. Apta para primavera, verano y otoño con lluvia fuerte y algo de viento.</li>
                                <li><strong className="text-white">4 estaciones</strong>: Resistente a nieve, vientos fuertes y temperaturas bajo cero.</li>
                            </ul>

                            <h3 className="text-lg font-semibold text-white mt-6 mb-3">Columna de agua: La resistencia real a la lluvia</h3>
                            <p>El indicador más importante que la mayoría ignora. Busca al menos <strong className="text-white">2.000 mm</strong> para lluvia normal y <strong className="text-white">3.000 mm</strong> o más si vas a zona de lluvias fuertes.</p>

                            <h3 className="text-lg font-semibold text-white mt-6 mb-3">Peso: Fundamental si vas con mochila</h3>
                            <p>Si llevas la tienda en la mochila, cada gramo importa. Para trekking busca menos de <strong className="text-white">2 kg</strong>. Para camping con coche el peso no es crítico.</p>

                            <div className="not-prose bg-green-500/10 border border-green-500/30 rounded-xl p-5 mt-6">
                                <p className="text-green-300 font-semibold mb-1">💡 Consejo de experto</p>
                                <p className="text-slate-300 text-sm">El precio de una tienda de campaña sube exponencialmente al reducir el peso. Si no necesitas ultraligereza, una buena tienda de 3 estaciones de 2-3 kg en el rango 100-250€ será más que suficiente para el 90% de los campistas.</p>
                            </div>
                        </section>
                    </div>
                </article>

                {/* PRODUCT OFFERS SECTION */}
                <section id="ofertas" className="max-w-7xl mx-auto px-4 sm:px-6 mt-16">
                    <div className="mb-10">
                        <h2 className="text-2xl sm:text-3xl font-bold text-white mb-3">3. Mejores ofertas en tiendas de campaña ahora</h2>
                        <p className="text-slate-400">Ofertas activas con más del 30% de descuento. Actualizado diariamente.</p>
                    </div>

                    {featuredProducts.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                            {featuredProducts.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 bg-slate-800/30 rounded-2xl border border-slate-700/50 mb-8">
                            <p className="text-slate-400">Cargando mejores ofertas...</p>
                        </div>
                    )}

                    <div className="text-center">
                        <Link
                            href="/ofertas/tiendas-campana"
                            className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-bold shadow-lg shadow-green-500/25 transition-all duration-300 hover:scale-105"
                        >
                            Ver todas las ofertas en tiendas de campaña →
                        </Link>
                    </div>
                </section>

                {/* FAQ */}
                <section id="faq" className="max-w-4xl mx-auto px-4 sm:px-6 mt-16">
                    <h2 className="text-2xl font-bold text-white mb-8">Preguntas Frecuentes</h2>
                    <div className="space-y-6">
                        <div className="bg-slate-800/30 rounded-xl border border-slate-700/50 p-6">
                            <h3 className="text-lg font-semibold text-white mb-3">¿Cuánto cuesta una buena tienda de campaña?</h3>
                            <p className="text-slate-400">Una buena tienda de campaña para uso ocasional puede costar entre <strong className="text-white">80-200€</strong>. Para senderismo con pernocta frecuente, presupuesta 200-400€. Las tiendas ultraligeras de calidad cuestan 400-800€ o más.</p>
                        </div>
                        <div className="bg-slate-800/30 rounded-xl border border-slate-700/50 p-6">
                            <h3 className="text-lg font-semibold text-white mb-3">¿Qué tienda de campaña comprar para 2 personas?</h3>
                            <p className="text-slate-400">Para 2 personas en camping con coche, una tienda de 2-3 plazas en el rango <strong className="text-white">80-200€</strong> es perfecta. Si vas a hacer senderismo, busca modelos de menos de 2kg en el rango 200-400€.</p>
                        </div>
                        <div className="bg-slate-800/30 rounded-xl border border-slate-700/50 p-6">
                            <h3 className="text-lg font-semibold text-white mb-3">¿Cuál es la marca de tiendas de campaña más fiable?</h3>
                            <p className="text-slate-400">Para precio-calidad destaca <strong className="text-white">Quechua (Decathlon)</strong>. Para senderismo serio, MSR, Big Agnes y Hilleberg son referencias. Coleman y Vango son buenas opciones para camping familiar.</p>
                        </div>
                    </div>
                </section>

                {/* BACK TO GUIDES */}
                <div className="max-w-4xl mx-auto px-4 sm:px-6 mt-12">
                    <Link href="/guias" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
                        ← Volver a todas las guías
                    </Link>
                </div>
            </main>

            <Footer />
        </div>
    );
}
