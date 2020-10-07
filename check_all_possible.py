import os
import struct, socket
import Queue
import threading
import urllib2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

new_dict = dict()

#store all the current candidates in a map
myfile=open("/Users/mr.Robot/Desktop/PROXY_CHECKER/candidates.txt")
read=myfile.read()
read=read.split()
for line in read:
	new_dict[line] = 1
myfile.close()

#put all the proxy ranges
myfile = open("/Users/mr.Robot/Desktop/PROXY_CHECKER/proxy_ranges.txt")
read = myfile.read()
read = read.split()
myfile.close()


response_url = "https://www.google.com/humans.txt"
google_return_value="Google is built by a large team of engineers, designers, researchers, robots, and others in many different sites across the globe. It is updated continuously, and built with more tools and technologies than we can shake a stick at. If you'd like to help us out, see google.com/careers.\n"
l=[]
threads=[]

def inc(str):
	ip2int = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]
	val = ip2int(str) + 1
	int2ip = lambda n: socket.inet_ntoa(struct.pack('!I', n))
	rev = int2ip(val)
	# ans = lambda n: socket.inet_ntoa(struct.pack('!I', n))
	return rev

myfile = open("/Users/mr.Robot/Desktop/PROXY_CHECKER/full_list.txt",'w')

for line in read:
	str = line.split("-")
	place = str[0]
	starting_add = str[1]
	ending_add = str[2]
	print(place + starting_add + ending_add)
	temp = starting_add
	while(temp!=ending_add):
		myfile.write(temp+":3128\n")
		myfile.write(temp+":8080\n")
		myfile.write(temp+":808\n")
		temp = inc(temp)

myfile.close()

myfile = open("/Users/mr.Robot/Desktop/PROXY_CHECKER/full_list.txt")
read = myfile.read()
urls = read.split()
myfile.close()


def CheckProxy(s):
    comm = "curl -s --connect-timeout 10 --proxy " + "http://" + s + " " + response_url
    var = os.popen(comm).read()
    if(var==google_return_value):
        print(s)
        l.append(s)


for u in urls:
    t = threading.Thread(target=CheckProxy,args=(u,))
    t.Daemon=False
    threads.append(t)

for x in threads:
	x.start()

for x in threads:
	x.join()

#Write all the new candidates into candidates.txt
write_into_candidates = open("/Users/mr.Robot/Desktop/PROXY_CHECKER/candidates.txt",'a')
for x in l:
	if not new_dict.has_key(x):
		write_into_candidates.write(x+"\n")
write_into_candidates.close()
