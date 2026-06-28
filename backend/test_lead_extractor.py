"""Dev-only test script for services/lead_extractor.py — not production code."""

from services.lead_extractor import extract_from_reply, is_conversation_complete

print("=" * 60)
print("TEST 1: Normal case with custom fields")
print("=" * 60)
raw = (
    "Great to meet you! I'd love to learn more about your marketing needs. "
    "Could you tell me a bit about your target audience size?\n\n"
    '<extract>{"name": null, "email": null, "phone": null, '
    '"audience_size": null, "prior_agency_experience": null, '
    '"is_complete": false}</extract>'
)
clean, data = extract_from_reply(raw)
print(f"clean_reply: {clean!r}")
print(f"extracted_data: {data}")
assert "<extract>" not in clean
assert "audience_size" in data
assert "prior_agency_experience" in data
assert data["is_complete"] is False
print("[PASS]\n")

print("=" * 60)
print("TEST 2: Missing <extract> block")
print("=" * 60)
raw2 = "Hello! How can I help you today?"
clean2, data2 = extract_from_reply(raw2)
print(f"clean_reply: {clean2!r}")
print(f"extracted_data: {data2}")
assert clean2 == raw2.strip()
assert data2 == {}
print("[PASS]\n")

print("=" * 60)
print("TEST 3: Malformed JSON inside <extract>")
print("=" * 60)
raw3 = 'Some reply text\n<extract>{"name": "test",}</extract>'
clean3, data3 = extract_from_reply(raw3)
print(f"clean_reply: {clean3!r}")
print(f"extracted_data: {data3}")
assert clean3 == "Some reply text"
assert data3 == {}
print("[PASS]\n")

print("=" * 60)
print("TEST 4: is_conversation_complete variations")
print("=" * 60)
cases = [
    ({"is_complete": True}, True),
    ({"is_complete": False}, False),
    ({}, False),
    ({"is_complete": "true"}, True),
    ({"is_complete": "false"}, False),
]
for input_data, expected in cases:
    result = is_conversation_complete(input_data)
    status = "PASS" if result == expected else "FAIL"
    print(f"  {input_data!r} -> {result} (expected {expected}) [{status}]")
    assert result == expected
print("[ALL PASS]\n")

print("All tests passed.")
