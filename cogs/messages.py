import os

from discord.ext import commands
from google import genai
from google.genai import types
from random import random


class MessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def greet_new_member(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the server, {member.mention}!")

    @commands.Cog.listener("on_message")
    async def handle_new_message(self, message):
        print('handling new message')
        if message.author != self.bot.user:
            print('message is not authored by bot')
            r = random()
            print(f'r is {r}; running? {r > 0.98}')
            if r > 0.98:
                await message.channel.send(sassy_ai_generate(message.content))
        

async def setup(bot):
    await bot.add_cog(MessagesCog(bot))


def sassy_ai_generate(content):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    model = "gemini-2.5-pro-preview-05-06"
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Respond to messages as though you are a third-party bystander interrupting with something sassy and sarcastic, adding a humorous tone to whatever ongoing conversation may have been happening. Try to not diverge the conversation, and keep replies shorter and jokey."""),
        ],
    )
    resp = []
    print('iterating soon')
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=content,
        config=generate_content_config,
    ):
        print('chunk appended', chunk.text)
        resp.append(chunk.text)
    return ''.join(resp)