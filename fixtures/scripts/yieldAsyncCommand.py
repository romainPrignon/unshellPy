# type: ignore

async def script():
    [cmd1, cmd2] = yield ["echo cmd1...; sleep 1", "echo cmd2...; sleep 2"]
