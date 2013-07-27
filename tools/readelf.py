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

import sys

sys.path.insert(0, "/home/ncr/github/pylibelf/")

import pylibelf
import elfdatatypes

import optparse

def prepareOptions(parser):
    parser.add_option("-H", "--header", dest="show_elf_header", action="store_true", default=False, help="print ELF header")
    parser.add_option("-s", "--section-headers", dest="show_section_hdrs", action="store_true", default=False, help="print section headers")
    parser.add_option("-p", "--program-headers", dest="show_program_hdrs", action="store_true", default=False, help="print program headers")
    return parser

def showElfHdr(elfInstance):
    f = elfInstance.elfHdr.getFields()
    
    for field in f:
        if isinstance(f[field], elfdatatypes.Array):
            print "--> %s - Array length: %d" % (field, len(f[field]))
            c = 0
            for element in f[field]:
                print "[%d] 0x%01x" % (c, element.value)
                c += 1
        else:
            print "--> %s = 0x%08x" % (field, f[field].value)

def showSectionHeaders(elfInstance):
    for entry in elfInstance.ShdrTable:
        f = entry.getFields()
        print "Section Name: %s" % entry.sectionName
        for field in f:
            print "-> %s = 0x%08x" % (field, f[field].value)

        print "\n"

def showProgramHeaders(elfInstance):
    for entry in elfInstance.PhdrTable:
        f = entry.getFields()
        for field in f:
            print "-> %s = 0x%08x" % (field, f[field].value)

        print "\n"

def main():

    parser = optparse.OptionParser("usage: %prog [options] filename")    
    parser = prepareOptions(parser)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    elf = pylibelf.ELF(args[0])

    if options.show_elf_header:
        showElfHdr(elf)
    elif options.show_section_hdrs:
        showSectionHeaders(elf)
    elif options.show_program_hdrs:
        showProgramHeaders(elf)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
