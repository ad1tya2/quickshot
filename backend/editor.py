import app
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import db
import cv2
import numpy as np
import tempfile

TRANSITIONS = {
    "startTransitions": ["crossfadein","slidein"],
    "endTransitions": ["crossfadeout","slideout"]
}
'''
duration in msec
{
images: [{
    path: "filename",
    duration: 5444,
    startTransition: {
        type: "fade",
        duration: 3123
    },
    endTransition: {
        type: "fade",
        duration: 3122
    }
}],
audio: [{
    path: "filename",
    duration: 5000,
}]
}
'''
def customResize(img, IMG_ROW, IMG_COL):
    border_v = 0
    border_h = 0
    if (IMG_COL/IMG_ROW) >= (img.shape[0]/img.shape[1]):
        border_v = int((((IMG_COL/IMG_ROW)*img.shape[1])-img.shape[0])/2)
    else:
        border_h = int((((IMG_ROW/IMG_COL)*img.shape[0])-img.shape[1])/2)
    img = cv2.copyMakeBorder(img, border_v, border_v, border_h, border_h, cv2.BORDER_CONSTANT, 0)
    img = cv2.resize(img, (IMG_ROW, IMG_COL))
    return img
def edit(session,data):
    vidclips = []
    width = data["width"] or 1920
    height = data["height"] or 1080
    print(width, height)
    for img in data['images']:
        print(img)
        if(img['path'] == s["filename"] for s in session.paths) and (file := db.getfile(img['path'])):
            filergb = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_ANYCOLOR)
            filergb = customResize(filergb, width, height)
            filergb = cv2.cvtColor(filergb, cv2.COLOR_BGR2RGB)  
            clip = ImageClip(filergb).set_duration(img['duration'])

            if(clip.size[0] > width):
                clip = clip.resize(width=width)
            if(clip.size[1] > height):
                clip = clip.resize(height=height)
            # clip = CompositeVideoClip([clip], size=(1920,1080), bg_color=(0,0,0))
            if('startTransition' in img):
                if(img['startTransition']['type'] == "crossfadein"):
                    clip = clip.fx(vfx.fadein, img['startTransition']['duration'])
                elif(img['startTransition']['type'] == "slidein"):
                    clip = CompositeVideoClip([clip.fx(transfx.slide_in, img['startTransition']['duration'], "left")])
            if('endTransition' in img):
                if(img['endTransition']['type'] == "crossfadeout"):
                    clip = clip.fx(vfx.fadeout, img['endTransition']['duration'])
                elif(img['endTransition']['type'] == "slideout"):
                    clip = CompositeVideoClip([clip.fx(transfx.slide_out, img['startTransition']['duration'], "left")])
        vidclips.append(clip)
    concatenated = concatenate_videoclips(vidclips, method="compose")
    # concatenated = concatenated.resize((width, height))
    concatenated = concatenated.set_fps(24)
    audios = []
    if 'audios' in data and len(data['audios']) > 0:
        for audio in data['audios']:
            print(audio)
            audioclip = None
            # print("reac")
            if(audio['path'].startswith('preloadedaudio')):
                if(audio['path'] in app.preloaded_audio): # check to avoid path traversal attack
                    filename = '.'.join(audio['path'].split('.')[1:])
                    audioclip = AudioFileClip(os.path.join("preloadedaudio",filename))
            if(audio['path'] == s["filename"] for s in session.paths) and (file := db.getfile(audio['path'])):
                # print(file)
                tmpfile = tempfile.NamedTemporaryFile(suffix=".mp3",delete=False)
                tmpfile.write(file)
                audioclip = AudioFileClip(tmpfile.name)
                tmpfile.close()
            if(audioclip is None):
                continue
            

            audioclip = audioclip.set_duration(audio['duration'])
            print("reac")
            audios.append(audioclip)
        final_audio = concatenate_audioclips(audios)
        final_audio = final_audio.set_duration(concatenated.duration)
        final_clip = concatenated.set_audio(final_audio)
    else:
        final_clip = concatenated
    tmpfile = tempfile.NamedTemporaryFile(suffix=".mp4",delete=False)
    final_clip.write_videofile(tmpfile.name, codec="libx264", audio_codec="aac", fps=24, threads=4, preset="ultrafast")
    tmpfile.seek(0)
    vidbytes = tmpfile.read()
    tmpfile.close()
    os.remove(tmpfile.name)
    return vidbytes, 200, {'Content-Type': 'application/octet-stream', 
                            'Content-Disposition': f'attachment; filename=edited.mp4',
                             'Content-Length': len(vidbytes),
                             'Accept-Ranges': 'bytes'
                            }