import soundfile as sf
import numpy as np

def concat_audios(path_files, gender):
	'''
	This function will concatenate all the audios given in path_files to one mega audio(same gender)
	and then we will break this mega audio to 10s chunks and extract features
	gender can be 'm' or 'f'
	'''
	sdat = np.array([])
	samplerate = 0
	for audio in sorted(os.listdir(path_files)):
		if(audio[0] == gender):
			data, samplerate = sf.read(audio)
			sdat = np.concatenate((sdat,data),axis=0)
		
	sf.write(gender + '_fl' + '.wav', sdat, samplerate)
#******************************************************----------------------------------------------------------------**********************************************************
