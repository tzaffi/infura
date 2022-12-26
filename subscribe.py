import asyncio

from infura.query import Q
from infura.secrets import Secrets, keyring_get_secret_with_install

secrets = Secrets()
keyring_get_secret_with_install(
    secrets.infura_keyring_service, secrets.infura_eth_api_key
)
keyring_get_secret_with_install(secrets.eth_address_service, secrets.eth_address)

print(secrets.infura_ws())

q = Q(secrets)

q.subscribe_full_block_header()
q.subscribe_gas()
q.subscribe_address()

if __name__ == "__main__":
    asyncio.run(q.report_forever())
