from __future__ import annotations

from datetime import datetime

import requests
from metapiston.minecraft._model import LauncherModel
from pydantic import AnyUrl, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class VersionManifestV1(BaseModel):
    """Manifest for Minecraft Java Edition versions available in the official launcher.

    Keys:
        latest: The latest release and snapshot version.
        versions: A list of versions available.
    """

    @staticmethod
    def download(url: str | bytes | AnyUrl) -> VersionManifestV1:
        if not isinstance(url, (str, bytes)):
            url = url.unicode_string()
        return VersionManifestV1.model_validate_json(requests.get(url).content)

    model_config = ConfigDict(
        title="MinecraftVersionManifestV1",
        extra="forbid",
        frozen=True,
        alias_generator=to_camel,
    )

    latest: Latest
    versions: list[Version]

    class Latest(LauncherModel):
        """The latest release and snapshot versions.

        Keys:
            release: The ID of the latest release version.
            snapshot: The ID of the latest snapshot version.
        """

        release: str
        snapshot: str

    class Version(LauncherModel):
        """A version entry.

        Keys:
            id: The ID of this version.
            type: The type of this version; usually release or snapshot.
            url: The link to the <version id>.json for this version.
            time: A timestamp in ISO 8601 format of when the version files were last updated on the manifest.
            release_time: The release time of this version in ISO 8601 format.
        """

        id: str
        type: str
        url: AnyUrl
        time: datetime
        release_time: datetime


if __name__ == "__main__":
    import json

    print(json.dumps(VersionManifestV1.model_json_schema(), indent=4))
