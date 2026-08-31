from hermes.core.errors import ConfigError


class HermesConfig:

    def __init__(self) -> None:
        self._api_keys: dict[str, str] = {}
        self._settings: dict[str, str] = {}

    def set_api_key(self, source: str, key: str) -> None:
        ...

    def get_api_key(self, source: str) -> str | None:
        ...

    def set(self, key: str, value: str) -> None:
        ...

    def get(self, key: str, default: str | None = None) -> str | None:
        ...

    def require_api_key(self, source: str) -> str:
        ...

    def resolve_config(self, source: str) -> dict[str, str]:
        ...


_config: HermesConfig | None = None


def configure(api_keys: dict[str, str] | None = None, **settings: str) -> HermesConfig:
    ...


def get_config() -> HermesConfig:
    ...
