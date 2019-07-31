import os


def script():
    SOME_ENV_VAR = os.environ["SOME_ENV_VAR"]
    print(f"node: {SOME_ENV_VAR}")
    yield f"echo $SOME_ENV_VAR"
