
import os

#path = '/Users/ravijayanth/Desktop'
path = os.getcwd()
x = 0
for filename in os.listdir(path):
    if (filename.endswith(".mp3")): #or .avi, .mpeg, whatever.
        [a,b] = filename.split('.')
        os.system('ffmpeg -i '+filename+' -acodec pcm_s16le -ac 1 -ar 16000 '+a+'.wav'.format(filename))
        x = x +1
    else:
    	continue

