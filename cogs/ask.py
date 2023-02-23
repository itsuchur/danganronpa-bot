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

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Ask(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.monokuma_moods = {
        'happy': "assets/monokuma/bustup_15_04.png",
        'angry': "assets/monokuma/bustup_15_05.png",
        'mischievous': "assets/monokuma/bustup_15_13.png",
        'shy': "assets/monokuma/bustup_15_13.png",
        'sad': "assets/monokuma/bustup_15_08.png",
        'confused': "assets/monokuma/bustup_15_10.png",
        }

        self.happy_mood = ["assets/audio/phuhuhu.ogg", "assets/audio/barelycontain.ogg", "assets/audio/ahahaha.ogg", "assets/audio/cantwait.ogg", "assets/audio/hihi.ogg", "assets/audio/goodmorning.ogg", "assets/audio/excitement.ogg", "assets/audio/howexciting.ogg", "assets/audio/justhehe.ogg", "assets/audio/excitement.ogg", "assets/audio/khehehe.ogg", "assets/audio/wow.ogg", "assets/audio/verynice.ogg", "assets/audio/puhaha_loud.ogg", "assets/audio/phuhuominous.ogg", "assets/audio/monoappears.ogg", "assets/audio/kuaha.ogg"]

        self.angry_mood = ["assets/audio/argh.ogg", "assets/audio/arghangry.ogg", "assets/audio/damnit.ogg", "assets/audio/idontbelieveit.ogg", "assets/audio/myentireexistence.ogg", "assets/audio/rawr.ogg", "assets/audio/reallyangry.ogg", "assets/audio/umakingangry.ogg", "assets/audio/unbelievable.ogg", "assets/audio/youguysangry.ogg"]

        self.mischievous_mood = ["assets/audio/phuhuhu.ogg", "assets/audio/barelycontain.ogg", "assets/audio/ahahaha.ogg", "assets/audio/isntwonderful.ogg", "assets/audio/hihi.ogg", "assets/audio/indeed.ogg", "assets/audio/cmon.ogg", "assets/audio/cmonnow.ogg", "assets/audio/actually.ogg", "assets/audio/puhaha_loud.ogg", "assets/audio/phuhuominous.ogg", "assets/audio/inotherwords.ogg", "assets/audio/shinn.ogg", "assets/audio/kuaha.ogg"]

        self.shy_mood = ["assets/audio/disgusting.ogg", "assets/audio/shy.ogg", "saywhaa.ogg"]

        self.sad_mood = ["assets/audio/okay.ogg", "assets/audio/unbelievable.ogg", "assets/audio/ohno.ogg", "assets/audio/hmmm.ogg"]

        self.confused_mood = ["assets/audio/confused_hmm.ogg", "assets/audio/confused_wawa.ogg", "assets/audio/confused_a.ogg", "assets/audio/hmmm.ogg", "assets/audio/inotherwords.ogg", "assets/audio/saywhaa.ogg", "assets/audio/whatthis.ogg", "assets/audio/whyyou.ogg"]

        self.monokuma_sounds = {
            'happy': random.choice(self.happy_mood),
            'angry': random.choice(self.angry_mood),
            'mischievous': random.choice(self.mischievous_mood),
            'shy': random.choice(self.shy_mood),
            'sad': random.choice(self.sad_mood),
            'confused': random.choice(self.confused_mood)
        }
    
    @app_commands.command(name="askmonokuma")
    async def askmonokuma(self, interaction: discord.Interaction, question: str) -> None:

        await interaction.response.send_message("Monokuma's thinking!")

        thing = functools.partial(self.request_to_openai, question)

        await self.bot.loop.run_in_executor(None, thing)

        asyncio.sleep(20)

        myfile = discord.File('output.mp4')

        await interaction.channel.send(f"{interaction.user.mention} You asked and so shall I have an answer! Puhuhu!~", file=myfile)


    def request_to_openai(self, question):
        response = openai.Completion.create(
        model="text-davinci-003", # text-davinci-003  # good results but can't mood text-curie-001
        prompt=f""""Prompt: "{question}" Imagine you're Monokuma. Answer in a twisted way like Monokuma would. If the question is inappropriate or political Monokuma must dodge the question and give angry reply. The answer must not be longer than 150 characters. Possible Monokuma moods: happy, angry, mischievous, shy, sad, confused. The structure of your response: answer to the prompt, separator "|" and here goes Monokuma mood-- a single word, must be lowercase without fluff.""",
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

        image_path = self.monokuma_moods.get(mood, None)

        if image_path is not None:

            monokuma_width = 973

            monokuma_height = 1060

            monokuma = Image.open(image_path).convert("RGBA")

            # main(new_response)

            return monokuma.resize((monokuma_width, monokuma_height), Image.LANCZOS)

        else:
            print("The mood is not found in dictionary.")

    def get_wrapped_text(self, text: str, font: ImageFont.ImageFont, line_length: int):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return '\n'.join(lines)


    def render_dialog_box(self, prompt):

        dialog_box = Image.open("assets/dialog_box.png")

        draw = ImageDraw.Draw(dialog_box)
        font = ImageFont.truetype("fonts/TREBUCBD.ttf", 60) # potentially Tresbuchet MS

        wrapped_text = self.get_wrapped_text(prompt, font, line_length=1500)

        draw.text((65, 90), wrapped_text,("#ffffff"),font=font)

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
        video_clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")

        self.add_phrase_over_ost("output.mp4", mood)

    def add_phrase_over_ost(self, video, mood):
        videoclip = VideoFileClip(video)

        path_to_audio = self.monokuma_sounds.get(mood, None)

        audioclip = AudioFileClip(path_to_audio)

        new_audioclip = CompositeAudioClip([videoclip.audio, audioclip])
        videoclip.audio = new_audioclip
        videoclip.duration = 3.0
        videoclip.fps = 1
        videoclip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")

    def main(self, specific_monokuma, new_response, mood):

        transparent_background = Image.open("assets/splash_dangan1.png")

        random_background = self.select_random_background()

        random_background.paste(specific_monokuma, (494, 155), specific_monokuma) # 594, 155

        random_background.paste(transparent_background, (0, 0), transparent_background)

        dialog_box = self.render_dialog_box(new_response)

        random_background.paste(dialog_box, (0, 708), dialog_box)

        random_background.save('test.png')

        self.add_static_image_to_audio(mood)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Ask(bot))