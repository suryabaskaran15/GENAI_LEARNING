# Phase 2, Topic 10: Retries
# LLM calls can fail transiently (network blip, timeout, rate limit). Instead of
# failing on the first error, retry a few times with backoff before giving up.
# POST /api/learn/retries/  body: { "message": "...", "simulate_failure": true }

import time

from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError
from rest_framework.decorators import api_view
from rest_framework.response import Response

MAX_ATTEMPTS = 3


@api_view(['POST'])
def retries_example(request):
    # INPUT from user
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'message is required'}, status=400)

    # simulate_failure: points at a port nothing is listening on, so every attempt
    # fails - lets us watch the retry loop actually run instead of waiting for a real outage.
    simulate_failure = request.data.get('simulate_failure', False)
    base_url = 'http://localhost:11499/v1' if simulate_failure else 'http://localhost:11434/v1'

    client = OpenAI(base_url=base_url, api_key='ollama', timeout=5)

    attempts = []  # log of what happened on each try, just to make the retry loop visible
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.responses.create(
                model='smollm2:135m-instruct-q2_K',
                input=user_message,
            )
            attempts.append({'attempt': attempt, 'status': 'succeeded'})
            return Response({'reply': response.output_text, 'attempts': attempts})
        except (APIConnectionError, APITimeoutError, RateLimitError) as e:
            attempts.append({'attempt': attempt, 'status': 'failed', 'error': str(e)})
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)  # backoff: wait longer after each failure before retrying

    return Response({'error': 'LLM call failed after retries', 'attempts': attempts}, status=502)
