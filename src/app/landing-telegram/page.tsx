'use client';

import { useState } from 'react';

/**
 * Landing Page optimizada para captación masiva de suscriptores de Telegram
 * Incluye: Giveaway, incentivos, social proof, optimización de conversión
 */
export default function TelegramLandingPage() {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch('/api/telegram/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email,
                    name,
                    source: 'landing',
                    utm_source: typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('utm_source') : null,
                    utm_campaign: typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('utm_campaign') : null,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error al procesar');
            }

            setSuccess(true);
            setEmail('');
            setName('');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error desconocido');
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-green-900 via-green-800 to-emerald-900 flex items-center justify-center p-4">
                <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 max-w-2xl w-full text-center border border-white/20">
                    <div className="text-6xl mb-6">🎉</div>
                    <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
                        ¡Bienvenido a CampingDeals!
                    </h1>
                    <p className="text-green-100 text-lg mb-8">
                        Revisa tu email para recibir el enlace al canal de Telegram
                    </p>
                    <div className="bg-white/10 rounded-xl p-6 mb-6">
                        <p className="text-white font-medium mb-2">Próximos pasos:</p>
                        <ul className="text-green-100 text-left space-y-2">
                            <li>✅ Únete a nuestro canal de Telegram</li>
                            <li>✅ Recibe ofertas exclusivas diarias</li>
                            <li>✅ Participa en giveaways semanales</li>
                            <li>✅ Acceso anticipado a las mejores ofertas</li>
                        </ul>
                    </div>
                    <a
                        href="https://t.me/camper_deals_bot"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-xl transition-colors"
                    >
                        Ir a Telegram →
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
            {/* Hero Section */}
            <div className="container mx-auto px-4 py-16">
                <div className="max-w-4xl mx-auto text-center mb-12">
                    <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
                        🏕️ Únete a las Mejores Ofertas de Camping
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-300 mb-4">
                        Recibe ofertas exclusivas con +30% de descuento
                    </p>
                    <p className="text-lg text-slate-400">
                        Más de 10,000 campistas ya se benefician de nuestras ofertas diarias
                    </p>
                </div>

                {/* Form Section */}
                <div className="max-w-2xl mx-auto bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 border border-white/20">
                    <div className="text-center mb-8">
                        <h2 className="text-3xl font-bold text-white mb-4">
                            🎁 Gana un Kit de Camping Premium
                        </h2>
                        <p className="text-slate-300">
                            Suscríbete ahora y participa en nuestro sorteo semanal
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <input
                                type="text"
                                placeholder="Tu nombre"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full px-4 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        <div>
                            <input
                                type="email"
                                placeholder="tu@email.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        {error && (
                            <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 text-red-200">
                                {error}
                            </div>
                        )}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600 text-white font-bold py-4 px-8 rounded-xl transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Procesando...' : '🎁 Quiero las Ofertas + Participar en el Sorteo'}
                        </button>
                    </form>

                    {/* Social Proof */}
                    <div className="mt-8 pt-8 border-t border-white/20">
                        <div className="grid grid-cols-3 gap-4 text-center">
                            <div>
                                <div className="text-3xl font-bold text-white">10K+</div>
                                <div className="text-slate-400 text-sm">Suscriptores</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-white">500+</div>
                                <div className="text-slate-400 text-sm">Ofertas/mes</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-white">€50K+</div>
                                <div className="text-slate-400 text-sm">Ahorrados</div>
                            </div>
                        </div>
                    </div>

                    {/* Benefits */}
                    <div className="mt-8 space-y-4">
                        <h3 className="text-xl font-bold text-white mb-4">✨ Lo que recibirás:</h3>
                        <div className="space-y-3 text-slate-300">
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">🔥</span>
                                <div>
                                    <strong className="text-white">Ofertas exclusivas diarias</strong>
                                    <p className="text-sm">Las mejores ofertas con +30% descuento</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">⚡</span>
                                <div>
                                    <strong className="text-white">Notificaciones instantáneas</strong>
                                    <p className="text-sm">Sé el primero en conocer las ofertas flash</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">🎁</span>
                                <div>
                                    <strong className="text-white">Giveaways semanales</strong>
                                    <p className="text-sm">Participa en sorteos de equipamiento premium</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">💬</span>
                                <div>
                                    <strong className="text-white">Comunidad activa</strong>
                                    <p className="text-sm">Comparte experiencias con otros campistas</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Trust Badges */}
                <div className="max-w-4xl mx-auto mt-12 text-center">
                    <p className="text-slate-400 mb-4">Confían en nosotros:</p>
                    <div className="flex flex-wrap justify-center gap-8 items-center opacity-60">
                        <div className="text-slate-300 font-semibold">Amazon Affiliate</div>
                        <div className="text-slate-300 font-semibold">✓ Verificado</div>
                        <div className="text-slate-300 font-semibold">🔒 100% Seguro</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
