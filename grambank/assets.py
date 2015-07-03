from clld.web.assets import environment
from path import path

import grambank


environment.append_path(
    path(grambank.__file__).dirname().joinpath('static'), url='/grambank:static/')
environment.load_path = list(reversed(environment.load_path))
