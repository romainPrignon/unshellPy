# ![un](./unshell.png) shell

> Set your shell free !

Combine PHP and shell command.


## Features

* **Light**: No dependencies
* **Async**: Work Asynchronously
* **Testable**: Unshell script are easily testable because they yield execution control


## Setup

```sh
composer require romainprignon/unshell
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

Given the script: `pause.php` to pause all docker containers
```php
function pause():
  $ids = yield from fetchContainerIds();

  for $id in $ids:
    yield "docker pause {$id}";


function fetchContainerIds():
  $ids = yield "docker ps -q --no-trunc";

  return explode("\n", $ids);
```

Run it through unshell
```sh
unshell run pause.php
```


### Embedded script inside apps
Given the precedent script `pause.php`
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
- [Pause containers](examples/pause-resume-container/)

## Contribute
```sh
poetry config --local virtualenvs.in-project true
poetry shell
make install
watch make dev
```

## License

The code is available under the [MIT license](LICENSE.md).


## TODO
- everything
