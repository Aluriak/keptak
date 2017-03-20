"""Write a bash script operating on files found in current directory.

"""

import glob
import argparse


def parsed_cli() -> dict:
    """Implement the CLI, return parsed args from command line parameters"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script-name', type=str, default='next.sh',
                        help='name of the script to print')
    parser.add_argument('--targets', metavar='N', nargs='+', type=str,
                        default=['*.mkv', '*.avi'],
                        help="files to read, in given order (unless -s)")
    parser.add_argument('-s', '--sort', action='store_true',
                        help="sort file name alphabetically before generating lines")
    parser.add_argument('-m', '--makefile', action='store_true',
                        help="write a makefile with a recipe launching the bash script")
    parser.add_argument('-p', '--player', type=str, default='mplayer',
                        help="command to invoke for playing input files")
    return parser.parse_args()


def targets_from(globs:iter) -> iter:
    """Yield all files found with given globs."""
    for pattern in globs:
        yield from glob.glob(pattern)

def command_from(player:str, targets:iter, sep:str=' \\\n') -> str:
    """Build and return the command invokating given targets with given player."""
    return player + sep + sep.join(targets)

def write_script(name:str, player:str, targets:iter):
    """Overwrite file 'name' with the command invoking targets with player."""
    with open(name, 'w') as ofd:
        ofd.write(command_from(player, targets))

def write_makefile(script_name:str, name:str='Makefile', shell:str='sh'):
    with open(name, 'w') as ofd:
        ofd.write('play:\n\t{} {}\n'.format(shell, script_name))


if __name__ == "__main__":
    args = parsed_cli()
    targets = tuple(targets_from(args.targets))
    if not targets:
        print('No target found. Exit.')
        exit()
    print(len(targets), 'targets found.')
    if args.sort:
        targets = sorted(targets)
    if args.makefile:
        write_makefile(args.script_name)
        print('Makefile created')
    write_script(args.script_name, args.player, targets)
    print('{} created'.format(args.script_name))
