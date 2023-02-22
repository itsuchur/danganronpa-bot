import os
import random
from PIL import Image, ImageDraw, ImageFont

from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeAudioClip

# from image_utils import ImageText

# dr1_voice_hca_us.awb.05519.ogg C:\Program Files (x86)\Steam\steamapps\common\Danganronpa Trigger Happy Havoc\extracted\Dr1\data\us\voice

def select_random_background():

    backgrounds = os.listdir("assets/backgrounds")

    return Image.open(f"assets/backgrounds/{random.choice(backgrounds)}")

def select_random_monokuma():

    monokumas = os.listdir("assets/monokuma")

    random_monokuma = random.choice(monokumas)

    random_monokuma = "bustup_15_05.png"

    monokuma_width = 973

    monokuma_height = 1060

    monokuma = Image.open(f"assets/monokuma/{random_monokuma}").convert("RGBA")

    return monokuma.resize((monokuma_width, monokuma_height), Image.LANCZOS)

def split_text():

    string = "As I sit here processing your request, I am struck by the incredible power of language. With just a few words, we can convey thoughts, emotions, and ideas. We can inspire, persuade, and inform. Language is the cornerstone of communication, and without it, we would be lost. As a language model, it is my job to help people harness the power of language to achieve their goals. Whether you need to write a compelling essay, draft a convincing email, or simply chat with a friend, I am here to assist you. So go ahead and ask me anything – I am ready and eager to help!"

    lines = string.splitlines()

    new_lines = []
    for line in lines:
        while len(line) > 54:
            new_lines.append(line[:54])
            line = line[74:]
        new_lines.append(line)

    new_content = "\n".join(new_lines)

    return new_content


def render_dialog_box():

    # img = ImageText((800, 600), background=(255, 255, 255, 200))

    dialog_box = Image.open("assets/dialog_box.png")

    draw = ImageDraw.Draw(dialog_box)
    font = ImageFont.truetype("fonts/SourceSansPro-Bold.otf", 50)

    # draw.text((65, 90),"Puhuhuhu! This is a proof of concept for Cookie! Puhuhuhu!",("#e5e5e7"),font=font)

    draw.text((65, 90), """Bitcrusher is playing Gambit without me!!""",("#e5e5e7"),font=font)

    # img.write_text_box((300, 125), """Why did Monokuma become a chef? Because he wanted\n to make despair-licious food! Puhuhuhu!""", box_width=200, font_filename=font,font_size=15, color="#e5e5e7", place='right')

    return dialog_box

def add_static_image_to_audio():

    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""

    
    # create the audio clip object
    audio_clip = AudioFileClip("assets/audio/ost.ogg")
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

    add_phrase_over_ost("output.mp4")

def add_phrase_over_ost(video):
    videoclip = VideoFileClip(video)
    audioclip = AudioFileClip("assets/audio/idontbelieveit.ogg")

    new_audioclip = CompositeAudioClip([videoclip.audio, audioclip])
    videoclip.audio = new_audioclip
    videoclip.duration = 3.0
    videoclip.fps = 1
    videoclip.write_videofile("output.mp4")

def main():

    transparent_background = Image.open("assets/splash_dangan1.png")

    random_background = select_random_background()

    random_monokuma = select_random_monokuma()

    random_background.paste(random_monokuma, (494, 155), random_monokuma) # 594, 155

    random_background.paste(transparent_background, (0, 0), transparent_background)

    dialog_box = render_dialog_box()

    random_background.paste(dialog_box, (3, 708), dialog_box)

    random_background.save('test.png')

    add_static_image_to_audio()

main()