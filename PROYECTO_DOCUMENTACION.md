# Camper Deals Bot - Documentacion Completa

## Resumen del Proyecto

Bot automatizado que busca ofertas de productos de camping en Amazon.es, genera videos profesionales con IA y los publica automaticamente en TikTok (@camperoutlet). El sistema corre de forma gratuita en GitHub Actions cada 6 horas.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GITHUB ACTIONS (Gratis)                               │
│                    Ejecuta cada 6 horas automaticamente                      │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PIPELINE                                        │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐│
│  │   SCRAPER    │───▶│   ENHANCER   │───▶│    VIDEO     │───▶│  UPLOADER  ││
│  │   Amazon     │    │   Gemini AI  │    │  Generator   │    │   TikTok   ││
│  └──────────────┘    └──────────────┘    └──────────────┘    └────────────┘│
│                                                                              │
│  Busca ofertas      Mejora titulos y    Genera video con    Publica via    │
│  de camping         descripciones       animacion AI        API interna    │
│                     con marketing                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Servicios y APIs

### 1. Supabase (Base de Datos)

**Proposito:** Almacenar historial de ofertas publicadas.

| Variable | Descripcion |
|----------|-------------|
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | API key (anon/public) |

**Configuracion:**
- Crear proyecto en https://supabase.com
- Crear tabla `deals` con campos: title, price, original_price, discount, image_url, category, marketing_title, marketing_description

---

### 2. Google AI (Gemini)

**Proposito:** Mejorar titulos y descripciones con IA para marketing.

| Variable | Descripcion |
|----------|-------------|
| `GOOGLE_AI_API_KEY` | API key de Google AI Studio |

**Modelo usado:** `gemini-2.0-flash`

**Obtener API Key:**
1. Ir a https://aistudio.google.com/
2. Click en "Get API Key"
3. Crear nueva key o usar existente

**Uso en el proyecto:**
- Genera titulos de marketing atractivos
- Crea descripciones persuasivas
- Sugiere hashtags relevantes

---

### 3. HuggingFace (IA Alternativa - Gratis)

**Proposito:** Alternativa gratuita a Google AI para generar contenido.

| Variable | Descripcion |
|----------|-------------|
| `HUGGINGFACE_API_KEY` | Token de acceso HuggingFace |
| `HUGGINGFACE_MODEL` | Modelo a usar (default: `HuggingFaceH4/zephyr-7b-beta`) |

**Obtener Token:**
1. Ir a https://huggingface.co/settings/tokens
2. Crear nuevo token con permisos de lectura

---

### 3.5. LangExtract (Extraccion Estructurada - Opcional)

**Proposito:** Extrae senales semanticas de los productos (resumen, keywords, entidades).

| Variable | Descripcion |
|----------|-------------|
| `ENABLE_LANGEXTRACT` | `true` para activar, `false` para desactivar |
| `LANGEXTRACT_MODEL_ID` | Modelo a usar (default: `gemini-2.5-flash`) |
| `LANGEXTRACT_API_KEY` | API key (usa GOOGLE_AI_API_KEY si no se especifica) |

**Que hace:**
- Genera un resumen estructurado del producto
- Extrae keywords semanticas (ej: "camping", "impermeabilidad", "ligero")
- Identifica entidades (marcas, materiales, etc.)
- Esta informacion mejora los prompts de marketing

---

### 4. Amazon Associates (Afiliados)

**Proposito:** Generar URLs de afiliado para monetizacion.

| Variable | Descripcion |
|----------|-------------|
| `AMAZON_PARTNER_TAG` | Tag de afiliado (ej: `camperdeals-21`) |
| `AMAZON_BASE_URL` | URL base (default: `https://www.amazon.es`) |

**Configuracion:**
1. Registrarse en https://afiliados.amazon.es
2. Obtener tu Partner Tag del dashboard

---

### 5. TikTok (Publicacion)

**Proposito:** Autenticacion para publicar videos automaticamente.

| Variable | Descripcion |
|----------|-------------|
| `TIKTOK_COOKIES_JSON` | JSON con cookies de sesion de TikTok |

**Como obtener las cookies:**

1. Instalar extension "EditThisCookie" en Chrome
2. Ir a https://www.tiktok.com e iniciar sesion
3. Click en el icono de EditThisCookie
4. Exportar cookies como JSON
5. Guardar el JSON completo como secret en GitHub

**Cookies importantes:**
- `sessionid` - Identificador de sesion (obligatorio)
- `msToken` - Token de seguridad
- `tt_chain_token` - Token de cadena

**Renovacion:**
Las cookies expiran cada ~30 dias. Debes re-exportarlas cuando el bot falle con "sesion invalida".

---

### 6. Replicate (Video AI - Recomendado)

**Proposito:** Genera videos animados profesionales donde el producto cobra vida.

| Variable | Descripcion |
|----------|-------------|
| `REPLICATE_API_TOKEN` | Token de API de Replicate |

**Modelos disponibles:**
| Modelo | ID | Costo | Descripcion |
|--------|----|----|-------------|
| Wan Fast | `wan-video/wan-2.5-i2v-480p` | ~$0.05/video | Rapido y economico |
| Hailuo | `minimax/video-01` | ~$0.50/video | Alta calidad |
| SVD | `stability-ai/stable-video-diffusion` | ~$0.18/video | Clasico |

**Obtener Token:**
1. Ir a https://replicate.com
2. Click en tu perfil > API tokens
3. Copiar el token

**Como funciona:**
1. Toma la imagen del producto
2. La anima con movimiento fluido (zoom, rotacion)
3. Genera audio TTS con dialogo persuasivo
4. Combina video + audio con FFmpeg

---

### 7. Runway ML (Video AI - Alternativa)

**Proposito:** Alternativa premium para videos animados 3D.

| Variable | Descripcion |
|----------|-------------|
| `RUNWAY_API_KEY` | API key de Runway ML |
| `ENABLE_RUNWAY` | `true` para activar, `false` para desactivar |

**Endpoint:** `https://api.dev.runwayml.com`

**Obtener API Key:**
1. Ir a https://dev.runwayml.com
2. Crear cuenta/iniciar sesion
3. Ir a Settings > API Keys
4. Crear nueva key

**Nota:** Requiere creditos en la cuenta. El bot usa Gen-4 Turbo.

---

### 8. HuggingFace Spaces (Video AI - Gratis)

**Proposito:** Genera videos con Stable Video Diffusion de forma gratuita.

**No requiere API key adicional** - Usa los Spaces publicos de HuggingFace.

**Limitaciones:**
- Los Spaces pueden estar ocupados/no disponibles
- Velocidad variable segun demanda
- Se usa como fallback si Replicate falla

---

## Generadores de Video (Prioridad)

El sistema intenta generar el video en este orden:

```
1. SadTalker (GRATIS)       ─── Producto que HABLA ───▶
2. Wan Animate (GRATIS)     ─── Producto GESTICULANDO ───▶
3. Replicate (wan-fast)     ─── Rotacion profesional ───▶
4. HuggingFace SVD          ─── Rotacion simple ───▶
5. Runway ML                ─── 3D premium ───▶
6. Remotion (siempre OK)    ◀── Fallback garantizado 2D
```

### SadTalker (GRATIS - Producto que habla)

**HuggingFace Space:** `vinthony/SadTalker`

Anima la imagen del producto para que parezca que "habla" sincronizado con audio TTS.

| Variable | Descripcion |
|----------|-------------|
| `ENABLE_SADTALKER` | `true` (default) / `false` |

**Como funciona:**
1. Genera audio TTS con dialogo persuasivo
2. Sube imagen + audio a HuggingFace Space
3. SadTalker anima la imagen sincronizada con el audio
4. Descarga video resultado

---

### Wan2.2 Animate (GRATIS - Producto gesticulando)

**HuggingFace Space:** `Wan-AI/Wan2.2-Animate`

Hace que el producto se mueva con gestos humanos extraidos de videos plantilla.

| Variable | Descripcion |
|----------|-------------|
| `ENABLE_WAN_ANIMATE` | `true` (default) / `false` |

**Gestos disponibles:**
- `excited` - Saltos de emocion (cocina, mochilas)
- `presenting` - Presentando producto (iluminacion, dormir)
- `waving` - Saludo amigable (hidratacion)

**Como funciona:**
1. Selecciona gesto segun categoria del producto
2. Descarga video plantilla de HuggingFace
3. Wan Animate transfiere movimiento a la imagen
4. Combina con audio TTS via FFmpeg

### Remotion (Fallback Garantizado)

Proyecto Node.js/React que genera videos 2D profesionales:
- Animaciones con spring()
- Tipografia moderna
- Gradientes segun categoria
- Audio TTS integrado

**Ubicacion:** `/video/`

**Dependencias:**
```json
{
  "@remotion/cli": "4.0.242",
  "@remotion/google-fonts": "4.0.242",
  "@remotion/tailwind": "4.0.242",
  "react": "18.3.1",
  "remotion": "4.0.242",
  "zod": "^3.22.0"
}
```

---

## Estructura de Archivos

```
camper/
├── .github/
│   └── workflows/
│       └── daily_bot.yml       # GitHub Actions workflow
├── backend/
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuracion centralizada
│   ├── requirements.txt        # Dependencias Python
│   ├── scraper/
│   │   └── amazon.py           # Scraper de Amazon
│   ├── database/
│   │   └── client.py           # Cliente Supabase
│   ├── content/
│   │   └── enhancer.py         # Mejora con IA (Gemini/HF)
│   └── social/
│       ├── manager.py          # Orquestador de video y publicacion
│       ├── uploader.py         # TikTok API uploader
│       ├── replicate_generator.py  # Replicate video AI
│       ├── ai_video_generator.py   # HuggingFace SVD
│       ├── runway_generator.py     # Runway ML
│       ├── tts_service.py      # Text-to-Speech
│       └── dialogue_generator.py   # Genera dialogos con IA
└── video/                      # Proyecto Remotion
    ├── package.json
    ├── remotion.config.ts
    ├── src/
    │   ├── Root.tsx            # Composicion principal
    │   ├── components/         # Componentes React
    │   └── lib/                # Utilidades
    └── public/
        └── silence.mp3         # Audio base
```

---

## GitHub Actions Workflow

**Archivo:** `.github/workflows/daily_bot.yml`

**Horario:** Cada 6 horas (06:00, 12:00, 18:00, 00:00 UTC)

**Secrets necesarios:**
```yaml
SUPABASE_URL
SUPABASE_KEY
GOOGLE_AI_API_KEY
HUGGINGFACE_API_KEY
HUGGINGFACE_MODEL
AMAZON_PARTNER_TAG
TIKTOK_COOKIES_JSON
REPLICATE_API_TOKEN
RUNWAY_API_KEY        # Opcional
ENABLE_RUNWAY         # Opcional (default: false)
```

**Configurar secrets:**
1. Ir a tu repo en GitHub
2. Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Agregar cada secret con su valor

---

## Dependencias Python

**Archivo:** `backend/requirements.txt`

```
requests==2.31.0
requests-auth-aws-sigv4==0.7.0
beautifulsoup4==4.12.3
python-dotenv==1.0.1
fake-useragent==1.4.0
schedule==1.2.1
edge-tts==6.1.19
gTTS==2.5.1
Pillow==10.2.0
gradio_client==1.5.3
replicate==0.25.1
```

---

## Flujo de Ejecucion

```
1. GitHub Actions dispara el workflow (cron o manual)
   │
2. Setup: Python 3.11 + Node.js 20
   │
3. Instala dependencias (pip + npm en paralelo)
   │
4. Ejecuta main.py
   │
   ├── AmazonScraper.search_deals()
   │   └── Selecciona 2 productos aleatorios del catalogo
   │
   ├── ContentEnhancer.enhance_product()
   │   └── Gemini genera titulo y descripcion de marketing
   │
   ├── SocialManager.process_deal()
   │   │
   │   ├── Intenta Replicate ────┐
   │   │   └── Si falla         │
   │   ├── Intenta HuggingFace ─┤
   │   │   └── Si falla         │
   │   ├── Intenta Runway ──────┤
   │   │   └── Si falla         │
   │   └── Usa Remotion ────────┘ (siempre funciona)
   │
   └── TikTokUploader.upload_video()
       └── Publica en @camperoutlet
```

---

## Ejecucion Local

### Requisitos
- Python 3.11+
- Node.js 20+
- FFmpeg (para combinar video+audio)

### Setup

```bash
# 1. Clonar repo
git clone https://github.com/adrimg3196/camper.git
cd camper

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 3. Instalar dependencias Python
pip install -r backend/requirements.txt

# 4. Instalar dependencias Node.js
cd video && npm install && cd ..

# 5. Ejecutar
python backend/main.py
```

### Variables de entorno (.env)

```env
# Base de datos
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# IA para contenido
GOOGLE_AI_API_KEY=AIza...
HUGGINGFACE_API_KEY=hf_...
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta

# Amazon
AMAZON_PARTNER_TAG=camperdeals-21

# TikTok (JSON completo de cookies)
TIKTOK_COOKIES_JSON='[{"name":"sessionid","value":"..."},...]'

# Video AI
REPLICATE_API_TOKEN=r8_...
RUNWAY_API_KEY=key_...
ENABLE_RUNWAY=false
```

---

## Troubleshooting

### "sesion invalida" en TikTok
Las cookies han expirado. Re-exportalas desde el navegador.

### "No se pudo conectar a HuggingFace"
Los Spaces estan ocupados. El sistema usara Remotion automaticamente.

### "You do not have enough credits" (Runway)
Tu cuenta de Runway no tiene creditos. Desactiva Runway o compra creditos.

### Video muy pequeno (<10KB)
Hubo un error en la generacion. Revisa los logs para ver cual generador fallo.

### Remotion falla
Verifica que Node.js 20 esta instalado y que `npm install` se ejecuto en `/video/`.

---

## Costos Estimados

| Servicio | Costo | Notas |
|----------|-------|-------|
| GitHub Actions | **GRATIS** | Repos publicos ilimitados |
| Supabase | **GRATIS** | Tier gratuito: 500MB |
| Google AI (Gemini) | **GRATIS** | 60 requests/minuto gratis |
| HuggingFace | **GRATIS** | API inference gratuita |
| **SadTalker** | **GRATIS** | HuggingFace Space |
| **Wan Animate** | **GRATIS** | HuggingFace Space |
| Replicate | ~$0.05-0.50/video | Wan Fast es el mas economico |
| Runway ML | ~$0.05/segundo | Requiere creditos |

**Estimacion mensual con SadTalker/Wan (GRATIS):**
- 4 ejecuciones/dia × 2 videos × 30 dias = 240 videos
- 240 × $0.00 = **$0/mes**

**Con Remotion (fallback):**
- **$0/mes** (100% gratuito)

---

## Contacto y Soporte

- **Repositorio:** https://github.com/adrimg3196/camper
- **TikTok:** @camperoutlet

---

*Documentacion generada automaticamente - Febrero 2026*
