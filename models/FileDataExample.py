# file_data.py
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Optional, Union


@dataclass
class FileDataExample:
    """
    Model class that stores data about a single file.

    All created instances are:
      - Stored in the class-level _registry list
      - Indexed by path in the class-level _index dict

    You can retrieve:
      - All instances via FileData.all()
      - A single instance via FileData.get_by_path(path)
    """
    path: str
    content: Union[str, bytes]

    # Class-level registry of all instances
    _registry: ClassVar[List["FileDataExample"]] = []
    # Class-level index: path -> instance
    _index: ClassVar[Dict[str, "FileDataExample"]] = {}

    def __post_init__(self) -> None:
        # Automatically register every new instance
        self._registry.append(self)
        # Index by path (last one wins if duplicates)
        self._index[self.path] = self

    @classmethod
    def all(cls) -> List["FileDataExample"]:
        """Return a *copy* of the list of all FileData instances."""
        return list(cls._registry)

    @classmethod
    def get_by_path(cls, path: str) -> Optional["FileDataExample"]:
        """
        Retrieve a single FileData instance by its file path.

        Returns None if no instance is found for the given path.
        """
        return cls._index.get(path)

    @classmethod
    def clear_registry(cls) -> None:
        """Clear the registry and index (useful before a new run or in tests)."""
        cls._registry.clear()
        cls._index.clear()
