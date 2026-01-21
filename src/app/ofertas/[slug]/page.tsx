import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/deals';
import { CATEGORIES } from '@/lib/types';
import { notFound } from 'next/navigation';
import Link from 'next/link';

export const dynamic = 'force-dynamic';
export const revalidate = 3600;

export async function generateMetadata({ params }: { params: { slug: string } }) {
    const category = CATEGORIES.find(c => c.slug === params.slug);
    if (!category) return { title: 'Categoría no encontrada' };

    return {
        title: `${category.icon} Ofertas en ${category.name} | Camper Deals`,
        description: `Las mejores ofertas y descuentos en ${category.name}. ${category.description}. Hasta 70% de descuento en Amazon.`,
        keywords: [...category.keywords, 'ofertas', 'descuentos', 'amazon', 'camping'],
        openGraph: {
            title: `Ofertas en ${category.name} | Camper Deals`,
            description: `${category.description}. Descuentos de hasta 70% en ${category.name}.`,
            type: 'website',
            locale: 'es_ES',
        },
        twitter: {
            card: 'summary_large_image',
            title: `Ofertas en ${category.name}`,
            description: category.description,
        }
    };
}

export default async function CategoryPage({ params }: { params: { slug: string } }) {
    const category = CATEGORIES.find(c => c.slug === params.slug);
    if (!category) notFound();

    const allProducts = await getProducts();
    const products = allProducts.filter(p => p.category === params.slug);

    // JSON-LD for category page
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": `Ofertas en ${category.name}`,
        "description": category.description,
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://camperdeals.es" },
                { "@type": "ListItem", "position": 2, "name": category.name, "item": `https://camperdeals.es/ofertas/${params.slug}` }
            ]
        }
    };

    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

            <main className="flex-grow pt-24 pb-16" role="main">
                <div className="max-w-7xl mx-auto px-4 sm:px-6">
                    {/* Breadcrumbs */}
                    <nav className="mb-6 text-sm" aria-label="Breadcrumb">
                        <ol className="flex items-center gap-2 text-slate-400">
                            <li><Link href="/" className="hover:text-white transition-colors">Inicio</Link></li>
                            <li>/</li>
                            <li className="text-white font-medium">{category.name}</li>
                        </ol>
                    </nav>

                    {/* Header */}
                    <div className="mb-12">
                        <div className="flex items-center gap-4 mb-4">
                            <span className="text-5xl sm:text-6xl">{category.icon}</span>
                            <div>
                                <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white">
                                    {category.name}
                                </h1>
                                <p className="text-slate-400 mt-1">{products.length} ofertas disponibles</p>
                            </div>
                        </div>
                        <p className="text-lg sm:text-xl text-slate-300 max-w-3xl">
                            {category.description}
                        </p>
                        <div className="w-20 h-1 bg-green-500 mt-6 rounded-full" />
                    </div>

                    {/* Other categories */}
                    <div className="mb-10 flex flex-wrap gap-2">
                        {CATEGORIES.map((cat) => (
                            <Link
                                key={cat.slug}
                                href={`/ofertas/${cat.slug}`}
                                className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-all ${
                                    cat.slug === params.slug
                                        ? 'bg-gradient-to-r from-green-600 to-green-500 text-white shadow-lg shadow-green-500/25'
                                        : 'bg-slate-800/50 text-slate-300 border border-slate-700 hover:border-green-500/50 hover:text-white'
                                }`}
                            >
                                <span>{cat.icon}</span>
                                <span className="hidden sm:inline">{cat.name}</span>
                            </Link>
                        ))}
                    </div>

                    {/* Products Grid */}
                    {products.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {products.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-slate-800/30 rounded-3xl border border-slate-700/50">
                            <span className="text-6xl mb-6 block">🔍</span>
                            <h2 className="text-2xl font-bold text-white mb-3">No hay ofertas activas</h2>
                            <p className="text-slate-400 max-w-md mx-auto mb-8">
                                Estamos buscando nuevos descuentos en {category.name.toLowerCase()}. ¡Vuelve pronto!
                            </p>
                            <Link href="/" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold hover:from-green-500 hover:to-green-400 transition-all">
                                ← Ver todas las ofertas
                            </Link>
                        </div>
                    )}
                </div>
            </main>

            <Footer />
        </div>
    );
}
