import json
import os

from google import genai
from google.genai import types
from ai.content import convert_to_parts
from ai.instructions.instructions import load_instruction_set
from util.logging import logger


def route_generate(contents, memories):
    logger.debug(f'route_generate called with contents {contents}')
    client = genai.Client(
        api_key=os.environ.get('GEMINI_API_KEY'),
    )

    model = "gemini-2.5-flash-preview-04-17"
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text=load_instruction_set('context.md', 'format.md', 'intention.md')),
            types.Part.from_text(text=make_memory_instructions(memories)),
        ],
    )
    resp = []
    logger.debug('generating route decision')
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=convert_to_parts(contents),
        config=generate_content_config,
    ):
        logger.debug(f'chunk: {chunk}')
        logger.debug('------')
        logger.debug(chunk.model_dump_json())
        resp.append(chunk.text)

    if resp is None or len(resp) == 0:
        raise Exception("No response received from the AI model.")
    if len(resp) > 1:
      return json.loads(''.join(resp))


def make_memory_instructions(memories):
    return """
    Here are the memories that you must take into account before making a decision or responding to a message.
    For example, if a user says "I like vanilla ice cream", and you see a memory that says "Ben's favorite ice cream is vanilla", you should remember that Ben's favorite ice cream is vanilla.
    If a user says "can you call me Bob", then you should remember that the user is Bob.
    """ + "\n".join(memories)
