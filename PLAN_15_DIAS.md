# Plan de Monetización: 15 Días para Empezar a Ganar

## Estado Actual de la Web

**Lo que YA tienes funcionando:**
- Web Next.js en producción con SEO optimizado
- Google Analytics 4 (ID: G-NEJH6DH78L)
- Google AdSense configurado (pub-7131240786023090) — **esta es tu primera fuente de ingresos**
- Schema.org estructurado (rich snippets en Google)
- Sitemap XML automático
- Bot TikTok automatizado (@camperoutlet)
- Amazon Associates con tag `camperdeals07-21`

**Lo que FALTA para monetizar:**
1. Google Search Console activo (indexación acelerada)
2. Supabase con clave service_role (para que el bot publique ofertas)
3. Google AI API key (para descripciones optimizadas)
4. Tráfico inicial (Chollometro, grupos Facebook, Reddit)

---

## Canales de Monetización (Por Impacto)

| Canal | Ingresos esperados mes 1 | Tiempo para setup |
|-------|--------------------------|-------------------|
| Google AdSense | 5-30€ (depende del tráfico) | YA CONFIGURADO |
| Amazon Associates | 10-50€ (7% comisión camping) | 1-2 días |
| Decathlon (Awin) | 5-20€ (3% comisión) | 2-3 días |
| TikTok (orgánico) | Indirecto (tráfico a web) | Ya activo |

---

## Días 1-2: Setup Crítico (Bloqueantes)

### URGENTE: Activar Supabase service_role
```
1. Supabase Dashboard → Settings → API
2. Copiar clave "service_role" (la secreta)
3. GitHub → Settings → Secrets → SUPABASE_KEY → actualizar valor
```
**Sin esto:** El bot no puede escribir ofertas en la web.

### URGENTE: Añadir Google AI API key
```
1. aistudio.google.com → Get API Key (gratis)
2. GitHub → Settings → Secrets → GOOGLE_AI_API_KEY → pegar clave
```
**Sin esto:** Las descripciones de productos son genéricas.

### Google Search Console (5 minutos, impacto enorme)
```
1. search.google.com/search-console
2. Añadir propiedad → URL prefix → ofertascamping.es
3. Método de verificación: HTML tag
4. Copiar código → pegar en src/app/layout.tsx (línea ~97)
5. Ir a Sitemaps → Enviar https://ofertascamping.es/sitemap.xml
```
**Por qué:** Google indexa tu sitio antes → apareces antes → más tráfico.

### Amazon Associates (si no lo tienes)
```
1. afiliados.amazon.es → Registrarse
2. Tag: camperdeals07-21 (ya está en el código)
3. Necesitas 3 ventas en 180 días para confirmar cuenta
```

---

## Días 3-5: Tráfico Inmediato (Gratis)

### Chollometro.com — MAYOR IMPACTO EN HORAS
Chollometro es la web de ofertas con más tráfico de España (millones de visitas/mes). Una buena oferta puede darte 1.000-10.000 visitas en 24 horas.

```
1. Crear cuenta en chollometro.com (gratis)
2. Publicar las mejores ofertas del bot así:
   - Título: "Tienda campaña 2 personas [MARCA] a X€ (-Y% descuento)"
   - Descripción: precio, características, por qué es un chollo
   - Enlace: a tu página de la oferta en ofertascamping.es (no directo a Amazon)
3. Publicar 2-3 ofertas al día
4. Responder comentarios rápido (mejora el ranking en Chollometro)
```

### Grupos de Facebook (días 3-4)
Buscar y unirse a estos grupos:
- "Camping España" (busca grupos con >10k miembros)
- "Senderismo y Montaña España"
- "Autocaravanas y Caravanas España"
- "Ofertas Amazon España"

Formato del post que funciona:
```
"🏕️ He encontrado esta tienda de campaña a X€ en Amazon (normalmente Y€).
Es perfecta para [caso de uso]. ¿Alguien la ha probado?
[enlace a tu artículo en ofertascamping.es]"
```
NO spam, NO enlace directo de afiliado — enlaza a tu web.

### Reddit (días 4-5)
- r/es (si la oferta es muy buena)
- r/senderismo
- Buscar subreddits españoles de camping

### Canal de Telegram — Crear YA
```
1. Crear canal @ofertascamping (o similar disponible)
2. Publicar cada oferta que encuentra el bot
3. Añadir enlace del canal en el header de la web
4. Promover en los grupos de Facebook
```
Cada suscriptor de Telegram = visita recurrente gratis.

---

## Días 6-10: Optimizar lo que Funciona

### Medir en Google Analytics qué convierte
```
Ir a: Analytics → Engagement → Pages and screens
Identificar:
- Qué páginas tienen más tiempo en pantalla (la gente lee)
- Qué páginas tienen más clics salientes a Amazon
- Qué tráfico viene de dónde (referral, organic, social)
```

Doblar esfuerzo en el canal que más tráfico envía.

### TikTok: Formato de video que convierte
El bot ya publica automáticamente. Además, publicar manualmente:

**Video tipo 1 — "Chollo del día":**
```
- Mostrar producto físico (o foto animada)
- Precio normal → precio oferta (efecto sorpresa)
- "Link en bio para comprarlo" → enlace a ofertascamping.es en bio
- Hashtags: #camping #ofertasamazon #chollos #senderismo #outdoor
```

**Video tipo 2 — "¿Qué llevo al camping?":**
```
- Mostrar 5 productos baratos
- Precio total: menos de 100€
- Enlazar a una página de categoría de tu web
```

Publicar mínimo 1 video manual por día en semana 2.

### Añadir Decathlon como afiliado alternativo
```
1. Ir a awin.com
2. Crear cuenta publisher (depósito 5€ reembolsable)
3. Solicitar programa Decathlon España
4. Aprobación en 1-5 días
5. Crear páginas comparativas "Amazon vs Decathlon"
```
Las comparativas posicionan bien en Google y convierten muy bien.

---

## Días 11-15: Escalar y Consolidar

### Publicar en Chollometro las 3 mejores ofertas de la semana
El objetivo es conseguir tu primera venta de afiliado Amazon (necesitas 3 en 180 días).

### SEO de largo plazo (empezar ahora, resultados en 2-4 semanas)
Las páginas que ya tienes en el sitemap son perfectas. Necesitas contenido:

Crear artículos tipo:
- "Mejor tienda de campaña barata 2026" → `/guias/mejores-tiendas-campana-2026`
- "Saco de dormir para 3 estaciones: cuál comprar en Amazon" → similar
- "Checklist material camping completo (y dónde comprarlo barato)"

Estos artículos posicionan para búsquedas con intención de compra alta.

### Verificar que AdSense está mostrando anuncios
```
1. Ir a adsense.google.com
2. Verificar que los anuncios están activos
3. Comprobar que la política de privacidad incluye mención a AdSense
4. El código ya está en el layout.tsx, solo necesita aprobación de Google
```
AdSense puede tardar 1-14 días en aprobar la cuenta nueva. Si ya tienes la cuenta aprobada, deberías ver ingresos desde el día 1 de tráfico.

---

## Objetivos Realistas a Día 15

| Métrica | Objetivo conservador | Objetivo optimista |
|---------|---------------------|-------------------|
| Visitas totales | 500-1.000 | 2.000-5.000 |
| Clics Amazon | 50-100 | 200-500 |
| Ventas afiliado | 1-3 | 5-15 |
| Ingresos estimados | 5-25€ | 25-100€ |
| Suscriptores Telegram | 20-50 | 100-300 |

---

## Checklist Diario (Una vez el sistema esté rodando)

```
□ Revisar que el bot ha publicado las ofertas del día
□ Publicar 1-2 ofertas en Chollometro
□ Publicar en grupos de Facebook (no más de 1 grupo/día para no parecer spam)
□ Publicar 1 video TikTok manual
□ Revisar Analytics: ¿alguna página/oferta destaca?
□ Responder comentarios en Chollometro y redes
```

---

## Recursos y Links

| Recurso | URL |
|---------|-----|
| Google Search Console | https://search.google.com/search-console |
| Google Analytics | https://analytics.google.com |
| Google AdSense | https://adsense.google.com |
| Amazon Associates | https://afiliados.amazon.es |
| Awin (Decathlon) | https://www.awin.com |
| Chollometro | https://www.chollometro.com |
| Supabase Dashboard | https://supabase.com/dashboard |
| GitHub Secrets | https://github.com/adrimg3196/camper/settings/secrets/actions |

---

## Lo que BLOQUEA la monetización ahora mismo

**Acción #1 (URGENTE):** `SUPABASE_KEY` con clave `service_role`
→ Sin esto, el bot no escribe ofertas en la web = la web está vacía

**Acción #2 (URGENTE):** `GOOGLE_AI_API_KEY`
→ Sin esto, las descripciones son genéricas = menor conversión

**Acción #3 (5 minutos):** Google Search Console
→ Sin esto, Google tarda semanas en indexar = sin tráfico orgánico

Una vez resueltos estos 3 puntos, el sistema funciona solo y solo necesitas:
1. Publicar en Chollometro cada día (15 min/día)
2. 1 video TikTok manual (20-30 min/día)
3. Revisar Analytics semanalmente

---

*Actualizado: Febrero 2026*
