import os
import re
from grkFrm import greekForms
new_dict = {}
dict_string = "greekForms="
for form,lemma in greekForms.items():
	for x in lemma:
		for y in x['a']:
			new_dict.setdefault(form,{}).setdefault(x['l'],set()).add(y)
print('%s{\n%s\n}'%(dict_string,',\n'.join(['"%s":%s'%(x,y) for (x,y) in new_dict.items()])), file=open('greekForms.py', 'w'))