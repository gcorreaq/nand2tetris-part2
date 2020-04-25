import argparse
import logging
from pathlib import Path
import sys

from parser import Parser
from command_writer import CommandWriter


logger = logging.getLogger(__name__)


def main(arguments):
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argument_parser.add_argument('target_file', help='The target file to process')
    args = argument_parser.parse_args(arguments)
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
