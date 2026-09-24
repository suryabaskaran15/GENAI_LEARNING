# Phase 2, Topic 4: Context
# Topic 3 sent one plain string as input, so the model had no memory of anything.
# Here, the user's new message is combined with prior context (past turns) before
# sending, so the model can see what was said earlier when answering the latest one.
# POST /api/learn/context/  body: { "message": "..." }

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def context_example(request):
    # INPUT from user
    user_message = request.data.get(
        "message"
    )  # the new message typed by the user right now
    if not user_message:
        return Response({"error": "message is required"}, status=400)

    # context = earlier turns of this conversation (system + past user/assistant messages).
    # In a real app this would be fetched from a database (per user/session) - hardcoded
    # here so we can see clearly how context gets combined with the new message.
    context = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "My name is Surya."},
        {"role": "assistant", "content": "Nice to meet you, Surya!"},
    ]

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    response = client.responses.create(
        model="smollm2:135m-instruct-q2_K",
        input=context + [{"role": "user", "content": user_message}],
    )

    return Response({"reply": response.output_text})
