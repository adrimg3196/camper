# 🛒 Guía Completa: Comprar y Configurar Dominio Premium

> **Objetivo**: Comprar dominio `.es` para mejor SEO y profesionalidad  
> **Tiempo estimado**: 30 minutos  
> **Coste**: ~€10-12/año

---

## 🎯 Paso 1: Elegir Dominio

### Opciones Recomendadas (en orden de preferencia)

1. **`ofertascamping.es`** ⭐ MEJOR OPCIÓN
   - Keywords principales: "ofertas camping"
   - SEO: Excelente
   - Precio: ~€10/año

2. **`cholloscamping.es`**
   - Keywords: "chollos camping"
   - SEO: Muy bueno
   - Precio: ~€10/año

3. **`campingdeals.es`**
   - Brandable
   - SEO: Bueno
   - Precio: ~€10/año

4. **`ofertascampingbarato.es`**
   - Muy descriptivo
   - SEO: Excelente
   - Precio: ~€10/año

### Verificar Disponibilidad

**Opción A: Namecheap**
1. Ve a: https://www.namecheap.com/domains/registration/results/?domain=ofertascamping.es
2. Busca el dominio
3. Si está disponible, añádelo al carrito

**Opción B: Cloudflare Registrar**
1. Ve a: https://www.cloudflare.com/products/registrar/
2. Busca el dominio
3. Cloudflare vende a precio de coste (sin margen)

**Opción C: Porkbun**
1. Ve a: https://porkbun.com/
2. Busca el dominio
3. Precios muy competitivos

---

## 🛒 Paso 2: Comprar el Dominio

### Recomendación: Namecheap (Más fácil)

**Pasos:**

1. **Ve a Namecheap**: https://www.namecheap.com/
2. **Busca el dominio**: Escribe `ofertascamping.es` en el buscador
3. **Añade al carrito**: Si está disponible
4. **Configuración**:
   - ✅ **WHOIS Privacy**: Incluido gratis (recomendado)
   - ✅ **Auto-renew**: Activar (para no perder el dominio)
   - ⏱️ **Duración**: 1 año mínimo (puedes comprar más)
5. **Paga**: Tarjeta o PayPal
6. **Confirma**: Recibirás email de confirmación

**Datos que necesitarás:**
- Email (donde recibirás confirmación)
- Datos de facturación
- Método de pago

---

## ⚙️ Paso 3: Configurar DNS en Vercel

Una vez comprado el dominio, configura DNS:

### Opción A: DNS de Namecheap (Recomendado)

1. **Ve a tu cuenta Namecheap**
2. **Domain List** → Selecciona tu dominio
3. **Advanced DNS**
4. **Añade estos registros**:

```
Tipo: A Record
Host: @
Value: 76.76.21.21
TTL: Automatic

Tipo: CNAME Record
Host: www
Value: cname.vercel-dns.com
TTL: Automatic
```

### Opción B: Usar Cloudflare (Más rápido, gratis)

1. **Crea cuenta en Cloudflare** (gratis)
2. **Add Site** → Añade tu dominio
3. **Cambia nameservers en Namecheap**:
   - Namecheap → Domain → Nameservers
   - Cambia a los que Cloudflare te da
4. **En Cloudflare**:
   - DNS → Add record
   - Tipo: A, Name: @, Content: 76.76.21.21
   - Tipo: CNAME, Name: www, Target: cname.vercel-dns.com

---

## 🚀 Paso 4: Conectar en Vercel

1. **Ve a Vercel Dashboard**: https://vercel.com/dashboard
2. **Selecciona tu proyecto**: "camper"
3. **Settings** → **Domains**
4. **Add Domain**
5. **Escribe tu dominio**: `ofertascamping.es`
6. **Add**
7. **Vercel verificará automáticamente** (puede tardar unos minutos)

**Si Vercel pide verificación DNS:**
- Añade el registro TXT que Vercel te proporcione
- Espera 5-10 minutos
- Vercel verificará automáticamente

---

## 🔧 Paso 5: Actualizar Variables y Código

Una vez conectado el dominio, actualiza:

### Variables de Entorno en Vercel

1. **Vercel** → **Settings** → **Environment Variables**
2. **Añade/Actualiza**:
   ```
   NEXT_PUBLIC_SITE_URL=https://ofertascamping.es
   ```
3. **Selecciona**: Production, Preview, Development
4. **Save**

### Actualizar Código (Canonical URLs)

Ya está preparado para usar variables de entorno, pero verifica:

- `src/app/layout.tsx` - Usa `NEXT_PUBLIC_SITE_URL`
- `src/app/sitemap.ts` - Usa variable de entorno
- Schema.org - Ya usa variables

---

## ⏱️ Paso 6: Esperar Propagación DNS

**Tiempo**: 24-48 horas (normalmente 2-4 horas)

**Cómo verificar:**
```bash
# Verifica si el dominio apunta a Vercel
dig ofertascamping.es

# O usa herramienta online
https://www.whatsmydns.net/#A/ofertascamping.es
```

**Cuando esté listo:**
- Tu sitio estará disponible en `https://ofertascamping.es`
- También en `https://www.ofertascamping.es`

---

## ✅ Paso 7: Verificar que Funciona

1. **Visita**: `https://ofertascamping.es`
2. **Debería cargar** tu sitio de Vercel
3. **Verifica SSL**: Debería tener candado verde (HTTPS automático)
4. **Prueba subpáginas**: `/dashboard`, `/landing-telegram`

---

## 🎯 Paso 8: Configurar Email (Opcional)

Con tu dominio puedes crear emails profesionales:

**Opción A: Cloudflare Email Routing (Gratis)**
1. Cloudflare → Email → Routing
2. Crea `info@ofertascamping.es`
3. Redirige a tu email personal

**Opción B: Google Workspace (~€5/mes)**
- Email profesional completo
- Gmail con tu dominio

---

## 📊 Impacto Esperado

### Antes (Subdominio)
- SEO Score: 30/100
- Posicionamiento: Difícil
- Confianza: Baja
- Tráfico orgánico: Mínimo

### Después (Dominio Propio)
- SEO Score: 70-80/100
- Posicionamiento: Más fácil
- Confianza: Alta
- Tráfico orgánico: +50-100%

---

## 🆘 Troubleshooting

### El dominio no carga después de 48h

**Solución:**
1. Verifica DNS con `dig` o herramienta online
2. Asegúrate de que los registros A y CNAME están correctos
3. Limpia caché DNS: `sudo dscacheutil -flushcache` (Mac)

### Vercel no verifica el dominio

**Solución:**
1. Añade el registro TXT que Vercel pide
2. Espera 10-15 minutos
3. Haz clic en "Verify" de nuevo en Vercel

### Error SSL/HTTPS

**Solución:**
- Vercel configura SSL automáticamente
- Espera 5-10 minutos después de conectar dominio
- Si no funciona, contacta soporte de Vercel

---

## 💰 Costes Totales

- **Dominio**: €10-12/año
- **DNS**: Gratis (incluido o Cloudflare)
- **SSL**: Gratis (Vercel)
- **Total**: ~€1/mes

**ROI**: Inmediato - Mejor SEO = Más tráfico = Más dinero

---

## 📝 Checklist Final

- [ ] Dominio comprado
- [ ] DNS configurado
- [ ] Dominio conectado en Vercel
- [ ] Variables de entorno actualizadas
- [ ] Sitio carga en nuevo dominio
- [ ] SSL funcionando (candado verde)
- [ ] Subpáginas funcionando

---

**¿Listo para comprar?** Te guío paso a paso si necesitas ayuda en algún momento específico. 🚀
