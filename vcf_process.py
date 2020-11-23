import csv
import json 
import os

os.chdir('/home/raymond/Downloads/')
os.system('ls')

#extract the snp id information (use rs005 as an example)
os.system('less test_vcf.txt |grep "rs005" > rs005.txt ') #change me 'rs005'

#extract the sample information 
os.system('less test_vcf.txt |grep "CHROM" > sample.txt ') #change me

with open ('sample.txt') as f1:
  sample = f1.read().split('\t')[9:-1]
  #print(sample)

with open ('rs005.txt') as f2:
  snp = f2.read().split('\t')[9:-1]
  #print(snp)

#zip sample and snp together
sample_snp = list(zip(sample, snp))
print(sample_snp)

#save the sample and SNP information into a dictionary
def save_vcfinformation(input_tuple):
  sample_snp_dict = {}
  for i in input_tuple:
    sample_snp_dict[i[0]] = i[1]
  return sample_snp_dict

#transfer the genotype information to peptide information based on the genotype_peptide dict

genotype_peptide_dict = {
  'rs001:0|1':'H|R', 'rs002:0|1':'C|Y','rs003:0|1':'P|N','rs004:0|1':'J|K', 'rs005':'V|P'}

def trans_genotype(snp_id, input_dict):
  genotype_dict= {}
  for i in genotype_peptide_dict.keys():
    for j in input_dict.keys():
      if i.split(':')[0] == snp_id and input_dict[j] == '0|0':
        genotype_dict[j] = genotype_peptide_dict[i][0]+'|'+genotype_peptide_dict[i][0]
      elif i.split(':')[0] == snp_id and input_dict[j] == '0|1':
        genotype_dict[j] = genotype_peptide_dict[i][0]+'|'+genotype_peptide_dict[i][2]
      elif i.split(':')[0] == snp_id and input_dict[j] == '1|0':
        genotype_dict[j] = genotype_peptide_dict[i][2]+'|'+genotype_peptide_dict[i][0]
      elif i.split(':')[0] == snp_id and input_dict[j] == '1|1':
        genotype_dict[j] = genotype_peptide_dict[i][2]+'|'+genotype_peptide_dict[i][2]
  return genotype_dict


#save the result_peptide as a json file
def save_json(genotype_dict):
  with open ('/home/raymond/Desktop/sample_genotype_dict.json', mode='w', encoding='utf-8') as f:
    json.dump(genotype_dict, f)

#save the result_peptide as a csv file
def save_csv(genotype_dict):
  with open ('/home/raymond/Desktop/genotype_dict.csv', mode='w') as f:
    for i in genotype_dict.keys():
      f.write("%s, %s\n"%(i, genotype_dict[i]))


#test:
result_genotype = save_vcfinformation(sample_snp)
print(result_genotype)

result_peptide = save_vcfinformation(sample_snp)
#print(result_peptide)

result_genotype_peptide = trans_genotype('rs005', result_peptide)
#print(result_genotype_peptide)

save_json(result_genotype_peptide)
save_csv(result_genotype_peptide)


  