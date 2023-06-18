from abc import ABC, abstractmethod
from web3 import Web3
import logging

logging.basicConfig(level=logging.INFO)

class LendingProtocol(ABC):
    w3: Web3

    @abstractmethod
    def get_health_ratio(self, wallet: str) -> float:
        raise NotImplementedError()


class CompoundV3Lending(LendingProtocol):
    def get_health_ratio(self, wallet: str) -> float:
        logging.info(f'Collect health ratio for wallet: {wallet}')
        return 0.5