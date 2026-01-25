'use client';

import { Product } from '@/lib/types';
import { useState } from 'react';

interface ProductCardProps {
    product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
    const [imgError, setImgError] = useState(false);

    // Normalize product data
    const imageUrl = product.image_url || product.imageUrl || '';
    const price = product.price || product.discountedPrice || 0;
    const originalPrice = product.original_price || product.originalPrice || 0;
    const discount = product.discount || product.discountPercentage || 0;
    const reviewCount = product.review_count || product.reviewCount || 0;
    const rating = product.rating || 4.5;
    const savings = originalPrice - price;

    // Build affiliate URL
    const partnerTag = process.env.NEXT_PUBLIC_AMAZON_PARTNER_TAG || 'camperdeals07-21';
    let finalUrl = product.affiliate_url || product.affiliateUrl || product.url;
    if (finalUrl && finalUrl.includes('amazon.es') && !finalUrl.includes('tag=')) {
        const connector = finalUrl.includes('?') ? '&' : '?';
        finalUrl = `${finalUrl}${connector}tag=${partnerTag}`;
    }

    // Schema.org Product JSON-LD para Rich Snippets
    const productSchema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.marketing_title || product.title,
        "description": `${product.marketing_title || product.title} - Oferta con ${discount}% de descuento`,
        "image": imageUrl,
        "brand": {
            "@type": "Brand",
            "name": product.category.replace(/-/g, ' ')
        },
        "sku": product.id,
        "offers": {
            "@type": "Offer",
            "url": finalUrl,
            "priceCurrency": "EUR",
            "price": price.toFixed(2),
            "priceValidUntil": new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Amazon España"
            }
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating.toFixed(1),
            "bestRating": "5",
            "worstRating": "1",
            "reviewCount": reviewCount || 1
        }
    };

    return (
        <article className="product-card group relative bg-gradient-to-br from-slate-800/90 to-slate-900/90 rounded-2xl overflow-hidden border border-slate-700/50 hover:border-green-500/30">
            {/* Schema.org JSON-LD para SEO Rich Snippets */}
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(productSchema) }}
            />

            {/* Discount badge */}
            <div className="absolute top-3 left-3 z-10">
                <span className="discount-badge inline-flex items-center px-3 py-1.5 rounded-full text-sm font-bold bg-gradient-to-r from-red-500 to-orange-500 text-white shadow-lg">
                    -{discount}%
                </span>
            </div>

            {/* Prime badge */}
            {product.isPrime && (
                <div className="absolute top-3 right-3 z-10">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600 text-white shadow-md">
                        ✓ Prime
                    </span>
                </div>
            )}

            {/* Product image */}
            <div className="relative aspect-square overflow-hidden bg-white">
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10" />
                <div className="w-full h-full p-4 flex items-center justify-center">
                    {!imgError && imageUrl ? (
                        <img
                            src={imageUrl}
                            alt={product.title}
                            className="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-500"
                            loading="lazy"
                            width={400}
                            height={400}
                            onError={() => setImgError(true)}
                        />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center bg-slate-100">
                            <svg className="w-16 h-16 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                    )}
                </div>
            </div>

            {/* Content */}
            <div className="p-5 space-y-3">
                {/* Category */}
                <span className="inline-block text-xs font-semibold text-green-400 uppercase tracking-wider">
                    {product.category.replace(/-/g, ' ')}
                </span>

                {/* Title */}
                <h3 className="text-base font-semibold text-white line-clamp-2 min-h-[3rem] leading-snug group-hover:text-green-300 transition-colors">
                    {product.marketing_title || product.title}
                </h3>

                {/* Rating */}
                <div className="flex items-center gap-2">
                    <div className="flex items-center gap-0.5" aria-label={`${rating} de 5 estrellas`}>
                        {[...Array(5)].map((_, i) => (
                            <svg key={i} className={`w-4 h-4 ${i < Math.floor(rating) ? 'text-yellow-400' : 'text-slate-600'}`} fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        ))}
                    </div>
                    <span className="text-sm text-slate-400">({reviewCount.toLocaleString('es-ES')})</span>
                </div>

                {/* Prices */}
                <div className="flex items-baseline gap-3 pt-1">
                    <span className="text-2xl font-bold text-white">{price.toFixed(2)}€</span>
                    <span className="text-base text-slate-500 line-through">{originalPrice.toFixed(2)}€</span>
                </div>

                {/* Savings */}
                <div className="text-sm text-green-400 font-semibold">
                    Ahorras: {savings.toFixed(2)}€
                </div>

                {/* CTA Button */}
                <a
                    href={finalUrl}
                    target="_blank"
                    rel="noopener noreferrer sponsored"
                    className="block w-full py-3.5 px-4 text-center font-semibold rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white shadow-lg shadow-green-500/20 hover:shadow-green-500/30 transition-all duration-300 transform hover:scale-[1.02] mt-4"
                >
                    Ver en Amazon →
                </a>

                {/* Affiliate disclosure */}
                <p className="text-[10px] text-slate-500 text-center pt-1">Enlace de afiliado de Amazon</p>
            </div>
        </article>
    );
}
