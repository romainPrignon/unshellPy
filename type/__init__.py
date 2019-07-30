from typing import Any, Callable, Generator, AsyncGenerator, List, \
    Union, Optional, Awaitable

Args = List[Any]
Command = str
CommandResult = Optional[str]
Commands = Generator[Command, CommandResult, Command]
AsyncCommands = AsyncGenerator[Command, CommandResult]
Script = Callable[[Args], Commands]
AsyncScript = Callable[[Args], AsyncCommands]
Engine = Callable[[Union[Script, AsyncScript], Args], Awaitable[Any]]
