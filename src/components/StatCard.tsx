interface StatCardProps {
    icon: string;
    value: string | number;
    label: string;
    highlight?: boolean;
}

export default function StatCard({ icon, value, label, highlight = false }: StatCardProps) {
    return (
        <div
            className={`
        relative overflow-hidden rounded-2xl p-6 
        ${highlight
                    ? 'bg-gradient-to-br from-forest-600/20 to-forest-500/10 border-forest-500/30'
                    : 'bg-slate-800/50 border-slate-700/50'
                }
        border backdrop-blur-sm
      `}
        >
            {/* Decorative gradient */}
            {highlight && (
                <div className="absolute top-0 right-0 w-32 h-32 bg-forest-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            )}

            <div className="relative">
                <span className="text-3xl mb-3 block">{icon}</span>
                <p className={`text-3xl font-bold ${highlight ? 'text-forest-400' : 'text-white'}`}>
                    {typeof value === 'number' ? value.toLocaleString('es-ES') : value}
                </p>
                <p className="text-sm text-slate-400 mt-1">{label}</p>
            </div>
        </div>
    );
}
