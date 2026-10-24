-- =============================================================================
-- S&R CoreSync — D1 schema (initial)
-- Apply with:
--   npx wrangler d1 create sr-coresync
--   npx wrangler d1 execute sr-coresync --remote --file=migrations/0001_init.sql
-- =============================================================================

-- Leads: the durable business record. KV remains the fast path/fallback, but
-- KV cannot answer "how many leads this month, grouped by package" and it
-- expires entries, so D1 is the system of record.
CREATE TABLE IF NOT EXISTS leads (
    lead_id       TEXT PRIMARY KEY,
    client_name   TEXT,
    company_name  TEXT,
    email         TEXT,
    phone         TEXT,
    package       TEXT,
    notes         TEXT,
    language      TEXT,
    channel       TEXT,
    source_url    TEXT,
    received_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_leads_received ON leads (received_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_email    ON leads (email);

-- Payments: every webhook event we accept, with the verified provider state.
CREATE TABLE IF NOT EXISTS payments (
    provider     TEXT NOT NULL,
    payment_id   TEXT NOT NULL,
    status       TEXT,
    amount       TEXT,
    currency     TEXT,
    payload      TEXT,
    received_at  TEXT,
    PRIMARY KEY (provider, payment_id)
);

CREATE INDEX IF NOT EXISTS idx_payments_received ON payments (received_at DESC);

-- Consent log: GDPR evidence. One row per explicit opt-in, never overwritten.
CREATE TABLE IF NOT EXISTS consents (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    subject      TEXT NOT NULL,
    purpose      TEXT NOT NULL,
    granted      INTEGER NOT NULL,
    source_url   TEXT,
    created_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_consents_subject ON consents (subject);
