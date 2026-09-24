# Phase 2, Topic 8: Formatted Response
# Every topic so far got back free-form text. Here, `text.format` with a JSON schema
# forces the reply into an exact structure - useful when code needs to parse the
# answer instead of just displaying it to a person.
# POST /api/learn/formatted-response/  body: { "message": "..." }

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def formatted_response_example(request):
    # INPUT from user
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    # schema = the exact shape the reply must match - fixed here for the demo,
    # but this is normally shaped around whatever your code needs to consume next.
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'age': {'type': 'integer'},
            'hobby': {'type': 'string'},
        },
        'required': ['name', 'age', 'hobby'],
    }

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    response = client.responses.create(
        model='smollm2:135m-instruct-q2_K',
        input=user_message,
        text={'format': {'type': 'json_schema', 'name': 'person', 'schema': schema}},
    )

    # output_text is now a JSON string matching `schema`, not free-form prose
    return Response({'reply': response.output_text})
