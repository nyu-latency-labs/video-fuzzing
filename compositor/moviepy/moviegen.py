# Import everything needed to edit video clips
from moviepy.editor import *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
imageclip = ImageClip("./resources/street.jpg").resize((500,500))

clip = VideoFileClip("./resources/cars/1.mp4").resize((100,100))
clip = clip.set_position((0,0)).set_end(5)

clip1 = VideoFileClip("./resources/cars/1.mp4").subclip(5,15).resize((100,100))
clip1 = clip1.set_position((100,0))

clip2 = VideoFileClip("./resources/cars/1.mp4").subclip(10,20).resize((100,100))
clip2 = clip2.set_position((200,0))

clip3 = VideoFileClip("./resources/cars/2.mov").subclip(0,20).resize((100,100))
clip3 = clip3.set_position((0,0)).set_opacity(0.5)
# Overlay the text clip on the first video clip
video = CompositeVideoClip([imageclip, clip, clip1.set_start(5), clip2, clip3.set_start(5)], size=(500,500))

# Write the result to a file (many options available !)
video.set_duration(10).write_videofile("output.mp4",fps=30,bitrate="1000k",audio_codec="mp3",codec="mpeg4")