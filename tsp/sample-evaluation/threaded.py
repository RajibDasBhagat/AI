import subprocess, threading
import signal
import shlex
import time

"""We spawn a new process inside a thread"""

class Command(object):
    def __init__(self, cmd, infile, outfile):
        self.cmd = cmd
        self.infile = infile
        self.outfile = outfile
        self.process = None

    def run(self, timeout):
        def target():
            print('Thread started')
            self.process = subprocess.Popen(shlex.split(self.cmd), stdin=self.infile, stdout=self.outfile)
            self.process.communicate()
            print('Thread finished')

        thread = threading.Thread(target = target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print('Terminating process')
            self.process.terminate()
            #give it time to terminate
            time.sleep(4)
            print('after sleep')
            print thread.is_alive()
            if thread.is_alive():
               #SIGTERM failed. Resort to SIGKILL
               print('terminate failed: killing')
               self.process.kill()
            thread.join()
