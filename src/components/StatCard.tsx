interface StatCardProps {
    icon: string;
    value: string | number;
    label: string;
    highlight?: boolean;
}

export default function StatCard({ icon, value, label, highlight = false }: StatCardProps) {
    return (
        <div className={`stat-card relative overflow-hidden rounded-2xl p-5 sm:p-6 ${highlight ? 'bg-gradient-to-br from-green-600/20 to-green-500/10 border-green-500/30' : 'bg-slate-800/50 border-slate-700/50'} border backdrop-blur-sm transition-all duration-300 hover:border-green-500/30`}>
            {/* Decorative gradient */}
            {highlight && (
                <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            )}

            <div className="relative flex items-center gap-4">
                <span className="text-3xl sm:text-4xl">{icon}</span>
                <div>
                    <p className={`text-2xl sm:text-3xl font-bold ${highlight ? 'text-green-400' : 'text-white'}`}>
                        {typeof value === 'number' ? value.toLocaleString('es-ES') : value}
                    </p>
                    <p className="text-xs sm:text-sm text-slate-400">{label}</p>
                </div>
            </div>
        </div>
    );
}
