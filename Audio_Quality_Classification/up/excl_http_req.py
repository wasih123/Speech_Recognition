import urllib2
import xlrd
import os


ExcelFileName= 'up_hindi_belt_Item_data.xlsx' #initially mp
workbook = xlrd.open_workbook(ExcelFileName)
worksheet = workbook.sheet_by_name("up_hindi_belt_Item_data_v2")
num_rows = worksheet.nrows #Number of Rows
num_cols = worksheet.ncols #Number of Columns
print(num_rows)
print(num_cols)

c=0
for curr_row in range(0,num_rows, 1):
	state = worksheet.cell_value(curr_row, 8)
	tag = worksheet.cell_value(curr_row, 36)
	if state=='REJ' and tag=='noisy':
		c+=1
	
	if c==1501:
		break
	if state=='REJ' and tag=='noisy':
		s1 = worksheet.cell_value(curr_row, 12)
		print(s1)
		if not s1.endswith('.mp3'):
			c = c-1
			continue
		mp3file = urllib2.urlopen(s1)
		with open('rej_'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())
		filename = 'rej_'+str(c)+'.mp3'
		[idn,idn1] = filename.split('.')
		os.system('ffmpeg -i '+filename+' -acodec pcm_s16le -ac 1 -ar 16000 '+idn+'.wav'.format(filename))
			
			
print(c)
#
#
  #output.write(mp3file.read())