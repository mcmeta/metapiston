from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class LauncherModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, alias_generator=to_camel)
