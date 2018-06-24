import urllib2
import xlrd



ExcelFileName= 'up_hindi belt_Item_data.xlsx' #initially mp
workbook = xlrd.open_workbook(ExcelFileName)
worksheet = workbook.sheet_by_name("kab_item_data")
num_rows = worksheet.nrows #Number of Rows
num_cols = worksheet.ncols #Number of Columns
print(num_rows)
print(num_cols)
c=0
for curr_row in range(0,num_rows, 1):
	data = worksheet.cell_value(curr_row, 6)
	if data=='M':
		c+=1
	if c==4:
		break
	if data=='M':
		s1 = worksheet.cell_value(curr_row,2)
		mp3file = urllib2.urlopen(s1)
		with open('tstm'+str(c)+'.mp3','wb') as output:
			output.write(mp3file.read())


	
print(c)

#
#
  #output.write(mp3file.read())