# 🏕️ Camping Deals - Negocio 100% Gratis y Automático

[![GitHub Actions](https://github.com/camping-offers/camping-offers.github.io/actions/workflows/deal-scraper.yml/badge.svg)](https://github.com/camping-offers/camping-offers.github.io/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Negocio de afiliación Amazon 100% automático y sin costes fijos** centrado en ofertas de camping con más del 30% de descuento.

🎯 **Objetivo:** €300-500/mes con mantenimiento mínimo (1-2 horas/semana)

---

## 🚀 Stack Tecnológico (100% Gratis)

| Servicio | Coste | Límite Gratuito | Propósito |
|----------|-------|-----------------|-----------|
| **GitHub Pages** | €0 | Ilimitado + HTTPS | Hosting web estático |
| **GitHub Actions** | €0 | 2,000 min/mes | Automatización y scraping |
| **Supabase** | €0 | 500MB + 50K conn/mes | Base de datos cloud |
| **Resend** | €0 | 3,000 emails/mes | Email marketing |
| **Telegram Bot** | €0 | Ilimitado | Notificaciones ofertas |
| **IFTTT** | €0 | 3 applets | Instagram/TikTok |
| **Plausible** | €0 | Sitio propio | Analytics |

---

## 📁 Estructura del Proyecto

```
camping-offers/
├── .github/workflows/
│   └── deal-scraper.yml      # Cron cada 6 horas
├── scraper/
│   └── amazon_scraper.py     # Web scraping anti-detección
├── database/
│   └── supabase_client.py    # Cliente Supabase + JSON fallback
├── marketing/
│   └── email_sender.py       # Resend email marketing
├── social/
│   └── social_poster.py      # Telegram + IFTTT
├── analytics/
│   └── dashboard.py          # Google Sheets dashboard
├── data/
│   └── deals.json            # Ofertas actuales
├── index.html                # Web principal
├── _config.yml               # Jekyll config
├── main_automation.py        # Orquestador principal
├── requirements.txt          # Dependencias Python
└── .env.example              # Variables de entorno
```

---

## ⚡ Inicio Rápido

### 1. Clonar y configurar

```bash
git clone https://github.com/TU-USUARIO/camping-offers.git
cd camping-offers
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configurar credenciales

Edita `.env` con tus credenciales (ver guía en `.env.example`):

- **Amazon Associate**: [affiliate-program.amazon.es](https://affiliate-program.amazon.es/)
- **Telegram Bot**: 📖 **Guía completa**: Ver [`GUIA_TELEGRAM_BOT.md`](./GUIA_TELEGRAM_BOT.md) o seguir pasos en @BotFather
- **Supabase** (opcional): [supabase.com](https://supabase.com/)
- **Resend** (opcional): [resend.com](https://resend.com/)

> **💡 Para Next.js/Vercel**: El proyecto incluye un dashboard completo en `/dashboard` con verificación de estado en tiempo real. Ver [`claude_sigue.md`](./claude_sigue.md) para el estado actual del proyecto.

### 3. Ejecutar scraping

```bash
# Test local
python main_automation.py --scrape --dry-run

# Producción
python main_automation.py --scrape
```

### 4. Desplegar en GitHub

```bash
git add .
git commit -m "Initial setup"
git push origin main
```

Ve a **Settings → Pages** y habilita GitHub Pages desde `main` branch.

---

## 🔄 Automatización

El workflow de GitHub Actions ejecuta **cada 6 horas**:

1. 🔍 Scrapea Amazon buscando ofertas ≥30%
2. 💾 Guarda en Supabase/JSON
3. 📱 Publica top 3 en Telegram
4. 📄 Actualiza `deals.json` para la web
5. 📊 Registra métricas

### Ejecución manual

Desde GitHub: **Actions → Deal Scraper → Run workflow**

---

## ⚖️ Cumplimiento Amazon Associates

Este proyecto cumple **estrictamente** las políticas de Amazon:

✅ Enlaces solo en comunicaciones **opt-in** (canal Telegram)  
✅ **Disclosure visible** en cada enlace de afiliado  
✅ Datos obtenidos mediante **web scraping público** (no API modificada)  
✅ **Sin spam ni recompensas** por usar enlaces  
✅ Sin modificar contenido oficial de Amazon  

---

## 📊 Proyección de Ingresos

| Visitantes/Mes | Clics (15%) | Compras (4%) | Ingresos (€) |
|----------------|-------------|--------------|--------------|
| 1,000 | 150 | 6 | ~€108 |
| 2,000 | 300 | 12 | ~€216 |
| 3,000 | 450 | 18 | ~€324 |
| 5,000 | 750 | 30 | ~€540 |

*Basado en: comisión 4%, pedido promedio €45*

---

## 📱 Marketing Multicanal

### Telegram (Gratuito, ilimitado)

- Bot publica automáticamente top ofertas
- Canal público: @campingdeals
- Rate limiting para evitar spam

### IFTTT → Instagram/TikTok

- Webhook activa publicación automática
- Requiere configurar applets gratuitos
- Ver guía en `social/social_poster.py`

### SEO Orgánico

- Web optimizada con meta-tags
- Sitemap automático con Jekyll
- Palabras clave: ofertas camping, descuentos outdoor

---

## 🛠️ Mantenimiento Semanal (1-2 horas)

| Tarea | Tiempo |
|-------|--------|
| Revisar logs de errores | 15 min |
| Optimizar keywords SEO | 30 min |
| Publicar contenido blog | 45 min |
| Revisar métricas | 15 min |

---

## 📄 Licencia

MIT License - Uso libre con atribución.

---

## 🆘 Soporte

- **Issues**: Abre un issue en GitHub
- **Telegram**: @campingdeals

---

*Hecho con ❤️ para la comunidad outdoor*  
*Actualizado: Enero 2026*
