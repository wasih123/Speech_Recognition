import os
import sys
import json
import re

#normalize files(reference and automatic transcript) for running edit distance. Version 1.0
#Steps
#1. Eliminate punctuations(commas, poornvirams, ....,?,[],(),-,etc) and replace them with spaces
#2. Eliminate english unicodes(eg. unclear,etc) and replace them with spaces
#3. Put each hindi word on a separate line
#4. Run edit distance on each time stamp and keep track of the distance from one time stamp to the other
#5. The edit distance for the whole file is then:edit(file)= edit(t1) + ... + edit(tn) and WER = edit(file)/Total words(in manual transcript)
#6. For edit distance algorithm, treat each word as a symbol from some alphabet
#7. For edit distance algorithm, for testing two words are equal, develop some formal scheme of comparing their similarity in meanings.

def remove_all(alist,elem):
	while(elem in alist):
		alist.remove(elem)

def do_stuff(fname):
	fp = open(fname,'r')
	f = open('normalized_'+fname,'w')
	i = 0
	#Generate a new file as per steps 1,2,3.
	for line in fp:
		if(line!='\n'):	
			if(i == 0 or line.find('Chatra')!=-1):
				i=i+1
				f.write(line)
				continue	
			l = line	
			r = re.findall(r"[0-9]+\.[0-9]+\s{0,}-\s{0,}[0-9]+\.[0-9]+\s{0,}\w+\s{0,}-?\s{0,}",line)
			if(len(r)!=0):
				index = line.find(r[0]) + len(r[0]) -1
				l = line[index:]
				f.write('t'+'\n')
	
			
			for word in l.split():
				#remove danda
				char_list = list(word)
				remove_all(char_list,'\u0964')
				word = ''.join(char_list)
				word_list = re.split(',+|\.+|\[+|\]+|\(+|\)+|\?+',word)
				for w in word_list:
					if(w!=''):
						f.write(w+'\n')
			#print(line)
		
		i = i+1
	f.write('t'+'\n')	
	fp.close()
	f.close()
#Done steps 1,3
