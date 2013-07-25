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

import os

import elfconstants
import elfdatatypes
import elfutils
import elfexceptions

ELF32 = 0
ELF32_EHDR = 1
ELF32_SHDR = 2
ELF32_SYM = 3
ELF32_REL = 4
ELF32_RELA = 5
ELF32_PHDR = 6

ELF64 = 7
ELF64_EHDR = 8
ELF64_PHDR = 9
ELF64_SHDR = 10

class BaseStructClass(object):
    def __init__(self,  shouldPack = True):
        self.shouldPack = shouldPack
        self._fields = []
        
    def __str__(self):
        s = ""
        for i in self._fields:
            attr = getattr(self,  i)
            if attr.shouldPack:
                s += str(attr)
        return s
        
    def __len__(self):
        return len(str(self))

    def sizeof(self):
        return len(self)
        
    def getFields(self):
        d = {}
        for i in self._fields:
            key = i
            value = getattr(self,  i)
            d[key] = value
        return d
        
    def getType(self):
        raise NotImplementedError("getType() method not implemented.")
    
class ELF(object):
    def __init__(self,  pathToFile = None, data = None, fastLoad = False, verbose = False):
        self.elfHdr = None
        self.__data = None

        if data:
            print "--> Building ELF from data."
            self.__data = elfutils.ReadData(data)
            self.__parse__(self.__data)
            
        elif pathToFile:
            print "--> Building ELF from file."
            
            if os.path.exists(pathToFile):
                self.__data = elfutils.readFile(pathToFile)
                if self.validate(self.__data[:16]):                
                    self.__data = elfutils.ReadData(self.__data)
                    self.__parse__(self.__data)
                else:
                    raise elfexceptions.UnknownFormatException("It seems that the file is not a valid ELF.")
            else:
                raise elfexceptions.PathNotValidException("The specified path does not exists.")
        else:
            raise elfexceptions.PathOrDataNotSpecifiedException("Path nor data were specified!.")

    def readDataAtOffset(self, offset, size):
        return self.__data.readAt(offset, size)

    def validate(self, data):
        rd = elfdatatypes.Array.parse(elfutils.ReadData(data), elfdatatypes.TYPE_BYTE, 16)
        
        if rd[0] == elfconstants.ELF_MAGICS["ELFMAG0"] and rd[1] == elfconstants.ELF_MAGICS["ELFMAG1"]\
        and rd[2] == elfconstants.ELF_MAGICS["ELFMAG2"] and rd[3] == elfconstants.ELF_MAGICS["ELFMAG3"]:
            return True
        return False
            
    def getType(self):
        return self.elfHdr.e_ident[elfconstants.ELF_IDENT_TYPES["EI_CLASS"]]
    
    def __parse__(self, readDataInstance):
        data = elfdatatypes.Array.parse(elfutils.ReadData(readDataInstance.read(16)), elfdatatypes.TYPE_BYTE, 16)
        
        elfClass = data[elfconstants.ELF_IDENT_TYPES["EI_CLASS"]]
        dataEncoding = data[elfconstants.ELF_IDENT_TYPES["EI_DATA"]]
        
        readDataInstance.setOffset(0)
        if elfClass == elfconstants.ELF_FILE_CLASS["ELFCLASS32"]:
            print "--> File is ELF32."
            self.elfHdr = Elf32_Ehdr.parse(readDataInstance)
        elif elfClass == elfconstants.ELF_FILE_CLASS["ELFCLASS64"]:
            print "--> File is ELF64."
            self.elfHdr = Elf64_Ehdr.parse(readDataInstance)

            if self.elfHdr.e_phnum.value > 0:
                if self.elfHdr.e_phoff.value:

                    off = self.elfHdr.e_phoff.value
                    size = self.elfHdr.e_phentsize.value
                    noEntries = self.elfHdr.e_phnum.value

                    self.PhdrTable = Elf_PhdrTable.parse(readDataInstance, noEntries, off, size, ELFPHDR32 = False)

            if self.elfHdr.e_shnum.value > 0:
                if self.elfHdr.e_shoff.value:
                    off = self.elfHdr.e_shoff.value
                    size = self.elfHdr.e_shentsize.value
                    noSections = self.elfHdr.e_shnum.value

                    self.ShdrTable = Elf_ShdrTable.parse(readDataInstance, noSections, off, size, ELFSHDR32 = False)

        else:
            raise elfexceptions.UnknownFormatException("Unknown format error.")
        
        if dataEncoding == elfconstants.ELF_DATA_ENCODING_TYPES["ELFDATA2LSB"]:
            print "--> Data: LSB."
        elif dataEncoding == elfconstants.ELF_DATA_ENCODING_TYPES["ELFDATAMSB"]:
            print "--> Data: MSB."
        else:
            raise UnknownDataEncodingException("Unknown data encoding for ELF.")

class Elf32_Ehdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.e_ident = elfdatatypes.Array(elfdatatypes.TYPE_BYTE)
        self.e_type = elfdatatypes.Elf32_Half()
        self.e_machine = elfdatatypes.Elf32_Half()
        self.e_version = elfdatatypes.Elf32_Word()
        self.e_entry = elfdatatypes.Elf32_Addr()
        self.e_phoff = elfdatatypes.Elf32_Off()
        self.e_shoff = elfdatatypes.Elf32_Off()
        self.e_flags = elfdatatypes.Elf32_Word()
        self.e_ehsize = elfdatatypes.Elf32_Half()
        self.e_phentsize = elfdatatypes.Elf32_Half()
        self.e_phnum = elfdatatypes.Elf32_Half()
        self.e_shentsize = elfdatatypes.Elf32_Half()
        self.e_shnum = elfdatatypes.Elf32_Half()
        self.e_shstrndx = elfdatatypes.Elf32_Half()

        self._fields = ["e_ident", "e_type", "e_machine", "e_version", "e_entry", "e_phoff", "e_shoff",\
                        "e_flags", "e_ehsize", "e_phentsize", "e_phnum", "e_shentsize", "e_shnum", "e_shstrndx"]
    def getType(self):
        return ELF32_EHDR
    
    @staticmethod
    def parse(readDataInstance):
        elf32_ehdr = Elf32_Ehdr()
        elf32_ehdr.e_ident = elfdatatypes.Array.parse(elfutils.ReadData(readDataInstance.read(16)), elfdatatypes.TYPE_BYTE, 16)
        elf32_ehdr.e_type = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_machine = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_version = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_ehdr.e_entry = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_ehdr.e_phoff = elfdatatypes.Elf32_Off(readDataInstance.readElfOff())
        elf32_ehdr.e_shoff = elfdatatypes.Elf32_Off(readDataInstance.readElfOff())
        elf32_ehdr.e_flags = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_ehdr.e_ehsize = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_phentsize = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_phnum = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_shentsize = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_shnum = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        elf32_ehdr.e_shstrndx = elfdatatypes.Elf32_Half(readDataInstance.readElfHalf())
        return elf32_ehdr
        
class Elf32_Shdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.sh_name = elfdatatypes.Elf32_Word()
        self.sh_type = elfdatatypes.Elf32_Word()
        self.sh_flags = elfdatatypes.Elf32_Word()
        self.sh_addr = elfdatatypes.Elf32_Addr()
        self.sh_offset = elfdatatypes.Elf32_Off()
        self.sh_size = elfdatatypes.Elf32_Word()
        self.sh_link = elfdatatypes.Elf32_Word()
        self.sh_info = elfdatatypes.Elf32_Word()
        self.sh_addralign = elfdatatypes.Elf32_Word()
        self.sh_entsize = elfdatatypes.Elf32_Word()
    
        self._fields = ["sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset", "sh_size", "sh_link",\
                         "sh_info", "sh_addralign", "sh_entsize"]
        
    def getType(self):
        return ELF32_SHDR
        
    @staticmethod
    def parse(readDataInstance):
        elf32_shdr = Elf32_Shdr()
        elf32_shdr.sh_name = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_type = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_flags = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_addr = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_shdr.sh_offset = elfdatatypes.Elf32_Off(readDataInstance.readElfOff())
        elf32_shdr.sh_size = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_link = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_info = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_addralign = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_shdr.sh_entsize = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        return elf32_shdr
        
class Elf32_Sym(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.st_name = elfdatatypes.Elf32_Word()
        self.st_value = elfdatatypes.Elf32_Addr()
        self.st_size = elfdatatypes.Elf32_Word()
        self.st_info = elfdatatypes.Byte()
        self.st_other = elfdatatypes.Byte()
        self.st_shndx = elfdatatypes.Elf32_Half()

        self._fields = ["st_name", "st_value", "st_size", "st_info", "st_other", "st_shndx"]
        
    def getType(self):
        return ELF32_SYM
    
    @staticmethod
    def parse(readDataInstance):
        elf32_sym = Elf32_Sym()
        elf32_sym.st_name = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_sym.st_value = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_sym.st_size = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_sym.st_info = elfdatatypes.Byte(readDataInstance.readByte())
        elf32_sym.st_other = elfdatatypes.Byte(readDataInstance.readByte())
        elf32_sym.st_shndx = elfdatatypes.Elf32_Half(readDataInstance.readElf32Half())
        return elf32_sym
        
class Elf32_Rel(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.r_offset = elfdatatypes.Elf32_Addr()
        self.r_info = elfdatatypes.Elf32_Word()
    
        self._fields = ["r_offset", "r_info"]
        
    def getType(self):
        return ELF32_REL
        
    @staticmethod
    def parse(readDataInstance):
        elf32_rel = Elf32_Rel()
        elf32_rel.r_offset = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_rel.r_info = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        return elf32_rel
        
class Elf32_Rela(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.r_offset = elfdatatypes.Elf32_Addr()
        self.r_info = elfdatatypes.Elf32_Word()
        self.r_addend = elfdatatypes.Elf32_Sword()
    
        self._fields = ["r_offset", "r_info", "r_addend"]
        
    def getType(self):
        return ELF32_RELA
    
    @staticmethod
    def parse(readDataInstance):
        elf32_rela = Elf32_Rela()
        elf32_rela.r_offset = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_rela.r_info = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_rela.r_addend = elfdatatypes.Elf32_Sword(readDataInstance.readElfSword())
        return elf32_rela
        
class Elf32_Phdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.p_type = elfdatatypes.Elf32_Word()
        self.p_offset = elfdatatypes.Elf32_Off()
        self.p_vaddr = elfdatatypes.Elf32_Addr()
        self.p_paddr = elfdatatypes.Elf32_Addr()
        self.p_filesz = elfdatatypes.Elf32_Word()
        self.p_memsz = elfdatatypes.Elf32_Word()
        self.p_flags = elfdatatypes.Elf32_Word()
        self.p_align = elfdatatypes.Elf32_Word()

        self.segmentRawData = None
        
        self._fields = ["p_type", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz",\
        "p_flags", "p_align"]
        
    def getType(self):
        return ELF32_PHDR
    
    @staticmethod
    def parse(readDataInstance):
        elf32_phdr = Elf32_Phdr()
        elf32_phdr.p_type = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_phdr.p_offset = elfdatatypes.Elf32_Off(readDataInstance.readElfOff())
        elf32_phdr.p_vaddr = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_phdr.p_paddr = elfdatatypes.Elf32_Addr(readDataInstance.readElfAddr())
        elf32_phdr.p_filesz = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_phdr.p_memsz = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_phdr.p_flags = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        elf32_phdr.p_align = elfdatatypes.Elf32_Word(readDataInstance.readElfWord())
        return elf32_phdr
        
class Elf64_Ehdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.e_ident = elfdatatypes.Array(elfdatatypes.TYPE_BYTE)
        self.e_type = elfdatatypes.Elf64_Half()
        self.e_machine = elfdatatypes.Elf64_Half()
        self.e_version = elfdatatypes.Elf64_Word()
        self.e_entry = elfdatatypes.Elf64_Addr()
        self.e_phoff = elfdatatypes.Elf64_Off()
        self.e_shoff = elfdatatypes.Elf64_Off()
        self.e_flags = elfdatatypes.Elf64_Word()
        self.e_ehsize = elfdatatypes.Elf64_Half()
        self.e_phentsize = elfdatatypes.Elf64_Half()
        self.e_phnum = elfdatatypes.Elf64_Half()
        self.e_shentsize = elfdatatypes.Elf64_Half()
        self.e_shnum = elfdatatypes.Elf64_Half()
        self.e_shstrndx = elfdatatypes.Elf64_Half()        

        self._fields = ["e_ident", "e_type", "e_machine", "e_version", "e_entry", "e_phoff", "e_shoff",\
                        "e_flags", "e_ehsize", "e_phentsize", "e_phnum", "e_shentsize", "e_shnum", "e_shstrndx"]
    
    def getType(self):
        return ELF64_EHDR
    
    @staticmethod
    def parse(readDataInstance):
        elf64_ehdr = Elf64_Ehdr()
        elf64_ehdr.e_ident = elfdatatypes.Array.parse(elfutils.ReadData(readDataInstance.read(16)), elfdatatypes.TYPE_BYTE, 16)
        elf64_ehdr.e_type = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_machine = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_version = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_ehdr.e_entry = elfdatatypes.Elf64_Addr(readDataInstance.readElf64Addr())
        elf64_ehdr.e_phoff = elfdatatypes.Elf64_Off(readDataInstance.readElf64Off())
        elf64_ehdr.e_shoff = elfdatatypes.Elf64_Off(readDataInstance.readElf64Off())
        elf64_ehdr.e_flags = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_ehdr.e_ehsize = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_phentsize = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_phnum = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_shentsize = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_shnum = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        elf64_ehdr.e_shstrndx = elfdatatypes.Elf64_Half(readDataInstance.readElf64Half())
        return elf64_ehdr
        
class Elf64_Phdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)

        self.p_type = elfdatatypes.Elf64_Word()
        self.p_flags = elfdatatypes.Elf64_Word()
        self.p_offset = elfdatatypes.Elf64_Off()
        self.p_vaddr = elfdatatypes.Elf64_Addr()
        self.p_paddr = elfdatatypes.Elf64_Addr()
        self.p_filesz = elfdatatypes.Elf64_Xword()
        self.p_memsz = elfdatatypes.Elf64_Xword()
        self.p_align = elfdatatypes.Elf64_Xword()

        self.segmentRawData = None # this attribute holds program header + data

        self._fields = ["p_type", "p_flags", "p_offset", "p_vaddr", "p_paddr", "p_filesz",\
                        "p_memsz", "p_align"]

    def getType(self):
        return ELF64_PHDR

    @staticmethod
    def parse(readDataInstance):
        elf64_Phdr = Elf64_Phdr()
        elf64_Phdr.p_type = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_Phdr.p_flags = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_Phdr.p_offset = elfdatatypes.Elf64_Off(readDataInstance.readElf64Off())
        elf64_Phdr.p_vaddr = elfdatatypes.Elf64_Addr(readDataInstance.readElf64Addr())
        elf64_Phdr.p_paddr = elfdatatypes.Elf64_Addr(readDataInstance.readElf64Addr())
        elf64_Phdr.p_filesz = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        elf64_Phdr.p_memsz = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        elf64_Phdr.p_align = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        return elf64_Phdr

class Elf_PhdrTable(list):

    @staticmethod
    def parse(readDataInstance, noEntries, entryOff, entrySize, ELFPHDR32 = True):
        PhdrTable = Elf_PhdrTable()
        for i in range(noEntries):
            rd = elfutils.ReadData(readDataInstance.readAt(entryOff, entrySize))
            
            if ELFPHDR32:
                entry = Elf32_Phdr.parse(rd)
            else:
                entry = Elf64_Phdr.parse(rd)

            off = entry.p_offset.value
            size = entry.p_filesz.value
            
            if off and size:
                entry.segmentRawData = readDataInstance.readAt(off, size)

            PhdrTable.append(entry)

            entryOff += entrySize

        return PhdrTable

class Elf_ShdrTable(list):
    
    @staticmethod
    def parse(readDataInstance, noSections, sectionOff, sectionSize, ELFSHDR32 = True):
        #print "sectionSize: %x" % sectionSize
        ShdrTable = Elf_ShdrTable()
        for i in range(noSections):
            rd = elfutils.ReadData(readDataInstance.readAt(sectionOff, sectionSize))

            if ELFSHDR32:
                entry = Elf32_Shdr.parse(rd)
            else:
                entry = Elf64_Shdr.parse(rd)

            off = entry.sh_offset.value
            size = entry.sh_size.value

            #print "[%d] sectionOff: %x - off: %x - size: %x" % (i, sectionOff, off, size)
            if off and size: 
                entry.sectionRawData = readDataInstance.readAt(off, size)
                
            ShdrTable.append(entry)

            sectionOff += sectionSize
        
        return ShdrTable

class Elf64_Shdr(BaseStructClass):
    def __init__(self, shouldPack = True):
        BaseStructClass.__init__(self, shouldPack)
        
        self.sh_name = elfdatatypes.Elf64_Word()
        self.sh_type = elfdatatypes.Elf64_Word()
        self.sh_flags = elfdatatypes.Elf64_Xword()
        self.sh_addr = elfdatatypes.Elf64_Addr()
        self.sh_offset = elfdatatypes.Elf64_Off()
        self.sh_size = elfdatatypes.Elf64_Xword()
        self.sh_link = elfdatatypes.Elf64_Word()
        self.sh_info = elfdatatypes.Elf64_Word()
        self.sh_addralign = elfdatatypes.Elf64_Xword()
        self.sh_entsize = elfdatatypes.Elf64_Xword()
    
        self.sectionRawData = None

        self._fields = ["sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset", "sh_size", "sh_link",\
                         "sh_info", "sh_addralign", "sh_entsize"]
        
    def getType(self):
        return ELF64_SHDR
        
    @staticmethod
    def parse(readDataInstance):
        elf64_shdr = Elf64_Shdr()
        elf64_shdr.sh_name = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_shdr.sh_type = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_shdr.sh_flags = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        elf64_shdr.sh_addr = elfdatatypes.Elf64_Addr(readDataInstance.readElf64Addr())
        elf64_shdr.sh_offset = elfdatatypes.Elf64_Off(readDataInstance.readElf64Off())
        elf64_shdr.sh_size = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        elf64_shdr.sh_link = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_shdr.sh_info = elfdatatypes.Elf64_Word(readDataInstance.readElf64Word())
        elf64_shdr.sh_addralign = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        elf64_shdr.sh_entsize = elfdatatypes.Elf64_Xword(readDataInstance.readElf64Xword())
        return elf64_shdr
