# Phase 2, Topic 6: Conversation & Message History
# Topic 4 faked context with a hardcoded list. Here it's real - past messages are
# read from the database, and both the new message and the reply are saved back,
# so the conversation actually survives across requests (and server restarts).
# POST /api/learn/conversation/  body: { "conversation_id": "demo", "message": "..." }

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Message


@api_view(['POST'])
def conversation_history_example(request):
    # INPUT from user
    conversation_id = request.data.get('conversation_id', 'demo')  # which conversation this belongs to
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    # context = every earlier message in this conversation, read from the DB, oldest first
    past_messages = Message.objects.filter(conversation_id=conversation_id)
    context = [{'role': m.role, 'content': m.content} for m in past_messages]

    # save the user's new message before calling the model, so it's not lost either way
    Message.objects.create(conversation_id=conversation_id, role='user', content=user_message)

    # full_input = everything from the DB + this new message
    full_input = context + [{'role': 'user', 'content': user_message}]

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    response = client.responses.create(
        model='smollm2:135m-instruct-q2_K',
        input=full_input,
    )
    reply = response.output_text

    # save the assistant's reply too, so the next request sees it as context
    Message.objects.create(conversation_id=conversation_id, role='assistant', content=reply)

    return Response({'reply': reply})
