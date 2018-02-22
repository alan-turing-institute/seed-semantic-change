from grkLemmata import greekLemmata
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
print('Bear with me a sec...')

POS = set()
for key,value in greekLemmata.items():
	POS.add(value.get('pos','unknown'))
output = ' '.join([x for x in POS])

open('TreeTaggerData/openclass.txt', 'w').write(output)
print('All done')