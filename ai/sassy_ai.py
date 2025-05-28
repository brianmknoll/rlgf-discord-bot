import os

from google import genai
from google.genai import types
from ai.content import convert_to_parts
from ai.instructions.instructions import load_instruction_set
from util.logging import logger

def sassy_ai_generate(contents):
    client = genai.Client(
        api_key=os.environ.get('GEMINI_API_KEY'),
    )
    model = "gemini-2.5-flash-preview-04-17"
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=load_instruction_set('format.md', 'sassy.md')),
        ],
    )
    resp = []
    logger.debug('generating sassy AI message')
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=convert_to_parts(contents),
        config=generate_content_config,
    ):
        resp.append(chunk.text)
    return ''.join(resp)