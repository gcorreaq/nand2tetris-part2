import argparse
import logging
from pathlib import Path
from typing import Iterable
import sys

from parser import Parser
from command_writer import CommandWriter


def _setup_logger():
    new_logger = logging.getLogger("vm_translator")
    new_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    new_logger.addHandler(console_handler)
    return new_logger


logger = _setup_logger()


def _get_target_files(target_path: Path) -> Iterable[Path]:
    if target_path.is_dir():
        target_files = target_path.glob('*.vm')
    elif target_path.is_file():
        target_files = [target_path]
    else:
        raise ValueError(f"Invalid path {target_path}")

    return target_files


def _resolve_output_filename(path: Path) -> Path:
    if path.is_dir():
        new_filename = (path / path.name)
    else:
        new_filename = path
    return new_filename.with_suffix('.asm')


def main(arguments):
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argument_parser.add_argument('target_path', help='The target file to process')
    argument_parser.add_argument('-v', '--verbose', help='More verbose logging', action='store_true')
    args = argument_parser.parse_args(arguments)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    target_path = Path(args.target_path).resolve(strict=True)
    logger.info('Processing %s', target_path)

    input_files_paths = _get_target_files(target_path)
    output_file_path = _resolve_output_filename(target_path)

    logger.debug('Input files are %r', input_files_paths)
    logger.debug('Output will be written to %r', output_file_path)

    with output_file_path.open(mode='w') as output_file_obj:
        for input_file_path in input_files_paths:
            with input_file_path.open('r') as input_file_obj:
                parser = Parser(input_file_obj)
                parsed_commands = parser.parse_file()
                command_writer = CommandWriter(
                    output_file=output_file_obj,
                    input_file_path=input_file_path,
                    commands=parsed_commands,
                )
                logger.info('Initiating compilation')
                command_writer.compile()

    logger.info('Compilation finished')


if __name__ == '__main__':
    main(sys.argv[1:])
