from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.silence import split_on_silence


sound = AudioSegment.from_file("input0.wav", format="wav")
#ranges = detect_nonsilent(sound, min_silence_len=1000, silence_thresh=-16, seek_step=1)
chunks = split_on_silence(sound,min_silence_len=1000,silence_thresh=-24,keep_silence=0)

sound1 = AudioSegment.empty()

for e in chunks:
	sound1 = sound1 + e
#print(sound1)
sound1.export('output0.wav',format = "wav")
