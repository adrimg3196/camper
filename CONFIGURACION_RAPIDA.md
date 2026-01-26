# ⚡ Configuración Rápida de OpenRouter

## ✅ Ya está configurado para desarrollo local

He creado `.env.local` con tu API key. Para desarrollo local, ya está listo.

## 🚀 Para Producción en Vercel

Tienes **3 opciones**:

### Opción 1: Script Automático (Recomendado) ⚡

```bash
# 1. Instala Vercel CLI (si no lo tienes)
npm install -g vercel

# 2. Autentícate
vercel login

# 3. Ejecuta el script
./scripts/config-vercel-env.sh
```

### Opción 2: Manual con Vercel CLI

```bash
# Instala y autentica (si no lo has hecho)
npm install -g vercel
vercel login

# Configura la variable
vercel env add OPENROUTER_API_KEY production
# Cuando te pida el valor, pega: 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

# Repite para preview y development si quieres
vercel env add OPENROUTER_API_KEY preview
vercel env add OPENROUTER_API_KEY development

# Redespliega
vercel --prod
```

### Opción 3: Interfaz Web (Más fácil) 🌐

1. Ve a: https://vercel.com/dashboard
2. Selecciona tu proyecto
3. **Settings** → **Environment Variables**
4. **Add New**:
   - **Name**: `OPENROUTER_API_KEY`
   - **Value**: `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`
   - **Environments**: ✅ Production, ✅ Preview, ✅ Development
5. **Save**
6. Ve a **Deployments** → **Redeploy** del último deployment

## ✅ Verificar que Funciona

1. Ve a `/dashboard` en tu sitio
2. Verifica que "OpenRouter AI" aparezca en **verde** (Activo)
3. Prueba generar contenido desde el dashboard

## 📝 Notas

- ✅ `.env.local` ya está creado para desarrollo local
- ✅ El código ya está preparado para usar OpenRouter
- ⚠️ `.env.local` NO se sube a Git (está en .gitignore)
- 🔒 La API key en Vercel es segura (solo servidor)

---

**¿Prefieres usar la Opción 3 (interfaz web)? Es la más rápida y no requiere instalar nada.** 🚀
