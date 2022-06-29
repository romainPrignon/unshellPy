# ![un](./unshell.png) shell

> Set your shell free !

Combine python and shell command.


## Features

* **Light**: There are no dependencies
* **Async**: Work with async/await
* **Testable**: Unshell script are easily testable because they yield execution control


## Setup

```sh
pip install unshell
alias unshell=$(pip show unshell | grep Location | cut -d: -f2)/unshell/cli.py
```


## Usage

### Execute script through Shell
```
Execute script through unshell runtime

Usage:
  unshell COMMAND [SCRIPT_PATH] [ARGS...]

Commands:
  help      Print this help message
  run       run a script through unshell runtime
```

Given the script: `pause.py` to pause all docker containers
```py
def pause():
  ids = yield from fetchContainerIds()

  for id in ids:
    yield f"docker pause {id}"


def fetchContainerIds():
  ids = yield f"docker ps -q --no-trunc"

  return ids.splitlines()
```

Run it through unshell
```sh
unshell run pause.py
```


### Embedded script inside apps
Given the precedent script `pause.py`
```py
from unshell import Unshell
import os

def main():
    script = resolve('./scripts/pause.js') # resolve your python module
    
    try:
        Unshell({"env": os.environ})(script)
    except Exception as err:
        print(err)

```


## Examples
Here is some examples of what you can do with unshell
- [Pause containers](examples/pause-resume-container)

## Contribute
```sh
poetry config --local virtualenvs.in-project true
poetry shell
make install
watch make dev
```

## License

The code is available under the [MIT license](LICENSE.md).
