#!/usr/bin/env python3
"""
API Wrapper para el scraper de Amazon
Conecta el scraper con la API de Next.js
"""

import sys
import os
import json
import asyncio
import subprocess
from typing import Dict, List
from pathlib import Path

# Añadir el scraper al path
sys.path.append(str(Path(__file__).parent / "scraper"))

from amazon_scraper import FreeAmazonScraper
from supabase import create_client
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperAPI:
    def __init__(self):
        self.scraper = FreeAmazonScraper()

        # Configurar Supabase desde variables de entorno
        self.supabase_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        self.supabase_key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

        if self.supabase_url and self.supabase_key:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        else:
            logger.warning("⚠️ Supabase no configurado. Usando modo local.")
            self.supabase = None

    async def scrape_and_save(self, category: str = None) -> Dict:
        """
        Scrapea ofertas y las guarda en Supabase/GCS
        """
        try:
            logger.info("🚀 Iniciando scraping de ofertas...")

            # Ejecutar scraper
            if category:
                deals = self.scraper.scrape_category(category, max_pages=2)
            else:
                deals = self.scraper.scrape_all_categories()

            logger.info(f"📦 Se encontraron {len(deals)} ofertas")

            # Transformar datos al formato de la base de datos
            formatted_deals = []
            for deal in deals:
                formatted_deal = {
                    "asin": deal["asin"],
                    "title": deal["title"],
                    "description": f"{deal['title']} - {deal.get('category', 'camping')}",
                    "price": deal["current_price"],
                    "original_price": deal["original_price"],
                    "discount": deal["discount"],
                    "image_url": deal["image_url"],
                    "url": f"https://www.amazon.es/dp/{deal['asin']}",
                    "affiliate_url": deal["affiliate_url"],
                    "category": deal["category"],
                    "rating": deal.get("rating"),
                    "review_count": deal.get("review_count"),
                    "is_active": True,
                }
                formatted_deals.append(formatted_deal)

            # Guardar en Supabase si está configurado
            results = {"inserted": 0, "updated": 0, "errors": 0}

            if self.supabase:
                for deal in formatted_deals:
                    try:
                        deal["updated_at"] = os.environ.get("SCRAPE_TIME", "now")

                        result = (
                            self.supabase.table("deals")
                            .upsert(deal, on_conflict="asin")
                            .execute()
                        )

                        if result.data:
                            results["inserted"] += 1
                        else:
                            results["errors"] += 1

                    except Exception as e:
                        logger.error(f"❌ Error guardando deal {deal['asin']}: {e}")
                        results["errors"] += 1
            else:
                # Modo local: guardar en archivo JSON
                output_path = Path(__file__).parent / "data" / "latest_deals.json"
                output_path.parent.mkdir(exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "timestamp": os.environ.get("SCRAPE_TIME", "now"),
                            "total_deals": len(formatted_deals),
                            "deals": formatted_deals,
                        },
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )

                logger.info(f"💾 Datos guardados en {output_path}")
                results["inserted"] = len(formatted_deals)

            # Desactivar ofertas antiguas si hay Supabase
            if self.supabase:
                try:
                    seven_days_ago = os.environ.get("SEVEN_DAYS_AGO", "2025-01-01")

                    old_deals = (
                        self.supabase.table("deals")
                        .update({"is_active": False})
                        .lt("updated_at", seven_days_ago)
                        .execute()
                    )

                    results["deactivated"] = (
                        len(old_deals.data) if old_deals.data else 0
                    )

                except Exception as e:
                    logger.error(f"❌ Error desactivando ofertas antiguas: {e}")

            return {
                "success": True,
                "total_found": len(deals),
                "total_saved": results["inserted"],
                "errors": results["errors"],
                "deactivated": results.get("deactivated", 0),
                "category": category,
                "timestamp": os.environ.get("SCRAPE_TIME", "now"),
            }

        except Exception as e:
            logger.error(f"❌ Error en scraping: {e}")
            return {
                "success": False,
                "error": str(e),
                "category": category,
                "timestamp": os.environ.get("SCRAPE_TIME", "now"),
            }

    def test_scraper(self) -> Dict:
        """Prueba rápida del scraper"""
        try:
            # Probar una categoría con 1 página
            deals = self.scraper.scrape_category("tiendas-campana", max_pages=1)

            return {
                "success": True,
                "test_deals_found": len(deals),
                "sample_deal": deals[0] if deals else None,
                "message": "Scraper funciona correctamente",
            }

        except Exception as e:
            return {"success": False, "error": str(e), "message": "Error en el scraper"}


async def main():
    """Función principal para ejecutar desde línea de comandos"""
    import argparse

    parser = argparse.ArgumentParser(description="Camping Deals Scraper API")
    parser.add_argument("--category", type=str, help="Categoría específica")
    parser.add_argument("--test", action="store_true", help="Modo prueba")
    parser.add_argument("--output", type=str, help="Archivo de salida JSON")

    args = parser.parse_args()

    api = ScraperAPI()

    if args.test:
        result = api.test_scraper()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        result = await api.scrape_and_save(args.category)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Si se especificó output, guardar también allí
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
