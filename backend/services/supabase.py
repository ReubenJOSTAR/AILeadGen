"""Supabase client wrapper — two clients for different security contexts.

supabase_public: Uses the publishable (anon) key. Respects row-level security.
    Use for any read that should be scoped by RLS policies (e.g., dashboard
    queries where the caller is an authenticated user with a Supabase JWT).

supabase_admin: Uses the service-role key. Bypasses RLS entirely.
    Use for all backend writes (lead creation, conversation upserts) and
    any privileged read that must not be filtered by RLS.

Choosing the wrong client silently breaks things:
- Using supabase_public for writes → RLS blocks the insert, no error raised.
- Using supabase_admin for user-facing reads → bypasses security, leaks data.
"""

from supabase import create_client, Client
from config import settings

supabase_public: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
)

supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY,
)


async def check_connection() -> bool:
    """Verify Supabase is reachable by querying the widgets table."""
    try:
        supabase_admin.table("widgets").select("id").limit(1).execute()
        return True
    except Exception as e:
        raise ConnectionError(f"Supabase connection failed: {e}")
