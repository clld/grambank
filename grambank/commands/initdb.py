"""

"""
import pathlib
import contextlib

import transaction
from clldutils import db
from clldutils import clilib
from clld.scripts.util import SessionContext, ExistingConfig, get_env_and_settings
from cldfcatalog import Catalog

import grambank
from grambank.scripts.initializedb import main, prime_cache
from grambank.scripts import coverage

PROJECT_DIR = pathlib.Path(grambank.__file__).parent.parent
REPOS = ['Grambank', 'grambank-cldf', 'glottolog/glottolog']


def register(parser):
    parser.add_argument(
        "--config-uri",
        action=ExistingConfig,
        help="ini file providing app config",
        default=str(PROJECT_DIR / 'development.ini'))
    parser.add_argument(
        '--doi',
        default=None,
    )
    parser.add_argument(
        '--prime-cache-only',
        action='store_true',
        default=False,
    )
    for repo in REPOS:
        d = PROJECT_DIR.parent
        if '/' in repo:
            d, repo = repo.split('/', maxsplit=1)
            d = PROJECT_DIR.parent.parent / d
        parser.add_argument(
            '--{0}'.format(repo),
            default=pathlib.Path(d / repo),
            help='Clone of {0}'.format(repo),
            type=clilib.PathType,
        )
        parser.add_argument(
            '--{0}-version'.format(repo),
            help='Version tag of {0}'.format(repo),
            default=None,
        )


def run(args):
    args.env, settings = get_env_and_settings(args.config_uri)

    with contextlib.ExitStack() as stack:
        stack.enter_context(db.FreshDB.from_settings(settings, log=args.log))
        stack.enter_context(SessionContext(settings))

        for repo in REPOS:
            attr = repo.split('/')[-1].replace('-', '_')
            if getattr(args, attr + '_version'):
                stack.enter_context(
                    Catalog(getattr(args, attr), tag=getattr(args, attr + '_version')))

        if not args.prime_cache_only:
            with transaction.manager:
                main(args)
        with transaction.manager:
            prime_cache(args)

        coverage.main(args)
