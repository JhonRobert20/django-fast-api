from chats import views
from django.urls import path

urlpatterns = [
    path("chat/<str:chat_id>/", views.chat_page, name="chat"),
    path("", views.chat_home_page, name="chat_home"),
    path("new_chat", views.new_chat_request, name="new_chat"),
    path("new_message", views.new_message_request, name="new_message"),
]
