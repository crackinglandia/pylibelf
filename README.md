pylibelf <img src="http://goo.gl/nk11pi" align="right" height="150" style="max-width: 70px">
========

A pure Python library to parse [ELF](http://es.wikipedia.org/wiki/Executable_and_Linkable_Format) files.

At the moment, you can only read ELF files. The write functionallity is work-in process.

**NOTE**: This is not a wrapper around libelf!.

How to use it
========

```python
>>> import pylibelf
>>> elf = pylibelf.ELF("/bin/bash")
>>> elf.elfHdr
<pylibelf.Elf64_Ehdr object at 0x7f68672d2d50>
>>> elf.elfHdr.e_entry
<elfdatatypes.Elf64_Addr object at 0x7f6867277d50>
>>> elf.elfHdr.e_entry.value.__hex__()
'0x41d438'
>>> elf.ShdrTable[1]
<pylibelf.Elf64_Shdr object at 0x7f686727d6d0>
>>> elf.ShdrTable[1].sectionName
'.interp'
>>> elf.ShdrTable[1].sectionRawData
'/lib64/ld-linux-x86-64.so.2\x00'
```

License
========

pylibelf is distributed under [BSD 3-Clause](http://opensource.org/licenses/BSD-3-Clause).
