import sys
from hun_date_parser import text2datetime


def main():
    if len(sys.argv) > 1:
        print(text2datetime(' '.join(sys.argv[1:])))


if __name__ == '__main__':
    main()