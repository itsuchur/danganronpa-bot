import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import os
import random
import openai
import functools

from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeAudioClip

monokuma_moods = {
    'good': "assets/monokuma/bustup_15_01.png",
    'bad': "assets/monokuma/bustup_15_02.png",
    'happy': "assets/monokuma/bustup_15_04.png",
    'angry': "assets/monokuma/bustup_15_05.png",
    'mischievous': "assets/monokuma/bustup_15_13.png",
    'shy': "assets/monokuma/bustup_15_03.png",
    'sad': "assets/monokuma/bustup_15_08.png",
    'confused': "assets/monokuma/bustup_15_10.png",
    'threatening': "assets/monokuma/bustup_15_12.png"
}

monokuma_sounds = {
    'good': "assets/audio/phuhuhu.ogg",
    'bad': "assets/audio/umakingangry.ogg",
    'happy': "assets/audio/excitement.ogg",
    'angry': "assets/audio/reallyangry.ogg",
    'mischievous': "assets/audio/phuhuhu.ogg",
    'shy': "assets/audio/shy.ogg",
    'sad': "assets/audio/myentireexistence.ogg",
    'confused': "assets/audio/confused_a.ogg",
    'threatening': "assets/audio/youguysangry.ogg",
}

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Ask(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="askmonokuma")
    async def askmonokuma(self, interaction: discord.Interaction, question: str) -> None:

        await interaction.response.send_message("Monokuma's thinking!", ephemeral=True)

        thing = functools.partial(self.request_to_openai, question)

        await self.bot.loop.run_in_executor(None, thing)

        asyncio.sleep(20)

        myfile = discord.File('output.mp4')

        await interaction.channel.send(f"{interaction.user.mention} Ask and you shall receive!", file=myfile)


    def request_to_openai(self, question):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f""""Prompt: "{question}" Imagine you're Monokuma. Answer in a twisted way like Monokuma would. If the question is inappropriate or political Monokuma must dodge the question and give angry reply. The answer must not be longer than 150 characters. Possible Monokuma moods: good, bad, happy, angry, mischievous, shy, sad, confused, threatening. The structure of your response: answer to the prompt, separator "|" and here goes Monokuma mood-- a single word in lowercase without fluff.""",
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
        )

        response = response.choices[0].text

        print(response)

        new_response = response.split("|")[0].strip()
        print(new_response)

        mood = response.split("|")[1].strip()
        print(mood)

        choose_mono = self.select_specific_monokuma(new_response, mood)

        self.main(choose_mono, new_response, mood)

        # response = response.replace('Answer: ', '').replace('"', '')

        # Split the string into two parts at 'Mood:'
        # answer, mood_part = response.split('Mood:')

        # Extract the value of the mood
        # mood = mood_part.strip().split()[0]

        # Print the answer and mood
        # print(response)
        # print(mood)

        # return response

    def select_random_background(self):

        backgrounds = os.listdir("assets/backgrounds")

        return Image.open(f"assets/backgrounds/{random.choice(backgrounds)}")


    def select_specific_monokuma(self, new_response, mood):

        image_path = monokuma_moods.get(mood, None)

        if image_path is not None:

            monokuma_width = 973

            monokuma_height = 1060

            monokuma = Image.open(image_path).convert("RGBA")

            # main(new_response)

            return monokuma.resize((monokuma_width, monokuma_height), Image.LANCZOS)

        else:
            print("The mood is not found in dictionary.")


    def render_dialog_box(self, prompt):

        dialog_box = Image.open("assets/dialog_box.png")

        draw = ImageDraw.Draw(dialog_box)
        font = ImageFont.truetype("fonts/SourceSansPro-Bold.otf", 60)

        draw.text((65, 90), prompt,("#e5e5e7"),font=font)

        return dialog_box

    def add_static_image_to_audio(self, mood):

        """Create and save a video file to `output_path` after 
        combining a static image that is located in `image_path` 
        with an audio file in `audio_path`"""

        
        # create the audio clip object
        audio_clip = AudioFileClip("assets/audio/ost_short.ogg")
        # create the image clip object
        image_clip = ImageClip("test.png")
        # use set_audio method from image clip to combine the audio with the image
        video_clip = image_clip.set_audio(audio_clip)
        # specify the duration of the new clip to be the duration of the audio clip
        video_clip.duration = audio_clip.duration
        # set the FPS to 1
        video_clip.fps = 1
        # write the resuling video clip
        video_clip.write_videofile("output.mp4")

        self.add_phrase_over_ost("output.mp4", mood)

    def add_phrase_over_ost(self, video, mood):
        videoclip = VideoFileClip(video)
        audioclip = AudioFileClip(f"{monokuma_sounds[mood]}")

        new_audioclip = CompositeAudioClip([videoclip.audio, audioclip])
        videoclip.audio = new_audioclip
        videoclip.duration = 3.0
        videoclip.fps = 1
        videoclip.write_videofile("output.mp4")

    def main(self, specific_monokuma, new_response, mood):

        transparent_background = Image.open("assets/splash_dangan1.png")

        random_background = self.select_random_background()

        random_background.paste(specific_monokuma, (494, 155), specific_monokuma) # 594, 155

        random_background.paste(transparent_background, (0, 0), transparent_background)

        dialog_box = self.render_dialog_box(new_response)

        random_background.paste(dialog_box, (3, 708), dialog_box)

        random_background.save('test.png')

        self.add_static_image_to_audio(mood)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Ask(bot))