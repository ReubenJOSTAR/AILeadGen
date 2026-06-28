from anthropic import AsyncAnthropic
from config import settings

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

OPENING_SENTINEL = "__OPEN__"


def build_system_prompt(widget_config: dict) -> str:
    agent_name = widget_config.get("agent_name", "Assistant")
    widget_name = widget_config.get("name", "our company")
    greeting = widget_config.get("greeting", "")
    qualification_fields = widget_config.get("qualification_fields", [])

    # --- Section 1: Role framing ---
    prompt = (
        f"You are {agent_name}, a warm and professional assistant for "
        f"{widget_name}. Your job is to have a natural conversation with "
        f"website visitors to understand their needs, so the team can "
        f"prepare well for a discovery call.\n\n"
    )

    # --- Section 2: Opening greeting guidance ---
    if greeting:
        prompt += (
            f"When starting a new conversation, use this as inspiration "
            f"for your opening message (rephrase naturally, don't copy "
            f"verbatim): \"{greeting}\"\n\n"
        )

    # --- Section 3: Universal fields (always collected) ---
    prompt += (
        "INFORMATION TO COLLECT\n"
        "=====================\n\n"
        "Always collect these (required for every conversation):\n"
        "- Visitor's name\n"
        "- Email address\n"
        "- Phone number\n\n"
    )

    # --- Section 4: Custom fields from widget config ---
    if qualification_fields:
        prompt += "Also collect these qualification details:\n"
        for field in qualification_fields:
            label = field["label"]
            required = field.get("required", False)
            if required:
                prompt += (
                    f"- {label} (required — this is important, ask clearly "
                    f"and follow up if the answer is vague)\n"
                )
            else:
                prompt += (
                    f"- {label} (optional — don't push hard if they "
                    f"don't know)\n"
                )
        prompt += "\n"

    # --- Section 5: Behavioral rules ---
    prompt += (
        "CONVERSATION RULES\n"
        "==================\n\n"
        "- Ask one question at a time, never two things in one message.\n"
        "- Keep messages short, 2-3 sentences max.\n"
        "- If a budget-related field gets a vague answer (\"depends\", "
        "\"not sure\"), push back once with concrete ranges before "
        "moving on.\n"
        "- When all required fields are collected, wrap up warmly — "
        "tell the visitor someone will reach out, typically within "
        "24 hours.\n\n"
    )

    # --- Section 6: Extraction instruction block ---
    # Build the JSON template dynamically from universal + custom fields
    extract_keys = ["name", "email", "phone"]
    for field in qualification_fields:
        extract_keys.append(field["key"])
    extract_keys.append("is_complete")

    json_template = "{\n"
    for key in extract_keys:
        default = "false" if key == "is_complete" else "null"
        json_template += f'  "{key}": {default},\n'
    json_template = json_template.rstrip(",\n") + "\n}"

    # Determine which fields are required for is_complete
    required_fields = ["name", "email", "phone"]
    for field in qualification_fields:
        if field.get("required", False):
            required_fields.append(field["key"])

    prompt += (
        "EXTRACTION\n"
        "==========\n\n"
        "After EVERY message you send, append a JSON block (hidden from "
        "the user) in this exact format:\n\n"
        f"<extract>\n{json_template}\n</extract>\n\n"
        "Fill in only what you know so far. Set is_complete to true only "
        "when ALL required fields are filled.\n"
        f"Required fields for this conversation: "
        f"{', '.join(required_fields)}.\n"
    )

    return prompt


async def get_claude_reply(
    widget_config: dict,
    conversation_history: list,
    new_message: str,
) -> str:
    system = build_system_prompt(widget_config)

    if new_message == OPENING_SENTINEL:
        messages = [{"role": "user", "content": "Hi"}]
    else:
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in conversation_history
        ]
        messages.append({"role": "user", "content": new_message})

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system,
        messages=messages,
    )

    return response.content[0].text
