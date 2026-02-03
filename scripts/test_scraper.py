#!/usr/bin/env python3
"""
Script de testing para el scraper de Amazon
Verifica que el scraper funciona correctamente antes de integrarlo
"""

import sys
import os
import json
from pathlib import Path

# Añadir el scraper al path
sys.path.append(str(Path(__file__).parent.parent / "scraper"))


def test_scraper():
    """Prueba básica del scraper"""
    try:
        from amazon_scraper import FreeAmazonScraper

        print("🧪 Iniciando prueba del scraper...")

        # Crear instancia
        scraper = FreeAmazonScraper()

        # Probar búsqueda simple
        print("🔍 Probando búsqueda de 'tienda campaña'...")
        deals = scraper.scrape_category("tiendas-campana", max_pages=1)

        if deals:
            print(f"✅ Encontradas {len(deals)} ofertas")

            # Mostrar primera oferta como ejemplo
            if deals[0]:
                print(f"📋 Ejemplo: {deals[0]['title'][:50]}...")
                print(
                    f"💰 Precio: €{deals[0]['current_price']} (-{deals[0]['discount']}%)"
                )
                print(f"⭐ Rating: {deals[0].get('rating', 'N/A')}")

            return True
        else:
            print("❌ No se encontraron ofertas")
            return False

    except ImportError as e:
        print(f"❌ Error importando scraper: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False


def test_environment():
    """Verifica variables de entorno necesarias"""
    print("\n🔧 Verificando entorno...")

    # Verificar dependencias
    try:
        import requests
        import bs4

        print("✅ Dependencias básicas instaladas")
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        return False

    # Verificar variables de entorno Supabase (opcional)
    supabase_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

    if supabase_url and supabase_key:
        print("✅ Supabase configurado")
    else:
        print("⚠️ Supabase no configurado (modo local)")

    # Verificar Amazon partner tag
    partner_tag = os.environ.get("AMAZON_PARTNER_TAG", "camperdeals-21")
    print(f"🏷️ Amazon Partner Tag: {partner_tag}")

    return True


if __name__ == "__main__":
    print("🏕️ Test del Camping Deals Scraper")
    print("=" * 40)

    # Test de entorno
    env_ok = test_environment()

    if not env_ok:
        print("\n❌ Falló verificación de entorno")
        sys.exit(1)

    # Test del scraper
    scraper_ok = test_scraper()

    if scraper_ok:
        print("\n✅ Todos los tests pasaron")
        print("🚀 El scraper está listo para producción")
        sys.exit(0)
    else:
        print("\n❌ Falló test del scraper")
        print("🔧 Revisa la configuración y dependencias")
        sys.exit(1)
