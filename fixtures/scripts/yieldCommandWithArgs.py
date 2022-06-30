# type: ignore

def script(foo, bar):
    yield f"echo {foo}"
    yield f"echo {bar}"
