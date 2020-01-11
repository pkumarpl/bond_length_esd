
import sys
import collections
from collections import deque
if len(sys.argv)!=4:
    print("expected arguments: lsdb_output csv_file output_file")

lines = collections.deque()
with open(sys.argv[1], 'r', encoding="utf8", errors='ignore') as lsdb_out:
    lines = lsdb_out.readlines()
#    0     1  2       3       4   5     6     7  8   9       10    
#   X-H group : N((21)-H((21) >  X2-N-H =  0.777 /  1.027 Angstroms
bonds=collections.deque()
#bonds =[[]]

def get_label(label):
    result=""
    for c in label:
        if c!='(' and c!=')':
            result += c
    return result.lower()

def get_bond_label_h_first(label1, label2):
    if not (label1[0]=='H' and label2[0]=='H'):
        if label1[0]=='H':
            return (label1, label2)
        else:
            return (label2, label1)

def get_number(s):
    words=s.split('(')
    return float(words[0])

#   X-H group : O(1)-H(1) >  O-H in phenol =  0.853 /  0.992 Angstroms
def get_bond_type(words):
    type = words[5]
    i = 6
    while words[i] != "=":
        type += " "+words[i]
        i += 1
    return type
	
bond2type = dict()
bond2length = dict()

for line in lines:
    words = line.split()
    if len(words) > 10:
        if words[0]=="X-H":
            bonds.append(collections.deque())
            atoms=words[3].split('-')
            label1 = get_label(atoms[0])
            label2 = get_label(atoms[1])
            #bond2type[get_bond_label_h_first(label1,label2)] = words[5]
            bond2type[get_bond_label_h_first(label1,label2)] = get_bond_type(words)



with open(sys.argv[2], 'r') as csv:
    lines = csv.readlines()


for line in lines:
    words = line.split(',')
    if len(words)==8:
        if words[1][0]=='H' or  words[2][0]=='H':
            bond2length[get_bond_label_h_first(get_label(words[1]), get_label(words[2]))] = get_number(words[6])

typeInstances = dict()

for k, v in bond2type.items():
    if v in typeInstances:
        typeInstances[v].append( [k,bond2length[k]] )
    else:
        typeInstances[v] = [[k,bond2length[k]]]



with open(sys.argv[3],'w') as out:
    for type, data in typeInstances.items():
        out.write(type+"\n")
        for instance in data:
            out.write("   " + str(instance[0]) + " "  + str(instance[1]) + "\n")

