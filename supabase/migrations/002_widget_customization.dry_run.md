# 002_widget_customization.sql — Manual Verification Checklist

Run the migration against your Supabase project (SQL Editor or CLI),
then verify each item below.

- [ ] widgets.qualification_fields column exists, type jsonb
- [ ] widgets.qualification_rules column exists, type jsonb
- [ ] Existing widget rows (if any) now show the backfilled default qualification_fields array (4 objects: budget_range, campaign_type, timeline, call_time_pref), not an empty array
- [ ] Existing widget rows show the backfilled default qualification_rules object (min_budget: null, disqualify_if_under_min: false, priority_threshold: null, required_fields_for_complete: ["budget_range", "timeline"])
- [ ] leads.qualification_status column exists, type text, default 'qualified'
- [ ] CHECK constraint rejects an invalid value — try: `UPDATE leads SET qualification_status = 'bogus_value' WHERE false;` or insert a test row with qualification_status = 'bogus_value', confirm it's rejected
- [ ] A lead inserted without specifying qualification_status defaults to 'qualified'
- [ ] conversations table is completely unchanged (no new columns)
- [ ] No RLS policy errors — confirm an existing authenticated read against leads still works exactly as before
