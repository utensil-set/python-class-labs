# Alex Cutler
# Lab #16
# 
# This lab is a simple port scanner. It is given an IP address, performs a sweep of the target,
# and prints the results here and to a file it generates.
#
# This lab heavily borrows from what I learned at this site:
# https://www.neuralnine.com/threaded-port-scanner-in-python/
# As in all cases like this, I have tried to be original in my code creation, understand what it's all doing,
# and not simply copy. However, I struggled to understand many of the concepts behind port scanning,
# so my best efforts still are mostly a case of just following along with past examples.
#

import socket, threading
from queue import Queue

# portMin and PortMax are used to ensure user input doesn't fall outside of the acceptable range.
portMin = 0
portMax = 65535

#queueing is new to me but necessary to run the threads in the way we need.
queue = Queue() 
open_ports = []
closed_ports = []
target = '45.33.32.156'

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect ((target, port))
        return True
    except:
        return False

# this function is pulled from the site almost word-for-word
# since I was unable to find a way to "put my spin on it" without ruining the function.
# an addition that I can call my own is the else action for adding closed ports to a list.
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f'Port {port} is open!')
            open_ports.append(port)
        else:
            closed_ports.append(port)


# This portion of the program gets the threads up, running, and working to scan.
# Without this, things would move way, waaaay too slowly.
# I attempted to make it as original as possible, but again, I was only able to deviate from the source code by so much.
def scanGo(threads):

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print(f'There were {len(open_ports)} open ports and {len(closed_ports)} closed ports.')
    print('Open ports are:')
    open_ports.sort()
    print(open_ports)
    print('\nClosed (or maybe filtered) ports are:')
    closed_ports.sort()
    print(closed_ports)
    print()

# Writing output to the created file.    
    cutlerLab16File = open(r'cutlerLab16.txt', 'a')
    for i in open_ports:
        cutlerLab16File.write(f'Port #{i} is open!\n')
    cutlerLab16File.write(' \n')
    for i in closed_ports:
        cutlerLab16File.write(f'Port #{i} is closed or potentially filtered.\n')
    cutlerLab16File.close()
        

# In the program I drew inspiration from, this function was the mode selector.
# But for our purposes, the user has already specified the port range to scan so this is very short.
def portExec(portLow, portHigh):
    for port in range(portLow, portHigh + 1):
        queue.put(port)
    

def labStart():

    cutlerLab16File = open(r'cutlerLab16.txt', 'w')
    cutlerLab16File.close()

    print('This program is going to run a scan against http://scanme.nmap.org/')
    print('Please select the range of ports you\'d like to scan.\nSmaller ranges will scan faster...')
    while True:
        portLowEntry = input('Select the low end of your range: ')
        if int(portLowEntry) < portMin or int(portLowEntry) > portMax:
            print('No. Try again.')
            continue
        portHighEntry = input('Select the high end of your range: ')
        if int(portHighEntry) < int(portLowEntry) or int(portHighEntry) > portMax:
            print('No. Try again.')
            continue
        else:
            break
        
        
    portLow = int(portLowEntry)
    portHigh = int(portHighEntry)

    portExec(portLow, portHigh)

#I decided to have 200 threads running. if this speed is too slow or fast, please feel free to adjust it.    
    scanGo(200)
    
labStart()
