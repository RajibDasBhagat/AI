
# coding: utf-8

# In[3]:


import os
import stat
import sys
import csv
from threaded import *

"""run 'make' in every group's folder
"""
def makeall(dirname):
    origdir = os.getcwd()
    subdir = os.path.join(os.getcwd(), dirname)
    submission_dirs = [ name for name in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, name)) ]
    
    for name in submission_dirs:
        os.chdir(os.path.join(subdir, name))
        if os.path.isfile('makefile') or os.path.isfile('MakeFile') or os.path.isfile('makeFile') or os.path.isfile('Makefile'):
            print('making in ' + str(os.getcwd()))
            os.system('make')
        os.chdir(subdir)
    os.chdir(origdir)
    
"""
Checks if the last tour printed by the program is valid or not.
Returns the cost of valid tour. If the last line is partially printed, checks the last-but-one line instead

outfile: Path of the program's output file
probfile: Path of the problem file
"""
def validate(outfile, probfile):
    pfile = open(probfile, 'r')
    ofile = open(outfile, 'r')
    plines = pfile.readlines()
    pfile.close()
    #mat is the pairwise distance matrix
    #n is the number of cities
    n = int(plines[1])
    mat = []
    for i in range(2+n, 2+(2*n)): 
        line = plines[i].split()
        row = [float(s) for s in line]
        mat.append(row)
        
    olines = ofile.readlines()
    ofile.close()
    
    if len(olines) == 0:
        print('empty file - program printed nothing')
        return 'empty file'
    last_line = olines[-1].split()
    
    if len(last_line)!=n and len(olines)>=2:
        #last line incomplete - go to second last line
        second_last_line = olines[-2].split()
        if len(second_last_line) != n:
            print('last second line also has wrong number of cities:')
            print(len(second_last_line))
            return '-2 also x'
        else:
            l = second_last_line
    elif len(last_line)!=n and len(olines)<2:
        print('last line has incorrect no. of cities but no second last line to go to:')
        print(len(last_line)) 
        return '-1 x no -2'
    else:
        l = last_line
    try:
        l = [int(x) for x in l]
    except:
        print('Not printing integers')
        return 'not int'
    l_copy = list(l)
    l.sort()
    
    for i in range(n-1):
        if l[i] == l[i+1]:
            print('city repitition - invalid tour:')
            print(l[i])
            return 'city repeat'
    
    if l[n-1] == len(l_copy):
        print('city indexing error - start from 0')
        return 'city indexing error'
    
    #valid tour - computing the cost
    print("computing cost now")
    print(len(l_copy))
    
    cost = 0
    for i in range(n-1):
        cost += mat[l_copy[i]][l_copy[i+1]]
    cost += mat[l_copy[n-1]][l_copy[0]]
    print("cost:", cost)
    return cost
    


# In[ ]:


"""
   probdirname: the folder conatining problem files
   subdirname: the folder containing group folders
   trial: the trial number 
"""
def main_run(probdirname, subdirname, trial):
    #print(probdirname, subdirname, trial)
    origdir = os.getcwd()
    #print(origdir)
    probdir = os.path.join(origdir, probdirname)
    #print(probdir)
    
    #probfiles is the list of paths of problem files:
    probfiles = [ os.path.join(probdir,f) for f in os.listdir(probdir) if os.path.isfile(os.path.join(probdir,f)) ]
    #print(probfiles)
    #print(subdirname)
    subdir = os.path.join(origdir, subdirname)
    
    #subdirs is the list of paths of group folders:
    subdirs = [ os.path.join(subdir,name) for name in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, name)) ]
    #print(subdirs)
    #rows in this matrix are groups. columns are problem instances, though the first column holds group name. 
    #result[i][j] records the performance of group i on problem j-1.
    result = [ [0 for x in range(len(probfiles)+1)] for y in range(len(subdirs)) ]
    #print(result)
    g = 0
    
    #iterating over group folders
    for groupdir in subdirs:
        #print(groupdir)
        result[g][0] = os.path.basename(groupdir)
        #change current working directory to the group directory
        os.chdir(groupdir)
        #create directory named with current trial for this group 
        try:
            os.mkdir('trial'+ str(trial))
        except:
            print('Incorrect trial number: folder already exists in the group directory')
        p = 1
        
        #iterating over problem files
        for probfile in probfiles:          
            print(p)
            
            prob_in = open(probfile,'r')
            prob_out_path = os.path.join(groupdir, 'trial'+str(trial), os.path.basename(probfile)+'_out')
            prob_out = open(prob_out_path, 'w+')
            TIMEOUT = 300
            if os.path.isfile('run'):
                run_path = os.path.join(groupdir, 'run')
                cmdfile = open(run_path, 'r')
                cmdline = cmdfile.readlines()
                #print("cmdline",cmdline)
                cmdfile.close()
                command = Command(cmdline[0], prob_in, prob_out)
                command.run(timeout=TIMEOUT) 
				#print("command",command)
            else:
                print('cmd failed')
            prob_in.close()
            prob_out.close()
            
            #validate and compute cost
            result[g][p] = str(os.path.basename(probfile)+' : '+str(validate(prob_out_path, probfile)))
            #print(result[g][p])
            p += 1
            
        g += 1
    os.chdir(origdir)
    return result

	
#problems="G://sample-evaluation/problems"
#submissions="G://sample-evaluation/submission/32"	
trial = int(sys.argv[1])
makeall('submissions')
result = main_run("problems", "submissions", trial)
mycsv = open('results'+ str(trial),'w+')
wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)
wr.writerows(result)
mycsv.close()

