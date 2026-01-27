-- Tabla para tracking de leads de Telegram
-- Ejecutar en Supabase SQL Editor

CREATE TABLE IF NOT EXISTS telegram_leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT,
    source TEXT DEFAULT 'unknown',
    utm_source TEXT,
    utm_campaign TEXT,
    utm_medium TEXT,
    subscribed BOOLEAN DEFAULT FALSE,
    subscribed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_telegram_leads_email ON telegram_leads(email);
CREATE INDEX IF NOT EXISTS idx_telegram_leads_source ON telegram_leads(source);
CREATE INDEX IF NOT EXISTS idx_telegram_leads_subscribed ON telegram_leads(subscribed);
CREATE INDEX IF NOT EXISTS idx_telegram_leads_created_at ON telegram_leads(created_at DESC);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at
CREATE TRIGGER update_telegram_leads_updated_at
    BEFORE UPDATE ON telegram_leads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios
COMMENT ON TABLE telegram_leads IS 'Leads capturados para suscripción a Telegram';
COMMENT ON COLUMN telegram_leads.source IS 'Fuente: landing, giveaway, popup, etc.';
COMMENT ON COLUMN telegram_leads.subscribed IS 'Si el usuario se ha suscrito realmente al canal';
