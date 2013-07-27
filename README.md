pylibelf
========

A pure Python library to parse ELF files.

At the moment, you can only read [ELF](http://es.wikipedia.org/wiki/Executable_and_Linkable_Format) files. The write functionallity is work-in process.

**NOTE**: This is not a wrapper around libelf!.

How to use it
========

```python
>>> import pylibelf
>>> elf = pylibelf.ELF("/bin/bash")
```

License
========

pylibelf is distributed under [BSD 3-Clause](http://opensource.org/licenses/BSD-3-Clause).
