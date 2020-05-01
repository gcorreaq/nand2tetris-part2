import argparse
import logging
from pathlib import Path
import sys

from parser import Parser
from command_writer import CommandWriter


logger = logging.getLogger("vm_translator")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def main(arguments):
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argument_parser.add_argument('target_file', help='The target file to process')
    argument_parser.add_argument('-v', '--verbose', help='More verbose logging', action='store_true')
    args = argument_parser.parse_args(arguments)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        print('Setting log level to DEBUG')
    else:
        logger.setLevel(logging.INFO)
        print('Setting log level to INFO')

    input_file = Path(args.target_file).absolute()
    logger.info('Processing file %s', input_file)

    with input_file.open('r') as input_file_obj:
        parser = Parser(input_file_obj)
        parsed_commands = parser.parse_file()
        command_writer = CommandWriter(input_file, parsed_commands)
        logger.info('Initiating compilation')
        command_writer.compile()

    logger.info('Compilation finished')


if __name__ == '__main__':
    main(sys.argv[1:])
