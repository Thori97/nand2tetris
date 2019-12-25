import os
import time
from pprint import pprint
filename = input()
#filename = "rect/Rect.asm"
while not os.path.exists(filename):
    print(filename," not found")
    filename = input()
f=open(filename, "r")
print(filename," opened!")
codes = []
for row in f:
    codes.append(row)
f.close()

class Parser:
    def __init__(self, Codes):
        self.codes=Codes
    def remove_comments(self):
        tcodes = self.codes
        for c in tcodes:
            if "//" in c:
              start = c.find("//")
              index = tcodes.index(c)
              tcodes[index] = c[0:start]
        self.codes=tcodes
    def remove_emptyline(self):
        tcodes = self.codes
        newCodes=[]
        for i in range(0,len(tcodes)):
            c = tcodes[i]
            if c== '' or c == '\n':
                continue
            else:
                newCodes.append(c)
        self.codes=newCodes
    def remove_return(self):
        tcodes = self.codes
        for i in range(0, len(tcodes)):
            c = tcodes[i]
            if '\n' in c:
                tcodes[i] = c[0:c.find('\n')]
        self.codes = tcodes
    def cut_space(self):
        for i in range(len(self.codes)):
            self.codes[i] = self.codes[i].strip()
    def separate(self):
        tcodes = self.codes
        for i in range(0, len(tcodes)):
            if "@" in tcodes[i]:#A
                s=tcodes[i].find('@')
                tcodes[i] = ["A","@", tcodes[i][s+1:]]
            elif (';' in tcodes[i]) and ('J' in tcodes[i]):#J
                s = tcodes[i].find(';')
                tcodes[i] = ["J",[tcodes[i][0:s]],tcodes[i][s+1:]]
                if "=" in tcodes[i][1]:
                    s1 = tcodes[i][1].find('=')
                    tcodes[i][1] = [tcodes[i][1][0:s1],tcodes[i][1][s1+1:]]
            elif '=' in tcodes[i]:#C
                s = tcodes[i].find('=')
                tcodes[i] = ["C",tcodes[i][0:s],tcodes[i][s+1:]]
            elif '(' in tcodes[i] and ')' in tcodes[i]:
                s=tcodes[i].find('(')
                e=tcodes[i].find(')')
                tcodes[i] = ["L",tcodes[i][s+1:e]]
            else:
                print("line",i+1, "invalid code", tcodes[i])
        self.codes = tcodes
    def parse(self):
        self.remove_comments()
        self.remove_emptyline()
        self.remove_return()
        self.cut_space()
        self.separate()
def comptobin(c):
    comp = ""
    if c == "M" or c == "A":
        comp = "110000"
    elif c == "!M" or c== "!A":
        comp = "110001"
    elif c=="-M" or c=="-A":
        comp = "110011"
    elif c=="M+1" or c=="A+1":
        comp = "110111"
    elif c=="A-1" or c=="M-1":
        comp = "110010"
    elif c=="D+A" or c=="D+M":
        comp = "000010"
    elif c=="D-A" or c=="D-M":
        comp = "010011"
    elif c=="A-D" or c=="M-D":
        comp = "000111"
    elif c=="D&A" or c=="D&M":
        comp = "000000"
    elif c=="D|A" or c=="D|M":
        comp = "010101"
    elif c=="0":
        comp = "101010"
    elif c=="1":
        comp = "111111"
    elif c=="-1":
        comp = "111010"
    elif c=="D":
        comp = "001100"
    elif c=="!D":
        comp = "001101"
    elif c=="-D":
        comp = "001111"
    elif c=="D+1":
        comp = "011111"
    elif c=="D-1":
        comp="001110"
    return comp
def desttobin(c):
    d = ""
    if c=="null":
        d="000"
    elif c=="M":
        d="001"
    elif c=="D":
        d="010"
    elif c=="MD":
        d="011"
    elif c=="A":
        d="100"
    elif c=="AM":
        d="101"
    elif c=="AD":
        d="110"
    elif c=="AMD":
        d="111"
    return d
def jumptobin(c):
    j=""
    if c=="null":
        j="000"
    elif c=="JGT":
        j="001"
    elif c=="JEQ":
        j="010"
    elif c=="JGE":
        j="011"
    elif c=="JLT":
        j="100"
    elif c=="JNE":
        j="101"
    elif c=="JLE":
        j="110"
    elif c=="JMP":
        j="111"
    return j
def interA(Acommand):
    if Acommand[0]!='A':
        print("This is not A command!!")
        return 0
    else:
        ret = "0"
        val = format(int(Acommand[2]), '015b')
        return ret+val
def interC(Ccommand):
    if Ccommand[0]!='C':
        print("This is not Ccommand!!")
    else:
        ret = "111"
        if 'M' in Ccommand[2]:
            a = '1'
        else:
            a = '0'
        c = Ccommand[2]
        comp=comptobin(c)
        dest=desttobin(Ccommand[1])
        jump = "000"
        return ret+a+comp+dest+jump
def interJ(Jcommand):
    if Jcommand[0]!='J':
        print("This is not Jcommand!")
    else:
        ret = "111"
        comp = ""
        jump = ""
        a= ""
        if len(Jcommand[1])==1:
            if 'M' in Jcommand[1]:
                a='1'
            else:
                a='0'
            comp = comptobin(Jcommand[1][0])
            dest = "000"
            jump = jumptobin(Jcommand[2])
            return ret+a+comp+dest+jump
        else:
            if 'M' in Jcommand[1][0]:
                a='1'
            else:
                a='0'
            comp = comptobin(Jcommand[1][1])
            dest = desttobin(Jcommand[1][0])
            jump = jumptobin(Jcommand[2])
            return ret+a+comp+dest+jump
class Encode:
    def __init__(self, Codes):
        self.codes = Codes
    def conversion(self):
        Codes = self.codes
        for i in range(len(Codes)):
            c = Codes[i]
            if c[0] == 'A':
                #print(interA(c))
                self.codes[i] = interA(c)
            elif c[0] == 'C':
                #print(interC(c))
                self.codes[i] = interC(c)
            elif c[0] == 'J':
                #print(interJ(c))
                self.codes[i] = interJ(c)
            else:
                print("syntaxerror")
                time.sleep(100000)
class SymbolTable:
    def __init__(self, codes):
        self.codes = codes
        self.table = {}
    def init_table(self):
        t = self.table
        t['SP'] = 0
        t['LCL'] = 1
        t['ARG'] = 2
        t['THIS'] = 3
        t['THAT'] = 4
        t['R0'] = 0
        t['R1'] = 1
        t['R2'] = 2
        t['R3'] = 3
        t['R4'] = 4
        t['R5'] = 5
        t['R6'] = 6
        t['R7'] = 7
        t['R8'] = 8
        t['R9'] = 9
        t['R10'] = 10
        t['R11'] = 11
        t['R12'] = 12
        t['R13'] = 13
        t['R14'] = 14
        t['R15'] = 15
        t['SCREEN'] = 16384
        t['KBD'] = 24576
        self.table = t
    def firstcheck(self):
        Codes = self.codes
        t = self.table
        newCodes = []
        for i in range(len(Codes)):
            c = Codes[i]
            if c[0] == 'L':
                if not c[1] in t:
                    t[c[1]] = len(newCodes)
            else:
                newCodes.append(c)
        self.codes = newCodes
        self.table = t
    def secondcheck(self):
        Codes = self.codes
        t = self.table
        nex = 16
        for i in range(len(Codes)):
            c = Codes[i]
            if c[0] == 'A':
                if not c[2][0].isdigit():
                    if not c[2] in t:
                        t[c[2]] = nex
                        nex+=1
                    c[2] = t[c[2]]
            elif c[0] == 'C':
                for j in range(1, 3):
                    if c[j][0].isdigit():
                        continue
                    elif c[j] == 'null' or c[j] == 'M' or c[j] == 'D'or c[j] == 'MD'or c[j] == 'A'or c[j] == 'AM'or c[j] == 'AD'or c[j] == 'AMD'\
                        or '-' in c[j] or '!' in c[j] or '+' in c[j] or '&' in c[j] or '|' in c[j]:
                        continue
                    elif not c[j] in t:
                        t[c[j]] = next
                        nex+=1
                        c[j]=t[c[j]]
        self.codes=Codes
        self.table = t

    def encode(self):
        self.init_table()
        self.firstcheck()
        self.secondcheck()
print("start parse...\n")
pprint(codes)
parser = Parser(codes)
parser.parse()
codes = parser.codes
print("↓")
pprint(codes)
table = SymbolTable(codes)
table.encode()
codes = table.codes
encoder = Encode(codes)
encoder.conversion()
bcodes = encoder.codes
print("↓")
for b in bcodes:
    print(b)
#print("enter the file where this code is saved")
savefilename = filename[0:filename.find('.')]+'.hack'
print("the binary codes was be saved as {}".format(savefilename))
with open(savefilename,mode = 'w') as f:
    for b in bcodes:
        f.write(b)
        f.write("\n")
