from __future__ import annotations

from unittest import TestCase

from metapiston.minecraft import VersionManifestV1, VersionManifestV2
from metapiston.minecraft.urls import version_manifest_url


class TestManifest(TestCase):
    def test_download_manifest_v1(self) -> None:
        version_manifest = VersionManifestV1.download(version_manifest_url(1))
        self.assertEqual(
            version_manifest.latest.snapshot,
            version_manifest.versions[0].id,
        )

        with open("downloads/version_manifest_v1.json", "w") as file:
            file.write(version_manifest.model_dump_json(by_alias=True, indent=4))

    def test_download_manifest_v2(self) -> None:
        version_manifest = VersionManifestV2.download(version_manifest_url(2))

        self.assertEqual(
            version_manifest.latest.snapshot,
            version_manifest.versions[0].id,
        )

        with open("downloads/version_manifest_v2.json", "w") as file:
            file.write(version_manifest.model_dump_json(by_alias=True, indent=4))
