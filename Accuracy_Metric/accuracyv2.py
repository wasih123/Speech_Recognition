import json
import os
import sys
import re
import itertools

def evaluate(man_file,auto_file):
	f1 = open(man_file,'r')	#manual transcription(normalized)
	f2 = open(auto_file,'r')	#automatic transcription(normalized)

	#4. Run edit distance on each time stamp and keep track of the distance from one time stamp to the other
	#5. The edit distance for the whole file is then:edit(file)= edit(t1) + ... + edit(tn) and WER = edit(file)/Total words(in manual transcript)
	#6. For edit distance algorithm, treat each word as a symbol from some alphabet
	#7. For edit distance algorithm, for testing two words are equal, develop some formal scheme of comparing their similarity in meanings.

	#8. Do this step instead of steps 4,5,6,7: Just forget about timestamps and treat the whole file as a single transcript, i.e. do global alignment.

	man = f1.readlines()
	auto = f2.readlines()
	f1.close()
	f2.close()
	#if(man[0]!=auto[0]):
	#	print('Panic! Manual and Automatic transcripts are for different files')
	#	exit(0)

	manual = []
	automatic = []
	for word in man[1:]:
		if(re.match(r"unclear",word)):
			continue
		elif(re.match(r"blank",word)):
			continue
		else:
			manual.append(word[:-1])

	for word in auto[1:]:
		if(re.match(r"unclear",word)):
			continue
		elif(re.match(r"blank",word)):
			continue
		else:
			automatic.append(word[:-1])

	#manual is the now the string to be aligned with automatic and so apply DP
	def editD(S,T):
		n = len(S)
		m = len(T)
		#need a DP table of size n*m
		#insertions/deletions/modifications are allowed
		DP = [[0 for j in range(m)] for i in range(n)]
		for j in range(0,m):
			if(S[n-1] in T[j:]):
				DP[n-1][j] = abs(m-1-j)
			else:
				DP[n-1][j] = abs(m-1-j)+1

		for i in range(0,n):
			if(T[m-1] in S[i:]):
				DP[i][m-1] = abs(n-1-i)
			else:
				DP[i][m-1] = abs(n-1-i)+1

		for i in range(n-2,-1,-1):
			for j in range(m-2,-1,-1):
				if(S[i]==T[j] or S[i] + S[i+1] == T[j]):
					DP[i][j] = DP[i+1][j+1]
				else:
					DP[i][j] = min(min(1 + DP[i+1][j], 1 + DP[i][j+1]),1 + DP[i+1][j+1])

		return DP[0][0]

	m_timestamps = 0
	a_timestamps = 0

	for x,y in itertools.zip_longest(manual,automatic):
		if(x == 't'):
			m_timestamps +=1
		if(y == 't'):
			a_timestamps +=1
	m_timestamps -=1
	a_timestamps -=1
	mpointer = 1
	apointer = 1
	edit_distance = 0
	max_WER = 0
	min_WER = 10
	avg_WER = 0
	for l in range(min(m_timestamps,a_timestamps)):
		i = mpointer
		j = apointer
		s = []
		t = []
		while True:
			if(i != len(manual) and j != len(automatic)):
				if(manual[i] == 't' and automatic[j] == 't'):
					break
				else:
					if(automatic[j] != 't'):
						s.append(automatic[j])
						j+=1
					if(manual[i] != 't'):
						t.append(manual[i])				
						i+=1
			else:
				break
		e = editD(s,t)
		edit_distance += e
		WER = (float)(e/len(t))
		if(WER < 0.3):
			avg_WER += 0.5*WER
		else:
			avg_WER += 1*WER
		if(WER > max_WER):
			max_WER = WER
		if(WER < min_WER):
			min_WER = WER
		mpointer = i+1
		apointer = j+1
	
	avg_WER = (float)(avg_WER/min(m_timestamps,a_timestamps))
	edit2Distance = editD(automatic,manual)
	WER2 = (float)(edit2Distance/len(manual))
	#print('Manual length = ',len(manual))
	#print('Automatic length = ',len(automatic))
	#print('Edit Distance = ',edit_distance)
	WER1 = (float)(edit_distance/len(manual))
	#print('Word Error Rate =',WER)
	#print('Maximum Word Error Rate =',max_WER)
	#print('Minimum Word Error Rate =',min_WER)
	WER = min(avg_WER,min(WER2,WER1))
	accuracy = (1-WER)*100
	return (WER,accuracy)
