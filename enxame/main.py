import asyncssh

from typing import Union

from fastapi import FastAPI


from enxame.config import settings

app = FastAPI()

async def run_client() -> None:
    async with asyncssh.connect(
        settings.dokku_hostname,
        username=settings.dokku_username,
        options=asyncssh.SSHClientConnectionOptions(
            client_keys=[asyncssh.import_private_key(settings.dokku_ssh_key)],
            known_hosts=None,
        ),
    ) as conn:
        result = await conn.run("ls /", check=True)
        return result.stdout


@app.get("/")
async def read_root():
    return {"Hello": await run_client()}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
