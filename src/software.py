#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import factory

def print_help():
    print('Usage:')
    print('  python3 software.py [install|uninstall] [all|go|java]\n')
    print('Examples:')
    print('  python3 software.py install all')
    print('  python3 software.py install go')
    print('  python3 software.py install java')
    print('  -------------------------------')
    print('  python3 software.py uninstall all')
    print('  python3 software.py uninstall go')
    print('  python3 software.py uninstall java')

def install(mode):
    if mode == 'all':
        factory.InstallAllSoftwareJobFactory().job().run()
    elif mode == 'go':
        factory.InstallGoJobFactory().job().run()
    elif mode == 'java':
        factory.InstallJavaJobFactory().job().run()
    else:
        raise ValueError('Invalid Input Parameters')

def uninstall(mode):
    if mode == 'all':
        factory.InstallAllSoftwareJobFactory().job().run()
    elif mode == 'go':
        factory.InstallGoJobFactory().job().run()
    elif mode == 'java':
        factory.InstallJavaJobFactory().job().run()
    else:
        raise ValueError('Invalid Parameters')

def main():
    try:
        if len(sys.argv) != 3:
            raise ValueError('Invalid Parameters')

        if sys.argv[1] == 'install':
            install(sys.argv[2])
        elif sys.argv[1] == 'uninstall':
            install(sys.argv[2])
        else:
            raise ValueError('Invalid Parameters')
    except ValueError:
        print_help()
        sys.exit(2)

if __name__ == '__main__':
    main()
