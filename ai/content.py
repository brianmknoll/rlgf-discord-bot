from google.genai import types
from util.logging import logger

def convert_to_parts(contents):
    parts = []
    logger.debug(f'Converting {len(contents)} contents to parts')
    for content in contents:
        logger.debug(f'Converting content: {content}')
        text = f'{content.timestamp.strftime("%Y-%m-%d %I:%M %p")} {content.author}: {content.message}'
        part = types.Content(
            role='model' if content.is_bot else 'user',
            parts=[
                types.Part.from_text(text=text),
            ],
        )
        parts.append(part)
    logger.debug(f'Converted {len(contents)} contents to {len(parts)} parts')
    return parts
