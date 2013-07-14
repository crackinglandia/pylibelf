#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Copyright (c) 2013, Nahuel Riva 
# All rights reserved. 
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met: 
# 
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer. 
#     * Redistributions in binary form must reproduce the above copyright 
#       notice,this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution. 
#     * Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE. 

__revision__ = "$Id$"
__author__ = "Nahuel Riva"
__contact__ = "crackinglandia@gmail.com"
__license__ = ""

"""
TODO:
[] Implementar los writeElf*() en la clase WriteData.
"""

import elfdatatypes

from StringIO import StringIO
from cStringIO import StringIO as cstringio
from struct import pack, unpack

def ELF32_ST_BIND(i):
    return i >> 4
    
def ELF32_ST_TYPE(i):
    return i & 0xf
    
def ELF32_ST_INFO(b, t):
    return (b << 4) + (t & 0xf)
    
def ELF32_R_SYM(i):
    return i >> 8
    
def ELF32_R_TYPE(i):
    return BYTE(i)

def ELF32_R_INFO(s, t):
    return (s << 8) + elfdatatypes.BYTE(t)

def readFile(filename):
    fd = open(filename, "rb")
    data = fd.read()
    fd.close()
    return data
    
class WriteData(object):
    def __init__(self,  data):
        self.data = StringIO(data)
        self.endianness = "<"
        self.signed = False
    
    def __len__(self):
        return len(self.data.buf[self.data.tell():])
    
    def writeByte(self,  byte):
        self.data.write(pack("B" if not self.signed else "b", byte))
        
    def writeWord(self,  word):
        self.data.write(pack(self.endianness + ("H" if not self.signed else "h"), word)) 
        
    def writeDword(self,  dword):
        self.data.write(pack(self.endianness + ("L" if not self.signed else "l"), dword))
        
    def writeQword(self,  qword):
        self.data.write(pack(self.endianness + ("Q" if not self.signed else "q"),  qword))
        
    def write(self, dataToWrite):
        self.data.write(dataToWrite)
    
    def setOffset(self, value):
        if value >= self.data.len:
            raise elfexceptions.WrongOffsetValueException("Wrong offset value. Must be less than %d" % self.data.len)
        self.data.seek(offset)
        
    def skipBytes(self,  nroBytes):
        newPos = self.data.tell()+ nroBytes
        self.data.seek(newPos)
        
    def tell(self):
        return self.data.tell()

    def __del__(self):
        self.data.close()
        del self.data
        
class ReadData(object):
    def __init__(self, data):
        self.data = cstringio(data)
        self.endianness = '<'
        self.signed = False
    
    def __len__(self):
        return len(self.data.getvalue()[self.data.tell():])
        
    def readDword(self):
        dword = unpack(self.endianness + ('L' if not self.signed else 'l'), self.data.read(4))[0]
        return dword

    def readWord(self):
        word = unpack(self.endianness + ('H' if not self.signed else 'h'), self.data.read(2))[0]
        return word
        
    def readByte(self):
        byte = unpack('B' if not self.signed else 'b', self.data.read(1))[0]
        return byte
    
    def readQword(self):
        qword = unpack(self.endianness + ('Q' if not self.signed else 'b'),  self.data.read(8))[0]
        return qword
    
    def readElfHalf(self):
        return self.readWord()
    
    def readElfOff(self):
        return self.readDword()
    
    def readElfWord(self):
        return self.readDword()
    
    def readElfAddr(self):
        return self.readDword()
        
    def readElfSword(self):
        # store original value before changing the sign
        oldSign = self.signed
        # change the sign
        self.signed = True
        # read the value and unpack it as a signed long
        value = self.readDword()
        # restore the original sign
        self.signed = oldSign
        return value
    
    def readElf64Addr(self):
        return self.readQword()
        
    def readElf64Off(self):
        return self.readQword()
        
    def readElf64Half(self):
        return self.readWord()
        
    def readElf64Word(self):
        return self.readDword()
        
    def readElf64Sword(self):
        return self.readElfSword()
        
    def readElf64Xword(self):
        return self.readQword()
        
    def readElf64Sxword(self):
        # store original value before changing the sign
        oldSign = self.signed
        # change the sign
        self.signed = True
        # read the value and unpack it as a signed long
        value = self.readQword()
        # restore the original sign
        self.signed = oldSign
        return value
        
    def readString(self):
        """ Reads ASCII string"""
        resultStr = ""
        while self.data.buf[self.data.tell()] != "\x00":
            resultStr += self.data.read(1)
        return resultStr

    def readAlignedString(self,  align = 4):
        """ Reads ASCII string aligned to the next align-bytes boundary """
        s = self.readString()
        r = align - len(s) % align
        while r:
            s += self.data.read(1)
            r -= 1
        return s
        
    def read(self, nroBytes):
        if nroBytes > len(self):
            raise elfexceptions.DataLengthException("Wrong number of bytes. Read %d or less bytes" % len(self.data[self.offset:]))
        else:
            resultStr = self.data.read(nroBytes)
        return resultStr
        
    def skipBytes(self,  nroBytes):
        newPos = self.data.tell() + nroBytes
        self.data.seek(newPos)
        
    def setOffset(self,  value):
        if value >= self.data.__sizeof__():
            raise elfexceptions.WrongOffsetValueException("Wrong offset value. Must be less than %d" % self.data.__sizeof__())
        self.data.seek(value)
    
    def tell(self):
        return self.data.tell()

    def __del__(self):
        self.data.close()
        del self.data
        
