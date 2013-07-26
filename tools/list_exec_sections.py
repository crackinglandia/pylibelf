import os
import sys
import pylibelf
import elfconstants

if len(sys.argv) < 2:
	print "Usage: %s <filename>" % __file__
	sys.exit(0)

sys.path.insert(0, "/home/ncr/github/pylibelf")

filename = sys.argv[1]

elf = pylibelf.ELF(filename)

for section in elf.ShdrTable:
	if (section.sh_flags.value & elfconstants.ELF_SHF_FLAGS["SHF_EXECINSTR"]) == elfconstants.ELF_SHF_FLAGS["SHF_EXECINSTR"]:
		print "[+] Section is marked as executable!"

