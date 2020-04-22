import argparse
import sys


def main(arguments):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('target_file', help='The target file to process')
    args = argument_parser.parse_args()


if __name__ == '__main__':
    main(sys.argv[1:])
