'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ProductCard from '@/components/ProductCard';
import CategoryFilter from '@/components/CategoryFilter';
import StatCard from '@/components/StatCard';
import { AmazonProduct, ProductCategory } from '@/lib/types';

// Datos de ejemplo para demostración (serán reemplazados por datos reales de la API)
const DEMO_PRODUCTS: AmazonProduct[] = [
    {
        asin: 'B08XXXX1',
        title: 'Tienda de Campaña 4 Estaciones - Impermeable para 4 Personas',
        imageUrl: 'https://m.media-amazon.com/images/I/81qpDmPPghL._AC_SX679_.jpg',
        category: 'tiendas-campana',
        originalPrice: 249.99,
        discountedPrice: 149.99,
        discountPercentage: 40,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX1?tag=camperdeals-21',
        rating: 4.5,
        reviewCount: 1234,
        isPrime: true,
        lastUpdated: new Date(),
    },
    {
        asin: 'B08XXXX2',
        title: 'Saco de Dormir Ultraligero -15°C Momia Camping Invierno',
        imageUrl: 'https://m.media-amazon.com/images/I/71o8Qb5V6OL._AC_SX679_.jpg',
        category: 'sacos-dormir',
        originalPrice: 129.99,
        discountedPrice: 79.99,
        discountPercentage: 38,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX2?tag=camperdeals-21',
        rating: 4.7,
        reviewCount: 856,
        isPrime: true,
        lastUpdated: new Date(),
    },
    {
        asin: 'B08XXXX3',
        title: 'Mochila Trekking 65L Impermeable con Funda Lluvia',
        imageUrl: 'https://m.media-amazon.com/images/I/81Zv9R9rMZL._AC_SX679_.jpg',
        category: 'mochilas',
        originalPrice: 89.99,
        discountedPrice: 54.99,
        discountPercentage: 39,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX3?tag=camperdeals-21',
        rating: 4.3,
        reviewCount: 2341,
        isPrime: true,
        lastUpdated: new Date(),
    },
    {
        asin: 'B08XXXX4',
        title: 'Hornillo de Gas Camping Plegable con 4 Cartuchos',
        imageUrl: 'https://m.media-amazon.com/images/I/61kqVjuJO6L._AC_SX679_.jpg',
        category: 'cocina-camping',
        originalPrice: 45.99,
        discountedPrice: 29.99,
        discountPercentage: 35,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX4?tag=camperdeals-21',
        rating: 4.6,
        reviewCount: 567,
        isPrime: false,
        lastUpdated: new Date(),
    },
    {
        asin: 'B08XXXX5',
        title: 'Linterna Frontal LED Recargable 1000 Lúmenes IPX6',
        imageUrl: 'https://m.media-amazon.com/images/I/71EqeN0HXIL._AC_SX679_.jpg',
        category: 'iluminacion',
        originalPrice: 34.99,
        discountedPrice: 19.99,
        discountPercentage: 43,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX5?tag=camperdeals-21',
        rating: 4.8,
        reviewCount: 3456,
        isPrime: true,
        lastUpdated: new Date(),
    },
    {
        asin: 'B08XXXX6',
        title: 'Silla Camping Plegable con Portavasos y Bolsa',
        imageUrl: 'https://m.media-amazon.com/images/I/71xqQrGmQcL._AC_SX679_.jpg',
        category: 'mobiliario',
        originalPrice: 59.99,
        discountedPrice: 35.99,
        discountPercentage: 40,
        affiliateUrl: 'https://www.amazon.es/dp/B08XXXX6?tag=camperdeals-21',
        rating: 4.4,
        reviewCount: 1890,
        isPrime: true,
        lastUpdated: new Date(),
    },
];

export default function Home() {
    const [selectedCategory, setSelectedCategory] = useState<ProductCategory | null>(null);

    const filteredProducts = selectedCategory
        ? DEMO_PRODUCTS.filter(p => p.category === selectedCategory)
        : DEMO_PRODUCTS;

    const stats = {
        totalDeals: DEMO_PRODUCTS.length,
        avgDiscount: Math.round(DEMO_PRODUCTS.reduce((acc, p) => acc + p.discountPercentage, 0) / DEMO_PRODUCTS.length),
        maxDiscount: Math.max(...DEMO_PRODUCTS.map(p => p.discountPercentage)),
    };

    return (
        <div className="min-h-screen flex flex-col">
            <Header />

            <main className="flex-1">
                {/* Hero Section */}
                <section className="relative overflow-hidden hero-pattern">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
                        <div className="text-center max-w-3xl mx-auto">
                            {/* Badge */}
                            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-forest-500/20 border border-forest-500/30 text-forest-400 text-sm font-medium mb-6">
                                <span className="relative flex h-2 w-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-forest-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-forest-500"></span>
                                </span>
                                Ofertas actualizadas cada 6 horas
                            </div>

                            {/* Title */}
                            <h1 className="text-4xl md:text-6xl font-bold font-display mb-6">
                                <span className="text-white">Ofertas</span>{' '}
                                <span className="text-gradient">Camping</span>
                                <br />
                                <span className="text-white">con más del</span>{' '}
                                <span className="text-sunset-400">30% OFF</span>
                            </h1>

                            {/* Description */}
                            <p className="text-lg md:text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
                                Descubre las mejores ofertas en tiendas de campaña, sacos de dormir,
                                mochilas y todo lo que necesitas para tu próxima aventura.
                            </p>

                            {/* CTA Buttons */}
                            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                <a
                                    href="#ofertas"
                                    className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-forest-600 to-forest-500 hover:from-forest-500 hover:to-forest-400 text-white font-semibold shadow-lg shadow-forest-500/30 hover:shadow-forest-500/50 transition-all duration-300 hover:scale-105"
                                >
                                    Ver ofertas
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                                    </svg>
                                </a>
                                <a
                                    href="https://t.me/camperdeals"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-400 font-semibold transition-all duration-300 hover:scale-105"
                                >
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                                    </svg>
                                    Únete a Telegram
                                </a>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Stats Section */}
                <section className="py-12 border-y border-slate-700/50 bg-slate-900/50">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <StatCard icon="🏷️" value={stats.totalDeals} label="Ofertas activas" highlight />
                            <StatCard icon="💰" value={`${stats.avgDiscount}%`} label="Descuento medio" />
                            <StatCard icon="🔥" value={`${stats.maxDiscount}%`} label="Mayor descuento" />
                            <StatCard icon="⏱️" value="6h" label="Actualización" />
                        </div>
                    </div>
                </section>

                {/* Products Section */}
                <section id="ofertas" className="py-16">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        {/* Section Header */}
                        <div className="text-center mb-12">
                            <h2 className="text-3xl md:text-4xl font-bold font-display text-white mb-4">
                                🔥 Mejores Ofertas de Hoy
                            </h2>
                            <p className="text-slate-400 max-w-2xl mx-auto">
                                Productos seleccionados con al menos un 30% de descuento.
                                Actualizado automáticamente cada 6 horas.
                            </p>
                        </div>

                        {/* Category Filter */}
                        <div id="categorias" className="mb-8">
                            <CategoryFilter
                                selectedCategory={selectedCategory}
                                onCategoryChange={setSelectedCategory}
                            />
                        </div>

                        {/* Products Grid */}
                        {filteredProducts.length > 0 ? (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                {filteredProducts.map(product => (
                                    <ProductCard key={product.asin} product={product} />
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-16">
                                <span className="text-6xl mb-4 block">🏕️</span>
                                <h3 className="text-xl font-semibold text-white mb-2">
                                    No hay ofertas en esta categoría
                                </h3>
                                <p className="text-slate-400">
                                    Vuelve a mirar más tarde o selecciona otra categoría
                                </p>
                            </div>
                        )}
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-16 bg-gradient-to-br from-forest-900/50 to-forest-800/30 border-y border-forest-500/20">
                    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                        <h2 className="text-3xl md:text-4xl font-bold font-display text-white mb-4">
                            📱 Recibe ofertas al instante
                        </h2>
                        <p className="text-lg text-slate-300 mb-8">
                            Únete a nuestro canal de Telegram y sé el primero en enterarte
                            de las mejores ofertas de camping y outdoor.
                        </p>
                        <a
                            href="https://t.me/camperdeals"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-white font-semibold text-lg shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all duration-300 hover:scale-105"
                        >
                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                            </svg>
                            Unirme al Canal de Telegram
                        </a>
                        <p className="text-sm text-slate-500 mt-4">
                            Gratis · Sin spam · Solo las mejores ofertas
                        </p>
                    </div>
                </section>
            </main>

            <Footer />
        </div>
    );
}
