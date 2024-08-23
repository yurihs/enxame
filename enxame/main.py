from typing import Annotated, Generic, TypeVar

from fastapi import Body, FastAPI, Path, HTTPException
from pydantic import BaseModel, computed_field

from enxame import dokku

app = FastAPI()


class AppCreateRequest(BaseModel):
    name: Annotated[str, Body(pattern=dokku.APP_NAME_REGEX)]


class AppCreateResponse(BaseModel):
    name: str


class AppSetConfigRequest(BaseModel):
    config: dict[str, str]


class AppDetailResponse(BaseModel):
    name: str
    config: dict[str, str]


ListItem = TypeVar("ListItem")


class ListResponse(BaseModel, Generic[ListItem]):
    items: list[ListItem]

    @computed_field
    def n_items(self) -> int:
        return len(self.items)


class AppListItem(BaseModel):
    name: str


@app.post("/apps")
async def create_app(request: AppCreateRequest) -> AppCreateResponse:
    await dokku.create_app(request.name)
    return AppCreateResponse(name=request.name)


@app.get("/apps")
async def list_apps() -> ListResponse[AppListItem]:
    app_names = await dokku.list_apps()
    return ListResponse(items=[AppListItem(name=x) for x in app_names])


@app.get("/apps/{name}")
async def get_app(
    name: Annotated[str, Path(pattern=dokku.APP_NAME_REGEX)],
) -> AppDetailResponse:
    config = await dokku.get_app_config(name)
    return AppDetailResponse(
        name=name,
        config=config,
    )


@app.delete("/apps/{name}")
async def delete_app(
    name: Annotated[str, Path(pattern=dokku.APP_NAME_REGEX)],
) -> AppDetailResponse:
    await dokku.destroy_app(name)
    raise HTTPException(status_code=204)


@app.put("/apps/{name}/config")
async def set_app_config(name, request: AppSetConfigRequest) -> AppDetailResponse:
    config = await dokku.set_app_config(name, request.config)
    return AppDetailResponse(
        name=name,
        config=config,
    )
