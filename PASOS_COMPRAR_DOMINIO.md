# 🛒 Pasos Exactos para Comprar Dominio

> **Tiempo**: 30 minutos | **Coste**: ~€10/año

---

## ✅ Paso 1: Comprar Dominio (10 minutos)

### En Namecheap:

1. **Abre**: https://www.namecheap.com/domains/registration/results/?domain=ofertascamping.es

2. **Si está disponible**:
   - ✅ Añade al carrito
   - ✅ WHOIS Privacy: Incluido (deja activado)
   - ✅ Auto-renew: Activa (importante)
   - ✅ Duración: 1 año mínimo
   - ✅ Paga (~€10-12)

3. **Si NO está disponible**, prueba:
   - `cholloscamping.es`
   - `campingdeals.es`
   - `ofertascampingbarato.es`

---

## ⚙️ Paso 2: Configurar DNS (10 minutos)

### En Namecheap:

1. **Domain List** → Clic en tu dominio
2. **Advanced DNS** (pestaña)
3. **Elimina registros existentes** (si los hay)
4. **Añade estos 2 registros**:

```
Registro 1:
Tipo: A Record
Host: @
Value: 76.76.21.21
TTL: Automatic

Registro 2:
Tipo: CNAME Record
Host: www
Value: cname.vercel-dns.com
TTL: Automatic
```

5. **Save All Changes**
6. **Espera 5 minutos**

---

## 🚀 Paso 3: Conectar en Vercel (5 minutos)

1. **Ve a**: https://vercel.com/dashboard
2. **Proyecto**: "camper"
3. **Settings** → **Domains**
4. **Add Domain**
5. **Escribe**: `ofertascamping.es` (o el que compraste)
6. **Add**

**Vercel verificará automáticamente** (2-5 minutos)

**Si pide verificación TXT:**
- Añade el registro TXT que Vercel te da
- En Namecheap → Advanced DNS
- Tipo: TXT, Host: @, Value: (el que Vercel te da)
- Espera 5 minutos y haz "Verify" en Vercel

---

## 🔧 Paso 4: Actualizar Variable (2 minutos)

1. **Vercel** → **Settings** → **Environment Variables**
2. **Add New**:
   ```
   Name: NEXT_PUBLIC_SITE_URL
   Value: https://ofertascamping.es
   Environments: ✅ Production ✅ Preview ✅ Development
   ```
3. **Save**

---

## ⏱️ Paso 5: Esperar (2-24 horas)

**Normalmente**: 2-4 horas  
**Máximo**: 24-48 horas

**Verificar**: https://www.whatsmydns.net/#A/ofertascamping.es

Cuando veas que apunta a `76.76.21.21`, está listo.

---

## ✅ Paso 6: Verificar (2 minutos)

1. **Visita**: `https://ofertascamping.es`
2. **Debería cargar** tu sitio
3. **SSL**: Candado verde 🔒
4. **Prueba**: `/dashboard`, `/landing-telegram`

---

## 🎯 Después del Dominio

### Inmediato:

1. **Google Search Console**
   - https://search.google.com/search-console
   - Añade propiedad: `ofertascamping.es`
   - Verifica propiedad
   - Envía sitemap: `https://ofertascamping.es/sitemap.xml`

2. **Google AdSense**
   - https://www.google.com/adsense/
   - Aplica (ahora puedes porque tienes dominio propio)

---

## 📊 Impacto Esperado

**Antes (Subdominio)**:
- SEO: 30/100
- Tráfico: ~50 visitas/mes
- Posicionamiento: Muy difícil

**Después (Dominio Propio)**:
- SEO: 70-80/100
- Tráfico: +50-100%
- Posicionamiento: Mucho más fácil
- Monetización: Posible

---

## 🆘 Si Algo Falla

**Dominio no carga después de 24h:**
- Verifica DNS: https://www.whatsmydns.net/
- Asegúrate de que A y CNAME están correctos

**Vercel no verifica:**
- Añade registro TXT
- Espera 10-15 minutos
- Haz "Verify" de nuevo

**SSL no funciona:**
- Vercel lo configura automáticamente
- Espera 10-15 minutos

---

**🚀 ¡Vamos a comprarlo! Te guío si necesitas ayuda en algún paso.**
