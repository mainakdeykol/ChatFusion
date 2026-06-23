import gradio as gr

from services.chat_service import (
    send_message,
    new_chat,
    load_chat
)


def create_ui():

    with gr.Blocks(
        title="Universal Chatbot",
        fill_height=True
    ) as demo:

        current_session = gr.State(None)

        with gr.Row():

            # LEFT SIDEBAR
            with gr.Column(scale=15):

                gr.Markdown("## Chats")

                new_chat_btn = gr.Button(
                    "➕ New Chat",
                    variant="primary"
                )

                chat_list = gr.Radio(
                    choices=[],
                    label="History",
                    interactive=True
                )

            # CENTER
            with gr.Column(scale=70):

                chatbot = gr.Chatbot(
                    label="Chat",
                    height=700
                )

                msg = gr.Textbox(
                    placeholder="Type a message...",
                    lines=2
                )

                send_btn = gr.Button(
                    "Send",
                    variant="primary"
                )

            # RIGHT SIDEBAR
            with gr.Column(scale=15):

                gr.Markdown("## Settings")

                model_name = gr.Textbox(
                    label="Model",
                    value="llama-3.3-70b-versatile"
                )

                base_url = gr.Textbox(
                    label="Base URL",
                    value="https://api.groq.com/openai/v1"
                )

                api_key = gr.Textbox(
                    label="API Key",
                    type="password"
                )

                temperature = gr.Slider(
                    minimum=0,
                    maximum=2,
                    value=0.7,
                    step=0.1,
                    label="Temperature"
                )

        # SEND MESSAGE

        send_btn.click(
            fn=send_message,
            inputs=[
                msg,
                chatbot,
                current_session,
                model_name,
                base_url,
                api_key,
                temperature
            ],
            outputs=[
                msg,
                chatbot,
                current_session,
                chat_list
            ]
        )

        # ENTER KEY SUPPORT

        msg.submit(
            fn=send_message,
            inputs=[
                msg,
                chatbot,
                current_session,
                model_name,
                base_url,
                api_key,
                temperature
            ],
            outputs=[
                msg,
                chatbot,
                current_session,
                chat_list
            ]
        )

        # NEW CHAT

        new_chat_btn.click(
            fn=new_chat,
            outputs=[
                chatbot,
                current_session,
                chat_list
            ]
        )

        # LOAD OLD CHAT

        chat_list.change(
            fn=load_chat,
            inputs=[chat_list],
            outputs=[chatbot]
        )

    return demo