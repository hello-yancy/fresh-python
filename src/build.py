#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import factory

def print_help():
    print('Usage:')
    print('  python build.py [all|clean]\n')
    print('Examples:')
    print('  python build.py all')
    print('  python build.py clean')

def run(mode):
    if mode == 'all':
        factory.FullBuildJobFactory().job().run()
    else:
        print_help()
        sys.exit(2)

def main():
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print_help()
        sys.exit(2)

if __name__ == '__main__':
    main()
