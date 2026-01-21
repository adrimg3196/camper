export default function Loading() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            <div className="text-center">
                <div className="relative">
                    <span className="text-6xl animate-bounce inline-block">🏕️</span>
                </div>
                <p className="text-slate-400 mt-4 animate-pulse">Cargando ofertas...</p>
            </div>
        </div>
    );
}
