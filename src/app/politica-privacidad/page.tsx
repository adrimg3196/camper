import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Política de Privacidad | CampingDeals España",
    description: "Política de privacidad de CampingDeals España. Información sobre cómo recopilamos y usamos tus datos.",
    robots: { index: false, follow: false },
    alternates: {
        canonical: `${getSiteUrl()}/politica-privacidad`,
    },
};

const LAST_UPDATED = "1 de febrero de 2026";

export default function PoliticaPrivacidad() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-3xl mx-auto px-4 sm:px-6">
                    <div className="mb-10">
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">Política de Privacidad</h1>
                        <p className="text-slate-400 text-sm">Última actualización: {LAST_UPDATED}</p>
                    </div>

                    <div className="prose prose-invert max-w-none text-slate-300 space-y-8">

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">1. Responsable del tratamiento</h2>
                            <p>CampingDeals España opera el sitio web <strong className="text-white">ofertascamping.es</strong>. Esta política describe cómo recopilamos, usamos y protegemos tu información.</p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">2. Datos que recopilamos</h2>
                            <h3 className="text-base font-semibold text-slate-200 mb-2">Datos recopilados automáticamente</h3>
                            <ul className="list-disc list-inside space-y-2 text-slate-400">
                                <li>Dirección IP (anonimizada)</li>
                                <li>Tipo de navegador y dispositivo</li>
                                <li>Páginas visitadas y tiempo en el sitio</li>
                                <li>Fuente de tráfico (cómo llegaste al sitio)</li>
                            </ul>
                            <h3 className="text-base font-semibold text-slate-200 mb-2 mt-4">Datos que NO recopilamos</h3>
                            <p className="text-slate-400">No recopilamos nombre, email, teléfono ni ningún dato de registro. No tenemos sistema de cuentas de usuario.</p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">3. Cookies y tecnologías de seguimiento</h2>
                            <p>Utilizamos las siguientes tecnologías:</p>
                            <ul className="list-disc list-inside space-y-2 text-slate-400 mt-3">
                                <li><strong className="text-white">Google Analytics 4</strong>: Análisis de tráfico web para mejorar el servicio. Datos anonimizados.</li>
                                <li><strong className="text-white">Google AdSense</strong>: Muestra anuncios relevantes. Google puede usar cookies para personalizar anuncios según tus intereses.</li>
                                <li><strong className="text-white">Amazon Associates</strong>: Cookie de sesión para atribuir compras realizadas desde nuestros enlaces de afiliado.</li>
                            </ul>
                            <p className="mt-4">Consulta nuestra <a href="/politica-cookies" className="text-green-400 hover:underline">Política de Cookies</a> para más información.</p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">4. Programa de Afiliados de Amazon</h2>
                            <p>
                                CampingDeals España es participante del Programa de Afiliados de Amazon EU, un programa de publicidad para afiliados diseñado para ofrecer un medio para que los sitios web ganen honorarios por publicidad mediante la publicidad y la vinculación a <strong className="text-white">amazon.es</strong>.
                            </p>
                            <p className="mt-3 text-slate-400">
                                Cuando haces clic en un enlace de afiliado y realizas una compra en Amazon, recibimos una pequeña comisión <strong className="text-white">sin coste adicional para ti</strong>. El precio que pagas es exactamente el mismo.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">5. Google AdSense y publicidad</h2>
                            <p>
                                Utilizamos Google AdSense para mostrar anuncios en este sitio. Google puede usar cookies e identificadores de dispositivo para mostrar anuncios personalizados basados en tus visitas anteriores a este y otros sitios web.
                            </p>
                            <p className="mt-3 text-slate-400">
                                Puedes optar por no recibir publicidad personalizada visitando <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">Configuración de anuncios de Google</a>.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">6. Tus derechos (RGPD)</h2>
                            <p>En cumplimiento del Reglamento General de Protección de Datos (RGPD), tienes derecho a:</p>
                            <ul className="list-disc list-inside space-y-2 text-slate-400 mt-3">
                                <li>Acceder a tus datos personales</li>
                                <li>Rectificar datos inexactos</li>
                                <li>Solicitar la supresión de tus datos</li>
                                <li>Oponerte al tratamiento</li>
                                <li>Portabilidad de datos</li>
                            </ul>
                            <p className="mt-4">Dado que no recopilamos datos personales identificables, el ejercicio de estos derechos se limitará principalmente a las cookies gestionadas por terceros (Google, Amazon).</p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">7. Cambios en esta política</h2>
                            <p>Podemos actualizar esta política ocasionalmente. La fecha de última actualización siempre estará visible al inicio de esta página.</p>
                        </section>

                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
