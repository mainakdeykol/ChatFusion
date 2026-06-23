from database.memory_db import MemoryDB
from services.llm_service import chat
import gradio as gr

db = MemoryDB()


def refresh_sessions(selected=None):

    sessions = db.get_sessions()

    choices = [
        (title, session_id)
        for session_id, title in sessions
    ]

    return gr.update(
        choices=choices,
        value=selected
    )


def new_chat():

    session_id = db.create_session()

    return (
        [],
        session_id,
        refresh_sessions(session_id)
    )


def load_chat(session_id):

    if not session_id:
        return []

    messages = db.get_messages(session_id)

    return messages


def send_message(
    message,
    history,
    current_session,
    model_name,
    base_url,
    api_key,
    temperature
):

    if not message:
        return (
            "",
            history,
            current_session,
            refresh_sessions(current_session)
        )

    if not current_session:
        current_session = db.create_session()

    db.save_message(
        current_session,
        "user",
        message
    )

    messages = db.get_messages(current_session)

    answer = chat(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
        messages=messages,
        temperature=temperature
    )

    db.save_message(
        current_session,
        "assistant",
        answer
    )

    history = db.get_messages(current_session)

    # Generate title from first message
    if len(history) <= 2:

        title = message[:40]

        db.update_title(
            current_session,
            title
        )

    return (
        "",
        history,
        current_session,
        refresh_sessions(current_session)
    )