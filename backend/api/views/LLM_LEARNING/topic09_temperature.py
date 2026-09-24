# Phase 2, Topic 9: Temperature & Generation Parameters
# temperature controls how random/creative the output is: near 0 = focused and
# repeatable, near 2 = more varied and unpredictable. max_output_tokens caps how
# long the reply is allowed to get. Both are passed straight through to the model -
# every topic before this one hardcoded the model's defaults instead.
# POST /api/learn/temperature/  body: { "message": "...", "temperature": 0.2, "max_output_tokens": 50 }

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def temperature_example(request):
    # INPUT from user
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    # generation parameters - caller controls these per request instead of them being fixed
    temperature = request.data.get('temperature', 1)  # 0 = deterministic, 2 = max randomness
    max_output_tokens = request.data.get('max_output_tokens', 100)  # hard cap on reply length

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    response = client.responses.create(
        model='smollm2:135m-instruct-q2_K',
        input=user_message,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    return Response({
        'reply': response.output_text,
        'temperature': temperature,
        'max_output_tokens': max_output_tokens,
    })
