from fastapi import APIRouter, HTTPException

from models.conversation import ChatRequest, ChatResponse
from services.claude import get_claude_reply
from services.lead_extractor import extract_from_reply, is_conversation_complete
from services.supabase import supabase_admin

router = APIRouter()


async def get_widget_config(widget_id: str) -> dict:
    result = supabase_admin.table("widgets").select("*").eq("id", widget_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail=f"Widget not found: {widget_id}")
    return result.data[0]


async def save_completed_lead(widget_id: str, session_id: str, extracted_data: dict):
    print(f"[PLACEHOLDER] Lead complete for widget {widget_id}, "
          f"session {session_id}. Data: {extracted_data}. "
          f"Persistence not yet implemented — see component 2.5.")


@router.post("", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    widget_config = await get_widget_config(body.widget_id)

    try:
        raw_reply = await get_claude_reply(
            widget_config=widget_config,
            conversation_history=[m.model_dump() for m in body.conversation_history],
            new_message=body.message
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {str(e)}")

    clean_reply, extracted_data = extract_from_reply(raw_reply)
    complete = is_conversation_complete(extracted_data)

    if complete:
        await save_completed_lead(
            widget_id=body.widget_id,
            session_id=body.session_id,
            extracted_data=extracted_data
        )

    return ChatResponse(
        reply=clean_reply,
        is_complete=complete,
        extracted_data=extracted_data
    )
