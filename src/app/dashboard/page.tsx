'use client';

import { useEffect, useState } from 'react';

interface SystemStatus {
    database: {
        connected: boolean;
        dealsCount: number;
        activeDeals: number;
    };
    apis: {
        gemini: boolean;
        telegram: boolean;
        supabase: boolean;
    };
    crons: {
        dailyPublish: string;
        scrapeDeals: string;
    };
    lastActivity: {
        lastScrape: string | null;
        lastPublish: string | null;
    };
}

function StatusBadge({ active, label }: { active: boolean; label: string }) {
    return (
        <div className="flex items-center gap-2">
            <span
                className={`w-2 h-2 rounded-full ${
                    active ? 'bg-green-400 animate-pulse' : 'bg-red-400'
                }`}
            />
            <span className={active ? 'text-green-400' : 'text-red-400'}>
                {label}: {active ? 'Activo' : 'Inactivo'}
            </span>
        </div>
    );
}

function formatRelativeTime(dateStr: string | null): string {
    if (!dateStr) return 'Nunca';
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Ahora mismo';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    return `Hace ${diffDays} días`;
}

export default function DashboardHome() {
    const [status, setStatus] = useState<SystemStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [testingCron, setTestingCron] = useState<string | null>(null);
    const [testResult, setTestResult] = useState<string | null>(null);

    useEffect(() => {
        fetchStatus();
        // Refrescar cada 30 segundos
        const interval = setInterval(fetchStatus, 30000);
        return () => clearInterval(interval);
    }, []);

    async function fetchStatus() {
        try {
            const res = await fetch('/api/system/status');
            const data = await res.json();
            setStatus(data.status);
        } catch (error) {
            console.error('Error fetching status:', error);
        } finally {
            setLoading(false);
        }
    }

    async function testCron(endpoint: string, name: string) {
        setTestingCron(name);
        setTestResult(null);
        try {
            const res = await fetch(`/api/cron/${endpoint}`, { method: 'POST' });
            const data = await res.json();
            setTestResult(
                data.success
                    ? `${name}: ${data.message || 'OK'}`
                    : `Error: ${data.error}`
            );
            // Refrescar status después del test
            await fetchStatus();
        } catch (error) {
            setTestResult(`Error: ${error}`);
        } finally {
            setTestingCron(null);
        }
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white mb-2">
                    Panel de Control de Marketing
                </h1>
                <p className="text-slate-400">
                    Gestiona tus campanas autonomas y genera contenido con IA.
                </p>
            </div>

            {/* System Status */}
            <div className="bg-gradient-to-r from-slate-800/80 to-slate-800/40 p-6 rounded-2xl border border-slate-700/50">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <span className="text-2xl">🤖</span> Estado del Sistema
                        Autonomo
                    </h2>
                    <button
                        onClick={fetchStatus}
                        className="text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        Actualizar
                    </button>
                </div>

                {loading ? (
                    <div className="text-slate-400 animate-pulse">
                        Cargando estado...
                    </div>
                ) : status ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* APIs Status */}
                        <div className="space-y-2">
                            <h3 className="text-sm font-medium text-slate-300 mb-3">
                                Conexiones API
                            </h3>
                            <StatusBadge
                                active={status.apis.supabase}
                                label="Supabase"
                            />
                            <StatusBadge
                                active={status.apis.gemini}
                                label="Google Gemini"
                            />
                            <StatusBadge
                                active={status.apis.telegram}
                                label="Telegram Bot"
                            />
                        </div>

                        {/* Database Stats */}
                        <div className="space-y-2">
                            <h3 className="text-sm font-medium text-slate-300 mb-3">
                                Base de Datos
                            </h3>
                            <div className="text-slate-400">
                                <span className="text-white font-bold text-2xl">
                                    {status.database.activeDeals}
                                </span>{' '}
                                ofertas activas
                            </div>
                            <div className="text-slate-500 text-sm">
                                {status.database.dealsCount} total en BD
                            </div>
                            <div
                                className={`text-sm ${
                                    status.database.connected
                                        ? 'text-green-400'
                                        : 'text-red-400'
                                }`}
                            >
                                {status.database.connected
                                    ? 'Conectado'
                                    : 'Desconectado'}
                            </div>
                        </div>

                        {/* CRON Schedule */}
                        <div className="space-y-2">
                            <h3 className="text-sm font-medium text-slate-300 mb-3">
                                Automatizacion CRON
                            </h3>
                            <div className="text-slate-400 text-sm">
                                <span className="text-slate-300">
                                    Scraping:
                                </span>{' '}
                                {status.crons.scrapeDeals}
                            </div>
                            <div className="text-slate-400 text-sm">
                                <span className="text-slate-300">
                                    Publicacion:
                                </span>{' '}
                                {status.crons.dailyPublish}
                            </div>
                            <div className="text-slate-500 text-xs mt-2">
                                Ultimo scrape:{' '}
                                {formatRelativeTime(
                                    status.lastActivity.lastScrape
                                )}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="text-red-400">
                        Error cargando estado del sistema
                    </div>
                )}

                {/* Test Buttons */}
                <div className="mt-6 pt-4 border-t border-slate-700/50">
                    <h3 className="text-sm font-medium text-slate-300 mb-3">
                        Ejecutar Manualmente
                    </h3>
                    <div className="flex flex-wrap gap-3">
                        <button
                            onClick={() => testCron('scrape-deals', 'Scraper')}
                            disabled={testingCron !== null}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white rounded-lg text-sm font-medium transition-colors"
                        >
                            {testingCron === 'Scraper'
                                ? 'Ejecutando...'
                                : 'Ejecutar Scraper'}
                        </button>
                        <button
                            onClick={() =>
                                testCron('daily-publish', 'Publicacion')
                            }
                            disabled={testingCron !== null}
                            className="px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-slate-600 text-white rounded-lg text-sm font-medium transition-colors"
                        >
                            {testingCron === 'Publicacion'
                                ? 'Publicando...'
                                : 'Publicar Ahora'}
                        </button>
                    </div>
                    {testResult && (
                        <div
                            className={`mt-3 text-sm ${
                                testResult.includes('Error')
                                    ? 'text-red-400'
                                    : 'text-green-400'
                            }`}
                        >
                            {testResult}
                        </div>
                    )}
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
                            📈
                        </div>
                        <span className="text-xs text-green-400 flex items-center gap-1">
                            +12%{' '}
                            <span className="text-slate-500">vs ayer</span>
                        </span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">
                        Clicks Totales
                    </p>
                    <p className="text-3xl font-bold text-white">1,248</p>
                </div>

                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-purple-500/20 rounded-lg text-purple-400">
                            🤖
                        </div>
                        <span className="text-xs text-slate-500">Hoy</span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">
                        Posts Generados
                    </p>
                    <p className="text-3xl font-bold text-white">24</p>
                </div>

                <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-green-500/20 rounded-lg text-green-400">
                            💰
                        </div>
                        <span className="text-xs text-green-400 flex items-center gap-1">
                            +8%{' '}
                            <span className="text-slate-500">vs ayer</span>
                        </span>
                    </div>
                    <p className="text-slate-400 text-sm mb-1">Conversiones</p>
                    <p className="text-3xl font-bold text-white">3.8%</p>
                </div>
            </div>

            {/* Environment Checklist */}
            <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50">
                <h2 className="text-lg font-bold text-white mb-4">
                    Variables de Entorno Requeridas
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <span
                                className={`w-2 h-2 rounded-full ${
                                    status?.apis.supabase
                                        ? 'bg-green-400'
                                        : 'bg-yellow-400'
                                }`}
                            />
                            <code className="text-slate-300">
                                NEXT_PUBLIC_SUPABASE_URL
                            </code>
                        </div>
                        <div className="flex items-center gap-2">
                            <span
                                className={`w-2 h-2 rounded-full ${
                                    status?.apis.supabase
                                        ? 'bg-green-400'
                                        : 'bg-yellow-400'
                                }`}
                            />
                            <code className="text-slate-300">
                                NEXT_PUBLIC_SUPABASE_ANON_KEY
                            </code>
                        </div>
                        <div className="flex items-center gap-2">
                            <span
                                className={`w-2 h-2 rounded-full ${
                                    status?.apis.gemini
                                        ? 'bg-green-400'
                                        : 'bg-yellow-400'
                                }`}
                            />
                            <code className="text-slate-300">
                                GOOGLE_API_KEY
                            </code>
                        </div>
                    </div>
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <span
                                className={`w-2 h-2 rounded-full ${
                                    status?.apis.telegram
                                        ? 'bg-green-400'
                                        : 'bg-yellow-400'
                                }`}
                            />
                            <code className="text-slate-300">
                                TELEGRAM_BOT_TOKEN
                            </code>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-slate-400" />
                            <code className="text-slate-300">
                                TELEGRAM_CHANNEL_ID
                            </code>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-slate-400" />
                            <code className="text-slate-300">CRON_SECRET</code>
                        </div>
                    </div>
                </div>
                <p className="text-slate-500 text-xs mt-4">
                    Configura estas variables en Vercel &gt; Settings &gt;
                    Environment Variables
                </p>
            </div>

            {/* Active Campaigns */}
            <div>
                <h2 className="text-lg font-bold text-white mb-4">
                    Campanas Activas
                </h2>
                <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 overflow-hidden">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-slate-700 text-slate-400 text-sm">
                                <th className="p-4 font-medium">Campana</th>
                                <th className="p-4 font-medium">Plataforma</th>
                                <th className="p-4 font-medium">Estado</th>
                                <th className="p-4 font-medium text-right">
                                    Clicks
                                </th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            <tr className="border-b border-slate-700/50 hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">
                                    Tienda Coleman 3P
                                </td>
                                <td className="p-4 text-slate-400">Telegram</td>
                                <td className="p-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
                                        Activo
                                    </span>
                                </td>
                                <td className="p-4 text-right text-white">
                                    432
                                </td>
                            </tr>
                            <tr className="border-b border-slate-700/50 hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">
                                    Sacos Invierno Top 10
                                </td>
                                <td className="p-4 text-slate-400">TikTok</td>
                                <td className="p-4">
                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                        Programado
                                    </span>
                                </td>
                                <td className="p-4 text-right text-white">-</td>
                            </tr>
                            <tr className="hover:bg-slate-800/80 transition-colors">
                                <td className="p-4 text-white font-medium">
                                    Kit Supervivencia
                                </td>
                                <td className="p-4 text-slate-400">
                                    Instagram
                                </td>
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
