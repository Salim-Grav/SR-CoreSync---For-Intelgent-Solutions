-- =============================================================================
-- S&R CoreSync — notification status on leads
-- A lead must never be "saved but silently unannounced". Every record carries
-- the outcome of its alert attempt so the weekly report can surface a channel
-- failure instead of a log line nobody reads.
--   npx wrangler d1 execute sr-coresync --remote --file=migrations/0002_notify_status.sql
-- =============================================================================

ALTER TABLE leads ADD COLUMN notify_status TEXT;
ALTER TABLE leads ADD COLUMN notified_at TEXT;

CREATE INDEX IF NOT EXISTS idx_leads_notify ON leads (notify_status);
