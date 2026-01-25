# Guía de Configuración SEO - CampingDeals España

## Estado Actual

### Implementado
- [x] Meta tags optimizados (title, description, keywords)
- [x] Schema.org JSON-LD (Organization, WebSite, WebPage, FAQPage, Product)
- [x] OpenGraph y Twitter Cards
- [x] Sitemap dinámico (`/sitemap.xml`)
- [x] Robots.txt optimizado con reglas por bot
- [x] PWA Manifest
- [x] Contenido SEO optimizado para keywords de alto volumen
- [x] Product schema en cada tarjeta de producto (rich snippets)

---

## Paso 1: Comprar el Dominio

### Dominios Recomendados (disponibles por 0,01€/año en GoDaddy):
1. **ofertascamping.es** ⭐ RECOMENDADO - keyword exacta
2. **campingdeals.es** - branding alternativo
3. **chollocamping.es** - estilo coloquial

### Pasos:
1. Ve a [GoDaddy España](https://www.godaddy.com/es-es)
2. Busca el dominio elegido
3. Completa la compra (0,01€ primer año)
4. Activa la renovación automática

---

## Paso 2: Conectar Dominio a Vercel

1. En Vercel, ve a tu proyecto: https://vercel.com/dashboard
2. Settings → Domains
3. Add Domain: `ofertascamping.es`
4. Vercel te dará los DNS records necesarios:
   - Tipo A: `76.76.21.21`
   - O CNAME: `cname.vercel-dns.com`
5. En GoDaddy → DNS → Añade los records
6. Espera 24-48h para propagación

---

## Paso 3: Google Search Console

### Crear Propiedad:
1. Ve a [Google Search Console](https://search.google.com/search-console)
2. "Añadir propiedad" → Prefijo de URL → `https://ofertascamping.es`
3. Verificación: Usa el método HTML tag

### Código de Verificación:
Actualiza en `src/app/layout.tsx`:
```typescript
verification: {
    google: "TU_CODIGO_AQUI", // Reemplaza con tu código
},
```

### Acciones Post-Verificación:
1. Enviar sitemap: `https://ofertascamping.es/sitemap.xml`
2. Solicitar indexación de página principal
3. Configurar alertas de errores

---

## Paso 4: Google Analytics 4

### Crear Propiedad:
1. Ve a [Google Analytics](https://analytics.google.com)
2. Admin → Crear propiedad
3. Nombre: "CampingDeals España"
4. Zona horaria: España
5. Moneda: EUR

### Obtener ID de Medición:
1. Flujos de datos → Web
2. Copia el ID (formato: `G-XXXXXXXXXX`)

### Implementar:
Actualiza en `src/app/layout.tsx`:
```typescript
// Reemplaza G-XXXXXXXXXX con tu ID real
<Script src="https://www.googletagmanager.com/gtag/js?id=G-TU_ID_AQUI" />
```

---

## Paso 5: Bing Webmaster Tools (Opcional pero recomendado)

1. Ve a [Bing Webmaster](https://www.bing.com/webmasters)
2. Importa desde Google Search Console
3. Añade código en `layout.tsx`:
```typescript
other: {
    "msvalidate.01": "TU_CODIGO_BING",
}
```

---

## Keywords Objetivo

### Keywords Principales (Alto Volumen):
| Keyword | Volumen Mensual | Dificultad |
|---------|-----------------|------------|
| ofertas camping | 8.100 | Media |
| tiendas campaña baratas | 5.400 | Baja |
| chollos camping | 2.900 | Baja |
| sacos dormir amazon | 2.400 | Media |
| mochilas trekking oferta | 1.900 | Baja |

### Keywords Long-tail:
- ofertas camping amazon españa
- tiendas campaña baratas amazon
- chollos material camping 2026
- descuentos equipamiento outdoor
- black friday camping españa

---

## Estrategia de Contenido (Fase 2)

### Guías a Crear:
1. `/guias/mejores-tiendas-campana-2026` - Review + ofertas
2. `/guias/mejores-sacos-dormir-2026` - Comparativa
3. `/guias/guia-camping-principiantes` - Evergreen
4. `/guias/como-elegir-tienda-campana` - Educational
5. `/guias/camping-con-ninos` - Nicho específico

### Páginas de Categoría:
Ya implementadas en sitemap:
- `/ofertas/tiendas-campana`
- `/ofertas/sacos-dormir`
- `/ofertas/mochilas`
- `/ofertas/cocina-camping`
- etc.

---

## Estrategia de Backlinks

### Fase 1 - Directorios:
1. Google Business Profile (si aplica)
2. Páginas Amarillas
3. Directorios de ecommerce español

### Fase 2 - Contenido:
1. Guest posts en blogs de viajes/camping
2. Colaboraciones con influencers outdoor
3. Menciones en foros de camping

### Fase 3 - PR:
1. Notas de prensa para ofertas especiales
2. Black Friday / Prime Day campaigns

---

## Checklist Pre-Lanzamiento

- [ ] Dominio comprado y conectado
- [ ] SSL activo (automático con Vercel)
- [ ] Google Search Console verificado
- [ ] Sitemap enviado
- [ ] Google Analytics configurado
- [ ] Test de velocidad (PageSpeed > 90)
- [ ] Test mobile-friendly
- [ ] Schema validator sin errores
- [ ] Open Graph debugger OK

---

## Recursos Útiles

- [Google Search Console](https://search.google.com/search-console)
- [Schema.org Validator](https://validator.schema.org/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [Open Graph Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)

---

## Contacto

Para más ayuda con SEO: adrimg3196@gmail.com

**Última actualización:** Enero 2026
