'use client';

import { useEffect } from 'react';

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error('Application Error:', error);
    }, [error]);

    return (
        <div className="min-h-screen flex items-center justify-center px-4 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            <div className="text-center max-w-md">
                <span className="text-6xl mb-6 block">⚠️</span>
                <h2 className="text-2xl font-bold text-white mb-4">
                    Algo salió mal
                </h2>
                <p className="text-slate-400 mb-8">
                    Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo.
                </p>
                <button
                    onClick={reset}
                    className="px-6 py-3 rounded-xl bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold shadow-lg shadow-green-500/25 transition-all duration-300"
                >
                    Intentar de nuevo
                </button>
            </div>
        </div>
    );
}
