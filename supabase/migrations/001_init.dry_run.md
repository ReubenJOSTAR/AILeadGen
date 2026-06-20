# 001_init.sql — Manual Verification Checklist

Run the migration against your Supabase project (SQL Editor or CLI),
then verify each item below.

- [ ] All three tables created without error (widgets, leads, conversations)
- [ ] Foreign keys enforced — try inserting a lead with a fake widget_id, confirm it's rejected
- [ ] session_id unique constraint works — try inserting two leads with the same session_id, confirm second fails
- [ ] CHECK constraint on leads.status works — try inserting a lead with status = 'invalid', confirm it's rejected
- [ ] RLS is enabled on leads and conversations (Supabase dashboard Table Editor shows a lock icon)
- [ ] RLS is NOT enabled on widgets (anon key should be able to SELECT from widgets without auth)
- [ ] All 4 indexes exist (check via Supabase dashboard Database > Indexes):
  - idx_leads_widget_id
  - idx_leads_status
  - idx_leads_created_at
  - idx_conversations_lead_id
- [ ] Authenticated user can SELECT from leads and conversations
- [ ] Anon user CANNOT select from leads or conversations (RLS blocks it)
