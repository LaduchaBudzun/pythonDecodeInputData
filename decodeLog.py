import web3
from web3._utils.events import get_event_data
from eth_utils import event_abi_to_log_topic, to_hex
from web3.auto import w3
from functools import lru_cache
import json
import traceback
from hexbytes import HexBytes

@lru_cache(maxsize=None)
def _get_topic2abi(abi):
  if isinstance(abi, (str)):
    abi = json.loads(abi)

  event_abi = [a for a in abi if a['type'] == 'event']
  topic2abi = {event_abi_to_log_topic(_): _ for _ in event_abi}
  return topic2abi

@lru_cache(maxsize=None)
def _get_hex_topic(t):
  hex_t = HexBytes(t)
  return hex_t

def convert_to_hex(arg, target_schema):
    """
    utility function to convert byte codes into human readable and json serializable data structures
    """
    output = dict()
    for k in arg:
      if isinstance(arg[k], (bytes, bytearray)):
        output[k] = to_hex(arg[k])
      elif isinstance(arg[k], (list)) and len(arg[k]) > 0:
        target = [a for a in target_schema if 'name' in a and a['name'] == k][0]
        if target['type'] == 'tuple[]':
          target_field = target['components']
          output[k] = decode_list_tuple(arg[k], target_field)
        else:
          output[k] = decode_list(arg[k])
      elif isinstance(arg[k], (tuple)):
        target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == k][0]
        output[k] = decode_tuple(arg[k], target_field)
      else:
        output[k] = arg[k]
    return output


def decode_log(data, topics, abi):
  if abi is not None:
    try:
      topic2abi = _get_topic2abi(abi)
      
      log = {
        'address': None, #Web3.toChecksumAddress(address),
        'blockHash': None, #HexBytes(blockHash),
        'blockNumber': None,
        'data': data, 
        'logIndex': None,
        'topics': [_get_hex_topic(_) for _ in topics],
        'transactionHash': None, #HexBytes(transactionHash),
        'transactionIndex': None
      }
      event_abi = topic2abi[log['topics'][0]]
      evt_name = event_abi['name']

      data = get_event_data(w3.codec, event_abi, log)['args']
      target_schema = event_abi['inputs']
      decoded_data = convert_to_hex(data, target_schema)
      
    
      return (evt_name, json.dumps(decoded_data), json.dumps(target_schema))
    except Exception as e: 
        print(e)
        return ('decode error', traceback.format_exc(), None)
    
  else:
    return ('no matching abi', None, None)
  
pair_abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
output = decode_log(
    '0x000000000000000000000000000000000000000000000000000000009502f90000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000093f8f932b016b1c',
    [
    '0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822',
    '0x0000000000000000000000007a250d5630b4cf539739df2c5dacb4c659f2488d',
    '0x000000000000000000000000242301fa62f0de9e3842a5fb4c0cdca67e3a2fab'],
    pair_abi
)

# pair_abi = '[{"inputs": [{"components": [{"internaltype": "address","name": "considerationtoken","type": "address"},{"internaltype": "uint256","name": "considerationidentifier","type": "uint256"},{"internaltype": "uint256","name": "considerationamount","type": "uint256"},{"internaltype": "address payable","name": "offerer","type": "address"},{"internaltype": "address","name": "zone","type": "address"},{"internaltype": "address","name": "offertoken","type": "address"},{ "internaltype": "uint256", "name": "offeridentifier", "type": "uint256" }, { "internaltype": "uint256", "name": "offeramount", "type": "uint256" }, { "internaltype": "enum basicordertype", "name": "basicordertype", "type": "uint8" }, { "internaltype": "uint256", "name": "starttime", "type": "uint256" }, { "internaltype": "uint256", "name": "endtime", "type": "uint256" }, { "internaltype": "bytes32", "name": "zonehash", "type": "bytes32" }, { "internaltype": "uint256", "name": "salt", "type": "uint256" }, { "internaltype": "bytes32", "name": "offererconduitkey", "type": "bytes32" }, { "internaltype": "bytes32", "name": "fulfillerconduitkey", "type": "bytes32" }, { "internaltype": "uint256", "name": "totaloriginaladditionalrecipients", "type": "uint256" }, { "components": [ { "internaltype": "uint256", "name": "amount", "type": "uint256" }, { "internaltype": "address payable", "name": "recipient", "type": "address" } ], "internaltype": "struct additionalrecipient[]", "name": "additionalrecipients", "type": "tuple[]" }, { "internaltype": "bytes", "name": "signature", "type": "bytes" } ], "internaltype": "struct basicorderparameters", "name": "parameters", "type": "tuple" } ], "name": "fulfillbasicorder", "outputs": [ { "internaltype": "bool", "name": "fulfilled", "type": "bool" } ], "statemutability": "payable", "type": "function" }]'
# output = decode_log(
#     '0xfb0f3ee1000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000084514e51f33980000000000000000000000000007773c7922aaddc76ee9b5561cbe7df55c3bbd79000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00000000000000000000000000a0e8a9941d1e1bc2ed25f138be6b0b51c059b2980000000000000000000000000000000000000000000000000000000000000490000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000063fa85e80000000000000000000000000000000000000000000000000000000063fa93f80000000000000000000000000000000000000000000000000000000000000000360c6ebe0000000000000000000000000000000000000000232f4ca800b0b6aa0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f00000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000002a00000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000aa37b5cc7a800000000000000000000000000295990ac057a3a4b786102a3b61c84eff764c0330000000000000000000000000000000000000000000000000000000000000041979017194416b7d910d9e5dc506f55795f3728490fa366177eadce54244bf77402557547139ee8ebb3939dbd2a8c77bc689c604247660ac6e45afa9b5d622a831b0000000000000000000000000000000000000000000000000000000000000000000000360c6ebe',
#     [
#     '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31',
#     '0x00000000000000000000000007773c7922aaddc76ee9b5561cbe7df55c3bbd79',
#     '0x000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00'],
#     pair_abi
# )

print('event emitted: ', output[0])
print('arguments: ', json.dumps(json.loads(output[1]), indent=2))