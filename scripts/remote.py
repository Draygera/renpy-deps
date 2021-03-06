#!/usr/bin/env python

import argparse
import socket
import subprocess
import os
import traceback
import sys
import threading

SECRET="I didn't really want to write this code, but ssh on windows sucked so bad."


def server():
    ss = socket.socket()
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(('0.0.0.0', 22222))
    ss.listen(1)
    
    while True:
        print
        print "Waiting..."
        print
        
        try:

            s, addr = ss.accept()

            f = s.makefile("rb+")

            secret = f.readline()
            if secret[:-1] != SECRET:
                print "Bad secret.", repr(secret)
                f.close()
                s.close()
                continue

            cmd = [ ]
            
            for l in f:
                l = l[:-1]
                if not l:
                    break

                cmd.append(l)

            print cmd
                
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            lock = threading.Lock()
            
            def stdout_thread():
                while True:
                    l = proc.stdout.readline()
                    if not l:
                        break
                    
                    with lock:                        
                        f.write("O " + l)
                        sys.stdout.write(l)


            def stderr_thread():
                while True:
                    l = proc.stderr.readline()
                    if not l:
                        break
                    
                    with lock:                        
                        f.write("E " + l)
                        sys.stdout.write(l)
                        
            t1 = threading.Thread(target=stdout_thread)
            t2 = threading.Thread(target=stderr_thread)
            t1.start()
            t2.start()


            t1.join()
            t2.join()

            proc.wait()

            f.write("R %d\n" % proc.returncode)

            f.close()
            s.close()
        except Exception:
            traceback.print_exc()
            continue

        
server()
