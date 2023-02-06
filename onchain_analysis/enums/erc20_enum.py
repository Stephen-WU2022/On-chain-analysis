from dataclasses import dataclass


@dataclass(frozen=True)
class Erc20tx_enum:
    base :str = 'https://api.etherscan.io/api'
    action : str = "&action="
    blockno: str = "&blockno="
    page: str = "&page="
    offset: str = "&offset="
    star_block: str = "&startblock="
    end_block: str = "&endblock="
    sort: str = "&sort="
    module: str = "?module="
    timestamp: str = "&timestamp="
    closest: str = "&closest="
    address : str = "&address="
    api_key: str = "&apikey="
    contract_address: str = "&contractaddress="
