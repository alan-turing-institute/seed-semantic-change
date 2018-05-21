
# coding: utf-8

# In[70]:


# Basic variables and imports:

import codecs, csv, os, time, re, io
from os import listdir
from os.path import isfile, join
from  more_itertools import unique_everseen
from collections import Counter

# directories

# change dir_in for where the new outputs are
dir_in = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "src", "dynamic-senses","greek_input","all_results","genre_topic_output"))
dir_out = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "src", "dynamic-senses","greek_input","all_results","genre_topic_output","unique_versions"))



# In[71]:


output_file = io.open(dir_in+"/example_3genre_output.dat","r") # change this to whatever it's called
output_file_bis = io.open(dir_in+"/example_3genre_output.dat","r") # change this to whatever it's called


output_id = os.path.basename(output_file.name)
for line in output_file_bis.readlines()[1:2]:
    deuxieme_ligne_split = line.split(",")
    print(deuxieme_ligne_split)
    k = deuxieme_ligne_split[4]
    k = k.replace(" ","")
    k = k.replace("K","")
    k = int(k)
    print("k",k)

output_file = output_file.read()
output_files = list() # here we store filenames for the deduplicated

compteur = 0
liste_times = list()

splitted = output_file.split("===============  per time  ===============")[1].split("\n")
first_splitted = output_file.split("===============  per time  ===============")[0].split("\n")

for i in range(0,len(splitted)):
    if splitted[i][0:5] == "Time=": # for every line starting with "Time=" we count
        compteur+=1
        ok_time = splitted[i][0:8].replace(" ","")
        liste_times.append(ok_time) # we append this thing
        
print(liste_times)

final_number_of_output_files = 0
number_of_output_files = Counter(liste_times)

for key in number_of_output_files.keys():
    final_number_of_output_files = number_of_output_files[key]
    
print(final_number_of_output_files)

final_files = dict()
for numero in range(1,final_number_of_output_files+1):
    
    final_files[numero] = io.open(dir_out+"/"+output_id+"_"+str(numero),"w")
        
    


# In[75]:


already_seen_first = dict()

for line in first_splitted:
    if line[:6] == "p(w|s)":
        check_this = line.split(":")[0]
        check_this = check_this.split("  ")[1]
        print(check_this)
        if check_this in already_seen_first.keys():
            final_files[already_seen_first[check_this]+1].write("\n")
            final_files[already_seen_first[check_this]+1].write(line)
            final_files[already_seen_first[check_this]+1].write("\n")
            print(final_files[already_seen_first[check_this]+1])
            already_seen_first[check_this] += 1
            
        else:
            already_seen_first[check_this] = 0
            final_files[already_seen_first[check_this]+1].write("\n")
            final_files[already_seen_first[check_this]+1].write(line)
            final_files[already_seen_first[check_this]+1].write("\n")
            print(final_files[already_seen_first[check_this]+1])
            already_seen_first[check_this] += 1
            


# In[76]:


for key in final_files.keys():
    final_files[key].write("\n\n\n")
    final_files[key].write("===============  per time  ===============")
    final_files[key].write("\n\n\n")


# In[77]:


already_seen = dict()

for i in range(0,len(splitted)):
    if splitted[i][0:5] == "Time=": # for every line starting with "Time=" we count
        ok_time = splitted[i][0:8].replace(" ","")
        
        if ok_time in already_seen.keys():
            final_files[already_seen[ok_time]+1].write("\n")
            final_files[already_seen[ok_time]+1].write(ok_time)
            final_files[already_seen[ok_time]+1].write("\n")
            
            for ligne in range(i+1,i+k+1): # for k lines after i
                final_files[already_seen[ok_time]+1].write(splitted[ligne])
                final_files[already_seen[ok_time]+1].write("\n")
                print(final_files[already_seen[ok_time]+1])

                
            already_seen[ok_time] += 1
            
        else:
            already_seen[ok_time] = 0
            final_files[already_seen[ok_time]+1].write("\n")
            final_files[already_seen[ok_time]+1].write(ok_time)
            final_files[already_seen[ok_time]+1].write("\n")
            for ligne in range(i+1,i+k+1): # for k lines after i
                print(ligne)
                print(splitted[ligne])
                print(final_files[already_seen[ok_time]+1])
                final_files[already_seen[ok_time]+1].write(splitted[ligne])
                final_files[already_seen[ok_time]+1].write("\n")
            already_seen[ok_time] = 1
                
            #already_seen[ok_time] += 0
            
        
        
       

