import tarfile
from typing import Any, Iterable

def validate_tar(
    members: Any,
    *,
    max_files: int = 10_000,
    require_unique_names: bool = True,
) -> bool:
    """
    Template-style validator analogous to validate_json(), but for a *decoded*
    representation of a tar archive:

    Expected format (Python object):
      [
        {"name": str, "size": int, "type": "file"|"dir"|"symlink", "linkname": Optional[str]},
        ...
      ]

    This is useful if your fuzzer produces a JSON description of a tar,
    rather than raw tar bytes.
    """
    if not isinstance(members, list):
        return False
    if len(members) > max_files:
        return False

    seen = set()
    allowed_types = {"file", "dir", "symlink"}

    for entry in members:
        if not isinstance(entry, dict):
            return False
        if "name" not in entry or "size" not in entry or "type" not in entry:
            return False

        name = entry["name"]
        size = entry["size"]
        typ = entry["type"]

        if not isinstance(name, str) or not name:
            return False
        if require_unique_names:
            if name in seen:
                return False
            seen.add(name)

        if not isinstance(size, int) or size < 0:
            return False
        if typ not in allowed_types:
            return False

        if typ == "symlink":
            # linkname is required for symlinks
            if "linkname" not in entry or not isinstance(entry["linkname"], str):
                return False

    return True
