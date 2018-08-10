import soundfile as sf

def break_into_chunks(input_file, gender):
	'''
	Given an input_file, this function will break this .wav file into chunks of 10s duration each
	gender is the gender of this input file, i.e. 'm' or 'f'
	'''
	data, samplerate = sf.read(input_file)
	i=0
	j=1
	temp = samplerate*10
	n = (len(data)/temp)
	while i<len(data):
		sf.write(gender + str(j) + '.wav', data[i: i+temp], samplerate)
		i += temp
		j += 1
#*******************************************************--------------------------------------------------------------------*****************************************************
