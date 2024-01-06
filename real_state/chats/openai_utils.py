import openai
from chats.models import Chat, Message
from django.conf import settings
from users.models import User

openai.api_key = settings.OPENAI_API_KEY


def new_chat(user: User):
    chat = Chat.objects.create(user=user)
    return chat


def new_message_in_chat(chat: Chat, content: str):
    try:
        Message.objects.create(chat=chat, content=content, role="user")
        messages = Message.objects.filter(chat=chat)
        messages = [
            {"role": message.role, "content": message.content} for message in messages
        ]

        response_message = (
            openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
            )
            .choices[0]
            .message.content
        )

        Message.objects.create(chat=chat, content=response_message, role="assistant")
        return response_message
    except Exception as e:
        return str(e)
