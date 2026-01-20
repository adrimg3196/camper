import Link from 'next/link';

export default function Header() {
    return (
        <header className="sticky top-0 z-50 glass-dark border-b border-slate-700/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 md:h-20">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="relative">
                            <span className="text-3xl md:text-4xl transform group-hover:scale-110 transition-transform inline-block">
                                🏕️
                            </span>
                            <div className="absolute -right-1 -top-1 w-3 h-3 bg-forest-500 rounded-full animate-pulse" />
                        </div>
                        <div className="hidden sm:block">
                            <h1 className="text-xl md:text-2xl font-bold font-display">
                                <span className="text-gradient">Camper</span>
                                <span className="text-white"> Deals</span>
                            </h1>
                            <p className="text-xs text-slate-400 -mt-0.5">
                                Ofertas +30% descuento
                            </p>
                        </div>
                    </Link>

                    {/* Nav links */}
                    <nav className="flex items-center gap-4 md:gap-6">
                        <Link
                            href="/#ofertas"
                            className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
                        >
                            Ofertas
                        </Link>
                        <Link
                            href="/#categorias"
                            className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
                        >
                            Categorías
                        </Link>

                        {/* Telegram CTA */}
                        <a
                            href="https://t.me/camperdeals"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-white text-sm font-medium shadow-lg shadow-blue-500/25 transition-all duration-300 hover:scale-105"
                        >
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                            </svg>
                            <span className="hidden md:inline">Únete</span>
                        </a>
                    </nav>
                </div>
            </div>
        </header>
    );
}
