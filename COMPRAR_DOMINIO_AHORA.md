# 🛒 Comprar Dominio AHORA - Guía Paso a Paso

> **Tiempo**: 30 minutos | **Coste**: ~€10/año | **Impacto**: +50-100% SEO

---

## 🎯 Paso 1: Verificar Disponibilidad (2 minutos)

### Opción Recomendada: Namecheap

1. **Abre este enlace**:
   ```
   https://www.namecheap.com/domains/registration/results/?domain=ofertascamping.es
   ```

2. **Si está disponible**:
   - ✅ Añádelo al carrito
   - ✅ Continúa al Paso 2

3. **Si NO está disponible**, prueba:
   - `cholloscamping.es`
   - `campingdeals.es`
   - `ofertascampingbarato.es`

---

## 🛒 Paso 2: Comprar en Namecheap (5 minutos)

### Proceso Completo:

1. **Crea cuenta** (si no tienes):
   - Email
   - Contraseña
   - Verifica email

2. **En el carrito**:
   - ✅ **WHOIS Privacy**: Incluido gratis (deja activado)
   - ✅ **Auto-renew**: Activa (importante)
   - ⏱️ **Duración**: 1 año (mínimo)

3. **Paga**:
   - Tarjeta o PayPal
   - Coste: ~€10-12

4. **Confirma**:
   - Recibirás email de confirmación
   - El dominio estará en tu cuenta

---

## ⚙️ Paso 3: Configurar DNS (10 minutos)

### Método Más Fácil: DNS de Namecheap

1. **Ve a tu cuenta Namecheap**
2. **Domain List** → Clic en tu dominio
3. **Advanced DNS** (pestaña)
4. **Añade estos registros** (elimina los que vengan por defecto):

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
6. **Espera 5 minutos** para que se propaguen

---

## 🚀 Paso 4: Conectar en Vercel (5 minutos)

1. **Ve a**: https://vercel.com/dashboard
2. **Selecciona proyecto**: "camper"
3. **Settings** → **Domains**
4. **Add Domain**
5. **Escribe**: `ofertascamping.es` (o el que compraste)
6. **Add**

**Vercel hará lo siguiente:**
- Verificará el dominio automáticamente
- Configurará SSL automáticamente
- Puede tardar 2-5 minutos

**Si pide verificación DNS:**
- Vercel te dará un registro TXT
- Añádelo en Namecheap → Advanced DNS
- Tipo: TXT, Host: @, Value: (el que Vercel te da)
- Espera 5 minutos y haz clic en "Verify" en Vercel

---

## 🔧 Paso 5: Actualizar Variables (2 minutos)

Una vez Vercel verifique el dominio:

1. **Vercel** → **Settings** → **Environment Variables**
2. **Add New**:
   ```
   Name: NEXT_PUBLIC_SITE_URL
   Value: https://ofertascamping.es
   Environments: ✅ Production ✅ Preview ✅ Development
   ```
3. **Save**

---

## ⏱️ Paso 6: Esperar Propagación (2-24 horas)

**Normalmente tarda**: 2-4 horas  
**Máximo**: 24-48 horas

**Cómo verificar que está listo:**

```bash
# Opción 1: Herramienta online
https://www.whatsmydns.net/#A/ofertascamping.es

# Opción 2: Desde terminal
dig ofertascamping.es
```

**Cuando veas que apunta a Vercel (76.76.21.21), está listo.**

---

## ✅ Paso 7: Verificar que Funciona

1. **Visita**: `https://ofertascamping.es`
2. **Debería cargar** tu sitio
3. **Verifica SSL**: Candado verde 🔒
4. **Prueba subpáginas**:
   - `https://ofertascamping.es/dashboard`
   - `https://ofertascamping.es/landing-telegram`

---

## 🎯 Después del Dominio

### Inmediato (Esta Semana)

1. ✅ **Actualizar Google Search Console**
   - Añade propiedad: `ofertascamping.es`
   - Verifica propiedad
   - Envía sitemap: `https://ofertascamping.es/sitemap.xml`

2. ✅ **Aplicar a Google AdSense**
   - Requiere dominio propio ✅
   - Aplica desde: https://www.google.com/adsense/

3. ✅ **Actualizar enlaces**
   - Todos los enlaces internos ya usan variables
   - El código está preparado

### Próximos Pasos

4. **Escribir primer artículo SEO**
5. **Promocionar landing page**
6. **Empezar a generar tráfico**

---

## 📊 Impacto Esperado

### Antes (Subdominio)
- ❌ SEO: 30/100
- ❌ Tráfico orgánico: ~50 visitas/mes
- ❌ Posicionamiento: Muy difícil

### Después (Dominio Propio)
- ✅ SEO: 70-80/100
- ✅ Tráfico orgánico: +50-100%
- ✅ Posicionamiento: Mucho más fácil
- ✅ Confianza: Mayor
- ✅ Monetización: Posible (AdSense)

---

## 🆘 Si Algo Falla

### El dominio no carga después de 24h

1. Verifica DNS: https://www.whatsmydns.net/
2. Asegúrate de que los registros A y CNAME están correctos
3. Contacta soporte de Namecheap si es necesario

### Vercel no verifica

1. Añade el registro TXT que Vercel pide
2. Espera 10-15 minutos
3. Haz clic en "Verify" de nuevo

### SSL no funciona

- Vercel configura SSL automáticamente
- Espera 10-15 minutos después de conectar dominio
- Si no funciona después de 1 hora, contacta soporte Vercel

---

## 💰 Resumen de Costes

- **Dominio**: €10-12/año (~€1/mes)
- **DNS**: Gratis (incluido)
- **SSL**: Gratis (Vercel)
- **Hosting**: Gratis (Vercel)
- **Total**: ~€1/mes

**ROI**: Inmediato - Mejor SEO = Más tráfico = Más dinero

---

## ✅ Checklist

- [ ] Dominio comprado en Namecheap
- [ ] DNS configurado (A + CNAME)
- [ ] Dominio añadido en Vercel
- [ ] Vercel verifica el dominio
- [ ] Variable `NEXT_PUBLIC_SITE_URL` actualizada
- [ ] Sitio carga en nuevo dominio
- [ ] SSL funcionando (candado verde)
- [ ] Google Search Console configurado

---

**🚀 ¡Vamos a comprarlo! Te guío en cada paso si necesitas ayuda.**

**Enlaces directos:**
- **Namecheap**: https://www.namecheap.com/domains/registration/results/?domain=ofertascamping.es
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Verificar DNS**: https://www.whatsmydns.net/
