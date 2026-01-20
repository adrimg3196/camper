#!/usr/bin/env python3
"""
Camping Deals - Cliente Supabase
Base de datos gratuita en la nube (500MB gratis)
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Supabase es opcional - si no está disponible, usamos JSON local
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("⚠️ supabase no instalado. Usando almacenamiento JSON local.")


class FreeDatabase:
    """Cliente de base de datos gratuito (Supabase o JSON fallback)"""
    
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_ANON_KEY')
        self.client: Optional[Client] = None
        
        if HAS_SUPABASE and self.supabase_url and self.supabase_key:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                print("✅ Conectado a Supabase")
            except Exception as e:
                print(f"⚠️ Error conectando a Supabase: {e}")
                self.client = None
        
        self.local_db_path = 'data/deals_db.json'
    
    def _load_local_db(self) -> List[Dict]:
        """Carga base de datos local JSON"""
        try:
            with open(self.local_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_local_db(self, deals: List[Dict]):
        """Guarda base de datos local JSON"""
        os.makedirs(os.path.dirname(self.local_db_path), exist_ok=True)
        with open(self.local_db_path, 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=2)
    
    def insert_deals(self, deals: List[Dict]) -> int:
        """Inserta ofertas en la base de datos (upsert)"""
        if self.client:
            return self._insert_supabase(deals)
        else:
            return self._insert_local(deals)
    
    def _insert_supabase(self, deals: List[Dict]) -> int:
        """Inserta en Supabase"""
        inserted = 0
        
        for deal in deals:
            try:
                # Verificar si existe
                existing = self.client.table('deals').select('asin').eq('asin', deal['asin']).execute()
                
                deal_data = {
                    'asin': deal['asin'],
                    'title': deal['title'],
                    'image_url': deal.get('image_url'),
                    'category': deal['category'],
                    'current_price': deal['current_price'],
                    'original_price': deal['original_price'],
                    'discount': deal['discount'],
                    'affiliate_url': deal['affiliate_url'],
                    'rating': deal.get('rating'),
                    'review_count': deal.get('review_count'),
                    'is_prime': deal.get('is_prime', False),
                    'updated_at': datetime.now().isoformat(),
                }
                
                if existing.data:
                    # Update
                    self.client.table('deals').update(deal_data).eq('asin', deal['asin']).execute()
                else:
                    # Insert
                    deal_data['created_at'] = datetime.now().isoformat()
                    self.client.table('deals').insert(deal_data).execute()
                    inserted += 1
                    
            except Exception as e:
                print(f"⚠️ Error insertando {deal['asin']}: {e}")
        
        print(f"💾 Supabase: {inserted} nuevas ofertas insertadas")
        return inserted
    
    def _insert_local(self, deals: List[Dict]) -> int:
        """Inserta en JSON local"""
        existing = self._load_local_db()
        existing_asins = {d['asin'] for d in existing}
        
        new_deals = []
        for deal in deals:
            if deal['asin'] not in existing_asins:
                deal['created_at'] = datetime.now().isoformat()
                new_deals.append(deal)
            else:
                # Actualizar existente
                for i, ex in enumerate(existing):
                    if ex['asin'] == deal['asin']:
                        deal['created_at'] = ex.get('created_at', datetime.now().isoformat())
                        deal['updated_at'] = datetime.now().isoformat()
                        existing[i] = deal
                        break
        
        existing.extend(new_deals)
        self._save_local_db(existing)
        
        print(f"💾 Local: {len(new_deals)} nuevas ofertas insertadas")
        return len(new_deals)
    
    def get_deals(self, category: Optional[str] = None, min_discount: int = 30, limit: int = 50) -> List[Dict]:
        """Obtiene ofertas filtradas"""
        if self.client:
            return self._get_supabase(category, min_discount, limit)
        else:
            return self._get_local(category, min_discount, limit)
    
    def _get_supabase(self, category: Optional[str], min_discount: int, limit: int) -> List[Dict]:
        """Obtiene de Supabase"""
        query = self.client.table('deals').select('*').gte('discount', min_discount)
        
        if category:
            query = query.eq('category', category)
        
        query = query.order('discount', desc=True).limit(limit)
        
        result = query.execute()
        return result.data if result.data else []
    
    def _get_local(self, category: Optional[str], min_discount: int, limit: int) -> List[Dict]:
        """Obtiene de JSON local"""
        deals = self._load_local_db()
        
        # Filtrar
        filtered = [d for d in deals if d.get('discount', 0) >= min_discount]
        
        if category:
            filtered = [d for d in filtered if d.get('category') == category]
        
        # Ordenar por descuento
        filtered.sort(key=lambda x: x.get('discount', 0), reverse=True)
        
        return filtered[:limit]
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la base de datos"""
        if self.client:
            try:
                result = self.client.table('deals').select('discount').execute()
                deals = result.data if result.data else []
            except:
                deals = []
        else:
            deals = self._load_local_db()
        
        if not deals:
            return {'total': 0, 'avg_discount': 0, 'max_discount': 0}
        
        discounts = [d.get('discount', 0) for d in deals]
        
        return {
            'total': len(deals),
            'avg_discount': round(sum(discounts) / len(discounts)),
            'max_discount': max(discounts),
        }
    
    def delete_old_deals(self, days: int = 7) -> int:
        """Elimina ofertas antiguas"""
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        if self.client:
            try:
                result = self.client.table('deals').delete().lt('updated_at', cutoff).execute()
                deleted = len(result.data) if result.data else 0
            except:
                deleted = 0
        else:
            deals = self._load_local_db()
            original_count = len(deals)
            deals = [d for d in deals if d.get('updated_at', d.get('created_at', '')) >= cutoff]
            self._save_local_db(deals)
            deleted = original_count - len(deals)
        
        print(f"🗑️ Eliminadas {deleted} ofertas antiguas")
        return deleted


# SQL para crear tabla en Supabase (ejecutar en Dashboard)
SUPABASE_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS deals (
    id SERIAL PRIMARY KEY,
    asin TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    image_url TEXT,
    category TEXT NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2) NOT NULL,
    discount INTEGER NOT NULL,
    affiliate_url TEXT NOT NULL,
    rating DECIMAL(2,1),
    review_count INTEGER,
    is_prime BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_deals_category ON deals(category);
CREATE INDEX IF NOT EXISTS idx_deals_discount ON deals(discount DESC);
"""


if __name__ == '__main__':
    # Test
    db = FreeDatabase()
    print("\n📊 Estadísticas actuales:")
    print(db.get_stats())
