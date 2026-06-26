-- ============================================================
-- Migration 002: Widget customization columns
-- ============================================================
--
-- Additive only — run after 001_init.sql has been applied.
-- Does not modify or drop any existing columns or policies.
--
-- Adds per-widget customization of qualification questions and
-- scoring rules, plus a lead-level qualification status column.
-- Motivation: marketing team research showed qualification
-- criteria vary per agency client — a one-size-fits-all field
-- list doesn't work. These columns let each widget define its
-- own qualification questions and basic scoring thresholds.
--
-- This migration should be run exactly once on the live project.
-- ============================================================

-- ===================
-- 1. WIDGETS TABLE — new columns
-- ===================

ALTER TABLE widgets
    ADD COLUMN IF NOT EXISTS qualification_fields jsonb DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS qualification_rules  jsonb DEFAULT '{}'::jsonb;

-- Backfill existing widget rows with the V1 default field set.
-- Why a two-step approach (column default is empty, then explicit backfill):
-- The SQL-level default is '[]' so that a future INSERT can explicitly opt
-- into a truly empty field set if needed. But any widget that currently has
-- the empty default should get the standard V1 fields so it doesn't silently
-- lose qualification behavior the moment this migration runs.
-- This UPDATE is idempotent — the WHERE clause ensures it only touches rows
-- still at the empty-array default, never overwriting real custom config.

UPDATE widgets
SET qualification_fields = '[
    {"key": "budget_range", "label": "Budget range", "required": true},
    {"key": "campaign_type", "label": "Campaign type", "required": true},
    {"key": "timeline", "label": "Timeline", "required": true},
    {"key": "call_time_pref", "label": "Preferred call time", "required": true}
]'::jsonb
WHERE qualification_fields = '[]'::jsonb;

-- Backfill default qualification_rules for the same reason.
-- null thresholds = "no minimum enforced" = every completed conversation
-- is simply "qualified" — customization is opt-in, not opt-out.

UPDATE widgets
SET qualification_rules = '{
    "min_budget": null,
    "disqualify_if_under_min": false,
    "priority_threshold": null,
    "required_fields_for_complete": ["budget_range", "timeline"]
}'::jsonb
WHERE qualification_rules = '{}'::jsonb;

-- ===================
-- 2. LEADS TABLE — new column
-- ===================

-- Clarification of the two status columns on leads:
-- status: sales pipeline state (new/reviewed/contacted/lost)
-- qualification_status: lead quality assessment (qualified/low_priority/
--   disqualified) — set once at creation time based on qualification_rules,
--   independent of pipeline state

ALTER TABLE leads
    ADD COLUMN IF NOT EXISTS qualification_status text DEFAULT 'qualified';

-- CHECK constraint for qualification_status values.
-- Using DO block to make this idempotent — skips if the constraint exists.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'leads_qualification_status_check'
    ) THEN
        ALTER TABLE leads
            ADD CONSTRAINT leads_qualification_status_check
            CHECK (qualification_status IN ('qualified', 'low_priority', 'disqualified'));
    END IF;
END
$$;
