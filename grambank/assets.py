import pathlib

from clld.web.assets import environment

import grambank


environment.append_path(
    str(pathlib.Path(grambank.__file__).parent.joinpath('static')), url='/grambank:static/')
environment.load_path = list(reversed(environment.load_path))
