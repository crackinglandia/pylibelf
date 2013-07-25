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
    """Returns a ReadData-like stream object."""
    def __init__(self, data, endianness = "<",  signed = False):
        """
        @type data: str
        @param data: The data from which we want to read.
        
        @type endianness: str
        @param endianness: (Optional) Indicates the endianness used to read the data. The C{<} indicates little-endian while C{>} indicates big-endian.
        
        @type signed: bool
        @param signed: (Optional) If set to C{True} the data will be treated as signed. If set to C{False} it will be treated as unsigned.
        """
        self.data = data
        self.offset = 0
        self.endianness = endianness
        self.signed = signed
        self.log = False

    def __len__(self):
        return len(self.data[self.offset:])

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

    def readDword(self):
        """
        Reads a dword value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The dword value read from the L{ReadData} stream.
        """
        dword = unpack(self.endianness + ('L' if not self.signed else 'l'), self.readAt(self.offset,  4))[0]
        self.offset += 4
        return dword

    def readWord(self):
        """
        Reads a word value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The word value read from the L{ReadData} stream.
        """
        word = unpack(self.endianness + ('H' if not self.signed else 'h'), self.readAt(self.offset, 2))[0]
        self.offset += 2
        return word
        
    def readByte(self):
        """
        Reads a byte value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The byte value read from the L{ReadData} stream.
        """
        byte = unpack('B' if not self.signed else 'b', self.readAt(self.offset,  1))[0]
        self.offset += 1
        return byte
    
    def readQword(self):
        """
        Reads a qword value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The qword value read from the L{ReadData} stream.
        """
        qword = unpack(self.endianness + ('Q' if not self.signed else 'b'),  self.readAt(self.offset, 8))[0]
        self.offset += 8
        return qword
        
    def readString(self):
        """
        Reads an ASCII string from the L{ReadData} stream object.
        
        @rtype: str
        @return: An ASCII string read form the stream.
        """
        resultStr = ""
        while self.data[self.offset] != "\x00":
            resultStr += self.data[self.offset]
            self.offset += 1
        return resultStr

    def readAlignedString(self, align = 4):
        """ 
        Reads an ASCII string aligned to the next align-bytes boundary.
        
        @type align: int
        @param align: (Optional) The value we want the ASCII string to be aligned.
        
        @rtype: str
        @return: A 4-bytes aligned (default) ASCII string.
        """
        s = self.readString()
        r = align - len(s) % align
        while r:
            s += self.data[self.offset]
            self.offset += 1
            r -= 1
        return s
        
    def read(self, nroBytes):
        """
        Reads data from the L{ReadData} stream object.
        
        @type nroBytes: int
        @param nroBytes: The number of bytes to read.
        
        @rtype: str
        @return: A string containing the read data from the L{ReadData} stream object.
        
        @raise DataLengthException: The number of bytes tried to be read are more than the remaining in the L{ReadData} stream.
        """
        if nroBytes > len(self.data[self.offset:]):
            if self.log:
                print "Warning: Trying to read: %d bytes - only %d bytes left" % (nroBytes,  len(self.data[self.offset:]))
            nroBytes = len(self.data[self.offset:])

        resultStr = self.data[self.offset:self.offset + nroBytes]
        self.offset += nroBytes
        return resultStr
        
    def skipBytes(self, nroBytes):
        """
        Skips the specified number as parameter to the current value of the L{ReadData} stream.
        
        @type nroBytes: int
        @param nroBytes: The number of bytes to skip.        
        """
        self.offset += nroBytes
        
    def setOffset(self, value):
        """
        Sets the offset of the L{ReadData} stream object in wich the data is read.
        
        @type value: int
        @param value: Integer value that represent the offset we want to start reading in the L{ReadData} stream.
            
        @raise WrongOffsetValueException: The value is beyond the total length of the data. 
        """
        #if value >= len(self.data):
        #    raise excep.WrongOffsetValueException("Wrong offset value. Must be less than %d" % len(self.data))
        self.offset = value
    
    def readAt(self, offset, size):
        """
        Reads as many bytes indicated in the size parameter at the specific offset.

        @type offset: int
        @param offset: Offset of the value to be read.

        @type size: int
        @param size: This parameter indicates how many bytes are going to be read from a given offset.

        @rtype: str
        @return: A packed string containing the read data.
        """
        if offset > len(self.data):
            if self.log:
                print "Warning: Trying to read: %d bytes - only %d bytes left" % (nroBytes,  len(self.data[self.offset:]))
            offset = len(self.data[self.offset:])
        tmpOff = self.tell()
        self.setOffset(offset)
        r = self.read(size)
        self.setOffset(tmpOff)
        return r
        
    def tell(self):
        """
        Returns the current position of the offset in the L{ReadData} sream object.
        
        @rtype: int
        @return: The value of the current offset in the stream.
        """        
        return self.offset
