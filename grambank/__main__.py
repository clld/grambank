import sys

from clldutils.clilib import ParserError, register_subcommands, get_parser_and_subparsers
from clldutils.loglib import Logging


def main(args=None, catch_all=False, parsed_args=None):
    import grambank.commands

    parser, subparsers = get_parser_and_subparsers('grambank-app')
    register_subcommands(subparsers, grambank.commands)

    args = parsed_args or parser.parse_args(args=args)
    if not hasattr(args, "main"):
        parser.print_help()
        return 1

    with Logging(args.log, level=args.log_level):
        try:
            return args.main(args) or 0
        except KeyboardInterrupt:  # pragma: no cover
            return 0
        except ParserError as e:
            print(e)
            return main([args._command, '-h'])
        except Exception as e:
            if catch_all:  # pragma: no cover
                print(e)
                return 1
            raise


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main() or 0)
