#! /usr/bin/python

import subprocess
import itertools
import json
import sys

req = ""
if len(sys.argv) == 2:
    req = sys.argv[1]

if len(sys.argv) == 4:
    px = sys.argv[1]
    sv = sys.argv[2]
    queryStat = sys.argv[3]

if len(sys.argv) != 2 and len(sys.argv) != 4:
    print "Usage: run script with one or three arguments\nOne argument: \n    discovery : json output of discovered pxname and svname \n\nThree arguments:\n    pxname : pxname in which you want to process the stat\n    svname : svname in the pxname in which you want to process the stat\n    stat : stat you want to query for pxname,svname"
    sys.exit(1)

allstats = subprocess.Popen('echo "show stat" | socat /var/lib/haproxy/stats stdio', shell=True, stdout=subprocess.PIPE).communicate()[0]

if req == "discovery":
    haDiscovery = []
    for myLine in allstats.splitlines()[1:-1]:
        lineStats = myLine.split(',')
        pxname = lineStats[0]
        svname = lineStats[1]
        haDiscovery.append({'{#PXNAME}' : pxname, '{#SVNAME}' : svname})
    print json.dumps({ "data": haDiscovery})
    sys.exit()

statNameList = allstats.splitlines()[0][2:-1].split(',')
monDico = {}
for myLine in allstats.splitlines()[1:-1]:
    statList = myLine.split(',')
    if px == statList[0] and sv == statList[1]:
        monDico = dict(itertools.izip(statNameList,statList))
        print monDico[queryStat]
