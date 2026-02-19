import schedule
import time
import logging
from functools import wraps
from scraper.amazon import AmazonScraper
from database.client import SupabaseManager
from content.enhancer import ContentEnhancer
from social.manager import SocialManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries=2, backoff_base=2, exceptions=(Exception,)):
    """Decorator that retries a function with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    wait_time = backoff_base ** attempt
                    logger.warning(f"Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator


def job():
    print("\n⏰ Iniciando ciclo de búsqueda de ofertas...")

    # 1. Inicializar componentes
    scraper = AmazonScraper()
    db = SupabaseManager()
    enhancer = ContentEnhancer()
    social = SocialManager()

    # 2. Buscar ofertas
    deals = scraper.search_deals()

    if not deals:
        print("🤷‍♂️ No se encontraron ofertas nuevas en este ciclo.")
        return

    print(f"💰 Procesando {len(deals)} ofertas encontradas...")

    # 3. Guardar y Publicar (with per-deal error handling)
    successful = 0
    failed_deals = []

    for deal in deals:
        deal_id = deal.get('id', 'unknown')
        deal_title = deal.get('title', 'Sin título')[:50]

        try:
            # Mejora con IA
            enhanced_deal = enhancer.enhance_product(deal)

            # Guardar en DB
            saved_deal = db.save_deal(enhanced_deal)

            # Publicar en Redes (with retry)
            @retry_with_backoff(max_retries=2)
            def publish_deal():
                social.process_deal(enhanced_deal)

            publish_deal()

            successful += 1
            logger.info(f"✅ Procesado exitosamente: {deal_title}")

        except Exception as e:
            logger.error(f"❌ Error procesando deal '{deal_title}': {e}")
            failed_deals.append({'id': deal_id, 'title': deal_title, 'error': str(e)})
            # Continue with next deal instead of crashing
            continue

    # Summary
    print(f"\n📊 Resumen: {successful}/{len(deals)} ofertas procesadas exitosamente")
    if failed_deals:
        print(f"⚠️  {len(failed_deals)} ofertas fallaron:")
        for fd in failed_deals:
            print(f"   - {fd['title']}: {fd['error'][:100]}")

    # Close social manager resources
    try:
        social.close()
    except Exception:
        pass

    print("✅ Ciclo completado. Esperando siguiente ejecución...")

if __name__ == "__main__":
    import os

    print("🚀 Iniciando Bot de Automatización 'Adventure Deals'...")

    # Configuración de frecuencia (horas entre ejecuciones)
    RUN_INTERVAL_HOURS = int(os.getenv("RUN_INTERVAL_HOURS", "6"))

    # En CI/CD (GitHub Actions), ejecutar una sola vez y salir
    if os.getenv("CI"):
        print("📍 Modo CI detectado - ejecución única")
        job()
        print("✅ Ejecución completada. Saliendo...")
    else:
        # Modo servidor (Render, local, etc): loop continuo
        print(f"📍 Modo servidor - ejecutando cada {RUN_INTERVAL_HOURS} horas")
        job()  # Ejecutar inmediatamente al iniciar
        schedule.every(RUN_INTERVAL_HOURS).hours.do(job)

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Revisar cada minuto (más eficiente)
        except KeyboardInterrupt:
            print("\n👋 Bot detenido manualmente.")
