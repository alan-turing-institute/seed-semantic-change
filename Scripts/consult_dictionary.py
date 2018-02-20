from grkLemmata import greekLemmata
import re
import pyperclip

query = input('Input either word form(s) or id(s): ')
output = []
for entry in query.split(' '):
	if re.search('\d', entry) == None:
		list_values = []
		for value, items in greekLemmata.items():
			if items['lemma'] == entry:
				list_values.append(value)
		output.append(list_values)
	else:
		output.append(greekLemmata.get(entry,{'lemma':'unknown'})['lemma'])
outputstring=''
if not isinstance(output[0],str):
	for idx,x in enumerate(output):
		output[idx]='/'.join(x)
print(' '.join(output))
pyperclip.copy(' '.join(output))
		