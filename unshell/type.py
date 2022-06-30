from typing import Any, Callable, Generator, AsyncGenerator, List, \
    Union, Optional, Awaitable, Dict

Options = Dict[Any, Any]
Args = Optional[Any]

Command = Union[str, List[str]]
CommandResult = Optional[Union[str, List[str]]]
Commands = Generator[Command, CommandResult, Command]
AsyncCommands = AsyncGenerator[Command, CommandResult]

NoArgsScript = Callable[[], Commands]
ArgsScript = Callable[[Args], Commands]
Script = Union[NoArgsScript, ArgsScript]

NoArgsAsyncScript = Callable[[], AsyncCommands]
ArgsAsynScript = Callable[[Args], AsyncCommands]
AsyncScript = Union[NoArgsAsyncScript, ArgsAsynScript]

Engine = Callable[[Union[Script, AsyncScript], Args], Awaitable[None]]
