import accuracyv2 as acc
import normalization as norm
import os
import sys

if __name__=="__main__":
	#first obtain normalization of both manual and automatic transcripts
	man_name = sys.argv[1]
	auto_name = sys.argv[2]
	norm.do_stuff(man_name)	#do normalization of manual transcript
	norm.do_stuff(auto_name)	#do normalization of automatic transcript	
	man_normalized = 'normalized_' + man_name
	auto_normalized = 'normalized_' + auto_name
	WER, accuracy = acc.evaluate(man_normalized, auto_normalized)	#evaluate automatic transcript
	print('Avg Word Error Rate = ', WER)
	print('Accuracy = ', accuracy)
	
	
	
