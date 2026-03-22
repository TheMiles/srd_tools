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
        r'((\w+)zauber\s+(\d)\.\s+Grades'   # z.B. "Beschwörungszauber 1. Grades"
        r'|Zaubertrick\s+der\s+(\w+))',     # z.B. "Zaubertrick der Verwandlung"
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


def splitType( spell ):

    s = " ".join(spell)

    spell_pattern = re.compile(    
        r'(\w+)zauber\s+(\d)\.\s+Grades\s+\(([^)]+)\).*',   # z.B. "Beschwörungszauber 1. Grades"
        re.IGNORECASE
    )

    cantripspell_pattern = re.compile(    
        r'Zaubertrick\s+der\s+(\w+)\s+\((.+)\)',     # z.B. "Zaubertrick der Verwandlung"
        re.IGNORECASE
    )

    spell_match = spell_pattern.search( s )
    cantrip_match = cantripspell_pattern.search( s )

    assert( (spell_match and not cantrip_match) or (not spell_match and cantrip_match) )

    if spell_match:
        school  = spell_match.group( 1 )
        level   = spell_match.group( 2 )
        classes = spell_match.group( 3 )

    if cantrip_match:

        school  = cantrip_match.group( 1 )
        level   = 0
        classes = cantrip_match.group( 2 )

    classes = [ c.strip() for c in classes.split( ",") ]

    school_conversion = {
        "Bann" :          "Bann",
        "Beschwörung" :   "Beschwörung",
        "Beschwörungs" :  "Beschwörung",
        "Erkenntnis" :    "Erkenntnis",
        "Hervorrufung" :  "Hervorrufung",
        "Hervorrufungs" : "Hervorrufung",
        "Illusion" :      "Illusion",
        "Illusions" :     "Illusion",
        "Nekromantie" :   "Nekromantie",
        "Verwandlung" :   "Verwandlung",
        "Verwandlungs" :  "Verwandlung",
        "Verzauberung" :  "Verzauberung",
        "Verzauberungs" : "Verzauberung"
    }

    school = school_conversion[ school ]

    return level, school, classes



def splitCastingTime( spell ):

    s = " ".join(spell)

    casting_time_pattern = re.compile(    
        r'Zeitaufwand:\s*(.+?)( oder Ritual)?\s*Reichweite:',
        re.IGNORECASE
    )

    casting_time_match = casting_time_pattern.search( s )

    assert( casting_time_match )

    g = casting_time_match.groups()

    casting_time = g[0]
    ritual       = bool(g[1])

    return casting_time, ritual



def convertSpell( spell_text ):

    spell = {}

    spell["title"] = spell_text[0]
    spell["level"], spell["school"], spell["classes"] = splitType( spell_text[1:5] )
    spell["castingTime"], spell["ritual"] = splitCastingTime( spell_text[2:8] ) 

    return spell



def main():

    global args

    pages = [ parse_page( x, args.input[0] ) for x in range( args.first, args.last + 1 ) ]
    pages = [ decolumnize( p ) for p in pages ]
    document = [ l.strip() for p in pages for l in p ]
    document = [ l for l in document if len( l ) > 0 ]
    spells   = [ convertSpell( s ) for s in splitSpells( document ) ]

    for s in spells:

        print( s["title"], s["castingTime"], s["ritual"] )

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
