import Database from 'better-sqlite3';
import path from 'path';
import { AmazonProduct, ProductCategory, DealStats } from './types';

const DB_PATH = process.env.DATABASE_PATH || path.join(process.cwd(), 'data', 'offers.db');

// Singleton para la conexión
let db: Database.Database | null = null;

export function getDatabase(): Database.Database {
    if (!db) {
        db = new Database(DB_PATH);
        db.pragma('journal_mode = WAL');
        initializeDatabase(db);
    }
    return db;
}

function initializeDatabase(database: Database.Database) {
    database.exec(`
    CREATE TABLE IF NOT EXISTS products (
      asin TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      description TEXT,
      image_url TEXT NOT NULL,
      category TEXT NOT NULL,
      original_price REAL NOT NULL,
      discounted_price REAL NOT NULL,
      discount_percentage INTEGER NOT NULL,
      affiliate_url TEXT NOT NULL,
      rating REAL,
      review_count INTEGER,
      is_prime INTEGER DEFAULT 0,
      last_updated TEXT NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_category ON products(category);
    CREATE INDEX IF NOT EXISTS idx_discount ON products(discount_percentage DESC);
    CREATE INDEX IF NOT EXISTS idx_last_updated ON products(last_updated DESC);
  `);
}

export function upsertProduct(product: AmazonProduct): void {
    const db = getDatabase();
    const stmt = db.prepare(`
    INSERT INTO products (
      asin, title, description, image_url, category,
      original_price, discounted_price, discount_percentage,
      affiliate_url, rating, review_count, is_prime, last_updated
    ) VALUES (
      @asin, @title, @description, @imageUrl, @category,
      @originalPrice, @discountedPrice, @discountPercentage,
      @affiliateUrl, @rating, @reviewCount, @isPrime, @lastUpdated
    )
    ON CONFLICT(asin) DO UPDATE SET
      title = excluded.title,
      description = excluded.description,
      image_url = excluded.image_url,
      original_price = excluded.original_price,
      discounted_price = excluded.discounted_price,
      discount_percentage = excluded.discount_percentage,
      affiliate_url = excluded.affiliate_url,
      rating = excluded.rating,
      review_count = excluded.review_count,
      is_prime = excluded.is_prime,
      last_updated = excluded.last_updated
  `);

    stmt.run({
        asin: product.asin,
        title: product.title,
        description: product.description || null,
        imageUrl: product.imageUrl,
        category: product.category,
        originalPrice: product.originalPrice,
        discountedPrice: product.discountedPrice,
        discountPercentage: product.discountPercentage,
        affiliateUrl: product.affiliateUrl,
        rating: product.rating || null,
        reviewCount: product.reviewCount || null,
        isPrime: product.isPrime ? 1 : 0,
        lastUpdated: product.lastUpdated.toISOString(),
    });
}

export function getProducts(options?: {
    category?: ProductCategory;
    minDiscount?: number;
    limit?: number;
    offset?: number;
}): AmazonProduct[] {
    const db = getDatabase();

    let query = 'SELECT * FROM products WHERE 1=1';
    const params: Record<string, unknown> = {};

    if (options?.category) {
        query += ' AND category = @category';
        params.category = options.category;
    }

    if (options?.minDiscount) {
        query += ' AND discount_percentage >= @minDiscount';
        params.minDiscount = options.minDiscount;
    }

    query += ' ORDER BY discount_percentage DESC, last_updated DESC';

    if (options?.limit) {
        query += ' LIMIT @limit';
        params.limit = options.limit;
    }

    if (options?.offset) {
        query += ' OFFSET @offset';
        params.offset = options.offset;
    }

    const stmt = db.prepare(query);
    const rows = stmt.all(params) as Record<string, unknown>[];

    return rows.map(mapRowToProduct);
}

export function getProductByAsin(asin: string): AmazonProduct | null {
    const db = getDatabase();
    const stmt = db.prepare('SELECT * FROM products WHERE asin = ?');
    const row = stmt.get(asin) as Record<string, unknown> | undefined;

    return row ? mapRowToProduct(row) : null;
}

export function getDealStats(): DealStats {
    const db = getDatabase();

    const stats = db.prepare(`
    SELECT 
      COUNT(*) as total_deals,
      AVG(discount_percentage) as avg_discount,
      MAX(discount_percentage) as max_discount,
      MAX(last_updated) as last_update
    FROM products
  `).get() as Record<string, unknown>;

    return {
        totalDeals: (stats.total_deals as number) || 0,
        avgDiscount: Math.round((stats.avg_discount as number) || 0),
        maxDiscount: (stats.max_discount as number) || 0,
        lastUpdate: stats.last_update ? new Date(stats.last_update as string) : new Date(),
    };
}

export function deleteOldProducts(daysOld: number = 7): number {
    const db = getDatabase();
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysOld);

    const stmt = db.prepare('DELETE FROM products WHERE last_updated < ?');
    const result = stmt.run(cutoffDate.toISOString());

    return result.changes;
}

function mapRowToProduct(row: Record<string, unknown>): AmazonProduct {
    return {
        asin: row.asin as string,
        title: row.title as string,
        description: row.description as string | undefined,
        imageUrl: row.image_url as string,
        category: row.category as ProductCategory,
        originalPrice: row.original_price as number,
        discountedPrice: row.discounted_price as number,
        discountPercentage: row.discount_percentage as number,
        affiliateUrl: row.affiliate_url as string,
        rating: row.rating as number | undefined,
        reviewCount: row.review_count as number | undefined,
        isPrime: Boolean(row.is_prime),
        lastUpdated: new Date(row.last_updated as string),
    };
}
