import Link from 'next/link';
import { CATEGORIES } from '@/lib/types';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="border-t border-slate-700/50 bg-slate-900/95">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                    {/* Brand */}
                    <div className="col-span-2 md:col-span-1">
                        <Link href="/" className="flex items-center gap-2 group">
                            <span className="text-3xl group-hover:scale-110 transition-transform">🏕️</span>
                            <span className="text-xl font-bold text-white">CampingDeals España</span>
                        </Link>
                        <p className="mt-4 text-sm text-slate-400 leading-relaxed">
                            Las mejores ofertas de camping, tiendas de campaña baratas, sacos de dormir y mochilas con más del 30% de descuento en Amazon España.
                        </p>
                        {/* Social icons */}
                        <div className="flex gap-3 mt-6">
                            <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-xl bg-slate-800 hover:bg-blue-500 flex items-center justify-center text-slate-400 hover:text-white transition-all" aria-label="Telegram">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" /></svg>
                            </a>
                            <a href="https://instagram.com/camperdeals" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-xl bg-slate-800 hover:bg-gradient-to-br hover:from-purple-500 hover:to-pink-500 flex items-center justify-center text-slate-400 hover:text-white transition-all" aria-label="Instagram">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" /></svg>
                            </a>
                            <a href="https://tiktok.com/@camperdeals" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-xl bg-slate-800 hover:bg-black flex items-center justify-center text-slate-400 hover:text-white transition-all" aria-label="TikTok">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" /></svg>
                            </a>
                        </div>
                    </div>

                    {/* Categorías */}
                    <div>
                        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Categorías</h3>
                        <ul className="space-y-2.5">
                            {CATEGORIES.slice(0, 4).map(category => (
                                <li key={category.slug}>
                                    <Link href={`/ofertas/${category.slug}`} className="text-sm text-slate-400 hover:text-green-400 transition-colors flex items-center gap-1.5">
                                        <span>{category.icon}</span> {category.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Más categorías */}
                    <div>
                        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Más</h3>
                        <ul className="space-y-2.5">
                            {CATEGORIES.slice(4).map(category => (
                                <li key={category.slug}>
                                    <Link href={`/ofertas/${category.slug}`} className="text-sm text-slate-400 hover:text-green-400 transition-colors flex items-center gap-1.5">
                                        <span>{category.icon}</span> {category.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                {/* Divider + Legal */}
                <div className="mt-12 pt-8 border-t border-slate-800">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                        <div className="flex flex-col gap-2">
                            <p className="text-xs text-slate-500">© {currentYear} CampingDeals España. Todos los derechos reservados.</p>
                            <div className="flex flex-wrap gap-x-4 gap-y-1">
                                <Link href="/aviso-legal" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Aviso Legal</Link>
                                <Link href="/politica-privacidad" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Privacidad</Link>
                                <Link href="/politica-cookies" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Cookies</Link>
                                <Link href="/sobre-nosotros" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Sobre Nosotros</Link>
                                <Link href="/contacto" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Contacto</Link>
                            </div>
                        </div>
                        <p className="text-xs text-slate-500 md:text-right max-w-lg">
                            <strong className="text-slate-400">Aviso:</strong> Como Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables. Los precios pueden cambiar.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
}
