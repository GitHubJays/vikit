#encoding:utf-8
import os

#default arguments
DEFAULT_ARUGUMENTS = '-n -Pn -T4'
DEFAULT_ARUGUMENTS_WITH_VERSION_DETECTION_PRO = '--version-all -sV -n -Pn -T4 '
DEFAULT_ARUGUMENTS_WITH_VERSION_DETECTION = '--version-all -sV -n -Pn -T4 '

#timeout setting
DEFAULT_NMAP_TIMEOUT = '--max-rtt-timeout 10000ms'

#detect_version
VERSION_DETECT = '-sV'

#Fast Scan Port List
ALL_KNOWN_PORT = [7,9,13,21,22, 23,25, 26,37,53,79 , 80 ,81,88,
                  106,110,111,113,119,135,139,143,144,179,199,389,427,443,444,445,
                  465,513,514,515,543,544,548,554,587,631,646,873,990,993,995,
                  1025,1026,1027,1028,1029,1110,1433,1720,1723,1755,1900,
                  2000,2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,
                  5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,
                  6000,6001,6646,7070,8000,8008,8009,8080,8081,8443,8888,
                  9100,9999,10000,32768,49152,49152,49153,49154,49155,49156,49157]

DEFAULT_SCAN_PORT = [20,21,69,
                     2049,
                     137,139,
                     389, 
                     22,
                     23,
                     3389,
                     5900,5901,5902,5903,5904,5905,
                     5632,
                     80,81,443,8080,7001,
                     1098,1099,4444,4445,8080,8009,8083,8093,
                     9090,9080,9081,9082,9083,9084,9085,9086,9087 ,9088 ,9089 ,
                     3700,4848,8089,5432,
                     1352,3306,1433,1434,
                     1521,1158,8080,210,
                     27017,6379,5000,4100,4200,
                     25,465,109,110,995,
                     143,993,53,67,68,546,161,
                     2181,8069,9200,9300,11211,512,513,514,1090,1099,873,1080]

#scan ports
SCAN_SERVERS_ON_NMAP_LIST = '-F'

#scan most common ports
COMMON_PORTS_100 = '--top-ports 100'
COMMON_PORTS_50  = '--top-ports 50'
COMMON_PORTS_150 = '--top-ports 150'
COMMON_PORTS_200 = '--top-ports 200'

#sys info
OS_SCAN = '-O'

#speed
SPEED_T4 = '-T4'
SPEED_T5 = '-T5'
SPEED_T3 = '-T3'
SPEED_T2 = '-T2'
SPEED_T1 = '-T0'

NO_DNS = '-n'
NO_HOST_DISCOVER = '-Pn'

def generate_arguments(*arg):
    arguments = ''
    if arg == None:
        arguments = ''
    else:
        for i in arg:
            arguments = arguments + ' ' + i
    #print arguments
    return arguments.strip()