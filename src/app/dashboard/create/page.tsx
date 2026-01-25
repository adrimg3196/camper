"use client";

import { useState } from 'react';

export default function CreateCampaign() {
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [activeTab, setActiveTab] = useState('telegram');

    const handleGenerate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const res = await fetch('/api/marketing/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic, productUrl: 'https://amazon.es/dp/B00example' })
            });
            const data = await res.json();
            setResult(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold text-white mb-6">Crear Nueva Campaña</h1>

            {/* Input Form */}
            <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50 mb-8">
                <form onSubmit={handleGenerate} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-400 mb-2">Tema o Producto</label>
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Ej: Tienda de campaña 4 personas impermeable"
                            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading || !topic}
                        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                    >
                        {loading ? (
                            <>
                                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                Generando con IA...
                            </>
                        ) : (
                            'Generar Campaña Multicanal ✨'
                        )}
                    </button>
                </form>
            </div>

            {/* Results View */}
            {result && (
                <div className="animate-fade-in">
                    <div className="flex gap-4 mb-6 border-b border-slate-700 pb-1 overflow-x-auto">
                        <button
                            onClick={() => setActiveTab('telegram')}
                            className={`pb-3 px-2 text-sm font-medium transition-colors ${activeTab === 'telegram' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-slate-400 hover:text-white'}`}
                        >
                            Telegram
                        </button>
                        <button
                            onClick={() => setActiveTab('tiktok')}
                            className={`pb-3 px-2 text-sm font-medium transition-colors ${activeTab === 'tiktok' ? 'text-pink-400 border-b-2 border-pink-400' : 'text-slate-400 hover:text-white'}`}
                        >
                            TikTok Script
                        </button>
                        <button
                            onClick={() => setActiveTab('instagram')}
                            className={`pb-3 px-2 text-sm font-medium transition-colors ${activeTab === 'instagram' ? 'text-purple-400 border-b-2 border-purple-400' : 'text-slate-400 hover:text-white'}`}
                        >
                            Instagram
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Content Preview */}
                        <div className="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
                            <div className="bg-slate-900/50 p-4 border-b border-slate-700 flex justify-between items-center">
                                <span className="text-sm font-medium text-white">Preview de Contenido</span>
                                <button className="text-xs bg-slate-700 hover:bg-slate-600 text-white px-2 py-1 rounded transition-colors">Copiar</button>
                            </div>
                            <div className="p-6 whitespace-pre-wrap font-mono text-sm text-slate-300">
                                {activeTab === 'telegram' && result.telegram.content}
                                {activeTab === 'tiktok' && result.tiktok.script}
                                {activeTab === 'instagram' && result.instagram.caption}
                            </div>
                        </div>

                        {/* Visual/Image Preview */}
                        <div className="space-y-6">
                            <div className="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
                                <div className="bg-slate-900/50 p-4 border-b border-slate-700">
                                    <span className="text-sm font-medium text-white">Idea Visual (IA)</span>
                                </div>
                                {activeTab === 'tiktok' ? (
                                    <div className="p-6">
                                        <p className="text-sm text-yellow-400 mb-2">🎬 Ajustes Visuales:</p>
                                        <p className="text-slate-300 italic">{result.tiktok.visualSettings}</p>
                                    </div>
                                ) : (
                                    <div className="relative aspect-video">
                                        <img
                                            src={result.telegram.image}
                                            alt="Preview"
                                            className="w-full h-full object-cover"
                                        />
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
                                            <p className="text-xs text-white/80">Imagen sugerida para el post</p>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {activeTab === 'instagram' && (
                                <div className="bg-purple-500/10 border border-purple-500/20 p-4 rounded-xl">
                                    <p className="text-xs font-bold text-purple-400 mb-1">PROMPT PARA GENERADOR DE IMAGEN:</p>
                                    <p className="text-xs text-purple-200">{result.instagram.imagePrompt}</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
