# ETH Web3, Sockets, and Secure Secrets using `keyring`

Experimenting with Infura + Keyring

* Raw websocket subscriptions
* Primitive event handling
* Storing secrets in OS's secure enclave using `keyring`
    * See `gpt.ipynb` for example of how to prep the keyring
* Tracking a specific ETH address
* Printing out the history of an ETH address

## `keyring` example:

See `gpt.ipynb` (named as an homage to chat GPT which offered some useful suggestions)
## Websocket Example

```sh
❯ python subscribe.py

wss://mainnet.infura.io/ws/v3/<<<API KEY>>>
sub.response={'jsonrpc': '2.0', 'id': 1, 'result': '0x41001037aecdee9751d745d55663d3391a66dac17fcc'}
sub.response={'jsonrpc': '2.0', 'id': 2, 'result': '0x41001037aecdf4e681cb4cc864b99a0b0edd4d62e906'}
sub.response={'jsonrpc': '2.0', 'id': 3, 'result': '0x41001037aecde63f4e4ea03cc99927ad3840fcd0c482'}

<<<<FULL HEADER round=16271166>>>>
{'number': '0xf8473e', 'hash': '0xa00411719ab2e80d59afad38b85459237e6a549dffcf05975920354939a1cef0', 'parentHash': '0x91c229bd5bd299c6a2409f56dc82d0df2f0c48675a5aa88f0d8cdc9e16011bd9', 'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347', 'logsBloom': '0x052c2c8cc9f0d045801f4da7a9258a703134c651a000a304da50a3b8cf2138605b860eb010ce441570c1a89852ef1fd742107e2c2fa1a4e4270d5ded906ee32642086850e83254d968596ebc535780e6c43382064b6ea7425101cb62aac8f0265ee05961bafff4374079808140072eb90b88e8c40091058123c040f5785c54247fcf8002e2824dec24aa9b014320c898a0f8848b97120d2e8c9b15e82b1a442cab1e658f571171b262e2e9f24759ae024250614f2c26a2a230f1865b62094848d5082c63854869f898a22154929f2633451102cc9ac9a419520cbd661114e0841c1cffe9516a7a44052c158e6035ecbe803a1483846e816273e00c404801401e', 'transactionsRoot': '0xb3c48ab2a611582759b544d7b3742b7c5785ac21ed7a4df5d982313ab9ed1951', 'stateRoot': '0xeac4e6ef9b44dff1fa27fb36186a81e7f484452473aa4ff74bd4dcb478afb2c5', 'receiptsRoot': '0x1cd19894b886d6900cfb843b5d407f35ceeed87aa91cfaef34cbece4fdb9031d', 'miner': '0xdafea492d9c6733ae3d56b7ed1adb60692c98bc5', 'difficulty': '0x0', 'extraData': '0x496c6c756d696e61746520446d6f63726174697a6520447374726962757465', 'gasLimit': '0x1c9c380', 'gasUsed': '0xd5edb1', 'timestamp': '0x63a9fcd3', 'baseFeePerGas': '0x267a0f522', 'nonce': '0x0000000000000000', 'mixHash': '0xef4b0369de9c059a0943e7bd28c46e10620610ae4579e0a6dd94df6697b041be'}
subid='0x41001037aecdee9751d745d55663d3391a66dac17fcc', sub=<infura.query.Subscription object at 0x10b592f50>

<<<<GAS USAGE round=16271166>>>>
gasUsed = 14020017
subid='0x41001037aecdf4e681cb4cc864b99a0b0edd4d62e906', sub=<infura.query.Subscription object at 0x10b592fb0>

<<<<BALANCE of  round=16271166>>>>
balance=Decimal(<<<SOME AMOUNT>>>)
subid='0x41001037aecde63f4e4ea03cc99927ad3840fcd0c482', sub=<infura.query.Subscription object at 0x10b593070>

<<<<GAS USAGE round=16271167>>>>
gasUsed = 16382745
subid='0x41001037aecdf4e681cb4cc864b99a0b0edd4d62e906', sub=<infura.query.Subscription object at 0x10b592fb0>

<<<<BALANCE of  round=16271167>>>>
...



```