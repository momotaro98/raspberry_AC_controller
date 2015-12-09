#!/usr/bin/env  python

import os
import sys

try:
    argvs = sys.argv
    argc = len(argvs)
    SIGNAL_FILES_PATH = argvs[1]
    CONTROLLER_NAME = argvs[2]
    with open('lircd.conf', 'w') as f1:
        f1.write("begin remote\n")
        f1.write("\n")
        f1.write("  name  " + CONTROLLER_NAME + "\n")
        f1.write("  flags RAW_CODES\n")
        f1.write("  eps       30\n")
        f1.write("  aeps     100\n")
        f1.write("  aeps     100\n")
        f1.write("  gap   100000\n")
        f1.write("\n")
        f1.write("      begin raw_codes\n")
        f1.write("\n")

        ### Parse Process Start ###
        for dpath, dnames, fnames in os.walk(SIGNAL_FILES_PATH):
            for fname in fnames:
                print("Generate {0} Button...".format(fname))
                f1.write("          name " + fname + "\n")
                # parse process
                with open(dpath + '/' + fname, 'r') as f2:
                    read_count = 0
                    six_stock = 0
                    for line in f2:
                        read_count += 1
                        if read_count == 1:
                            continue
                        six_stock += 1
                        if six_stock == 6:
                            pro_line = line.split(" ")[1]
                            six_stock = 0
                        else:
                            pro_line = line.split(" ")[1].rstrip() + '\t'
                        f1.write(pro_line)
                f1.write("\n")
                f1.write("\n")
        ### Parse Process END ###

        f1.write("      end raw_codes\n")
        f1.write("\n")
        f1.write("end remote\n")
        f1.write("\n")

except IndexError:
    print("Error!")
    print("Usage Example: $ python raw_convert.py /home/pi/lirc CONTROLLER_NAME")
