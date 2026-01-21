# 🏕️ Camper Deals - Documento de Traspaso Completo

> **Proyecto:** Sistema automatizado de ofertas de camping con web, automatización de contenido y publicación en redes sociales.
> **Última actualización:** Enero 2026
> **Estado:** ✅ Frontend en producción | 🔧 Backend local funcional

---

## 📋 Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Configuración de Entorno](#configuración-de-entorno)
6. [Frontend (Next.js)](#frontend-nextjs)
7. [Backend (Python)](#backend-python)
8. [Base de Datos (Supabase)](#base-de-datos-supabase)
9. [Automatización de Redes Sociales](#automatización-de-redes-sociales)
10. [Deployment](#deployment)
11. [Problemas Resueltos](#problemas-resueltos)
12. [Troubleshooting](#troubleshooting)
13. [Próximos Pasos](#próximos-pasos)
14. [Comandos Útiles](#comandos-útiles)

---

## Resumen Ejecutivo

**Camper Deals** es una plataforma de marketing de afiliados de Amazon especializada en productos de camping y outdoor. El sistema:

- **Scraping automatizado** de ofertas de Amazon España con +30% descuento
- **Enriquecimiento con IA** (HuggingFace) para generar títulos y descripciones de marketing
- **Web moderna** desplegada en Vercel que muestra las ofertas en tiempo real
- **Publicación automática** en TikTok mediante Selenium
- **Canal de Telegram** para notificaciones de ofertas

### URLs Importantes

| Servicio | URL |
|----------|-----|
| Web (Producción) | https://camper-omega.vercel.app |
| Supabase Dashboard | https://supabase.com/dashboard |
| Amazon Associates | https://afiliados.amazon.es |
| Telegram Canal | @camperdeals |
| TikTok | @camperdeals |

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FLUJO DE DATOS                                │
└─────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
     │   AMAZON.ES  │         │  HUGGINGFACE │         │   SUPABASE   │
     │   (Scraping) │         │     (IA)     │         │ (PostgreSQL) │
     └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
            │                        │                        │
            │ 1. Buscar ofertas      │                        │
            ▼                        │                        │
     ┌──────────────┐               │                        │
     │   BACKEND    │───────────────┘                        │
     │   (Python)   │ 2. Enriquecer con IA                   │
     │              │────────────────────────────────────────┘
     └──────┬───────┘ 3. Guardar en DB
            │
            │ 4. Publicar en redes
            ▼
     ┌──────────────┐         ┌──────────────┐
     │    TIKTOK    │         │   TELEGRAM   │
     │  (Selenium)  │         │    (API)     │
     └──────────────┘         └──────────────┘

            │
            │ 5. Usuario visita web
            ▼
     ┌──────────────┐         ┌──────────────┐
     │   VERCEL     │◄────────│    USUARIO   │
     │  (Next.js)   │         │              │
     └──────────────┘         └──────────────┘
            │
            │ 6. Click en oferta
            ▼
     ┌──────────────┐
     │ AMAZON.ES +  │
     │ AFFILIATE    │
     │    TAG       │
     └──────────────┘
```

---

## Estructura del Proyecto

```
camper/
├── 📁 src/                          # Frontend Next.js
│   ├── app/
│   │   ├── layout.tsx               # Layout principal
│   │   ├── page.tsx                 # Homepage con SSR
│   │   ├── robots.ts                # SEO robots
│   │   ├── sitemap.ts               # SEO sitemap
│   │   └── ofertas/[slug]/page.tsx  # Páginas de categoría
│   ├── components/
│   │   ├── Header.tsx               # Navegación superior
│   │   ├── Footer.tsx               # Pie con disclosure afiliados
│   │   ├── ProductCard.tsx          # Tarjeta de producto (crítico)
│   │   ├── CategoryFilter.tsx       # Filtro de categorías
│   │   └── StatCard.tsx             # Tarjetas de estadísticas
│   └── lib/
│       ├── deals.ts                 # Fetch de ofertas (Supabase/Mock)
│       ├── supabase.ts              # Cliente Supabase
│       └── types.ts                 # TypeScript interfaces
│
├── 📁 backend/                      # Backend Python
│   ├── main.py                      # Orquestador principal
│   ├── requirements.txt             # Dependencias Python
│   ├── schema.sql                   # Schema de Supabase
│   ├── .env                         # Variables de entorno (NO commitear)
│   ├── .env.example                 # Plantilla de variables
│   ├── scraper/
│   │   └── amazon.py                # Scraper de Amazon (con mock fallback)
│   ├── content/
│   │   └── enhancer.py              # Enriquecimiento con HuggingFace
│   ├── database/
│   │   └── client.py                # Cliente REST de Supabase
│   ├── social/
│   │   ├── manager.py               # Gestor de publicaciones
│   │   └── uploader.py              # Selenium TikTok uploader
│   └── tiktok_profile/              # Perfil Chrome persistente para TikTok
│
├── 📁 scripts/                      # Scripts auxiliares
│   ├── fetch_deals.py               # Fetch manual de ofertas
│   └── telegram_bot.py              # Bot de Telegram
│
├── 📁 data/                         # Datos locales
│   └── deals.json                   # Cache local de ofertas
│
├── 📄 next.config.js                # Configuración Next.js (imágenes Amazon)
├── 📄 tailwind.config.js            # Estilos Tailwind
├── 📄 package.json                  # Dependencias Node.js
└── 📄 tsconfig.json                 # Configuración TypeScript
```

---

## Stack Tecnológico

### Frontend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| Next.js | 14.2.3 | Framework React con SSR |
| React | 18.2.0 | UI Components |
| TypeScript | 5.3.3 | Type safety |
| Tailwind CSS | 3.4.1 | Estilos utility-first |
| Supabase SDK | 2.91.0 | Cliente de base de datos |

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Runtime |
| Selenium | 4.18.1 | Automatización browser |
| Requests | 2.31.0 | HTTP requests |
| BeautifulSoup4 | 4.12.3 | HTML parsing |
| Schedule | 1.2.1 | Cron jobs en Python |
| python-dotenv | 1.0.1 | Variables de entorno |

### Infraestructura
| Servicio | Uso |
|----------|-----|
| Vercel | Hosting frontend (gratis) |
| Supabase | PostgreSQL + API REST (gratis tier) |
| HuggingFace | IA para contenido (gratis tier) |
| Chrome | Browser para TikTok automation |

---

## Configuración de Entorno

### Variables de Entorno Frontend (Vercel)

```bash
# En Vercel Dashboard → Settings → Environment Variables

NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
NEXT_PUBLIC_AMAZON_PARTNER_TAG=camperdeals07-21
```

### Variables de Entorno Backend (`backend/.env`)

```bash
# Base de Datos
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbG...  # ⚠️ Usar SERVICE_ROLE key, no anon key

# IA (HuggingFace - Gratis)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta

# Amazon (Opcional para API)
AMAZON_PARTNER_TAG=camperdeals07-21

# Telegram (Opcional)
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHANNEL_ID=@camperdeals
```

### Obtener las Keys

1. **Supabase:**
   - Dashboard → Settings → API
   - `anon key` para frontend, `service_role` para backend

2. **HuggingFace:**
   - https://huggingface.co/settings/tokens
   - Crear token con permisos de lectura

3. **Telegram:**
   - Hablar con @BotFather
   - `/newbot` → copiar token

---

## Frontend (Next.js)

### Archivos Críticos

#### `src/lib/deals.ts`
```typescript
// Flujo de datos:
// 1. Intenta conectar a Supabase
// 2. Si falla o está vacío → usa MOCK_PRODUCTS
// 3. Mapea datos de DB a interface Product
```

**Importante:** Contiene logs de debug (`[PROD DEBUG]`) útiles para diagnosticar problemas en Vercel.

#### `src/components/ProductCard.tsx`
```typescript
// Inyección automática del tag de afiliado
let finalUrl = product.affiliate_url || product.url;
if (finalUrl.includes('amazon.es') && !finalUrl.includes('tag=')) {
    const connector = finalUrl.includes('?') ? '&' : '?';
    finalUrl = `${finalUrl}${connector}tag=${partnerTag}`;
}
```

#### `src/app/page.tsx`
```typescript
// Configuración SSR crítica
export const dynamic = 'force-dynamic';  // ⚠️ No cambiar
export const revalidate = 0;
```

Sin esto, Vercel cachea la página en build time y nunca muestra datos reales de Supabase.

#### `next.config.js`
```javascript
// Configuración de imágenes de Amazon
images: {
    remotePatterns: [
        { hostname: 'm.media-amazon.com' },
        { hostname: 'images-na.ssl-images-amazon.com' },
        // ... más dominios de Amazon
    ],
    unoptimized: true,  // ⚠️ Necesario para evitar errores de optimización
},
```

---

## Backend (Python)

### Flujo de Ejecución (`backend/main.py`)

```python
def job():
    # 1. Scraper busca ofertas (mock o real)
    deals = scraper.search_deals()

    # 2. Por cada oferta:
    for deal in deals:
        # 2a. IA mejora título/descripción
        enhanced_deal = enhancer.enhance_product(deal)

        # 2b. Guarda en Supabase
        db.save_deal(enhanced_deal)

        # 2c. Publica en TikTok
        social.process_deal(enhanced_deal)

# Ejecución cada 6 horas
schedule.every(6).hours.do(job)
```

### Scraper (`backend/scraper/amazon.py`)

El scraper tiene dos modos:

1. **Modo Real (comentado):** Hace requests a Amazon
   - Requiere proxies residenciales para evitar bloqueos
   - Amazon detecta y bloquea scraping agresivamente

2. **Modo Mock (activo):** Devuelve ofertas hardcodeadas
   - Útil para desarrollo y demo
   - Los productos mock son reales (URLs y ASINs válidos)

```python
# Para activar modo real, descomentar en amazon.py:
# response = requests.get(search_url, headers=self.get_headers(), timeout=10)
# if response.status_code == 200:
#     return self.parse_results(response.content)
```

### Enriquecedor de Contenido (`backend/content/enhancer.py`)

Usa HuggingFace Inference API (gratis) para generar:
- `marketing_title`: Título corto y llamativo
- `marketing_description`: Copy persuasivo
- Tags y hashtags

**Modelos recomendados (gratis):**
- `HuggingFaceH4/zephyr-7b-beta`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `google/gemma-7b-it`

### TikTok Uploader (`backend/social/uploader.py`)

**Funcionamiento:**
1. Abre Chrome con perfil persistente
2. Navega a tiktok.com/upload
3. Si no hay sesión → espera login manual (60s)
4. Sube video mediante input[type=file]
5. Espera confirmación manual de publicación

**Perfil de Chrome:**
```
backend/tiktok_profile/
```
Este directorio mantiene las cookies de sesión de TikTok.

**Primera ejecución:**
1. El bot abre Chrome
2. Login manual en TikTok
3. Las cookies se guardan en el perfil
4. Siguientes ejecuciones ya tienen sesión

---

## Base de Datos (Supabase)

### Schema (`backend/schema.sql`)

```sql
CREATE TABLE public.deals (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Producto
  title TEXT NOT NULL,
  marketing_title TEXT,
  marketing_description TEXT,
  description TEXT,

  -- Precios
  price DECIMAL(10,2) NOT NULL,
  original_price DECIMAL(10,2),
  discount INTEGER,

  -- Metadatos
  category TEXT NOT NULL,
  image_url TEXT NOT NULL,
  url TEXT NOT NULL,
  affiliate_url TEXT,

  -- Estado
  is_active BOOLEAN DEFAULT TRUE,
  rating DECIMAL(3,1) DEFAULT 4.5,
  review_count INTEGER DEFAULT 0
);

-- RLS habilitado
-- Lectura pública, escritura solo con service_role key
```

### Crear tabla en Supabase

1. Dashboard → SQL Editor
2. Pegar contenido de `backend/schema.sql`
3. Ejecutar

---

## Automatización de Redes Sociales

### TikTok

**Estado:** Funcional con supervisión manual

El uploader de Selenium:
- Sube el video automáticamente
- **NO** publica automáticamente (anti-ban)
- Requiere click manual en "Publicar"

**Por qué no es 100% automático:**
- TikTok detecta bots y banea cuentas
- Los selectores CSS cambian frecuentemente
- El click manual evita detección

### Telegram

**Estado:** Preparado, requiere configuración

```bash
# Ejecutar bot
cd scripts
python telegram_bot.py --publish-new

# Test sin publicar
python telegram_bot.py --test
```

**Dependencia extra:**
```bash
pip install python-telegram-bot
```

---

## Deployment

### Frontend (Vercel)

```bash
# Conectar repo a Vercel
vercel link

# Deploy manual
vercel --prod

# O simplemente push a main → auto-deploy
git push origin main
```

**Checklist pre-deploy:**
- [ ] Variables de entorno configuradas en Vercel
- [ ] `force-dynamic` en page.tsx
- [ ] `unoptimized: true` en next.config.js

### Backend (Local → VPS)

**Actualmente:** Corre localmente con `python main.py`

**Recomendación para producción:**
1. Oracle Cloud Free Tier (VM gratis)
2. Railway.app (fácil deploy Python)
3. Fly.io (tiene tier gratis)

**Docker (opcional):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

## Problemas Resueltos

### 1. Página en blanco en Vercel
**Causa:** Next.js cacheaba página sin datos en build time
**Solución:** `export const dynamic = 'force-dynamic'` en page.tsx

### 2. Imágenes de Amazon no cargan
**Causa:** Next.js Image optimization bloqueaba dominios externos
**Solución:** `remotePatterns` permisivos + `unoptimized: true`

### 3. Tag de afiliado no se añadía
**Causa:** URLs de DB no tenían tag
**Solución:** Inyección dinámica en ProductCard.tsx

### 4. Error `better-sqlite3` en Vercel
**Causa:** Dependencia nativa incompatible con serverless
**Solución:** Eliminar dependencia (usamos Supabase, no SQLite)

### 5. TikTok `input()` bloqueante
**Causa:** Script esperaba input de teclado
**Solución:** Eliminar input(), usar timeouts y logs

### 6. ChromeDriver path incorrecto en Mac ARM
**Causa:** webdriver-manager detectaba archivo incorrecto
**Solución:** Corrección de path en uploader.py

---

## Troubleshooting

### Frontend

**Problema:** Web muestra datos mock en lugar de DB
**Diagnóstico:**
1. Ver logs en Vercel → Functions
2. Buscar `[PROD DEBUG]`
3. Verificar variables de entorno

**Problema:** Imágenes rotas
**Solución:**
1. Verificar URL de imagen en DB
2. Añadir dominio a `next.config.js` si es nuevo
3. Clear cache: `vercel --force`

### Backend

**Problema:** `ChromeDriver not found`
```bash
# Limpiar cache de webdriver-manager
rm -rf ~/.wdm
# Reinstalar
pip install --upgrade webdriver-manager
```

**Problema:** TikTok pide login constantemente
**Solución:**
1. Borrar `backend/tiktok_profile/SingletonLock`
2. Ejecutar uploader
3. Login manual
4. No cerrar Chrome con Ctrl+C (usar cierre normal)

**Problema:** HuggingFace devuelve error 503
**Causa:** Modelo frío (no en memoria)
**Solución:** Reintentar en 20 segundos o usar template fallback

---

## Próximos Pasos

### Prioridad Alta
1. **Generación de video real:** Integrar `moviepy` para crear videos con imágenes de productos
2. **Hosting del backend:** Mover a VPS para ejecución 24/7
3. **Scraping real:** Integrar proxy service (BrightData/Oxylabs) para scraping sin bloqueos

### Prioridad Media
4. **Instagram Reels:** Añadir uploader similar a TikTok
5. **Analytics:** Dashboard con métricas de clicks y conversiones
6. **Notificaciones push:** Web push para nuevas ofertas

### Prioridad Baja
7. **API de Amazon:** Migrar de scraping a Product Advertising API
8. **Multi-país:** Soporte para Amazon UK, DE, FR
9. **A/B testing:** Probar diferentes títulos de marketing

---

## Comandos Útiles

### Frontend
```bash
# Desarrollo local
npm run dev

# Build de producción
npm run build

# Lint
npm run lint
```

### Backend
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar bot completo
cd backend && python main.py

# Test de TikTok uploader
cd backend && python -m social.uploader

# Test de scraper
cd backend && python -m scraper.amazon

# Test de enhancer
cd backend && python -m content.enhancer
```

### Telegram
```bash
# Publicar ofertas nuevas
python scripts/telegram_bot.py --publish-new

# Ver mensaje de prueba
python scripts/telegram_bot.py --test
```

### Git
```bash
# Deploy a producción
git add . && git commit -m "feat: descripción" && git push

# Ver logs de Vercel
vercel logs camper-omega.vercel.app
```

---

## Contacto y Recursos

- **Documentación Supabase:** https://supabase.com/docs
- **Next.js 14 Docs:** https://nextjs.org/docs
- **HuggingFace Inference:** https://huggingface.co/docs/api-inference
- **Selenium Python:** https://selenium-python.readthedocs.io
- **Amazon Associates:** https://afiliados.amazon.es

---

*Documento generado para facilitar el traspaso del proyecto. Actualizar con cada cambio significativo.*
