#!/usr/bin/env python
import sys
from os import path

import nose

def run_all(argv=None):
    sys.exitfunc = lambda: sys.stderr.write('Shutting down....\n')
    # always insert coverage when running tests
    if argv is None:
        argv = [
            'nosetests', '--with-xunit',
            '--with-xcoverage', '--cover-package=elasticsearch', '--cover-erase',
            '--logging-filter=elasticsearch', '--logging-level=DEBUG',
            '--verbose',
        ]
    else:
        for p in ('--with-coverage', '--cover-package=elasticsearch', '--cover-erase'):
            if p not in argv:
                argv.append(p)

    nose.run_exit(
        argv=argv,
        defaultTest=path.abspath(path.dirname(__file__))
    )

if __name__ == '__main__':
    run_all(sys.argv)

