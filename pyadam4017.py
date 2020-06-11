import time
import datetime
import serial
import glob
import os

# Scan for /dev/ttyUSB* port and use first available
dev  = '/dev/ttyUSB*'
scan = glob.glob(dev)
if (len(scan) == 0):
    print ('Unable to find any ports scanning for ' + dev)
    os.system(" ( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid")
    exit(1)
else:
    print('Use port: ' + scan[0])
serport = scan[0]
ser = serial.Serial(port=serport, timeout=0.08)

# Create .csv file
try:
    time_create = time.strftime("%Y_%m_%d-%H_%M_%S", time.gmtime())
    filename = 'adam_' + time_create + '.csv'
    file_csv = open(filename, 'w')
    head = "Time;Chanel 0;Chanel 1;Chanel 2;Chanel 3;Chanel 4;Chanel 5;Chanel 6;Chanel 7;" + \
    "Chanel 8;Chanel 9;Chanel 10;Chanel 11;Chanel 12;Chanel 13;Chanel 14;Chanel 15;\n"
    file_csv.write(head)
    file_csv.close()
    # Write data from 2 modules ADAM-4017 to .csv file
    while True:
        file_csv = open(filename, 'a')
        i = 1
        while i <= 60:
            time_current = time.strftime("%H:%M:%S", time.gmtime())
            ser.write(b'#01\r')     
            time.sleep(0.08)
            line1 = ser.readline().decode()
            ser.write(b'#02\r')     
            time.sleep(0.08)
            line2 = ser.readline().decode()
            full_line = time_current + ';' + line1[1:8] + ';' + line1[8:15] + ';' + line1[15:22] + \
            ';' + line1 [22:29] + ';' + line1[29:36] + ';' + line1[36:43] + ';' + line1[43:50] + \
            ';' + line1[50:57] + ';' + line2[1:8] + ';' + line2[8:15] + ';' + line2[15:22] + \
            ';' + line2 [22:29] + ';' + line2[29:36] + ';' + line2[36:43] + ';' + line2[43:50] + \
            ';' + line2[50:57] + '\n'
            file_csv.write(full_line)
            time.sleep(0.84)
            i += 1
        file_csv.close()
except OSError:
    os.system(" ( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid")
except UnicodeError:
    os.system(" ( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid")
    time.sleep(0.4)
    os.system(" ( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid")   