from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.silence import split_on_silence

def remove_silence(input_file, output_file):
	'''
	Given an input_file path/name, this function will break into non-silence chunks
	and combine those chunks and write them to output_file path/name
	'''
	sound = AudioSegment.from_file(input_file, format = "wav")
	chunks = split_on_silence(sound, min_silence_len = 1000, silence_thresh = -24, keep_silence = 0)
	sound1 = AudioSegment.empty()
	for e in chunks:
		sound1 = sound1 + e
	sound1.export(output_file, format = "wav")
#****************************************************-----------------------------------------------------------------***********************************************************
