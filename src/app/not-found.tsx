import Link from 'next/link';

export default function NotFound() {
    return (
        <div className="min-h-screen flex items-center justify-center px-4 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            <div className="text-center max-w-md">
                <span className="text-8xl mb-6 block">🏕️</span>
                <h1 className="text-4xl font-bold text-white mb-4">404</h1>
                <h2 className="text-xl text-slate-300 mb-4">Página no encontrada</h2>
                <p className="text-slate-400 mb-8">
                    Parece que te has perdido en el bosque. Esta página no existe.
                </p>
                <Link
                    href="/"
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold shadow-lg shadow-green-500/25 transition-all duration-300"
                >
                    ← Volver al campamento
                </Link>
            </div>
        </div>
    );
}
