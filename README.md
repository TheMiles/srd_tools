# SRD parser

**THIS IS NOT READY YET**

`srd_parser` is a python script which helps converting some information
from the [System Reference Document v5.2.1](https://www.dndbeyond.com/srd)
for the 5.5e of the "greatest tabletop roleplaying game".

The script currently works only on the german edition of the SRD.

It converts all the spells to a json format



## Usage

```bash
usage: srd_parser.py [-h] [-f FIRST] [-l LAST] [-o OUTPUT] input

Convert 5.5e SRD 2025 spells

positional arguments:
  input                Input srd pdf

options:
  -h, --help           show this help message and exit
  -f, --first FIRST    first page
  -l, --last LAST      last page
  -o, --output OUTPUT  Output file (default: stdout)
```
