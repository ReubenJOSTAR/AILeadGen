-- ============================================================
-- Migration 001: Initial schema for LeadQualify
-- ============================================================
--
-- Creates three tables: widgets, leads, conversations
-- plus indexes and Row Level Security policies.
--
-- RLS simplification (V1):
--   leads and conversations use a simple "authenticated users
--   can SELECT all rows" policy. This is acceptable because V1
--   is a single-agency MVP — there is only one widget owner.
--   For multi-tenant SaaS, replace with ownership-based policies
--   that match widget.owner_email against auth.jwt()->>'email'.
--
-- Backend writes (INSERT/UPDATE) use SUPABASE_SERVICE_KEY, which
-- bypasses RLS entirely. No INSERT/UPDATE RLS policies are needed
-- for the authenticated role — only the service role writes.
--
-- This is migration 001. Future schema changes go in
-- 002_xxx.sql, 003_xxx.sql, etc. Never edit this file once
-- it has been run against a live Supabase project.
-- ============================================================

-- ===================
-- 1. TABLES
-- ===================

CREATE TABLE IF NOT EXISTS widgets (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name         text NOT NULL,
    owner_email  text NOT NULL,
    greeting     text DEFAULT 'Hi! How can I help you today?',
    brand_color  text DEFAULT '#534AB7',
    agent_name   text DEFAULT 'Assistant',
    created_at   timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS leads (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    widget_id       uuid NOT NULL REFERENCES widgets(id),
    session_id      text NOT NULL,
    name            text,
    email           text,
    phone           text,
    company         text,
    budget_range    text,
    campaign_type   text,
    timeline        text,
    call_time_pref  text,
    requirements    text,
    status          text DEFAULT 'new'
                    CHECK (status IN ('new', 'reviewed', 'contacted', 'lost')),
    raw_summary     text,
    created_at      timestamptz DEFAULT now(),
    updated_at      timestamptz DEFAULT now(),
    CONSTRAINT leads_session_id_unique UNIQUE (session_id)
);

CREATE TABLE IF NOT EXISTS conversations (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id     uuid NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    messages    jsonb NOT NULL DEFAULT '[]'::jsonb,
    updated_at  timestamptz DEFAULT now()
);

-- ===================
-- 2. INDEXES
-- ===================

CREATE INDEX IF NOT EXISTS idx_leads_widget_id  ON leads(widget_id);
CREATE INDEX IF NOT EXISTS idx_leads_status      ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at  ON leads(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_lead_id ON conversations(lead_id);

-- ===================
-- 3. ROW LEVEL SECURITY
-- ===================

-- widgets: RLS intentionally DISABLED.
-- The embed script fetches widget config via GET /widget/:id with no auth
-- token (visitors are unauthenticated), so anon SELECT must work.

-- leads: RLS enabled.
-- Authenticated dashboard users can read all leads (V1 single-agency simplification).
-- Writes come from the backend using SUPABASE_SERVICE_KEY (service role),
-- which bypasses RLS — no INSERT/UPDATE policy needed for authenticated role.
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Note: DROP POLICY IF EXISTS is not standard SQL but is supported by
-- PostgreSQL 9.5+. This migration should only be run once on a fresh project.
CREATE POLICY leads_select_authenticated
    ON leads
    FOR SELECT
    TO authenticated
    USING (true);

-- conversations: RLS enabled, same pattern as leads.
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY conversations_select_authenticated
    ON conversations
    FOR SELECT
    TO authenticated
    USING (true);
