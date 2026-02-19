import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Link from 'next/link';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Sobre Nosotros | CampingDeals España",
    description: "CampingDeals España: quiénes somos, cómo encontramos las mejores ofertas de camping y cómo ganamos dinero con el programa de afiliados de Amazon.",
    alternates: {
        canonical: `${getSiteUrl()}/sobre-nosotros`,
    },
};

export default function SobreNosotros() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-3xl mx-auto px-4 sm:px-6">
                    <div className="mb-10">
                        <span className="inline-block py-1 px-3 rounded-full bg-green-500/20 text-green-300 text-xs font-semibold mb-4 border border-green-500/30">
                            Quiénes somos
                        </span>
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">Sobre CampingDeals España</h1>
                        <p className="text-xl text-slate-300">
                            Encontramos las mejores ofertas de camping en Amazon España para que tú no tengas que hacerlo.
                        </p>
                    </div>

                    <div className="prose prose-invert max-w-none text-slate-300 space-y-8">

                        <section>
                            <h2 className="text-xl font-bold text-white mb-4">Qué hacemos</h2>
                            <p>
                                <strong className="text-white">CampingDeals España</strong> es un portal de ofertas especializado en equipamiento de camping y outdoor. Escaneamos Amazon España diariamente para encontrar los mejores descuentos en tiendas de campaña, sacos de dormir, mochilas, cocina camping y todo el material que necesitas para tus aventuras al aire libre.
                            </p>
                            <p className="mt-4">Solo mostramos ofertas con <strong className="text-white">más del 30% de descuento</strong> sobre el precio habitual del producto, verificado antes de publicarse.</p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-4">Cómo ganamos dinero (transparencia total)</h2>
                            <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 p-6">
                                <p className="text-slate-300 mb-4">
                                    Este sitio participa en el <strong className="text-white">Programa de Afiliados de Amazon</strong>. Cuando haces clic en uno de nuestros enlaces y realizas una compra en Amazon, recibimos una pequeña comisión (entre el 3% y el 7% dependiendo de la categoría).
                                </p>
                                <p className="text-green-400 font-semibold">
                                    ✅ El precio que pagas en Amazon es exactamente el mismo, tanto si llegas desde nuestro enlace como si no.
                                </p>
                            </div>
                            <p className="mt-4 text-slate-400">
                                También mostramos anuncios de <strong className="text-white">Google AdSense</strong>. Estos anuncios son gestionados por Google y pueden personalizarse según tus intereses. Más información en nuestra <Link href="/politica-cookies" className="text-green-400 hover:underline">Política de Cookies</Link>.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-4">Nuestra metodología</h2>
                            <ul className="space-y-3">
                                <li className="flex items-start gap-3">
                                    <span className="text-green-400 mt-0.5">✓</span>
                                    <span><strong className="text-white">Solo descuentos reales:</strong> Verificamos el precio histórico del producto antes de publicarlo. No mostramos descuentos inflados sobre precios artificialmente altos.</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="text-green-400 mt-0.5">✓</span>
                                    <span><strong className="text-white">Actualización diaria:</strong> El sistema revisa precios automáticamente para asegurarse de que las ofertas sigan activas.</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="text-green-400 mt-0.5">✓</span>
                                    <span><strong className="text-white">Sin sesgos comerciales:</strong> Publicamos las mejores ofertas independientemente de si generan comisión alta o baja.</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="text-green-400 mt-0.5">✓</span>
                                    <span><strong className="text-white">Envío rápido:</strong> Priorizamos productos con envío Prime para que recibas tu pedido en 1-2 días.</span>
                                </li>
                            </ul>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-4">Síguenos</h2>
                            <p>La mejor forma de no perderte ninguna oferta es uniéndote a nuestro canal de Telegram:</p>
                            <a
                                href="https://t.me/camperdeals"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 mt-4 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-400 hover:to-blue-500 text-white font-semibold transition-all duration-300 hover:scale-105 no-underline"
                            >
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                                </svg>
                                Unirse a @camperdeals
                            </a>
                        </section>

                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
