from pathlib import Path

from clld.web.assets import environment

import polyglottaafricana


environment.append_path(
    Path(polyglottaafricana.__file__).parent.joinpath('static').as_posix(),
    url='/polyglottaafricana:static/')
environment.load_path = list(reversed(environment.load_path))
