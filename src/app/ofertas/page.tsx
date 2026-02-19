import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/deals';
import { CATEGORIES } from '@/lib/types';
import { getSiteUrl } from '@/lib/config';
import Link from 'next/link';

export const dynamic = 'force-dynamic';
export const revalidate = 3600;

export const metadata: Metadata = {
    title: "Todas las Ofertas de Camping 2026 | Descuentos +30% | CampingDeals España",
    description: "🔥 Todas las ofertas de material de camping con más del 30% de descuento en Amazon España. Tiendas de campaña, sacos de dormir, mochilas y más. Actualizado diariamente.",
    alternates: {
        canonical: `${getSiteUrl()}/ofertas`,
    },
    openGraph: {
        title: "Todas las Ofertas de Camping 2026 — Descuentos Diarios",
        description: "Las mejores ofertas de camping actualizadas diariamente. Más del 30% de descuento en Amazon España.",
    },
};

export default async function OfertasPage() {
    const allProducts = await getProducts();

    // Sort by discount descending
    const products = [...allProducts].sort((a, b) => (b.discount || 0) - (a.discount || 0));

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Todas las Ofertas de Camping 2026",
        "description": "Todas las ofertas de material de camping con más del 30% de descuento en Amazon España",
        "url": `${getSiteUrl()}/ofertas`,
        "numberOfItems": products.length,
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6">

                    {/* HEADER */}
                    <div className="mb-10">
                        <nav className="flex items-center gap-2 text-sm text-slate-400 mb-4">
                            <Link href="/" className="hover:text-white transition-colors">Inicio</Link>
                            <span>›</span>
                            <span className="text-slate-300">Todas las Ofertas</span>
                        </nav>
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-3">
                            🔥 Todas las Ofertas de Camping
                        </h1>
                        <p className="text-slate-400">
                            {products.length} ofertas activas con más del 30% de descuento · Actualizado cada hora
                        </p>
                    </div>

                    {/* CATEGORY FILTER */}
                    <div className="mb-8 overflow-x-auto pb-2">
                        <div className="flex gap-2 min-w-max">
                            <Link
                                href="/ofertas"
                                className="px-4 py-2 rounded-full text-sm font-semibold bg-green-500/20 text-green-300 border border-green-500/40"
                            >
                                🏕️ Todas
                            </Link>
                            {CATEGORIES.map((cat) => (
                                <Link
                                    key={cat.slug}
                                    href={`/ofertas/${cat.slug}`}
                                    className="px-4 py-2 rounded-full text-sm font-medium bg-slate-800/50 text-slate-300 border border-slate-700/50 hover:border-green-500/40 hover:text-white whitespace-nowrap transition-all"
                                >
                                    {cat.icon} {cat.name}
                                </Link>
                            ))}
                        </div>
                    </div>

                    {/* PRODUCTS GRID */}
                    {products.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {products.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-slate-800/30 rounded-3xl border border-slate-700/50">
                            <span className="text-6xl mb-6 block">🔍</span>
                            <h2 className="text-2xl font-bold text-white mb-3">Buscando las mejores ofertas...</h2>
                            <p className="text-slate-400 mb-6 max-w-md mx-auto">
                                El bot está escaneando Amazon en este momento. ¡Vuelve en unos minutos o activa las alertas de Telegram!
                            </p>
                            <a
                                href="https://t.me/camperdeals"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 px-6 py-3 bg-blue-500 text-white font-bold rounded-xl hover:bg-blue-400 transition-colors"
                            >
                                📱 Activar alertas en Telegram
                            </a>
                        </div>
                    )}

                    {/* SEO CONTENT */}
                    {products.length > 0 && (
                        <section className="mt-16 bg-slate-800/30 rounded-2xl border border-slate-700/50 p-8">
                            <h2 className="text-xl font-bold text-white mb-4">Sobre nuestras ofertas de camping</h2>
                            <div className="text-slate-400 space-y-3 text-sm">
                                <p>
                                    En CampingDeals España publicamos diariamente las mejores <strong className="text-white">ofertas de material de camping</strong> disponibles en Amazon España. Nuestro sistema analiza automáticamente los precios para detectar descuentos reales superiores al 30%.
                                </p>
                                <p>
                                    Todas nuestras ofertas incluyen el <strong className="text-white">precio original verificado</strong>, el descuento real aplicado y un enlace directo al producto en Amazon. Los precios pueden cambiar en cualquier momento — siempre mostramos el precio actualizado.
                                </p>
                                <p>
                                    Como participantes del <strong className="text-white">Programa de Afiliados de Amazon</strong>, podemos recibir una comisión si realizas una compra a través de nuestros enlaces, sin coste adicional para ti.
                                </p>
                            </div>
                        </section>
                    )}
                </div>
            </main>
            <Footer />
        </div>
    );
}
