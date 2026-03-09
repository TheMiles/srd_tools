#!/usr/bin/env python3

import sys,os,argparse


def main():

    global args

    print( F"Mein file ist {args.input[0]}")


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
