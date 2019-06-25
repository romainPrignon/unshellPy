from typing import Any, Callable, Iterator, Dict, List
from dataclasses import dataclass

Args = List[Any]
Commands = Iterator
Script = Callable[[Args], Commands]


@dataclass
class Options:
    env: Dict[str, str]
