from __future__ import annotations

from pydantic import AnyHttpUrl
from pydantic_core import Url


def package_url(hash: str, file: str, api_version: int = 1) -> AnyHttpUrl:
    return Url(f"https://piston-meta.mojang.com/v{api_version}/packages/{hash}/{file}")


def resource_url(hash: str) -> AnyHttpUrl:
    return Url(f"https://resources.download.minecraft.net/{hash[:2]}/{hash}")


def version_manifest_url(file_version: int = 2) -> AnyHttpUrl:
    version = "" if file_version == 1 else f"_v{file_version}"
    return Url(f"https://piston-meta.mojang.com/mc/game/version_manifest{version}.json")
