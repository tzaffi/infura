from decimal import Decimal
from itertools import count
import json
from typing import Any, Callable, cast

from eth_utils.currency import from_wei
from glom import glom
from web3 import Web3
from websockets import WebSocketCommonProtocol, connect

from infura.secrets import Secrets

ActionType = Callable[[Any], None]


class Subscription:
    _id_gen = count()

    def __init__(self, topic: str, action: ActionType):
        self.index: int = 1 + next(self._id_gen)
        self.topic: str = topic
        self.action: ActionType = action
        self.response: dict | None = None
        self.subid: str | None = None

    def asdict(self, omit_subid: bool = True) -> dict:
        d = {
            "id": self.index,
            "method": "eth_subscribe",
            "params": [self.topic],
        }
        if not omit_subid:
            d["subid"] = self.subid
        return d


class Q:
    def __init__(self, secrets: Secrets):
        self.secrets = secrets

        self.w3: Web3 = Web3(Web3.HTTPProvider(self.secrets.infura_http()))
        self.w3ws: Web3 = Web3(Web3.WebsocketProvider(self.secrets.infura_ws()))

        self.latest_round: int = -1

        self._balances: dict[str, Decimal] = {}

        # self.subscriptions = ["newHeads"]
        self._presubscribe: list[Subscription] = []
        self._ws: WebSocketCommonProtocol | None = None
        self.subscriptions: dict[str, Subscription] = {}
        self.debug: bool = True

    def latest_block_number(self) -> int:
        block = self.w3.eth.get_block(block_identifier="latest")
        return block.get("number", -1)

    def balance(
        self, *, address: str = "", round: str | int = "latest", verbose: bool = True
    ) -> Decimal:
        if not address:
            address = cast(str, self.secrets.eth())

        wei = self.w3.eth.get_balance(address, block_identifier=round)
        eth = from_wei(wei, "ether")

        if verbose:
            print(
                f"balance in ether of address={self.secrets.eth()} at block={round}: {eth}"
            )

        return cast(Decimal, eth)

    # websocket'ish
    def balance_ws(self):
        return self.w3ws.eth.get_balance(self.secrets.eth())

    # true websockets:
    def _add_subscription(self, topic: str, action: ActionType):
        self._presubscribe.append(Subscription(topic, action))

    def _header(self, title: str, resp: dict) -> str:
        return f"""
<<<<{title} round={int(glom(resp, "params.result.number"), base=16)}>>>>"""  # type: ignore

    def subscribe_full_block_header(self):
        def action(resp: dict) -> None:
            print(
                f"""{self._header("FULL HEADER", resp)}
{glom(resp, "params.result")}"""
            )

        self._add_subscription("newHeads", action)

    def subscribe_gas(self):
        def action(resp: dict) -> None:
            print(
                f"""{self._header("GAS USAGE", resp)}
gasUsed = {int(glom(resp, "params.result.gasUsed"), base=16)}"""  # type: ignore
            )

        self._add_subscription("newHeads", action)

    def subscribe_address(self, address: str = ""):
        def action(resp: dict) -> None:
            round = int(glom(resp, "params.result.number"), base=16)  # type: ignore
            balance = self.balance(address=address, round=round, verbose=False)

            prev_balance = self._balances.get(address, None)

            delta_msg = ""
            if prev_balance:
                delta = balance - prev_balance
                delta_msg = f"ETH delta since last round: {delta}"

            self._balances[address] = balance

            print(
                f"""{self._header(f"BALANCE of {address}", resp)}
{balance=}"""
            )
            if delta_msg:
                print(delta_msg)

        self._add_subscription("newHeads", action)

    async def _push_subscription(self, sub: Subscription):
        assert self._ws, "websocket.connect() must be called prior to _subscribe()"

        await self._ws.send(json.dumps(sub.asdict()))
        sub.response = json.loads(await self._ws.recv())
        sub.subid = sub.response["result"]
        self.subscriptions[sub.subid] = sub
        print(f"{sub.response=}")

    async def report_forever(self):
        async with connect(self.secrets.infura_ws()) as ws:
            self._ws = ws
            for sub in self._presubscribe:
                await self._push_subscription(sub)

            async for msg in ws:
                d = json.loads(msg)
                sub = self.subscriptions[(subid := d["params"]["subscription"])]
                sub.action(d)
                print(f"{subid=}, {sub=}")
