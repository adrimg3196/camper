import { AmazonProduct } from '@/lib/types';
import Image from 'next/image';

interface ProductCardProps {
    product: AmazonProduct;
}

export default function ProductCard({ product }: ProductCardProps) {
    return (
        <article className="product-card group relative bg-gradient-to-br from-slate-800/80 to-slate-900/80 rounded-2xl overflow-hidden border border-slate-700/50 hover:border-forest-500/50 transition-all duration-300">
            {/* Badge de descuento */}
            <div className="absolute top-4 left-4 z-10">
                <span className="discount-badge inline-flex items-center px-3 py-1.5 rounded-full text-sm font-bold bg-gradient-to-r from-red-500 to-orange-500 text-white shadow-lg">
                    -{product.discountPercentage}%
                </span>
            </div>

            {/* Prime badge */}
            {product.isPrime && (
                <div className="absolute top-4 right-4 z-10">
                    <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-600/90 text-white">
                        Prime
                    </span>
                </div>
            )}

            {/* Imagen del producto */}
            <div className="relative aspect-square overflow-hidden bg-white/5 p-4">
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <Image
                    src={product.imageUrl}
                    alt={product.title}
                    fill
                    className="object-contain group-hover:scale-110 transition-transform duration-500"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
            </div>

            {/* Contenido */}
            <div className="p-5 space-y-4">
                {/* Categoría */}
                <span className="inline-block text-xs font-medium text-forest-400 uppercase tracking-wider">
                    {product.category.replace(/-/g, ' ')}
                </span>

                {/* Título */}
                <h3 className="text-lg font-semibold text-white line-clamp-2 min-h-[3.5rem] group-hover:text-forest-300 transition-colors">
                    {product.title}
                </h3>

                {/* Rating */}
                {product.rating && (
                    <div className="flex items-center gap-2">
                        <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                                <svg
                                    key={i}
                                    className={`w-4 h-4 ${i < Math.floor(product.rating!)
                                            ? 'text-yellow-400'
                                            : 'text-slate-600'
                                        }`}
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                            ))}
                        </div>
                        <span className="text-sm text-slate-400">
                            ({product.reviewCount?.toLocaleString('es-ES')})
                        </span>
                    </div>
                )}

                {/* Precios */}
                <div className="flex items-end gap-3">
                    <span className="text-2xl font-bold text-white">
                        {product.discountedPrice.toFixed(2)}€
                    </span>
                    <span className="text-lg text-slate-500 line-through">
                        {product.originalPrice.toFixed(2)}€
                    </span>
                </div>

                {/* Ahorro */}
                <div className="text-sm text-forest-400 font-medium">
                    Ahorras: {(product.originalPrice - product.discountedPrice).toFixed(2)}€
                </div>

                {/* Botón de compra */}
                <a
                    href={product.affiliateUrl}
                    target="_blank"
                    rel="noopener noreferrer sponsored"
                    className="block w-full py-3 px-4 text-center font-semibold rounded-xl bg-gradient-to-r from-forest-600 to-forest-500 hover:from-forest-500 hover:to-forest-400 text-white shadow-lg shadow-forest-500/25 hover:shadow-forest-500/40 transition-all duration-300 transform hover:scale-[1.02]"
                >
                    Ver en Amazon
                </a>

                {/* Disclosure de afiliado */}
                <p className="text-xs text-slate-500 text-center">
                    Enlace de afiliado Amazon
                </p>
            </div>
        </article>
    );
}
