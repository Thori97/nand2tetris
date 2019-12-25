import sys
import os
args = sys.argv
if len(args)<2:
    print("Enter the source!!")
    sys.exit()
elif len(args)>2:
    print("Too many arguments")
    sys.exit()
path = args[1]
Filetype = "FILE"
if not os.path.exists(path):
    print("Not exiist suuch a file or directory")
if os.path.isfile(path):
    Filetype = "FILE"
elif os.path.isdir(path):
    Filetype = "DIR"
else:
    sys.exit()
#path = files
files = []
path2 = ""
filename =  ""
FIRST = 0
if Filetype == "FILE":
    path2 = path[0:path.rfind('/')]#dir to write .asmfile
    filename = path[path.rfind('/'):]
    fi = filename[1:filename.rfind('.')]
    filename = filename[0:filename.rfind('.')]+".asm"
elif Filetype == "DIR":
    path2 = path
    for x in os.listdir(path2):
        if x[x.rfind('.'):] == ".vm":
            path3 = path2[0:path2.rfind('/')]
            path3 = path3[path3.rfind('/'):]
            filename = path3+".asm"
print("filename =",filename)
class Parser:
    def __init__(self, path):
        s = []
        with open(path) as f:
            s = f.readlines()
        self.codes = s
        self.command = ""
    def remove_comments(self):
        newCodes = self.codes
        for i in range(len(newCodes)):
            c = newCodes[i]
            c = c.strip()
            if '//' in c:
                s = c.find('//')
                c = c[0:s]
            newCodes[i] = c
        newnew = []
        for i in range(len(newCodes)):
            c = newCodes[i]
            if c != "\n" and c != "":
                newnew.append(c)
        self.codes = newnew
    def hasMoreCommands(self):
        if len(self.codes) > 0:
            return True
        else:
            return False
    def advance(self):
        self.command = self.codes[0]
        self.codes = self.codes[1:]
    def commandType(self):
        c = self.command
        if c == "":
            print("please advance")
            return "None"
        c = c.split()
        if ("add" in c[0]) or ("sub" in c[0]) or ("neg" in c[0]) or ("eq" in c[0]) or ("gt" in c[0]) or ("lt" in c[0]) or ("and" in c[0]) or ("or" in c[0]) or ("not" in c[0]):
            return "C_ARITHMETIC"
        elif "push" in c[0]:
            return "C_PUSH"
        elif "pop" in c[0]:
            return "C_POP"
        elif "label" in c[0]:
            return "C_LABEL"
        elif "goto" in c[0] and "if" not in c[0]:
            return "C_GOTO"
        elif "if-goto" in c[0]:
            return "C_IF"
        elif "function" in c[0]:
            return "C_FUNCTION"
        elif "return" in c[0]:
            return "C_RETURN"
        elif "call" in c[0]:
            return "C_CALL"
    def arg1(self):
        c = self.command
        l = c.split()
        if self.commandType() == "C_ARITHMETIC":
            return l[0]
        elif self.commandType() != "C_RETURN":
            return l[1]
        else:
            print("Don't use this function arg1")
    def arg2(self):
        c = self.command
        l = c.split()
        if self.commandType() == "C_PUSH" or self.commandType() == "C_POP" or self.commandType() == "C_FUNCTION" or self.commandType() == "C_CALL":
            l = c.split()
            return l[2]
        else:
            print("Don't use this function arg2")
class CodeWriter:
    def __init__(self):
        if FIRST == 0:
            f = open("{}{}".format(path2, filename), 'w')
        else:
            f = open("{}{}".format(path2, filename), 'a')
        self.file = f
        self.jtimes=0
        self.ftimes=0
        if FIRST == 0:
            f.write("@256\nD=A\n@SP\nM=D\n")
            print("@256\nD=A\n@SP\nM=D\n")
    def setFileName(self):
        return 0
    def writeArithmetic(self, command):
        #write = "@SP\nM=M-1\nD=M\nA=D\nD=M\n@SP\nAM=M-1\n"#D=yにしてSP=SP-1にした
        write = "@SP\nM=M-1\nA=M\nD=M\n"
        if command!= "neg" and command != "not":
            write=write+"@SP\nAM=M-1\n"#D=yにしてSP=SP-2にした
        if command == "add":
            write=write+"M=M+D\n@SP\nM=M+1\n"
        elif command == "sub":
            write=write+"M=M-D\n@SP\nM=M+1\n"
        elif command == "neg":
            write=write+"M=-D\n@SP\nM=M+1\n"
        elif command == "eq":
            write=write+"D=M-D\n@JUMP{}\nD;JEQ\n@SP\nA=M\nM=0\n@JUMPEND{}\n0;JMP\n(JUMP{})\n@SP\nA=M\nM=-1\n(JUMPEND{})\n@SP\nM=M+1\n"\
                .format(self.jtimes,self.jtimes,self.jtimes,self.jtimes)
            self.jtimes+=1
        elif command == "gt":
            write=write+"D=M-D\n@JUMP{}\nD;JGT\n@SP\nA=M\nM=0\n@JUMPEND{}\n0;JMP\n(JUMP{})\n@SP\nA=M\nM=-1\n(JUMPEND{})\n@SP\nM=M+1\n"\
                .format(self.jtimes,self.jtimes,self.jtimes,self.jtimes)
            self.jtimes+=1
        elif command == "lt":
            write=write+"D=M-D\n@JUMP{}\nD;JLT\n@SP\nA=M\nM=0\n@JUMPEND{}\n0;JMP\n(JUMP{})\n@SP\nA=M\nM=-1\n(JUMPEND{})\n@SP\nM=M+1\n"\
                .format(self.jtimes,self.jtimes,self.jtimes,self.jtimes)
            self.jtimes+=1
        elif command == "and":
            write=write+"M=M&D\n@SP\nM=M+1\n"
        elif command == "or":
            write=write+"M=M|D\n@SP\nM=M+1\n"
        elif command == "not":
            write=write+"M=!M\n@SP\nM=M+1\n"
        #write=write+"A=M\nM=0\n"
        self.file.write(write)
        print(command, "\n",write)
    def writePushPop(self, command, segment, index):
        write = ""
        if segment == "local":
            segment = "LCL"
        elif segment == "argument":
            segment = "ARG"
        elif segment == "this":
            segment = "THIS"
        elif segment == "that":
            segment = "THAT"
        elif segment == "temp":
            segment = "5"
        elif segment == "pointer":
            segment = "3"
        if not(command == "C_PUSH" or command == "C_POP"):
            print("invalid command")
            sys.exit()
        if command == "C_PUSH":
            if segment == "static":
                write = "@{}.{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(fi,index)
            elif segment == "constant":
                write = "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(index)
            elif segment == "3":
                write = "@{}\nD=A\n@{}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(index, segment)
            elif segment == "5":
                write = "@{}\nD=A\n@{}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(index, segment)
            else:
                write = "@{}\nD=A\n@{}\nAM=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@{}\nD=A\n@{}\nM=M-D\n".format(index,segment,index,segment)
        elif command == "C_POP":
            if segment == "static":
                write = "@SP\nAM=M-1\nD=M\n@{}.{}\nM=D\n".format(fi,index)
            elif segment != "5" and segment != "3":
                write = "@{}\nD=A\n@{}\nM=M+D\n@SP\nAM=M-1\nD=M\n@{}\nA=M\nM=D\n@{}\nD=A\n@{}\nM=M-D\n".format(index,segment,segment,index,segment)
            elif segment == "3":
                #write = "@{}\nD=A\n@{}\nA=A+D\n@SP\nAM=M-1\nD=M\n@{}\nA=M\nM=D\n@{}\nD=A\n@{}\nM=M-D\n".format(index,segment,segment,index,segment)
                write = "@SP\nAM=M-1\nD=M\n@{}\nM=D\n".format(int(segment)+int(index))
            elif segment == "5":
                write = "@SP\nAM=M-1\nD=M\n@{}\nM=D\n".format(int(segment)+int(index))
        self.file.write(write)
        print(command, segment, index, "\n",write)
        return 0
    def writeLabel(self, label):
        write = "({})\n".format(label)
        self.file.write(write)
        print(write)
        return 0
    def writeGoto(self,label):
        write = "@{}\n0;JMP\n".format(label)
        self.file.write(write)
        print(write)
        return 0
    def writeIf(self,label):
        write = "@SP\nAM=M-1\nD=M\n@{}\nD;JNE\n".format(label)
        self.file.write(write)
        print(write)
        return 0
    def writeCall(self,functionName,numArgs):
        ft = functionName+"."+str(self.ftimes)
        self.writePushPop("C_PUSH","constant",ft)
        write = ""
        write = write +"@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        write = write +"@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        write = write +"@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        write = write +"@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        write = write +"@{}\nD=A\n@LCL\nM=-D\n@SP\nD=M\n@LCL\nM=D+M\n".format(int(numArgs)+5)
        write = write +"@SP\nD=M\n@LCL\nM=D\n"
        self.file.write(write)
        self.writeGoto(functionName)
        print(functionName,numArgs,"\n", write)
        return 0
    def writeReturn(self):
        self.writePushPop("C_POP", "ARG", "0")
        write = ""
        write += "@{}\nD=A\n@LCL\nA=M-D\nD=M\n@R15\nM=D\n".format("5")
        write += "@ARG\nD=M+1\n@SP\nM=D\n"
        write += "@{}\nD=A\n@LCL\nA=M-D\nD=M\n@THAT\nM=D\n".format("1")
        write += "@{}\nD=A\n@LCL\nA=M-D\nD=M\n@THIS\nM=D\n".format("2")
        write += "@{}\nD=A\n@LCL\nA=M-D\nD=M\n@ARG\nM=D\n".format("3")
        write += "@{}\nD=A\n@LCL\nA=M-D\nD=M\n@LCL\nM=D\n".format("4")
        write += "@15\nA=M\n0;JMP\n"
        self.file.write(write)
        print("return\n",write)
        return 0
    def writeFunction(self,functionName,numLocals):
        write = "({})\n".format(functionName)
        fd = functionName+".declearEnd"+str(self.ftimes)
        fd2 = functionName+".declearBegin"+str(self.ftimes)
        self.ftimes+=1
        p = "@SP\nA=M\nM=0\n@SP\nM=M+1"#push 0
        write = write+"@{}\nD=A\n({})\n@{}\nD;JEQ\nD=D-1\n{}\n@{}\n0;JMP\n({})\n".format(numLocals,fd2,fd,p,fd2,fd)
        self.file.write(write)
        print(write)
        return 0
    def close(self):
        self.file.close()
        return 0
if Filetype == "FILE":
    files.append(path)
elif Filetype == "DIR":
    files.append("{}Sys.vm".format(path2))
    for x in os.listdir(path2):
        if x[x.rfind('.'):] == ".vm" and x != "Sys.vm":
            files.append("{}{}".format(path2, x))
print(files)
for path in files:
    parser = Parser(path)
    parser.remove_comments()
    print(parser.codes)
    print(path2, filename)
    cw = CodeWriter()
    while parser.hasMoreCommands():
        parser.advance()
        t = parser.commandType()
        print(parser.command, t)
        if t == "C_ARITHMETIC":
            cw.writeArithmetic(parser.arg1())
        elif t == "C_PUSH" or t == "C_POP":
            #print("command = {}, arg1 = {}, arg2 = {}".format(parser.commandType(),parser.arg1(),parser.arg2()))
            cw.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())
        elif t == "C_LABEL":
            cw.writeLabel(parser.arg1())
        elif t == "C_GOTO":
            cw.writeGoto(parser.arg1())
        elif t == "C_IF":
            cw.writeIf(parser.arg1())
        elif t == "C_FUNCTION":
            cw.writeFunction(parser.arg1(), parser.arg2())
        elif t == "C_CALL":
            cw.writeCall(parser.arg1(),parser.arg2())
        elif t == "C_RETURN":
            cw.writeReturn()
    cw.close()
    FIRST=FIRST+1
"""
@index
D=A
@segment
M=M+D
@SP
AM=M-1//SP-1
D=M//D=top of stack
@segment
A=M
M=D
@index
D=A
@segment
M=M-D
"""