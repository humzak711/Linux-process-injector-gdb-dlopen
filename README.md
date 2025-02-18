**FOR EDUCATIONAL PURPOSES ONLY, WE DO NOT CONDONE ANY MISUSE OF THIS REPOSITORY, THE AUTHORS CLAIM NO LIABILITY FOR ANY MISUSE, YOU ARE RESPONSIBLE FOR YOUR OWN ACTIONS, THIS REPOSITORY WAS CREATED TO LEARN ABOUT LINUX AND HOW YOU CAN CARRY OUT PROCESS INJECTIONS IN LINUX WITHOUT ELEVATED PRIVILEGES USING GDB**

***THIS TOOL DOES NOT REQUIRE ELEVATED PRIVILEGES***

**IF YOU ARE USING THIS TOOL TO INJECT A SHARED OBJECT FILE, YOUR SHARED OBJECT MUST INCLUDE AN `__attribute__((constructor))` TO BE COMPATIBLE AS THAT IS THE FUNCTION WHICH WILL BE EXECUTED ONCE THE SHARED OBJECT FILE IS INJECTED AND EXECUTED WITHIN THE MEMORY OF IT'S TARGET PROCESS, SEE 'src/exampleSO2.c'**

*Do not be a fucking idiot and start creaming if you intend to misuse this for illegal purposes, if you cant code something like this you wont be able to do much with it*

This is a program created (kind of rushed) in python/C, which takes the path to either an executable ELF or shared object ELF file and embed it into a compiled program at a filepath specified by you.<br>
The compiled program when ran will inject an executable ELF or shared object ELF file of your choice into a random non root, non critical process via the lovely GNU debugger gdb and this means the embedded ELF will be executed within the memory of the target process rather than on disk.

Dependencies:

gcc, gdb, libdl-dev, python3

To install and use:

`sudo apt install -y gcc gdb libdl-dev python3` <br>
`git clone https://github.com/EthanTwofishBlackwell/SharedObject_Injector.git` <br>
`cd SharedObject_Injector` <br>
`cd src` <br>

`Usage: python3 builder.py <ELF_path> <output_executable_filepath>`
