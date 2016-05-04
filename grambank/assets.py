from clld.web.assets import environment
from clldutils.path import Path

import grambank


environment.append_path(
    Path(grambank.__file__).parent.joinpath('static').as_posix(), url='/grambank:static/')
environment.load_path = list(reversed(environment.load_path))
