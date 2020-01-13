import sys

try:
    if len(sys.argv) > 1:
        if sys.argv[1] == 'charge':
            print('charging')
            raise KeyboardInterrupt

    print('main')

finally:
    print('terminated')

