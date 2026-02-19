import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Contacto | CampingDeals España",
    description: "¿Tienes alguna pregunta o sugerencia sobre CampingDeals España? Escríbenos.",
    robots: { index: false, follow: false },
    alternates: {
        canonical: `${getSiteUrl()}/contacto`,
    },
};

export default function Contacto() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-2xl mx-auto px-4 sm:px-6">
                    <div className="mb-10">
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">Contacto</h1>
                        <p className="text-slate-400 text-lg">
                            ¿Tienes alguna pregunta, sugerencia u oferta que quieras compartir con nosotros?
                        </p>
                    </div>

                    <div className="space-y-6">
                        {/* Telegram - main channel */}
                        <a
                            href="https://t.me/camperdeals"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-4 p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50 hover:border-blue-500/50 transition-all group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                                <svg className="w-6 h-6 text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                                </svg>
                            </div>
                            <div>
                                <p className="font-bold text-white group-hover:text-blue-300 transition-colors">Canal de Telegram</p>
                                <p className="text-sm text-slate-400">@camperdeals — La forma más rápida de contactar y recibir alertas</p>
                            </div>
                            <svg className="w-5 h-5 text-slate-500 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </a>

                        {/* TikTok */}
                        <a
                            href="https://tiktok.com/@camperoutlet"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-4 p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-500/50 transition-all group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-slate-700/50 flex items-center justify-center flex-shrink-0">
                                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" />
                                </svg>
                            </div>
                            <div>
                                <p className="font-bold text-white group-hover:text-slate-300 transition-colors">TikTok</p>
                                <p className="text-sm text-slate-400">@camperoutlet — Vídeos de ofertas y consejos de camping</p>
                            </div>
                            <svg className="w-5 h-5 text-slate-500 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </a>

                        {/* Info box */}
                        <div className="p-6 rounded-2xl bg-green-500/10 border border-green-500/20">
                            <h2 className="font-bold text-white mb-2">¿Quieres reportar una oferta incorrecta?</h2>
                            <p className="text-sm text-slate-400">
                                Si encuentras un precio desactualizado o un enlace roto, escríbenos directamente por Telegram. Lo corregimos en menos de 24 horas.
                            </p>
                        </div>

                        <div className="p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
                            <h2 className="font-bold text-white mb-2">Sobre este sitio</h2>
                            <p className="text-sm text-slate-400">
                                CampingDeals España es un portal de afiliados de Amazon. Más información en nuestra página{' '}
                                <a href="/sobre-nosotros" className="text-green-400 hover:underline">Sobre Nosotros</a>.
                            </p>
                        </div>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
