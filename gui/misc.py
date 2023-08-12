import sys
import subprocess
import customtkinter as ctk
from typing import TextIO


class StdoutRedirector(TextIO):
    def __init__(self,text_widget: ctk.CTkTextbox):
        self._text_space = text_widget
        #self._text_space.tag_config(tagName='ERROR', background="black", foreground="red")
        self._default_stdout = None
        self.enable()

    def write(self, string):
            # FIXME: Next line would be preffered to keep config after writing but get next incoherent exception
            #        ValueError: 'state' is not a supported argument. Look at the documentation for supported arguments.
            # prev_state = self._text_space.cget("state")
            self._text_space.configure(state="normal")
            #try:
            #    # FIXME: No aplica el tag. De todas formas este codigo no se lo deseo ni a mi peor enemigo, hay que mejorar esta abominacion
            #    start_idx = string.index(bcolors.FAIL)
            #    string = string.replace(bcolors.FAIL,"")
            #    end_idx = string.index(bcolors.ENDC)
            #    string = string.replace(bcolors.ENDC,"")
            #    self._text_space.insert('end', string)
            #    self._text_space.tag_add(tagName='ERROR', index1=int(start_idx), index2=int(end_idx))
            #except:
            #    pass
            self._text_space.insert('end', string)
            self._text_space.see('end')
            #self._text_space.configure(prev_state)
            self._text_space.configure(state="disabled")

    def enable(self, on:bool=True):
        if on:
            self._default_stdout = sys.stdout
            sys.stdout = self
        else:
            sys.stdout = self._default_stdout
        self._enabled = on

    def disable(self):
        self.enable(False)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def execute(cmd) -> int:
    #proc = subprocess.Popen( "python querier.py -h".split(), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print( proc.stdout.read() )
    proc = subprocess.Popen( cmd.split(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    out, err = proc.communicate()
    if len(out) > 0: print( out )
    if len(err) > 0: print( bcolors.FAIL + err + bcolors.ENDC ) # print in red
    return proc.returncode