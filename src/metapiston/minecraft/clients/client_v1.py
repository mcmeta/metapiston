from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import requests
from metapiston.minecraft._model import LauncherModel
from pydantic import AnyUrl, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    IncEx: TypeAlias = set[int] | set[str] | dict[int, Any] | dict[str, Any] | None


class ClientV1(BaseModel):
    """Python model of the file that accompanies client.jar in .minecraft/versions/<version> and lists the version's attributes.

    When using the latest version of the Minecraft launcher, it is named <game version>.json.

    Keys:
        arguments: Command line arguments passed to the game client and JVM.
        asset_index: Details about the client's assets file.
        assets: The assets version.
        compliance_level: Its value is 1 for all recent versions of the game (1.16.4 and above) or 0 for all others.
            If 0, the launcher warns the user about this version not being recent enough to support the latest player safety features.
        downloads: Details about the version's client, server, and obfuscation maps.
        id: The name of this version client.
        java_version: The version of the Java Runtime Environment.
        libraries: A list of libraries.
        logging: Information about Log4j log configuration.
        main_class: The main game class.
            For modern versions, it is `net.minecraft.client.main.Main`, but it may differ for older or ancient versions.
        minimum_launcher_version: The minimum Launcher version that can run this version of the game.
        release_time: The release time of this version in ISO 8601 format.
        time: A timestamp in ISO 8601 format of when this version's files were last updated.
        type: The type of this game version.
            It is shown in the version list when you create a new installation. The default values are "release" and "snapshot".
    """

    @staticmethod
    def download(url: str | bytes | AnyUrl) -> ClientV1:
        if not isinstance(url, (str, bytes)):
            url = url.unicode_string()
        return ClientV1.model_validate_json(requests.get(url).content)

    def model_dump_json(
        self,
        *,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super().model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )

    model_config = ConfigDict(
        title="MinecraftClientV1",
        extra="forbid",
        frozen=True,
        alias_generator=to_camel,
    )

    arguments: Optional[Arguments] = None
    asset_index: AssetIndex
    assets: str
    compliance_level: int
    downloads: Downloads
    id: str
    java_version: JavaVersion
    libraries: list[Library]
    logging: Optional[Logging]
    main_class: str
    minecraft_arguments: Optional[str] = None
    minimum_launcher_version: int
    release_time: str
    time: str
    type: str

    class Arguments(LauncherModel):
        """Command line arguments passed to the game client and JVM.

        Keys:
            game: Contains arguments supplied to the game, such as information about the username and the version.
            jvm: Contains JVM arguments, such as information about memory allocation, garbage collector selection, or environmental variables.
        """

        game: list[str | ConditionalGameArgument]
        jvm: list[str | ConditionalJVMArgument]

        class ConditionalGameArgument(LauncherModel):
            """A conditional command line argument for the game client.

            Keys:
                rules: A list of rules.
                value: An argument or a list of arguments that is added when the condition is matched..
            """

            rules: list[Rule]
            value: str | list[str]

            class Rule(LauncherModel):
                """A rule.

                Keys:
                    action: What to do if the features are true.
                    features: Includes a set of features that can be checked.
                """

                action: str
                features: dict[str, bool]

        class ConditionalJVMArgument(LauncherModel):
            """A conditional command line argument for the JVM.

            Keys:
                rules: A list of rules.
                value: An argument or a list of arguments that is added when the condition is matched..
            """

            rules: list[Rule]
            value: str | list[str]

            class Rule(LauncherModel):
                """A rule.

                Keys:
                    action: What to do if the os matches.
                    os: Contains a name, version, or arch to check.
                """

                action: str
                os: OS

                class OS(LauncherModel):
                    """OS flags to check.

                    Keys:
                        name: Name of the OS (e.g. "osx" or "windows").
                        version: An OS version to match (e.g. "^10\\.").
                        arch: The OS architecture (e.g. "x86").
                    """

                    name: Optional[str] = None
                    version: Optional[str] = None
                    arch: Optional[str] = None

    class AssetIndex(LauncherModel):
        """Details about the client's assets file.

        Keys:
            id: The assets version.
            sha1: The SHA1 of the assets file.
            size: The size of the version.
            total_size: The total size of the version.
            url: The URL that the game should visit to download the assets.
        """

        id: str
        sha1: str
        size: int
        total_size: int
        url: AnyUrl

    class Downloads(BaseModel):
        """Details about the version's client, server, and obfuscation maps.

        Keys:
            client: The client.jar download information.
            client_mappings: The obfuscation maps for this client version.
                Added in Java Edition 19w36a but got included in 1.14.4 also. Repeats the structure of the client download information.
            server: The server download information.
                Repeats the structure of the client download information.
            server_mappings: The obfuscation maps for this server version.
                Added in Java Edition 19w36a but got included in 1.14.4 also. Repeats the structure of the client download information.
        """

        model_config = ConfigDict(extra="forbid", frozen=True)

        client: Download
        client_mappings: Optional[Download] = None
        server: Download
        server_mappings: Optional[Download] = None
        windows_server: Optional[Download] = None

        class Download(LauncherModel):
            """File download details.

            Keys:
                sha1: The SHA1 of the jar.
                size: The size of jar in bytes.
                url: The URL where the jar is hosted.
            """

            sha1: str
            size: int
            url: AnyUrl

    class JavaVersion(LauncherModel):
        """The version of the Java Runtime Environment

        Keys:
            component: Its value for all 1.17 snapshots is "jre-legacy" until 21w18a and "java-runtime-alpha" since 21w19a.
            major_version: Its value for all 1.17 snapshots is 8 until 21w18a and 16 since 21w19a.
        """

        component: str
        major_version: int

    class Library(LauncherModel):
        """A library.

        Keys:
            downloads: The library's download information.
            name: A maven name for the library, in the form of "groupId:artifactId:version".
            url: The URL of the Maven repository (used by Forge).
            natives: Information about native libraries (in C) bundled with this library. Appears only when there are classifiers for natives.
                This tag's name depends on the natives that appear in the classifiers, so it can be "linux", "macos", "windows", or "osx".
                Its value is the corresponding classifier ("natives-linux" etc.).
            extract: Rules for library extraction.
            rules: A list of rules.
        """

        downloads: Downloads
        name: str
        url: Optional[AnyUrl] = None
        natives: Optional[dict[str, str]] = None
        extract: Optional[Extract] = None
        rules: Optional[list[Rule]] = None

        class Downloads(LauncherModel):
            """The library's download information.

            Args:
                artifact: Information about the artifact.
                classifiers: Specifies artifact information for the artifact with the corresponding classifier.
            """

            artifact: Optional[Artifact] = None
            classifiers: Optional[dict[str, Artifact]] = None

            class Artifact(LauncherModel):
                """Information about the artifact.

                Args:
                    path: Path to store the downloaded artifact, relative to the "libraries" directory in .minecraft.
                    sha1: The SHA1 of the file.
                    size: The size of the file.
                    url: The URL that the game should visit to download the file.
                """

                path: str
                sha1: str
                size: int
                url: str

        class Extract(LauncherModel):
            """Rules for library extraction.

            Keys:
                exclude: Shows what to exclude from the extraction.
            """

            exclude: list[str]

        class Rule(LauncherModel):
            """A rule.

            Keys:
                action: What to do if the os matches.
                os: Contains a name, version, or arch to check.
            """

            action: str
            os: Optional[OS] = None

            class OS(LauncherModel):
                """OS flags to check.

                Keys:
                    name: Name of the OS (e.g. "osx" or "windows").
                    version: An OS version to match (e.g. "^10\\.").
                    arch: The OS architecture (e.g. "x86").
                """

                name: Optional[str] = None
                version: Optional[str] = None
                arch: Optional[str] = None

    class Logging(LauncherModel):
        """Information about Log4j log configuration.

        Args:
            client: The logging client.
        """

        client: Client

        class Client(LauncherModel):
            """The logging client.

            Args:
                argument: The JVM argument for adding the log configuration (e.g. "-Dlog4j.configurationFile=${path}").
                file: The Log4j2 XML configuration used by this version for the launcher for launcher's log screen.
                type: The logging client type (e.g. "log4j2-xml").
            """

            argument: str
            file: File
            type: str

            class File(LauncherModel):
                """The Log4j2 XML configuration used by this version for the launcher for launcher's log screen.

                Args:
                    id: The logging client id. Typically "client-1.12.xml", but may differ for older versions.
                    sha1: The SHA1 for this file.
                    size: The size of the file.
                    url: The URL the game should visit to download the log configuration.
                """

                id: str
                sha1: str
                size: int
                url: str
