import sys
import json
from Lexer.Lexer import *
from Update import *
import os

#Info-------
ZircVer: str = "0.1"

#------------

def main(argc: int = sys.argv.__len__(), argv: list[str] = sys.argv):
    File = argv[1:2]

    if File == []:
        print("zirc: no input files", file=sys.stderr)
        sys.exit(1)

    if File[0] == "--h":
        print("Usage: zirc <file> [options]")

        print("options:")
        print("     -o <file>            puts the output into <file>")
        print("     -filet=<filetype>    generates an asm file(-filet=asm) an obj file(-filet=o)")
        print("     --dwarf              enables dwarf")
        print("     -link=<file>         adds a libary to links with")
        sys.exit(0)

    elif File[0] == "--v":
        print(ZircVer)        
        sys.exit(0)
    
    # elif File[0] == "--t":
    #     print("Test Work")
    #     sys.exit(0)
    

    
if __name__ == '__main__':
    main()
    sys.exit(0)

