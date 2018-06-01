import re
import os
from grkLemmata import greekLemmata
files = input('Data file(s) to decode: ').strip().split(' ')
for file in files:
	file = file.replace('\\ ', ' ')
	data = open(file, 'r').read()
	print('Processing')
	if os.path.splitext(file)[1] == '.dat':
		processed_data = re.sub('((nlsj)?\d+)( \(.*?\) ;)', lambda m : '%s [%s]%s'%(greekLemmata[m.group(1)]['lemma'], m.group(1), m.group(3)), data)
	else:
		processed_data = re.sub('(?<=[ \t])(nlsj)?\d+',lambda m : greekLemmata.get(m.group(0),{'lemma':m.group(0)})['lemma'], data)
	output = open(file+'_decoded.txt', 'w')
	output.write(processed_data)
	output.close()
print('All done')