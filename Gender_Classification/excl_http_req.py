import urllib2
import xlrd

def get_audio_from_url(input_url, output_file):
	'''
	Given an audio url, this function will fetch it and generate an mp3 file for it;
	output_file should be a proper name for an mp3, i.e. ending with .mp3
	'''
	mp3file = urllib2.urlopen(input_url)
	FP = open(output_file, 'wb')
	FP.write(mp3file.read())
	FP.close()
#*****************************------------------------------------*******************************	

def get_audio_from_excel(input_file = 'up_hindi_belt_Item_data.xlsx'):
	ExcelFileName = input_file 
	workbook = xlrd.open_workbook(ExcelFileName)
	worksheet = workbook.sheet_by_name("kab_item_data")
	num_rows = worksheet.nrows #Number of Rows
	num_cols = worksheet.ncols #Number of Columns
	m = 0
	f = 0
	for curr_row in range(0,num_rows, 1):
		data = worksheet.cell_value(curr_row, 6)
		if data == 'M':
			m += 1
			s1 = worksheet.cell_value(curr_row, 2)
			mp3file = urllib2.urlopen(s1)
			with open('m' + str(m) + '.mp3', 'wb') as output:
				output.write(mp3file.read())
				
		if data == 'F':
			f += 1
			s2 = worksheet.cell_value(curr_row, 2)
			mp3 = urllib2.urlopen(s2)
			with open('f' + str(f) + '.mp3', 'wb') as outputs:
				outputs.write(mp3.read())
#****************************-------------------------------------********************************
