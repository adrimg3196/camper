import Link from 'next/link';
import { CATEGORIES } from '@/lib/types';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function NotFound() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow flex flex-col items-center justify-center px-4 py-20">
                <div className="text-center max-w-2xl mx-auto">
                    <span className="text-8xl mb-6 block">🧭</span>
                    <h1 className="text-5xl font-bold text-white mb-4">404</h1>
                    <h2 className="text-2xl text-slate-300 mb-4">Página no encontrada</h2>
                    <p className="text-slate-400 mb-10 text-lg">
                        Parece que te has perdido en el bosque. Esta página no existe, pero tenemos ofertas increíbles esperándote.
                    </p>

                    {/* Primary CTA */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center mb-14">
                        <Link
                            href="/"
                            className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-bold shadow-lg shadow-green-500/25 transition-all duration-300 hover:scale-105"
                        >
                            🏕️ Ver todas las ofertas
                        </Link>
                        <Link
                            href="/guias"
                            className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium border border-slate-700 transition-all duration-300"
                        >
                            📚 Ver guías de compra
                        </Link>
                    </div>

                    {/* Category shortcuts */}
                    <div>
                        <p className="text-slate-500 text-sm mb-4 uppercase tracking-wider font-semibold">O explora por categoría</p>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                            {CATEGORIES.slice(0, 8).map((cat) => (
                                <Link
                                    key={cat.slug}
                                    href={`/ofertas/${cat.slug}`}
                                    className="flex flex-col items-center gap-2 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-green-500/50 hover:bg-slate-800 transition-all group"
                                >
                                    <span className="text-2xl group-hover:scale-110 transition-transform">{cat.icon}</span>
                                    <span className="text-xs text-slate-400 group-hover:text-white text-center">{cat.name}</span>
                                </Link>
                            ))}
                        </div>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
