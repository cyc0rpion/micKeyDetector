#!/usr/bin/

from subprocess import Popen, PIPE
import os, signal
from sys import stdout
from re import split

class Process(object):
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
        ''' Return user, pid, and command '''
        return '%s %s %s' % (self.user, self.pid, self.cmd)
    
    def name(self):
	''' Return command only'''
	return '%s' %self.cmd	
   
    def procid(self):
	'''Return pid only'''
	return '%s' %self.pid


def kill_logger(key_pid):
    stdout.write("\n\nDo you want to stop this process: y/n ?"),
    response = raw_input()
    if (response=="y" or response =="Y"):
	os.kill(int(key_pid), signal.SIGKILL)
    else:
	pass
	 

def get_process_list():
    ''' Retrieves a list of Process objects representing the active process list list '''
    process_list = []
    sub_process = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    #Discard the first line (ps aux header)
    sub_process.stdout.readline()
    for line in sub_process.stdout:
        #The separator for splitting is 'variable number of spaces'
        proc_info = split(" *", line.strip())
        process_list.append(Process(proc_info))
    return process_list

if __name__ == "__main__":
	
	process_list = get_process_list()
	
	stdout.write('Reading Process list...\n')
	
		
	process_cmd=[]
	process_pid=[]

	for process in process_list:	
    		process_cmd.append(process.name())
		process_pid.append(process.procid())		

	l1 = ["logkey","keylog","keysniff","kisni","lkl","ttyrpld","uber","vlogger"]

	record=0
	flag=1

    	for x in process_cmd:
		for y in l1:
			if(x.find(y)>-1):
				stdout.write("KeyLogger Detected: \nThe following proccess may be a key logger: \n\n\t"+process_pid[record]+" ---> "+x)
				kill_logger(process_pid[record])
				flag=0
		record+=1
				

	if(flag):
		print("No Keylogger Detected")
		
		

		
