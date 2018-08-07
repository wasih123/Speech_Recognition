import soundfile as sf
import numpy as np

dat = np.array([])
samplerate = 0
for i in range(0,2,1):
	data, samplerate = sf.read('fl51.'+str(i)+'.wav')
	dat = np.concatenate((dat,data),axis=0)
	print(i)

sf.write('fl51'+'.wav',dat,samplerate)
#ffmpeg -i input.flac -ab 320k -map_metadata 0 -id3v2_version 3 output.mp3