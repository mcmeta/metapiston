from __future__ import annotations

import json
from unittest import TestCase

import requests
from metapiston.minecraft import ClientV1
from metapiston.minecraft.urls import resource_url


class TestClient(TestCase):
    def test_download_client_v1_mc_1_20_2(self) -> None:
        client = ClientV1.download(
            "https://piston-meta.mojang.com/v1/packages/9ead053b2dea80522c19f1f0e2dcb437d3392d7f/1.20.2.json"
        )
        self.assertEqual(
            client.assets,
            client.asset_index.id,
        )

        with open("downloads/1.20.2.json", "w") as file:
            file.write(client.model_dump_json(by_alias=True, indent=4))

    def test_download_client_v1_mc_1_13(self) -> None:
        client = ClientV1.download(
            "https://piston-meta.mojang.com/v1/packages/c24c2fd37c8ca2e1c18721e2c77caf4d24c87f92/1.13.json"
        )
        self.assertEqual(
            client.assets,
            client.asset_index.id,
        )

        with open("downloads/1.13.json", "w") as file:
            file.write(client.model_dump_json(by_alias=True, indent=4))

    def test_download_client_v1_mc_1_8(self) -> None:
        client = ClientV1.download(
            "https://piston-meta.mojang.com/v1/packages/9eb165eef46294062d8698c8a78e8ac914949e7a/1.8.json"
        )
        self.assertEqual(
            client.assets,
            client.asset_index.id,
        )

        with open("downloads/1.8.json", "w") as file:
            file.write(client.model_dump_json(by_alias=True, indent=4))

    def test_mcmeta(self) -> None:
        mcmeta = requests.get(str(resource_url("a4b8e10ef85fede15e62686724205f18cd819c77")))
        with open("downloads/pack.mcmeta", "wb") as file:
            file.write(mcmeta.content)

    def test_jar(self) -> None:
        jar = requests.get(
            "https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar"
        )
        with open("downloads/server.jar", "wb") as file:
            file.write(jar.content)

    def test_dump_schema(self) -> None:
        with open("downloads/schema.json", "w") as file:
            json.dump(ClientV1.model_json_schema(), file)
