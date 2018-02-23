#this code is used to call metamap free text indexer and process the results
#Author: Bin Chen, July 2013

import csv
import os
import sys
from sets import Set

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def call_metamap(input_file, meta_file, temp_file):
    count = 0
    with open(input_file, 'rb') as f:
        lines = f.readlines()
        for line in lines:
            count = count + 1
            line = line.strip()
            line = removeNonAscii(line) # metamap does not support non-ascii characters
            os.system('echo "' + line + '" | ' + meta_file + ' -I > ' + temp_file + str(count) + '.txt')

def process_metamap(input_file, output_file):
    extract_pairs = open(output_file, "w")
    extract_pairs.write("input\tscore\tconcept_id\tconcept_name\tconcept_type\n")
    count = 0
    with open(input_file, 'rb') as f:
        reader = f.readlines()      
        for record in reader:
            count = count + 1 
            candidate_dzs = []
            try:
                with open(temp_file + str(count) + '.txt', "r") as f1:
                    lines = f1.readlines()
                    for line in lines:
                        line = line.strip()
                        if (line.find('[Disease or Syndrome]')>0):
                            line = line.replace('[Disease or Syndrome]','')
                            type = "Disease or Syndrome"
                        elif (line.find('[Neoplastic Process]')>0):
                            line = line.replace('[Neoplastic Process]','')
                            type = "Neoplastic Process"
                        elif (line.find('[Sign or Symptom]')>0):
                            line = line.replace('[Sign or Symptom]','')
                            type = "Sign or Symptom"
                        else:
                            continue
                            
                        #get the score
                        score = (line[0:line.find(" ")].strip()).strip()
                        concept_id = (line[line.find(" "):].split(":")[0]).replace(" E ","").strip()
                        concept_name = (line[line.find(" "):].split(":")[1]).strip()
                        candidate_dzs.append(str(score) + "\t" + concept_id + "\t" + concept_name + "\t" + type)
            except IOError:
               print 'no file found for ' + str(count)
               
            #remove the redunct
            candidate_dzs = Set(candidate_dzs)

            for candidate_dz in candidate_dzs:
                extract_pairs.write( record.strip() + "\t" + candidate_dz + "\n")

    extract_pairs.close()
        
    
if len(sys.argv) != 5:
    print("please input as : python call_metamap.py input_file (the data to process), output_file, temp_file, meta_file ")
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    temp_file = sys.argv[3]
    meta_file = sys.argv[4]

print(input_file + output_file + temp_file + meta_file)
call_metamap(input_file, meta_file, temp_file)
process_metamap(input_file, output_file)
    

        
    
