import os
import random
import os
import openai

from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeAudioClip

# from image_utils import ImageText

# dr1_voice_hca_us.awb.05519.ogg C:\Program Files (x86)\Steam\steamapps\common\Danganronpa Trigger Happy Havoc\extracted\Dr1\data\us\voice

"""Question: "What do you think of Danganronpa?". Answer in a humorous twisted way like Monokuma would. The answer must be given in humorous twisted way. If the question is inappropriate or political, Monokuma must dodge the question and answer like he's upset. The answer must not be longer than 150 characters. Imagine with what mood Monokuma would answer the question: good, bad, happy, angry, mischievous, shy, sad, confused, threatening. Indicate the mood by sending "mood" key and value being Monokumo's mood back with answer to this API request."""

monokuma_moods = {
    'good': "assets/monokuma/bustup_15_01.png",
    'bad': "assets/monokuma/bustup_15_02.png",
    'happy': "assets/monokuma/bustup_15_04.png",
    'angry': "assets/monokuma/bustup_15_05.png",
    'mischievous': "assets/monokuma/bustup_15_13.png",
    'shy': "assets/monokuma/bustup_15_13.png",
    'sad': "assets/monokuma/bustup_15_08.png",
    'confused': "assets/monokuma/bustup_15_10.png",
    'threatening': "assets/monokuma/bustup_15_12.png"
}

monokuma_sounds = {
    'happy': "assets/audio/excitement.ogg",
    'angry': "assets/audio/reallyangry.ogg",
    'mischievous': "assets/audio/phuhuhu.ogg",
    'shy': "assets/audio/shy.ogg",
    'sad': "assets/audio/myentireexistence.ogg",
    'confused': "assets/audio/confused_a.ogg",
}

happy_mood = ["assets/audio/phuhuhu.ogg", "assets/audio/barelycontain.ogg", "assets/audio/ahahaha.ogg", "assets/audio/cantwait.ogg", "assets/audio/hihi.ogg", "assets/audio/goodmorning.ogg", "assets/audio/excitement.ogg", "assets/audio/howexciting.ogg", "assets/audio/justhehe.ogg", "assets/audio/excitement.ogg", "assets/audio/khehehe.ogg", "assets/audio/wow.ogg", "assets/audio/verynice.ogg", "assets/audio/puhaha_loud.ogg", "assets/audio/phuhuominous.ogg", "assets/audio/monoappears.ogg", "assets/audio/kuaha.ogg"]

angry_mood = ["assets/audio/argh.ogg", "assets/audio/arghangry.ogg", "assets/audio/damnit.ogg", "assets/audio/idontbelieveit.ogg", "assets/audio/myentireexistence.ogg", "assets/audio/rawr.ogg", "assets/audio/reallyangry.ogg", "assets/audio/umakingangry.ogg", "assets/audio/unbelievable.ogg", "assets/audio/youguysangry.ogg"]

mischievous_mood = ["assets/audio/phuhuhu.ogg", "assets/audio/barelycontain.ogg", "assets/audio/ahahaha.ogg", "assets/audio/isntwonderful.ogg", "assets/audio/hihi.ogg", "assets/audio/indeed.ogg", "assets/audio/cmon.ogg", "assets/audio/cmonnow.ogg", "assets/audio/actually.ogg", "assets/audio/puhaha_loud.ogg", "assets/audio/phuhuominous.ogg", "assets/audio/inotherwords.ogg", "assets/audio/shinn.ogg", "assets/audio/kuaha.ogg"]

shy_mood = ["assets/audio/disgusting.ogg", "assets/audio/shy.ogg", "saywhaa.ogg"]

sad_mood = ["assets/audio/okay.ogg", "assets/audio/unbelievable.ogg", "assets/audio/ohno.ogg", "assets/audio/hmmm.ogg"]

confused_mood = ["assets/audio/confused_hmm.ogg", "assets/audio/confused_wawa.ogg", "assets/audio/confused_a.ogg", "assets/audio/hmmm.ogg", "assets/audio/inotherwords.ogg", "assets/audio/saywhaa.ogg", "assets/audio/whatthis.ogg", "assets/audio/whyyou.ogg"]

# make lists for each mood, and sounds as elements. Random.choice element 

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def request_to_openai():
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=""""Prompt: "You're a useless freaking idiot!" Imagine you're Monokuma. Answer in a twisted way like Monokuma would. If the question is inappropriate or political, Monokuma must dodge the question. The answer must not be longer than 150 characters. Possible Monokuma moods: happy, angry, mischievous, shy, sad, confused. The structure of your response: answer to the prompt, separator "|" and here goes Monokuma mood-- a single word in lowercase without fluff.""",
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

    select_specific_monokuma(new_response, mood)

    # response = response.replace('Answer: ', '').replace('"', '')

    # Split the string into two parts at 'Mood:'
    # answer, mood_part = response.split('Mood:')

    # Extract the value of the mood
    # mood = mood_part.strip().split()[0]

    # Print the answer and mood
    # print(response)
    # print(mood)

    # return response

def select_random_background():

    backgrounds = os.listdir("assets/backgrounds")

    return Image.open(f"assets/backgrounds/{random.choice(backgrounds)}")

def select_random_monokuma():

    monokumas = os.listdir("assets/monokuma")

    random_monokuma = random.choice(monokumas)

    # random_monokuma = "bustup_15_05.png"

    monokuma_width = 973

    monokuma_height = 1060

    monokuma = Image.open(f"assets/monokuma/{random_monokuma}").convert("RGBA")

    return monokuma.resize((monokuma_width, monokuma_height), Image.LANCZOS)


def select_specific_monokuma(new_response, mood):

    image_path = monokuma_moods.get(mood, None)

    if image_path is not None:

        monokuma_width = 973

        monokuma_height = 1060

        monokuma = Image.open(image_path).convert("RGBA")

        # main(new_response)

        main(monokuma.resize((monokuma_width, monokuma_height), Image.LANCZOS), new_response)

    else:
        print("The mood is not found in dictionary.")

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)


def render_dialog_box(prompt = None):

    dialog_box = Image.open("assets/dialog_box.png")

    draw = ImageDraw.Draw(dialog_box)
    font = ImageFont.truetype("fonts/SourceSansPro-Bold.otf", 50)

    if prompt is None:

        text = """Why did Monokuma become a chef? Because he wanted\n to make despair-licious food! Puhuhuhu!"""

        wrapped_text = get_wrapped_text(text, font, line_length=1500) # 1500 is the optimal value

    else:

        wrapped_text = get_wrapped_text(prompt, font, line_length=1500) # 1500 is the optimal value
    
    draw.text((65, 90), wrapped_text,("#e5e5e7"),font=font)

    # img.write_text_box((300, 125), """Why did Monokuma become a chef? Because he wanted\n to make despair-licious food! Puhuhuhu!""", box_width=200, font_filename=font,font_size=15, color="#e5e5e7", place='right')

    return dialog_box

def add_static_image_to_audio():

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
    print(video_clip.duration)
    video_clip.write_videofile("output.mp4")

    add_random_phrase_over_ost("output.mp4")

def add_random_phrase_over_ost(video):
    videoclip = VideoFileClip(video)
    audioclip = AudioFileClip("assets/audio/inotherwords.ogg")

    new_audioclip = CompositeAudioClip([videoclip.audio, audioclip])
    videoclip.audio = new_audioclip
    videoclip.duration = 3.0
    videoclip.fps = 1
    videoclip.write_videofile("output.mp4")

def main(specific_monokuma = None, new_response = None):

    transparent_background = Image.open("assets/splash_dangan1.png")

    random_background = select_random_background()

    if specific_monokuma == None:

        random_monokuma = select_random_monokuma()

        random_background.paste(random_monokuma, (494, 155), random_monokuma) # 594, 155

    else:

        random_background.paste(specific_monokuma, (494, 155), specific_monokuma) # 594, 155

    random_background.paste(transparent_background, (0, 0), transparent_background)

    if new_response != None:

        dialog_box = render_dialog_box(new_response)

    else:

        dialog_box = render_dialog_box()

    random_background.paste(dialog_box, (3, 708), dialog_box)

    random_background.save('test.png')

    add_static_image_to_audio()

request_to_openai()