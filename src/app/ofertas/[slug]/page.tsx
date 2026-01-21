import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/deals';
import { CATEGORIES } from '@/lib/types';
import { notFound } from 'next/navigation';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export async function generateMetadata({ params }: { params: { slug: string } }) {
    const category = CATEGORIES.find(c => c.slug === params.slug);
    if (!category) return { title: 'Categoría no encontrada' };

    return {
        title: `${category.icon} Ofertas en ${category.name} | Camper Deals`,
        description: `Las mejores ofertas y descuentos en ${category.name} seleccionadas por expertos.`
    };
}

export default async function CategoryPage({ params }: { params: { slug: string } }) {
    const category = CATEGORIES.find(c => c.slug === params.slug);
    if (!category) notFound();

    const allProducts = await getProducts();
    const products = allProducts.filter(p => p.category === params.slug);

    return (
        <div className="min-h-screen flex flex-col font-sans text-slate-900 bg-slate-50">
            <Header />

            <main className="flex-grow pt-24 pb-16">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="mb-12">
                        <div className="flex items-center gap-3 mb-4">
                            <span className="text-4xl">{category.icon}</span>
                            <h1 className="text-3xl md:text-5xl font-bold text-slate-900">
                                {category.name}
                            </h1>
                        </div>
                        <p className="text-xl text-slate-600 max-w-3xl">
                            {category.description || `Explora las mejores ofertas en ${category.name.toLowerCase()} para tu próxima aventura camping.`}
                        </p>
                        <div className="w-20 h-1 bg-forest-500 mt-6 rounded-full"></div>
                    </div>

                    {products.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                            {products.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-white rounded-3xl border border-slate-200 shadow-sm">
                            <span className="text-6xl mb-6 block">🔍</span>
                            <h2 className="text-2xl font-bold text-slate-900 mb-2">No hay ofertas activas ahora mismo</h2>
                            <p className="text-slate-500 max-w-md mx-auto">
                                Estamos buscando nuevos descuentos en esta categoría. ¡Vuelve en unas horas!
                            </p>
                        </div>
                    )}
                </div>
            </main>

            <Footer />
        </div>
    );
}
