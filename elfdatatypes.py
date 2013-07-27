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
__license__ = "BSD 3-Clause"

import elfconstants
import elfutils

from struct import pack, unpack

TYPE_BYTE = 0
TYPE_WORD = 2
TYPE_DWORD = 1
TYPE_QWORD = 3
TYPE_ARRAY = 4

class Array(list):
    def __init__(self, arrayType,  shouldPack = True):
        list.__init__(self)

        self.arrayType = arrayType
        self.shouldPack = shouldPack
        
        if not self.arrayType in [TYPE_BYTE,  TYPE_WORD,  TYPE_DWORD,  TYPE_QWORD]:
            raise TypeError("Couldn\'t create an Array of type %r" % self.arrayType)
            
    def __str__(self):
        return ''.join([str(x) for x in self])

    def sizeof(self):
        return len(self)
        
    @staticmethod
    def parse(readDataInstance,  arrayType,  arrayLength):
        newArray = Array(arrayType)
        
        dataLength = len(readDataInstance)
        
        if arrayType is TYPE_DWORD:
            toRead = arrayLength * 4
            if dataLength >= toRead: 
                for i in range(arrayLength):
                    newArray.append(DWORD(readDataInstance.readDword()))
            else:
                raise excep.DataLengthException("Not enough bytes to read.")
                
        elif arrayType is TYPE_WORD:
            toRead = arrayLength * 2
            if dataLength >= toRead:
                for i in range(arrayLength):
                    newArray.append(DWORD(readDataInstance.readWord()))
            else:
                raise excep.DataLengthException("Not enough bytes to read.")
                
        elif arrayType is TYPE_QWORD:
            toRead = arrayLength * 8
            if dataLength >= toRead:
                for i in range(arrayLength):
                    newArray.append(QWORD(readDataInstance.readQword()))
            else:
                raise excep.DataLengthException("Not enough bytes to read.")
                
        elif arrayType is TYPE_BYTE:
            for i in range(arrayLength):
                newArray.append(BYTE(readDataInstance.readByte()))
        
        else:
            raise elfexceptions.ArrayTypeException("Could\'t create an array of type %d" % arrayType)
            
        return newArray
    
    def getType(self):
        return TYPE_ARRAY

class DataTypeBaseClass(object):
    def __init__(self, value = 0, endianness = "<", signed = False, shouldPack = True):
        self.value = value
        self.endianness = endianness
        self.signed = signed
        self.shouldPack = shouldPack

    def __eq__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value == other.value
        else:
            result = self.value == other
        return result
    
    def __ne__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value != other.value
        else:
            result = self.value != other
        return result
    
    def __lt__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value < other.value
        else:
            result = self.value < other
        return result        
    
    def __gt__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value > other.value
        else:
            result = self.value > other
        return result
    
    def __le__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value <= other.value
        else:
            result = self.value <= other
        return result
    
    def __ge__(self, other):
        result = None
        
        if isinstance(other, self.__class__):
            result = self.value >= other.value
        else:
            result = self.value >= other
        return result
        
    def __add__(self, other):
        result = None

        if isinstance(other,  self.__class__):
            try:
                result = self.value + other.value
            except TypeError, e:
                raise e
        else:
            try:
                result = self.value + other
            except TypeError, e:
                raise e
        return result
    
    def __sub__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            try:
                result = self.value - other.value
            except TypeError, e:
                raise e
        else:
            try:
                result = self.value - other
            except TypeError, e:
                raise e
        return result
    
    def __mul__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value * other.value
        else:
            try:
                result = self.value * other
            except TypeError, e:
                raise e
        return result
        
    def __div__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            try:
                result = self.value / other.value
            except (TypeError, ZeroDivisionError) as e:
                raise e
        else:
            try:
                result = self.value / other
            except (TypeError, ZeroDivisionError) as e:
                raise e
        return result

    def __xor__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value ^ other.value
        else:
            try:
                result = self.value ^ other
            except TypeError, e:
                raise e
        return result
        
    def __rshift__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value >> other.value
        else:
            try:
                result = self.value >> other
            except TypeError, e:
                raise e
        return result
        
    def __lshift__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value << other.value
        else:
            try:
                result = self.value << other
            except TypeError, e:
                raise e
        return result
        
    def __and__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value & other.value
        else:
            try:
                result = self.value & other
            except TypeError, e:
                raise e
        return result

    def __or__(self, other):
        result = None
        if isinstance(other,  self.__class__):
            result = self.value | other.value
        else:
            try:
                result = self.value | other
            except TypeError, e:
                raise e
        return result
        
class BYTE(DataTypeBaseClass):
    def __init__(self,  value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DataTypeBaseClass.__init__(self, value, endianness, signed, shouldPack)
        
    def __str__(self):
        return pack(self.endianness  + ("b" if self.signed else "B"),  self.value)
        
    def __len__(self):
        return len(str(self))

    def getType(self):
        return TYPE_BYTE
    
    def sizeof(self):
        return len(self)
    
    @staticmethod
    def parse(readDataInstance):
        return BYTE(readDataInstance.readByte())
        
class WORD(DataTypeBaseClass):
    def __init__(self,  value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DataTypeBaseClass.__init__(self, value, endianness, signed, shouldPack)
        
    def __str__(self):
        return pack(self.endianness + ("h" if self.signed else "H"),  self.value)
    
    def __len__(self):
        return len(str(self))

    def getType(self):
        return TYPE_WORD
    
    def sizeof(self):
        return len(self)
        
    @staticmethod
    def parse(readDataInstance):
        return WORD(readDataInstance.readWord())
        
class DWORD(DataTypeBaseClass):
    def __init__(self,  value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DataTypeBaseClass.__init__(self, value, endianness, signed, shouldPack)
        
    def __str__(self):
        return pack(self.endianness  + ("l" if self.signed else "L"),  self.value)
    
    def __len__(self):
        return len(str(self))

    def getType(self):
        return TYPE_DWORD
    
    def sizeof(self):
        return len(self)
        
    @staticmethod
    def parse(readDataInstance):
        return DWORD(readDataInstance.readDword())
        
class QWORD(DataTypeBaseClass):
    def __init__(self,  value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DataTypeBaseClass.__init__(self, value, endianness, signed, shouldPack)
        
    def __str__(self):
        return pack(self.endianness + ("q" if self.signed else "Q"),  self.value)
        
    def __len__(self):
        return len(str(self))
    
    def getType(self):
        return TYPE_QWORD
    
    def sizeof(self):
        return len(self)
        
    @staticmethod
    def parse(readDataInstance):
        return QWORD(readDataInstance.readQword())
        
class Elf32_Addr(DWORD):
    def __init__(self, value = 0, endianness = "<",  signed = False,  shouldPack = True):
        DWORD.__init__(self, value, endianness, signed, shouldPack)
        
    def getType(self):
        return elfconstants.ELF32ADDR
        
    @staticmethod
    def parse(readDataInstance):
        return Elf32_Addr(readDataInstance.readDword())
        
class Elf32_Off(DWORD):
    def __init__(self, value = 0, endianness = "<",  signed = False,  shouldPack = True):
        DWORD.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF32OFF
    
    @staticmethod
    def parse(readDataInstance):
        return Elf32_Off(readDataInstance.readDword())
        
class Elf32_Word(DWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DataTypeBaseClass.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF32WORD
        
    @staticmethod
    def parse(readDataInstance):
        return Elf32_Word(readDataInstance.readDword())
        
class Elf32_Half(WORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        WORD.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF32HALF
    
    @staticmethod
    def parse(readDataInstance):
        return Elf32_Half(readDataInstance.readWord())
        
class Elf32_Sword(DWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = True,  shouldPack = True):
        DWORD.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF32SWORD
    
    @staticmethod
    def parse(readDataInstance):
        return Elf32_Sword(readDataInstance.readDword())
        
class Elf64_Addr(QWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        QWORD.__init__(self, value, endianness, signed, shouldPack)

    def getType(self):
        return elfconstants.ELF64ADDR
    
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Addr(readDataInstance.readQword())
        
class Elf64_Half(WORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        WORD.__init__(self, value, endianness, signed, shouldPack)

    def getType(self):
        return elfconstants.ELF64HALF
    
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Half(readDataInstance.readWord())

class Elf64_Word(DWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        DWORD.__init__(self, value, endianness, signed, shouldPack)

    def getType(self):
        return elfconstants.ELF64WORD
    
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Word(readDataInstance.readDword())

class Elf64_Off(QWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        QWORD.__init__(self, value, endianness, signed, shouldPack)

    def getType(self):
        return elfconstants.ELF64OFF
    
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Off(readDataInstance.readQword())
        
class Elf64_Sword(DWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = True,  shouldPack = True):
        DWORD.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF64SWORD
    
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Sword(readDataInstance.readDword(), signed = True)
        
class Elf64_Sxword(QWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = True,  shouldPack = True):
        QWORD.__init__(self, value, endianness, signed, shouldPack)

    def getType(self):
        return elfconstants.ELF64SXWORD
        
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Sxword(readDataInstance.readQword(), signed = True)
        
class Elf64_Xword(QWORD):
    def __init__(self, value = 0,  endianness = "<",  signed = False,  shouldPack = True):
        QWORD.__init__(self, value, endianness, signed, shouldPack)
    
    def getType(self):
        return elfconstants.ELF64XWORD
        
    @staticmethod
    def parse(readDataInstance):
        return Elf64_Xword(readDataInstance.readQword())
        
