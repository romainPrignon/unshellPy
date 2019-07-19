from typing import Any, Callable, Generator, AsyncGenerator, Dict, List, Union, Optional, Awaitable
from dataclasses import dataclass

Args = List[Any]
Command = str
CommandResult = Optional[str]
Commands = Generator[Command, CommandResult, Command]
AsyncCommands = AsyncGenerator[Command, CommandResult]
Script = Callable[[Args], Commands]
AsyncScript = Callable[[Args], AsyncCommands]
Engine = Callable[[Union[Script, AsyncScript], Args], Awaitable[Any]]


@dataclass
class Options:
    env: Dict[str, str]
