#!/bin/bash

# Script para configurar variables de entorno en Vercel
# Requiere: Vercel CLI instalado y autenticado

echo "🔧 Configurando OpenRouter API Key en Vercel..."

# Verificar que Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI no está instalado."
    echo "📦 Instálalo con: npm install -g vercel"
    echo "🔐 Luego autentícate con: vercel login"
    exit 1
fi

# Verificar que está autenticado
if ! vercel whoami &> /dev/null; then
    echo "❌ No estás autenticado en Vercel."
    echo "🔐 Ejecuta: vercel login"
    exit 1
fi

# Configurar OpenRouter API Key
echo "📝 Añadiendo OPENROUTER_API_KEY..."

vercel env add OPENROUTER_API_KEY production <<EOF
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
EOF

vercel env add OPENROUTER_API_KEY preview <<EOF
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
EOF

vercel env add OPENROUTER_API_KEY development <<EOF
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
EOF

echo "✅ Variables de entorno configuradas!"
echo "🚀 Redespliega tu proyecto para aplicar los cambios:"
echo "   vercel --prod"
echo ""
echo "📊 O ve a Vercel Dashboard y haz 'Redeploy' del último deployment"
