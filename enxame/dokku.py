import asyncssh
import json
import shlex

from enxame.config import settings

APP_NAME_REGEX = r"^[a-z0-9][a-z0-9-]*$"


class DokkuError(Exception):
    pass


async def run_command(command) -> asyncssh.SSHCompletedProcess:
    key = asyncssh.import_private_key(settings.dokku_ssh_key)
    async with asyncssh.connect(
        settings.dokku_hostname,
        username=settings.dokku_username,
        client_keys=[key],
        known_hosts=None,
    ) as conn:
        result = await conn.run(command)
        if result.returncode != 0:
            raise DokkuError(result.stderr)
        return result


async def create_app(name: str):
    await run_command(f"dokku --quiet apps:create {shlex.quote(name)}")


async def destroy_app(name: str):
    await run_command(f"dokku --quiet apps:destroy --force {shlex.quote(name)}")


async def list_apps() -> list[str]:
    result = await run_command("dokku --quiet apps:list")
    return result.stdout.splitlines()


async def get_app_config(name: str) -> dict[str, str]:
    result = await run_command(
        f"dokku --quiet config:export --format json {shlex.quote(name)}"
    )
    return json.loads(result.stdout)


async def set_app_config(name: str, config: dict[str, str]) -> dict[str, str]:
    if not config:
        await run_command(f"dokku --quiet config:clear {shlex.quote(name)}")
    else:
        await run_command(
            f"dokku --quiet config:clear --no-restart {shlex.quote(name)}"
        )
        config_keyvalue = " ".join(shlex.quote(f"{k}={v}") for k, v in config.items())
        await run_command(f"dokku --quiet config:set {name} {config_keyvalue}")
    result = await run_command(
        f"dokku --quiet config:export --format json {shlex.quote(name)}"
    )
    return json.loads(result.stdout)
