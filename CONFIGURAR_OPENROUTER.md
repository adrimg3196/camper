# ⚡ Configurar OpenRouter API Key

## ✅ Tu API Key está lista

Tu API Key de OpenRouter:
```
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
```

## 📝 Pasos para Configurar en Vercel

### 1. Ve a tu proyecto en Vercel
- URL: https://vercel.com/dashboard
- Selecciona el proyecto "camper" o "quizzical-ptolemy"

### 2. Añade la Variable de Entorno
1. Ve a **Settings** → **Environment Variables**
2. Haz clic en **Add New**
3. Añade:
   - **Name**: `OPENROUTER_API_KEY`
   - **Value**: `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`
   - **Environments**: Selecciona todas (Production, Preview, Development)

### 3. Guarda y Redespliega
- Guarda los cambios
- Ve a **Deployments**
- Haz clic en los 3 puntos del último deployment → **Redeploy**
- O simplemente haz un push a main (auto-deploy)

## ✅ Verificar que Funciona

### Opción 1: Desde el Dashboard
1. Ve a `/dashboard`
2. Haz clic en "Ejecutar Scraper" o "Publicar Ahora"
3. Revisa los logs en Vercel → Functions

### Opción 2: Probar API Directamente
```bash
curl -X POST https://camper-omega.vercel.app/api/marketing/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Tienda de Campaña Coleman 4 Personas",
    "productUrl": "https://amazon.es/dp/B09SAMPLE01",
    "productData": {
      "price": 89.99,
      "originalPrice": 149.99,
      "discount": 40
    }
  }'
```

### Opción 3: Ver Logs en Vercel
1. Ve a Vercel → Tu Proyecto → **Functions**
2. Busca `/api/marketing/generate`
3. Revisa los logs para ver si usa OpenRouter

## 🎯 ¿Qué Modelos se Usarán?

El sistema usa automáticamente los mejores modelos según la tarea:

- **Marketing Premium**: `anthropic/claude-3-opus` (mejor calidad)
- **SEO Content**: `anthropic/claude-3-opus` (optimizado para SEO)
- **TikTok Shop**: `openai/gpt-4-turbo-preview` (creativo)
- **Balanceado**: `anthropic/claude-3-sonnet` (calidad/precio)

## 💡 Ventajas de OpenRouter

✅ **Múltiples IAs**: GPT-4, Claude, Gemini, Llama  
✅ **Mejor calidad**: Contenido más persuasivo y optimizado  
✅ **Fallback automático**: Si falla, usa Gemini  
✅ **Coste eficiente**: Solo pagas por lo que usas  

## 🔒 Seguridad

⚠️ **IMPORTANTE**: 
- La API key está configurada en Vercel (seguro)
- NO está en el código (no se puede ver en GitHub)
- Solo se usa en el servidor (nunca en el cliente)

## 📊 Monitoreo de Uso

Puedes ver tu uso en:
- https://openrouter.ai/activity
- Revisa cuántos tokens usas
- Ajusta modelos si necesitas ahorrar

---

**¡Listo!** Una vez configurado, el sistema usará automáticamente OpenRouter para generar contenido de máxima calidad. 🚀
