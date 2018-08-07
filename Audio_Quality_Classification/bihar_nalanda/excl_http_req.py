import urllib2
import xlrd
import os


ExcelFileName= 'bihar_nalanda_Item_data-all.xlsx' #initially mp
workbook = xlrd.open_workbook(ExcelFileName)
worksheet = workbook.sheet_by_name("bmgf_item_data_v5")
num_rows = worksheet.nrows #Number of Rows
num_cols = worksheet.ncols #Number of Columns
print(num_rows)
print(num_cols)
'''
c=0
for curr_row in range(0,num_rows, 1):
	data = worksheet.cell_value(curr_row, 24)
	source = worksheet.cell_value(curr_row, 32)
	if data==1:
		c+=1
	if c==101:
		break
	if data==1  and source==1:
		s1 = worksheet.cell_value(curr_row,12)
		print(s1)
		if(s1=="NULL"):
			c = c-1
			continue
		mp3file = urllib2.urlopen(s1)
		with open('tst1_'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())

print(c)
c=0
for curr_row in range(0,num_rows, 1):
	data = worksheet.cell_value(curr_row, 24)
	source = worksheet.cell_value(curr_row, 32)
	if data==2:
		c+=1
	if c==101:
		break
	if data==2  and source==1:
		s1 = worksheet.cell_value(curr_row,12)
		print(s1)
		if(s1=="NULL"):
			c = c-1
			continue
		mp3file = urllib2.urlopen(s1)
		with open('tst2_'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())
			
print(c)
c=0
for curr_row in range(0,num_rows, 1):
	data = worksheet.cell_value(curr_row, 24)
	source = worksheet.cell_value(curr_row, 32)
	if data==4:
		c+=1
	if c==101:
		break
	if data==4  and source==1:
		s1 = worksheet.cell_value(curr_row,12)
		print(s1)
		if(s1=="NULL"):
			c = c-1
			continue
		mp3file = urllib2.urlopen(s1)
		with open('tst4_'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())
			
print(c)
'''
c=0
for curr_row in range(0,num_rows, 1):
	state = worksheet.cell_value(curr_row, 2)
	tag = worksheet.cell_value(curr_row, 9)
	if state!='REJ':
		c+=1
	if c==1501:
		break
	if state!='REJ' and c>758:
		s1 = worksheet.cell_value(curr_row,3)
		print(s1)
		if not s1.endswith('.mp3'):
			c = c-1
			continue
		mp3file = urllib2.urlopen(s1)
		with open('acc_'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())
		filename = 'acc_'+str(c)+'.mp3'
		[idn,idn1] = filename.split('.')
		os.system('ffmpeg -i '+filename+' -acodec pcm_s16le -ac 1 -ar 16000 '+idn+'.wav'.format(filename))
			
print(c)
#
#
  #output.write(mp3file.read())