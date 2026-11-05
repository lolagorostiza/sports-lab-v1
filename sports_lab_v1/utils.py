from collections.abc import Iterator

from sports_lab_v1.domain.errors import DomainError  # ajusta al módulo donde esté DomainError


def read_lines(path: str) -> Iterator[str]:
    """Lee las líneas no vacías de un fichero, saltando la cabecera."""
    try:
        with open(path, encoding="utf-8") as file:
            next(file, None)  # Saltar la cabecera
            for line in file:
                if line.strip():
                    yield line
    except OSError as error:
        raise DomainError(
            f"No se puede leer el fichero '{path}': {error}"
        ) from error