import Header from '@/components/Header';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="min-h-screen bg-slate-950 flex flex-col text-white">
            <Header />
            <div className="flex flex-1 pt-16">
                {/* Sidebar */}
                <aside className="w-64 bg-slate-900 border-r border-slate-800 hidden md:block fixed h-full pt-6">
                    <div className="px-6 mb-8">
                        <h2 className="text-xs uppercase text-slate-500 font-bold tracking-wider">Marketing AI</h2>
                    </div>
                    <nav className="space-y-1 px-4">
                        <a href="/dashboard" className="flex items-center gap-3 px-4 py-3 bg-blue-600/10 text-blue-400 rounded-lg border border-blue-600/20 font-medium">
                            <span>📊</span> Dashboard
                        </a>
                        <a href="/dashboard/create" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                            <span>✍️</span> Crear Campaña
                        </a>
                        <a href="/dashboard/history" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                            <span>📚</span> Historial
                        </a>
                        <a href="/dashboard/settings" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                            <span>⚙️</span> Configuración
                        </a>
                    </nav>

                    <div className="absolute bottom-24 left-0 w-full px-6">
                        <div className="p-4 bg-slate-800 rounded-xl border border-slate-700">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                <span className="text-xs font-medium text-slate-300">Bot Activo</span>
                            </div>
                            <p className="text-xs text-slate-500">Próxima publicación automática: 14:00h</p>
                        </div>
                    </div>
                </aside>

                {/* Main Content */}
                <main className="flex-1 md:ml-64 p-6 sm:p-12 overflow-y-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}
