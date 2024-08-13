from pathlib import Path
import schemas


def path(file_name):
    return str(Path(schemas.__file__).parent.parent.joinpath(f'schemas/{file_name}'))
