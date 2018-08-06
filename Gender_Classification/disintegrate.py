import soundfile as sf
data, samplerate = sf.read('fl.wav')
i=0
j=119
print(len(data)/160000)
print(samplerate)
while i<len(data):
	sf.write('m'+str(j)+'.wav',data[i:i+160000],samplerate)
	i += 160000
	j += 1
#ffmpeg -i output.mp3 output.flac