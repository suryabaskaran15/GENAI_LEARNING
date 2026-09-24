# Phase 2, Topic 3: Your First LLM API Call
# GET /api/learn/first-llm-api-call/  -- test with Postman, curl, or the frontend

from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def first_llm_api_call(request):
    # client = the thing that talks to the LLM provider on our behalf.
    # Pointed at Ollama running locally, so no real API key is needed.
    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',  # Ollama ignores the value, it just needs something present
    )

    # model = which model should answer. input = what we're asking it.
    response = client.responses.create(
        model='smollm2:135m-instruct-q2_K',
        input='Explain Python in simple words.',
    )

    # response.output_text = the generated text the model sent back
    return Response({'reply': response.output_text})
