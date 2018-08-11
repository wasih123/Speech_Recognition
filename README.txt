This package is a useful library dealing with speech and text in Hindi
For installing package:
sudo pip install Indian_Speech_Lib==1.0.4

Utility functions:

utils.remove_silence(input_audio):
	given an input audio in WAV format, this function will remove silence periods from it
	and make an audio file named input_audio_rmsilence.wav
	
utils.get_gender(input_url, input_audio = None):
	given an input_url(or input_audio) of a file, this function will try to predict its gender
	It will return 0 for male and 1 for female
	
utils.get_automatic_transcript(input_url, path_to_key, bucket_name, input_audio = None, silence_removal = None):
	this function will return the text corresponding to the input_url(or input_audio) file
	The output will be available in a file named, "AutomaticTranscript.txt"
	path_to_key is the path of the service account key for gcloud and bucket_name is where the audio chunks will be stored
	

