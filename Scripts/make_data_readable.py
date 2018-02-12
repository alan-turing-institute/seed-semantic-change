import re
from grkLemmata import greekLemmata
file = input('Data file to decode: ').strip().replace('\\ ', ' ')
data = open(file, 'r').read()
print('Processing')
processed_data = re.sub('((nlsj)?\d+)( \(.*?\) ;)', lambda m : '%s [%s]%s'%(greekLemmata[m.group(1)]['lemma'], m.group(1), m.group(3)), data)
output = open(file+'_decoded.txt', 'w')
output.write(processed_data)
output.close()
print('All done')