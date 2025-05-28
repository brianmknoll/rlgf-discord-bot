from google.genai import types
from util.logging import logger

def convert_to_parts(contents):
    parts = []
    for content in contents:
        text = f'{content.timestamp.strftime("%Y-%m-%d %I:%M %p")} {content.author}: {content.message}'
        part = types.Content(
            role='model' if content.is_bot else 'user',
            parts=[
                types.Part.from_text(text=text),
            ],
        )
        parts.append(part)
    return parts
