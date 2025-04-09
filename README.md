This is a simple GUI for converting numbers between decimal, binary, and hexadecimal formats. Handles conversion of multiple numbers at a time, and preserves formatting for lists, columns, etc. 

Currently supports unsigned, signed, and floating point (IEEE 32-bit only) representations.

# Latest Windows Installer
[Version 0.3.0](https://github.com/leif-blake/hex2dec/releases/download/v0.3.0/Hex2Dec_Installer_0.3.0.exe)

# Building

In a terminal, run

```
pyinstaller ./Hex2Dec.spec --noconfirm
```

Compile hex2dec_install_compiler.iss using Inno Setup to build an installer
