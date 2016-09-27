import datetime
import os
import sys

verbose = False
if len(sys.argv) == 2:
	if sys.argv[1] == "-v":
		verbose = True

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

files = listdir_nohidden("running_instructions")
for fname in files:
	print ""
	team_name = fname.split(".")[0]
	fname = "running_instructions/" + fname
	f = open(fname,"r")
	instructions =  f.read().strip()
	out_fname = "outputs/" + team_name + ".out"
	call = instructions + " > " + out_fname
	f.close()
	start = datetime.datetime.now()
	os.system(call)
	end = datetime.datetime.now()
	t = end - start
	print team_name
	if t.seconds >= 120:
		print "\n\tcode took too long to run. No points awarded."
	if verbose:
		os.system("python OTManager.py given_info.txt " + out_fname + " -v")
	else:
		os.system("python OTManager.py given_info.txt " + out_fname)
	


