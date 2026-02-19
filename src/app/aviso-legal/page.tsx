import { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSiteUrl } from '@/lib/config';

export const metadata: Metadata = {
    title: "Aviso Legal | CampingDeals España",
    description: "Aviso legal y condiciones de uso de CampingDeals España.",
    robots: { index: false, follow: false },
    alternates: {
        canonical: `${getSiteUrl()}/aviso-legal`,
    },
};

export default function AvisoLegal() {
    return (
        <div className="min-h-screen flex flex-col font-sans text-white">
            <Header />
            <main className="flex-grow pt-24 pb-20">
                <div className="max-w-3xl mx-auto px-4 sm:px-6">
                    <div className="mb-10">
                        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">Aviso Legal</h1>
                        <p className="text-slate-400 text-sm">Última actualización: 1 de febrero de 2026</p>
                    </div>

                    <div className="prose prose-invert max-w-none text-slate-300 space-y-8">

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">1. Identificación del titular</h2>
                            <p>
                                En cumplimiento del artículo 10 de la Ley 34/2002 de Servicios de la Sociedad de la Información y Comercio Electrónico (LSSI), se pone a disposición del usuario la siguiente información:
                            </p>
                            <ul className="list-none space-y-1 mt-3 text-slate-400">
                                <li><strong className="text-white">Sitio web:</strong> ofertascamping.es</li>
                                <li><strong className="text-white">Denominación:</strong> CampingDeals España</li>
                                <li><strong className="text-white">País:</strong> España</li>
                                <li><strong className="text-white">Actividad:</strong> Portal de ofertas y afiliación de Amazon</li>
                            </ul>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">2. Condiciones de uso</h2>
                            <p>
                                El acceso y uso del sitio web implica la aceptación plena de las condiciones aquí establecidas. El usuario se compromete a hacer un uso adecuado de los contenidos y servicios, con plena sujeción a la legislación vigente y a los presentes términos.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">3. Propiedad intelectual</h2>
                            <p>
                                Los contenidos, diseños, textos, imágenes y demás elementos del sitio web son propiedad de CampingDeals España o de terceros que han autorizado su uso. Queda prohibida su reproducción total o parcial sin autorización expresa.
                            </p>
                            <p className="mt-3 text-slate-400">
                                Las imágenes de productos pertenecen a Amazon y sus vendedores. Las fotografías de portada son cortesía de <a href="https://unsplash.com" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline">Unsplash</a> y sus autores.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">4. Exención de responsabilidad</h2>
                            <p>
                                Los precios y disponibilidad mostrados en este sitio son orientativos y pueden cambiar en cualquier momento. CampingDeals España no garantiza la exactitud de los precios mostrados y no se responsabiliza de las diferencias entre el precio mostrado y el precio final en Amazon.
                            </p>
                            <p className="mt-3 text-slate-400">
                                Los enlaces a Amazon.es son enlaces de afiliado. Las transacciones se realizan directamente entre el usuario y Amazon, siendo este último el único responsable del proceso de compra, envío y garantía.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">5. Programa de Afiliados de Amazon</h2>
                            <p>
                                CampingDeals España es participante del <strong className="text-white">Programa de Afiliados de Amazon EU</strong> (Amazon Associates). Como Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-white mb-3">6. Legislación aplicable</h2>
                            <p>
                                Este aviso legal se rige por la legislación española. Para cualquier controversia derivada del uso del sitio web, las partes se someten a los juzgados y tribunales de España.
                            </p>
                        </section>

                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
