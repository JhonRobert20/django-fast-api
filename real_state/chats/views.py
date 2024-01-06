from chats import openai_utils
from chats.models import Chat, Message
from django.http import JsonResponse
from django.shortcuts import redirect, render


def new_chat_request(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        chat = Chat.objects.create(user=request.user)
        response_data = {"chat_id": str(chat.id)}
        return JsonResponse(response_data)
    return redirect("chat_home")


def chat_page(request, chat_id):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return redirect("chat_home")
    except Exception:
        return redirect("chat_home")

    content_messages = list(
        Message.objects.filter(chat=chat, role__in=["assistant", "user"])
    )
    content_messages = [
        {"content": message.content, "assistant": message.role == "assistant"}
        for message in content_messages
    ]
    return render(
        request=request,
        template_name="chat.html",
        context={"chat_id": str(chat_id), "content_messages": content_messages},
        status=200,
    )
    return redirect("chat_home")


def chat_home_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    chat_ids = list(Chat.objects.filter(user=request.user).values_list("id", flat=True))
    chat_ids = [str(chat_id) for chat_id in chat_ids]

    return render(
        request=request, template_name="chat_home.html", context={"chat_ids": chat_ids}
    )


def new_message_request(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        import json

        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        content = body["content"]
        chat_id = body["chat_id"]
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()

        response_data = {"message": openai_utils.new_message_in_chat(chat, content)}

        return JsonResponse(response_data)
