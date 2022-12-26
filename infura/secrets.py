from dataclasses import dataclass
import getpass  # _NOT_ available on WASM!!!

import keyring


@dataclass
class HiddenString:
    value: str | None = None

    def filled(self) -> bool:
        return self.value is not None


def keyring_get_secret_with_install(
    service: str,
    secret: HiddenString,
    user: str | None = None,
) -> None:
    if not user:
        user = getpass.getuser()
    assert "user", "Failed to get current user from the OS"

    def get_try():
        secret.value = keyring.get_password(service, user)
        assert secret.filled()

    try:
        get_try()
        return
    except AssertionError:
        pass

    keyring.set_password(
        service, user, input(f"Please provide the secret for {user=} {service=}")
    )

    get_try()


class Secrets:
    infura_keyring_service = "infura_eth_api_key"
    infura_eth_api_key = HiddenString()

    eth_address_service = "eth_account"
    eth_address = HiddenString()

    infura_http_endpoint_template = "https://mainnet.infura.io/v3/{}"
    infura_ws_endpoint_template = "wss://mainnet.infura.io/ws/v3/{}"

    def eth(self):
        return self.eth_address.value

    def infura_http(self):
        return self.infura_http_endpoint_template.format(self.infura_eth_api_key.value)

    def infura_ws(self):
        return self.infura_ws_endpoint_template.format(self.infura_eth_api_key.value)
