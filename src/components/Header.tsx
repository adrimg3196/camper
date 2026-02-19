'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';

export default function Header() {
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-slate-900/95 backdrop-blur-lg shadow-lg shadow-black/20' : 'bg-slate-900/50 backdrop-blur-sm'}`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 md:h-20">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="relative">
                            <span className="text-3xl md:text-4xl transform group-hover:scale-110 transition-transform inline-block">🏕️</span>
                            <div className="absolute -right-1 -top-1 w-2.5 h-2.5 bg-green-500 rounded-full animate-pulse" />
                        </div>
                        <div className="hidden sm:block">
                            <span className="text-xl md:text-2xl font-bold tracking-tight">
                                <span className="text-gradient">Camping</span>
                                <span className="text-white">Deals</span>
                            </span>
                            <p className="text-[10px] text-slate-400 -mt-0.5 tracking-wide">Ofertas Camping España</p>
                        </div>
                    </Link>

                    {/* Desktop Nav */}
                    <nav className="hidden md:flex items-center gap-8">
                        <Link href="/#ofertas" className="text-sm font-medium text-slate-300 hover:text-white transition-colors relative group">
                            Ofertas
                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-500 group-hover:w-full transition-all duration-300" />
                        </Link>
                        <Link href="/#categorias" className="text-sm font-medium text-slate-300 hover:text-white transition-colors relative group">
                            Categorías
                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-500 group-hover:w-full transition-all duration-300" />
                        </Link>
                        <Link href="/guias" className="text-sm font-medium text-slate-300 hover:text-white transition-colors relative group">
                            Guías
                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-500 group-hover:w-full transition-all duration-300" />
                        </Link>
                        <Link href="/black-friday-camping" className="text-sm font-medium text-orange-300 hover:text-orange-200 transition-colors relative group">
                            Black Friday
                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-orange-500 group-hover:w-full transition-all duration-300" />
                        </Link>
                        <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" aria-label="Únete a nuestro canal de Telegram" className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-white text-sm font-medium shadow-lg shadow-blue-500/25 transition-all duration-300 hover:scale-105 hover:shadow-blue-500/40">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                            </svg>
                            <span>Únete</span>
                        </a>
                    </nav>

                    {/* Mobile menu button */}
                    <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="md:hidden p-2 text-slate-300 hover:text-white" aria-label="Abrir menú" aria-expanded={mobileMenuOpen}>
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            {mobileMenuOpen ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /> : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />}
                        </svg>
                    </button>
                </div>

                {/* Mobile menu */}
                <div className={`md:hidden overflow-hidden transition-all duration-300 ${mobileMenuOpen ? 'max-h-64 pb-4' : 'max-h-0'}`}>
                    <nav className="flex flex-col gap-3 pt-4 border-t border-slate-700/50">
                        <Link href="/#ofertas" onClick={() => setMobileMenuOpen(false)} className="text-base font-medium text-slate-300 hover:text-white transition-colors px-2 py-2 rounded-lg hover:bg-slate-800/50">🔥 Ofertas</Link>
                        <Link href="/#categorias" onClick={() => setMobileMenuOpen(false)} className="text-base font-medium text-slate-300 hover:text-white transition-colors px-2 py-2 rounded-lg hover:bg-slate-800/50">📂 Categorías</Link>
                        <Link href="/guias" onClick={() => setMobileMenuOpen(false)} className="text-base font-medium text-slate-300 hover:text-white transition-colors px-2 py-2 rounded-lg hover:bg-slate-800/50">📚 Guías de compra</Link>
                        <Link href="/black-friday-camping" onClick={() => setMobileMenuOpen(false)} className="text-base font-medium text-orange-300 hover:text-orange-200 transition-colors px-2 py-2 rounded-lg hover:bg-slate-800/50">🛒 Black Friday</Link>
                        <a href="https://t.me/camperdeals" target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium mt-2">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" /></svg>
                            Únete a Telegram
                        </a>
                    </nav>
                </div>
            </div>
        </header>
    );
}
