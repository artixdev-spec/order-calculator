-- Схема и начальные промокоды. Выполняется PostgreSQL при первом создании volume.
CREATE TABLE IF NOT EXISTS promo_codes (
    code         TEXT PRIMARY KEY,
    kind         TEXT NOT NULL CHECK (kind IN ('percent', 'fixed')),
    value        NUMERIC(12, 2) NOT NULL CHECK (value >= 0),
    min_subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (min_subtotal >= 0)
);

INSERT INTO promo_codes (code, kind, value, min_subtotal) VALUES
    ('STUDENT10', 'percent', 10, 0),
    ('WELCOME200', 'fixed', 200, 1000),
    ('BIGORDER15', 'percent', 15, 5000)
ON CONFLICT (code) DO NOTHING;
