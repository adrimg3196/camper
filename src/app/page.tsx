import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import StatCard from '@/components/StatCard';
import { getProducts } from '@/lib/deals';
import { CATEGORIES } from '@/lib/types';
import Link from 'next/link';

export const dynamic = 'force-dynamic';
export const revalidate = 3600; // Revalidate every hour for better performance

export default async function Home() {
    const products = await getProducts();

    // Calculate average discount
    const avgDiscount = products.length > 0
        ? Math.round(products.reduce((acc, p) => acc + (p.discount || p.discountPercentage || 0), 0) / products.length)
        : 40;

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Ofertas de Camping y Outdoor - Camper Deals",
        "description": "Las mejores ofertas de camping y outdoor con más del 30% de descuento",
        "numberOfItems": products.length,
        "itemListElement": products.slice(0, 10).map((product, index) => ({
            "@type": "ListItem",
            "position": index + 1,
            "item": {
                "@type": "Product",
                "name": product.title,
                "description": product.marketing_description || product.description || '',
                "url": product.url,
                "image": product.image_url,
                "brand": { "@type": "Brand", "name": "Amazon" },
                "offers": {
                    "@type": "Offer",
                    "price": product.price,
                    "priceCurrency": "EUR",
                    "availability": "https://schema.org/InStock",
                    "seller": { "@type": "Organization", "name": "Amazon.es" }
                },
                "aggregateRating": product.rating ? {
                    "@type": "AggregateRating",
                    "ratingValue": product.rating,
                    "reviewCount": product.review_count || product.reviewCount || 0
                } : undefined
            }
        }))
    };

    const organizationSchema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Camper Deals",
        "url": "https://camperdeals.es",
        "logo": "https://camperdeals.es/logo.png",
        "description": "Las mejores ofertas de camping y outdoor con más del 30% de descuento en Amazon"
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }} />

            <main className="flex-grow" role="main">
                {/* HERO SECTION */}
                <section className="relative min-h-[500px] sm:min-h-[550px] md:min-h-[600px] flex items-center justify-center overflow-hidden pt-16">
                    <div
                        className="absolute inset-0 z-0 bg-cover bg-center"
                        style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&q=80&w=1600")' }}
                    >
                        <div className="hero-overlay absolute inset-0" />
                    </div>

                    {/* Decorative elements */}
                    <div className="absolute top-20 left-10 w-72 h-72 bg-green-500/10 rounded-full blur-3xl" />
                    <div className="absolute bottom-20 right-10 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl" />

                    <div className="relative z-10 text-center px-4 sm:px-6 max-w-4xl mx-auto">
                        <span className="inline-flex items-center gap-2 py-1.5 px-4 rounded-full bg-green-500/20 text-green-300 text-sm font-semibold mb-6 backdrop-blur-sm border border-green-500/30 tracking-wider uppercase animate-fade-in">
                            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                            Ofertas Actualizadas
                        </span>
                        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight tracking-tight">
                            Tu próxima aventura
                            <br />
                            <span className="text-gradient-warm">empieza aquí</span>
                        </h1>
                        <p className="text-lg sm:text-xl md:text-2xl text-slate-300 mb-8 font-light max-w-2xl mx-auto leading-relaxed">
                            Equipamiento premium con descuentos de hasta el <strong className="text-white">70%</strong>.
                            <br className="hidden sm:block" />
                            <span className="text-slate-400">Seleccionado por expertos, actualizado diariamente.</span>
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                            <a href="#ofertas" className="px-8 py-4 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all duration-300 hover:scale-105 text-lg">
                                Ver ofertas →
                            </a>
                            <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 text-white font-medium transition-all duration-300">
                                📱 Alertas en Telegram
                            </a>
                        </div>
                    </div>
                </section>

                {/* STATS SECTION */}
                <div className="max-w-7xl mx-auto px-4 sm:px-6 -mt-8 sm:-mt-12 relative z-20 grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 mb-16 sm:mb-20">
                    <StatCard icon="🔥" value={`${avgDiscount}%`} label="Descuento Medio" highlight />
                    <StatCard icon="⚡️" value={products.length.toString()} label="Ofertas Activas" />
                    <StatCard icon="🏕️" value="8" label="Categorías" />
                </div>

                {/* CATEGORIES SECTION */}
                <section id="categorias" className="max-w-7xl mx-auto px-4 sm:px-6 mb-16">
                    <div className="text-center mb-10">
                        <h2 className="text-2xl sm:text-3xl font-bold text-white mb-3">Explora por categoría</h2>
                        <p className="text-slate-400">Encuentra exactamente lo que necesitas para tu aventura</p>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
                        {CATEGORIES.map((cat) => (
                            <Link
                                key={cat.slug}
                                href={`/ofertas/${cat.slug}`}
                                className="flex flex-col items-center gap-2 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-green-500/50 hover:bg-slate-800 transition-all duration-300 group"
                            >
                                <span className="text-3xl group-hover:scale-110 transition-transform">{cat.icon}</span>
                                <span className="text-xs sm:text-sm text-slate-300 group-hover:text-white text-center font-medium">{cat.name}</span>
                            </Link>
                        ))}
                    </div>
                </section>

                {/* PRODUCTS GRID */}
                <section id="ofertas" className="max-w-7xl mx-auto px-4 sm:px-6 pb-20">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-10">
                        <div>
                            <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-2">Ofertas del día</h2>
                            <p className="text-slate-400">Los mejores descuentos actualizados cada hora</p>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-slate-400">
                            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                            {products.length} ofertas activas
                        </div>
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
                            <h3 className="text-2xl font-bold text-white mb-2">Buscando ofertas...</h3>
                            <p className="text-slate-400 max-w-md mx-auto">
                                Estamos actualizando las ofertas. ¡Vuelve en unos minutos!
                            </p>
                        </div>
                    )}
                </section>

                {/* CTA SECTION */}
                <section className="max-w-4xl mx-auto px-4 sm:px-6 pb-20">
                    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 p-8 sm:p-12 text-center">
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-green-500/10 rounded-full blur-3xl" />
                        <div className="relative z-10">
                            <span className="text-5xl mb-4 block">📱</span>
                            <h3 className="text-2xl sm:text-3xl font-bold text-white mb-4">No te pierdas ninguna oferta</h3>
                            <p className="text-slate-400 mb-8 max-w-lg mx-auto">
                                Únete a nuestro canal de Telegram y recibe alertas instantáneas cuando encontremos los mejores descuentos.
                            </p>
                            <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-white font-semibold shadow-lg shadow-blue-500/25 transition-all duration-300 hover:scale-105">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" /></svg>
                                Unirse al canal
                            </a>
                        </div>
                    </div>
                </section>
            </main>
            <Footer />
        </div>
    );
}
