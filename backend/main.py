import schedule
import time
from scraper.amazon import AmazonScraper
from database.client import SupabaseManager
from content.enhancer import ContentEnhancer
from social.manager import SocialManager

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

    # 3. Guardar y Publicar
    for deal in deals:
        # Mejora con IA
        enhanced_deal = enhancer.enhance_product(deal)
        
        # Guardar en DB
        saved_deal = db.save_deal(enhanced_deal)
        
        # Publicar en Redes
        social.process_deal(enhanced_deal)
        
    print("✅ Ciclo completado. Esperando siguiente ejecución...")

if __name__ == "__main__":
    print("🚀 Iniciando Bot de Automatización 'Adventure Deals'...")
    
    # Ejecutar inmediatamente al arrancar
    job()
    
    # Programar cada 6 horas
    schedule.every(6).hours.do(job)
    
    # Mantener vivo el proceso
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Bot detenido manualmente.")
