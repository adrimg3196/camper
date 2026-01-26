# 🤖 Guía Completa: Configurar Bot de Telegram

Esta guía te ayudará a configurar el bot de Telegram para que el sistema publique ofertas automáticamente.

## 📋 Pasos para Configurar el Bot

### Paso 1: Crear el Bot con BotFather

1. **Abre Telegram** en tu móvil o escritorio
2. **Busca** `@BotFather` en la búsqueda de Telegram
3. **Inicia conversación** y envía `/start`
4. **Crea un nuevo bot** enviando `/newbot`
5. **Sigue las instrucciones:**
   - Elige un nombre para tu bot (ej: "Camping Deals Bot")
   - Elige un username (debe terminar en `bot`, ej: `camperdeals_bot`)
6. **Copia el token** que te da BotFather (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
   - ⚠️ **IMPORTANTE**: Guarda este token de forma segura, lo necesitarás en el paso 7

### Paso 2: Crear el Canal de Telegram

1. En Telegram, **crea un nuevo canal**:
   - Móvil: Menú → "Nuevo canal"
   - Escritorio: Menú → "Nuevo canal"
2. **Configura el canal:**
   - Nombre: ej. "Camping Deals España"
   - Descripción: "Ofertas de camping con más del 30% de descuento"
   - Tipo: **Público** (recomendado) o Privado
3. **Obtén el ID del canal:**
   - Si es público: El ID es `@nombre_del_canal` (ej: `@camperdeals`)
   - Si es privado: Necesitarás el ID numérico (ver paso 3)

### Paso 3: Añadir el Bot como Administrador

1. **Abre tu canal** en Telegram
2. **Ve a la configuración del canal** (icono de engranaje)
3. **Selecciona "Administradores"**
4. **Añade administrador** → Busca tu bot por su username
5. **Permisos del bot:**
   - ✅ **Publicar mensajes** (obligatorio)
   - ✅ **Editar mensajes** (opcional, recomendado)
   - ❌ No necesita otros permisos

### Paso 4: Obtener ID del Canal (Solo si es Privado)

Si tu canal es privado, necesitas el ID numérico:

1. **Añade este bot temporal** a tu canal: `@userinfobot`
2. **Envía cualquier mensaje** en el canal
3. El bot te responderá con el ID del canal (formato: `-1001234567890`)
4. **Elimina el bot** `@userinfobot` del canal después

### Paso 5: Configurar Variables en Vercel

1. **Ve a tu proyecto en Vercel**: https://vercel.com/dashboard
2. **Selecciona el proyecto** "camper" o "quizzical-ptolemy"
3. **Ve a Settings** → **Environment Variables**
4. **Añade las siguientes variables:**

   | Variable | Valor | Ejemplo |
   |----------|-------|---------|
   | `TELEGRAM_BOT_TOKEN` | Token del paso 1 | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
   | `TELEGRAM_CHANNEL_ID` | ID del canal | `@camperdeals` o `-1001234567890` |

5. **Selecciona los entornos:**
   - ✅ Production
   - ✅ Preview (opcional)
   - ✅ Development (opcional)

6. **Guarda** los cambios

### Paso 6: Verificar la Configuración

1. **Ve al Dashboard**: https://camper-omega.vercel.app/dashboard
2. **Revisa el panel "Estado del Sistema"**
3. **Verifica que "Telegram Bot" esté en verde** (Activo)
4. **Prueba la publicación manual:**
   - Haz clic en "Publicar Ahora"
   - Deberías ver un mensaje de éxito
   - Revisa tu canal de Telegram para confirmar

### Paso 7: Probar el Bot (Opcional)

Puedes probar el bot directamente desde Telegram:

1. **Busca tu bot** en Telegram (por su username)
2. **Envía** `/start`
3. El bot debería responder (si tiene comandos configurados)

> **Nota**: El bot principal está diseñado para publicar en canales, no para responder mensajes directos.

## 🔧 Troubleshooting

### ❌ "TELEGRAM_BOT_TOKEN no configurado"

**Solución:**
- Verifica que la variable esté configurada en Vercel
- Asegúrate de haber seleccionado el entorno correcto (Production)
- Espera 1-2 minutos después de guardar para que se propague

### ❌ "Unauthorized" o "Forbidden"

**Causas posibles:**
1. **Token incorrecto**: Verifica que copiaste el token completo sin espacios
2. **Bot no es administrador**: Asegúrate de que el bot tenga permisos de publicación
3. **ID de canal incorrecto**: 
   - Si es público, debe empezar con `@`
   - Si es privado, debe ser un número negativo

### ❌ El bot no publica mensajes

**Verificaciones:**
1. ¿El bot es administrador del canal?
2. ¿Tiene permisos para publicar mensajes?
3. ¿El ID del canal es correcto?
4. ¿Hay ofertas activas en la base de datos? (revisa el dashboard)

### ❌ Error 400: "Bad Request: chat not found"

**Solución:**
- Si el canal es privado, asegúrate de usar el ID numérico (negativo)
- Si es público, verifica que el username del canal sea correcto (con `@`)

## 📊 Monitoreo

Una vez configurado, el sistema publicará automáticamente:

- **Horario**: Todos los días a las **09:00 UTC** (10:00 CET en invierno, 11:00 CEST en verano)
- **Cantidad**: Las 3 mejores ofertas del día (con más del 30% de descuento)
- **Formato**: Mensajes con emojis, precios y enlaces de afiliado

Puedes verificar el estado en:
- **Dashboard**: https://camper-omega.vercel.app/dashboard
- **API Status**: https://camper-omega.vercel.app/api/system/status

## 🎯 Próximos Pasos

Una vez configurado el bot:

1. ✅ El sistema publicará automáticamente cada día
2. ✅ Puedes ejecutar publicaciones manuales desde el dashboard
3. ✅ Los logs se guardan en Supabase (tabla `publication_logs`)
4. ✅ Puedes personalizar el formato de los mensajes editando `/api/cron/daily-publish/route.ts`

## 📝 Notas Importantes

- **Seguridad**: Nunca compartas tu `TELEGRAM_BOT_TOKEN` públicamente
- **Límites**: Telegram permite hasta 20 mensajes por minuto por bot
- **Rate Limiting**: El sistema espera 3 segundos entre mensajes para evitar límites
- **Formato**: Los mensajes usan Markdown, asegúrate de que tu canal lo soporte

---

**¿Necesitas ayuda?** Revisa los logs en Vercel → Functions → `/api/cron/daily-publish` para ver errores detallados.
