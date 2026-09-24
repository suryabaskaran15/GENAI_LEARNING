# Phase 2, Topic 7: Streaming
# Every topic so far waited for the full reply before responding. Here, text is sent
# to the client chunk by chunk as the model generates it - the "typing" effect chat
# UIs use, instead of a blank screen until the whole answer is ready.
# POST /api/learn/stream/  body: { "message": "..." }

from django.http import StreamingHttpResponse
from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def stream_example(request):
    # INPUT from user
    user_message = request.data.get('message')  # the new message typed by the user right now
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    def token_stream():
        # stream=True: the SDK returns an iterator of events instead of one final object
        stream = client.responses.create(
            model='smollm2:135m-instruct-q2_K',
            input=user_message,
            stream=True,
        )
        for event in stream:
            # only text-delta events carry new characters - other events mark progress/status
            if event.type == 'response.output_text.delta':
                yield event.delta

    # StreamingHttpResponse writes each yielded chunk to the client as soon as it's ready,
    # instead of waiting for the generator to finish (unlike the DRF Response used elsewhere)
    return StreamingHttpResponse(token_stream(), content_type='text/plain')
