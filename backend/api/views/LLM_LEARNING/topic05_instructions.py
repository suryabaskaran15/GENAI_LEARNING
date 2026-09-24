# Phase 2, Topic 5: Instructions
# Topic 4 put system behavior as a "system" role entry inside the input list.
# The Responses API also has a dedicated `instructions` param for that - kept
# separate from context (conversation history) and the user's new message.
# POST /api/learn/instructions/  body: { "message": "..." }

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def instructions_example(request):
    # INPUT from user
    user_message = request.data.get('message')  # the new message typed by the user right now
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    # instructions = system-level behavior/persona for the model, separate from
    # the conversation itself. Usually fixed per app/feature, not per message.
    instructions = 'You always answer in exactly one short sentence, no matter what is asked.'

    # context = earlier turns of this conversation. In a real app this would be
    # fetched from a database (per user/session) - hardcoded here for learning.
    context = [
        {'role': 'user', 'content': 'My name is Surya.'},
        {'role': 'assistant', 'content': 'Nice to meet you, Surya!'},
    ]

    # full_input = context + this new message = everything the model sees, besides instructions
    full_input = context + [{'role': 'user', 'content': user_message}]

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    response = client.responses.create(
        model='smollm2:135m-instruct-q2_K',
        instructions=instructions,
        input=full_input,
    )

    return Response({'reply': response.output_text})
