"""
DEV-ONLY test script for 2.1 Claude service.
Verifies build_system_prompt() generates dynamic prompts and
get_claude_reply() returns correctly shaped responses.
Not part of the production app — safe to delete.
"""

import asyncio
from services.claude import build_system_prompt, get_claude_reply

# --- Widget config #1: default qualification fields (matches 1.5 backfill) ---
widget_config_default = {
    "name": "Acme Digital Agency",
    "agent_name": "Sophie",
    "greeting": "Hi there! I'd love to learn about your project.",
    "brand_color": "#4F46E5",
    "qualification_fields": [
        {"key": "budget_range", "label": "Budget range", "required": True},
        {"key": "campaign_type", "label": "Campaign type", "required": True},
        {"key": "timeline", "label": "Timeline", "required": True},
        {"key": "call_time_pref", "label": "Preferred call time", "required": True},
    ],
    "qualification_rules": {
        "min_budget": None,
        "disqualify_if_under_min": False,
        "priority_threshold": None,
        "required_fields_for_complete": ["budget_range", "timeline"],
    },
}

# --- Widget config #2: custom fields NOT in the default set ---
widget_config_custom = {
    "name": "Stellar Content Studio",
    "agent_name": "Max",
    "greeting": "Welcome! Let's chat about your content needs.",
    "brand_color": "#10B981",
    "qualification_fields": [
        {"key": "audience_size", "label": "Target audience size", "required": True},
        {"key": "prior_agency", "label": "Prior agency experience", "required": False},
    ],
    "qualification_rules": {
        "min_budget": None,
        "disqualify_if_under_min": False,
        "priority_threshold": None,
        "required_fields_for_complete": ["audience_size"],
    },
}


def test_prompt_generation():
    print("=" * 70)
    print("WIDGET CONFIG #1 — Default fields (budget_range, campaign_type, etc.)")
    print("=" * 70)
    prompt1 = build_system_prompt(widget_config_default)
    print(prompt1)

    print("\n" + "=" * 70)
    print("WIDGET CONFIG #2 — Custom fields (audience_size, prior_agency)")
    print("=" * 70)
    prompt2 = build_system_prompt(widget_config_custom)
    print(prompt2)

    # Sanity checks
    assert "budget_range" in prompt1
    assert "campaign_type" in prompt1
    assert "audience_size" not in prompt1

    assert "audience_size" in prompt2
    assert "prior_agency" in prompt2
    assert "budget_range" not in prompt2

    print("\n[PASS] Both prompts correctly reflect their respective fields.")


async def test_live_api_call():
    print("\n" + "=" * 70)
    print("LIVE API CALL — Widget config #2, __OPEN__ sentinel")
    print("=" * 70)
    raw_reply = await get_claude_reply(
        widget_config=widget_config_custom,
        conversation_history=[],
        new_message="__OPEN__",
    )
    print(raw_reply)

    # Verify the extract block has the right keys
    assert "audience_size" in raw_reply, "Missing audience_size in extract block"
    assert "prior_agency" in raw_reply, "Missing prior_agency in extract block"
    if "budget_range" in raw_reply:
        print("\n[WARN] budget_range found in response -- prompt builder may be leaking defaults!")
    else:
        print("\n[PASS] Response correctly uses custom fields, no default field leakage.")


if __name__ == "__main__":
    test_prompt_generation()
    asyncio.run(test_live_api_call())
