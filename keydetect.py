#!/usr/bin/

from subprocess import Popen, PIPE
import os, signal
from sys import stdout
from re import split

class Proc(object):
    ''' Data structure to store the output of 'ps aux' command '''
    def __init__(self, proc_info):
        self.user = proc_info[0]
        self.pid = proc_info[1]
        self.cpu = proc_info[2]
        self.mem = proc_info[3]
        self.vsz = proc_info[4]
        self.rss = proc_info[5]
        self.tty = proc_info[6]
        self.stat = proc_info[7]
        self.start = proc_info[8]
        self.time = proc_info[9]
        self.cmd = proc_info[10]

    def to_str(self):
        ''' Returns a string containing minimalistic info
        about the process : user, pid, and command '''
        return '%s %s %s' % (self.user, self.pid, self.cmd)
    def name(self):
	''' Return command only'''
	return '%s' %self.cmd	
    def procid(self):
	'''Return pid only'''
	return '%s' %self.pid


def kill_logger(key_pid):
    print("Do you want to stop this keylogger: y/n ?")
    response = raw_input()
    if (response=="y" or response =="Y"):
	os.kill(int(key_pid), signal.SIGKILL)
    else:
	pass
	 

def get_proc_list():
    ''' Retrieves a list [] of Proc objects representing the active
    process list list '''
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    #Discard the first line (ps aux header)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        #The separator for splitting is 'variable number of spaces'
        proc_info = split(" *", line.strip())
        proc_list.append(Proc(proc_info))
    return proc_list

if __name__ == "__main__":
	proc_list = get_proc_list()
	#Show the minimal proc list (user, pid, cmd)
	stdout.write('Process list:\n')
	for proc in proc_list:
		stdout.write("\t" + proc.to_str() + "\n")
		

	proc_cmd=[]
	proc_pid=[]

	for proc in proc_list:
		stdout.write("\t" + proc.name()+ "\n")	
    		proc_cmd.append(proc.name())
		proc_pid.append(proc.procid())		

	print(proc_cmd)

	l1 = ["logkey","keylog","keysniff","kisni","lkl","ttyrpld","uber","vlogger"]

	record=0
	flag=1

    	for x in proc_cmd:
		for y in l1:
			if(x.find(y)>-1):
				print(" KeyLogger Detected: "+proc_pid[record]+" ---> "+x)
				kill_logger(proc_pid[record])
				flag=0
		record+=1
				

	if(flag):
		print("No Keylogger Detected")
