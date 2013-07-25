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

# http://stackoverflow.com/questions/592746/how-can-you-print-a-variable-name-in-python
# Example:
#
# >>> a = 'some var'
# >>> namestr(a, globals())
# ['a']

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def make_dict(the_list):
	return dict([(e[1], e[0]) for e in the_list]+the_list)

ELF32_EHDR = 0
ELF64_EHDR = 1

ELF32ADDR = 0
ELF32OFF = 1
ELF32WORD = 2
ELF32HALF = 3
ELF32SWORD = 4

ELF64ADDR = 0
ELF64HALF = 1
ELF64OFF = 2
ELF64SWORD = 3
ELF64SXWORD = 4
ELF64XWORD = 5
ELF64WORD = 6

elf_object_file_types = [
	("ET_NONE", 0),
	("ET_REL", 1),
	("ET_EXEC", 2),
	("ET_DYN", 3),
	("ET_CORE", 4),
	("ET_LOPROC", 0xff00),
	("ET_HIPROC", 0xffff)]

ELF_OBJECT_FILE_TYPES = make_dict(elf_object_file_types)

elf_machine_types = [
	("EM_NONE", 0),
	("EM_M32", 1),
	("EM_SPARC", 2),
	("EM_386", 3),
	("EM_68K", 4),
	("EM_88K", 5),
	("EM_860", 7),
	("EM_MIPS", 8)]

ELF_MACHINE_TYPES = make_dict(elf_machine_types)

elf_object_file_version = [
	("EV_NONE", 0),
	("EV_CURRENT", 1)]

ELF_OBJECT_FILE_VERSIONS = make_dict(elf_object_file_version)

elf_ident_types = [
	("EI_MAG0", 0),
	("EI_MAG1", 1),
	("EI_MAG2", 2),
	("EI_MAG3", 3),
	("EI_CLASS", 4),
	("EI_DATA", 5),
	("EI_VERSION", 6),
	("EI_PAD", 7),
	("EI_NIDENT", 16)]

ELF_IDENT_TYPES = make_dict(elf_ident_types)

elf_magics = [
	("ELFMAG0", 0x7f),
	("ELFMAG1", 0x45), # "E"
	("ELFMAG2", 0x4c), # "L"
	("ELFMAG3", 0x46)] # "F"

ELF_MAGICS = make_dict(elf_magics)

elf_file_class = [
	("ELFCLASSNONE", 0),
	("ELFCLASS32", 1),
	("ELFCLASS64", 2)]

ELF_FILE_CLASS = make_dict(elf_file_class)

elf_data_encoding_types = [
	("ELFDATANONE", 0),
	("ELFDATA2LSB", 1),
	("ELFDATA2MSB", 2)]

ELF_DATA_ENCODING_TYPES = make_dict(elf_data_encoding_types)

elf_shn_special = [
	("SHN_UNDEF", 0),
	("SHN_LORESERVE", 0xff00),
	("SHN_LOPROC", 0xff00),
	("SHN_HIPROC", 0xff1f),
	("SHN_ABS", 0xfff1),
	("SHN_COMMON", 0xfff2),
	("SHN_HIREVERSE", 0xffff)]

ELF_SHN_SPECIAL = make_dict(elf_shn_special)

elf_section_types = [
	("SHT_NULL", 0),
	("SHT_PROGBITS", 1),
	("SHT_SYMTAB", 2),
	("SHT_STRTAB", 3),
	("SHT_RELA", 4),
	("SHT_HASH", 5),
	("SHT_DYNAMIC", 6),
	("SHT_NOTE", 7),
	("SHT_NOBITS", 8),
	("SHT_REL", 9),
	("SHT_SHLIB", 10),
	("SHT_DYNSYM", 11),
	("SHT_LOPROC", 0x70000000),
	("SHT_HIPROC", 0x7fffffff),
	("SHT_LOUSER", 0x80000000),
	("SHT_HIUSER", 0xffffffff)]

ELF_SECTION_TYPES = make_dict(elf_section_types)

elf_shf_flags = [
	("SHF_WRITE", 1),
	("SHF_ALLOC", 2),
	("SHF_EXECINSTR", 4),
	("SHF_MASKPROC", 0xf0000000)]

ELF_SHF_FLAGS = make_dict(elf_shf_flags)

elf_symbol_bindig_types = [
	("STB_LOCAL", 0),
	("STB_GLOBAL", 1),
	("STB_WEAK", 2),
	("STB_LOPROC", 13),
	("STB_HIPROC", 15)]

ELF_SYMBOL_BINDING_TYPES = make_dict(elf_symbol_bindig_types)

elf_symbol_types = [
	("STT_NOTYPE", 0),
	("STT_OBJECT", 1),
	("STT_FUNC", 2),
	("STT_SECTION", 3),
	("STT_FILE", 4),
	("STT_LOPROC", 13),
	("STT_HIPROC", 15)]

ELF_SYMBOL_TYPES = make_dict(elf_symbol_types)

elf_relocation_types = [
	("R_386_NONE", 0),
	("R_386_32", 1),
	("R_386_PC32", 2),
	("R_386_GOT32", 3),
	("R_386_PLT32", 4),
	("R_386_COPY", 5),
	("R_386_GLOB_DAT", 6),
	("R_386_JMP_SLOT", 7),
	("R_386_RELATIVE", 8),
	("R_386_GOTOOFF", 9),
	("R_386_GOTOPC", 10)]

ELF_RELOCATION_TYPES = make_dict(elf_relocation_types)

elf_segment_types = [
	("PT_NULL", 0),
	("PT_LOAD", 1),
	("PT_DYNAMIC", 2),
	("PT_INTERP", 3),
	("PT_NOTE", 4),
	("PT_SHLIB", 5),
	("PT_PHDR", 6),
	("PT_LOPROC", 0x70000000),
	("PT_HIPROC", 0x7fffffff)]

ELF_SEGMENT_TYPES = make_dict(elf_segment_types)
