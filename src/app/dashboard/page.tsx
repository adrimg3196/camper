export default function DashboardHome() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white mb-2">Panel de Control de Marketing</h1>
                <p className="text-slate-400">Gestiona tus campañas autónomas y genera contenido con IA.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">📈</div>
                        <span className="text-xs text-green-400 flex items-center gap-1">
                            +12% <span className="text-slate-500">vs ayer</span>
                        </span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">Clicks Totales</p>
                    <p className="text-3xl font-bold text-white">1,248</p>
                </div>

                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-purple-500/20 rounded-lg text-purple-400">🤖</div>
                        <span className="text-xs text-slate-500">Hoy</span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">Posts Generados</p>
                    <p className="text-3xl font-bold text-white">24</p>
                </div>

                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-green-500/20 rounded-lg text-green-400">💰</div>
                        <span className="text-xs text-green-400 flex items-center gap-1">
                            +8% <span className="text-slate-500">vs ayer</span>
                        </span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">Conversiones</p>
                    <p className="text-3xl font-bold text-white">3.8%</p>
                </div>
            </div>

            {/* Active Campaigns */}
            <div>
                <h2 className="text-lg font-bold text-white mb-4">Campañas Activas</h2>
                <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 overflow-hidden">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-slate-700 text-slate-400 text-sm">
                                <th className="p-4 font-medium">Campaña</th>
                                <th className="p-4 font-medium">Plataforma</th>
                                <th className="p-4 font-medium">Estado</th>
                                <th className="p-4 font-medium text-right">Clicks</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            <tr className="border-b border-slate-700/50 hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">Tienda Coleman 3P</td>
                                <td className="p-4 text-slate-400">Telegram</td>
                                <td className="p-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
                                        Activo
                                    </span>
                                </td>
                                <td className="p-4 text-right text-white">432</td>
                            </tr>
                            <tr className="border-b border-slate-700/50 hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">Sacos Invierno Top 10</td>
                                <td className="p-4 text-slate-400">TikTok</td>
                                <td className="p-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                        Programado
                                    </span>
                                </td>
                                <td className="p-4 text-right text-white">-</td>
                            </tr>
                            <tr className="hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">Kit Supervivencia</td>
                                <td className="p-4 text-slate-400">Instagram</td>
                                <td className="p-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-slate-500/10 text-slate-400 border border-slate-500/20">
                                        Borrador
                                    </span>
                                </td>
                                <td className="p-4 text-right text-white">-</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
