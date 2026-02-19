import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Política de Cookies | CampingDeals España",
    description: "Información sobre las cookies utilizadas en CampingDeals España: Google Analytics, AdSense y Amazon Associates.",
    robots: { index: false, follow: false },
    alternates: {
        canonical: `${getSiteUrl()}/politica-cookies`,
    },
};

const COOKIES = [
    {
        name: "_ga, _ga_*",
        owner: "Google Analytics",
        purpose: "Análisis de visitas y comportamiento de usuarios (anonimizado)",
        duration: "2 años",
        type: "Analítica"
    },
    {
        name: "__Secure-3PAPISID, NID, DSID",
        owner: "Google AdSense",
        purpose: "Personalización de anuncios y medición de rendimiento",
        duration: "Hasta 2 años",
        type: "Publicidad"
    },
    {
        name: "session-id, ubid-acbes",
        owner: "Amazon Associates",
        purpose: "Seguimiento de clics en enlaces de afiliado de Amazon",
        duration: "Sesión / 1 año",
        type: "Afiliación"
    },
    {
        name: "telegram_banner_dismissed",
        owner: "CampingDeals (propio)",
        purpose: "Recuerda si el usuario ha cerrado el banner de Telegram",
        duration: "Sesión",
        type: "Funcional"
    },
];

export default function PoliticaCookies() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-3xl mx-auto px-4 sm:px-6">
                    <div className="mb-10">
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">Política de Cookies</h1>
                        <p className="text-slate-400 text-sm">Última actualización: 1 de febrero de 2026</p>
                    </div>

                    <div className="prose prose-invert max-w-none text-slate-300 space-y-8">

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">¿Qué son las cookies?</h2>
                            <p>
                                Las cookies son pequeños archivos de texto que los sitios web almacenan en tu dispositivo cuando los visitas. Se utilizan para recordar tus preferencias, analizar cómo usas el sitio y mostrar publicidad relevante.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-4">Cookies que utilizamos</h2>
                            <div className="not-prose overflow-x-auto -mx-4 sm:mx-0">
                                <table className="w-full text-sm border-collapse">
                                    <thead>
                                        <tr className="bg-slate-700/50">
                                            <th className="text-left p-3 text-slate-300 font-semibold border border-slate-700">Cookie</th>
                                            <th className="text-left p-3 text-slate-300 font-semibold border border-slate-700">Proveedor</th>
                                            <th className="text-left p-3 text-slate-300 font-semibold border border-slate-700">Finalidad</th>
                                            <th className="text-left p-3 text-slate-300 font-semibold border border-slate-700">Duración</th>
                                            <th className="text-left p-3 text-slate-300 font-semibold border border-slate-700">Tipo</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {COOKIES.map((cookie, i) => (
                                            <tr key={i} className={i % 2 === 0 ? 'bg-slate-800/30' : 'bg-slate-800/10'}>
                                                <td className="p-3 border border-slate-700 font-mono text-xs text-green-400">{cookie.name}</td>
                                                <td className="p-3 border border-slate-700 text-slate-300">{cookie.owner}</td>
                                                <td className="p-3 border border-slate-700 text-slate-400">{cookie.purpose}</td>
                                                <td className="p-3 border border-slate-700 text-slate-400">{cookie.duration}</td>
                                                <td className="p-3 border border-slate-700">
                                                    <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-slate-700 text-slate-300">{cookie.type}</span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">Cómo gestionar las cookies</h2>
                            <p>Puedes controlar y eliminar las cookies desde la configuración de tu navegador:</p>
                            <ul className="list-disc list-inside space-y-2 text-slate-400 mt-3">
                                <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">Google Chrome</a></li>
                                <li><a href="https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">Mozilla Firefox</a></li>
                                <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">Apple Safari</a></li>
                            </ul>
                            <p className="mt-4 text-slate-400">
                                Ten en cuenta que deshabilitar ciertas cookies puede afectar a la funcionalidad del sitio.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">Publicidad personalizada de Google</h2>
                            <p>
                                Puedes optar por no recibir publicidad personalizada de Google visitando{' '}
                                <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">
                                    Configuración de anuncios de Google
                                </a>{' '}
                                o mediante{' '}
                                <a href="http://www.aboutads.info/choices/" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">
                                    YourAdChoices
                                </a>.
                            </p>
                        </section>

                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
