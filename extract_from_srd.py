#!/usr/bin/env python3

import sys,os,argparse
import subprocess
import re

def findColumnGap( page ):

    for divider in range(55, 70):

        s = set()

        for l in page:

            if len( l ) <= divider: continue

            s.add( l[ divider ] )

        if len( s ) == 1 and  ' ' in s:

            return divider

    return -1


def split( page, divide_at ):


    if divide_at < 0: return page,[]

    first  = []
    second = []

    for l in page:

        if len(l) <= divide_at:
            
            first.append( l )
            continue

        first.append(  l[ : divide_at ] )
        second.append( l[ divide_at : ] )

    return first, second


def decolumnize( page ):

    d   = findColumnGap( page )
    f,s = split( page, d )

    return f + s


def parse_page( page, file ):

    p = str( page )

    r = subprocess.run(
        ["pdftotext", "-layout", "-f", p, "-l", p, file, "-"],
        capture_output=True,
        text=True,
        check=True
    )

    r = r.stdout.split('\n')
    r = r[:-2]
    return r


def splitSpells( document ):

    spell_header_pattern = re.compile(    
        r'(\w+zauber\s+\d+\.\s+Grades'   # z.B. "Beschwörungszauber 1. Grades"
        r'|Zaubertrick\s+der\s+\w+)',     # z.B. "Zaubertrick der Verwandlung"
        re.IGNORECASE
    )

    spell_start_indices = [
        i - 1
        for i, l in enumerate( document )
        if spell_header_pattern.search( l ) and i > 0
    ]

    spells = [
        document[ spell_start_indices[i]:idx ]
        for i, idx in enumerate( spell_start_indices[1:] )
    ]
    spells.append( document[ spell_start_indices[-1]:] )

    return spells


def main():

    global args

    pages = [ parse_page( x, args.input[0] ) for x in range( args.first, args.last + 1 ) ]
    pages = [ decolumnize( p ) for p in pages ]
    document = [ l.strip() for p in pages for l in p ]
    document = [ l for l in document if len( l ) > 0 ]
    spells   = splitSpells( document )

    for s in spells:
        print( s[0] )


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Convert 5.5e SRD 2025 spells')
        parser.add_argument('-f', '--first', type=int, default=122, help='first page')
        parser.add_argument('-l', '--last', type=int, default=202, help='last page')
        parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout, help='Output file (default: stdout)')
        parser.add_argument('input', nargs=1, help='Input srd pdf')
        args = parser.parse_args()
        main()
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
