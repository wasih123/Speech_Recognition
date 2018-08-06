import soundfile as sf
import numpy as np

dat = np.array([])
samplerate = 0
for i in range(100):
	if i!=0:
		data, samplerate = sf.read('tstm'+str(i)+'.wav')
		dat = np.concatenate((dat,data),axis=0)

sf.write('fl'+'.wav',dat,samplerate)
#ffmpeg -i input.flac -ab 320k -map_metadata 0 -id3v2_version 3 output.mp3