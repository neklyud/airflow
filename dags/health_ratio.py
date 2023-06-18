from hooks.web3 import Web3Hook
from web3 import Web3
from airflow import DAG, task
from datetime import datetime, timedelta
from lending.lending_protocol import LendingProtocol
import logging

logging.basicConfig(level=logging.INFO)

default_args = {
    'retries': 0,
    'catchup': False,
    'start_date': datetime(year=2023, month=6, day=18, hour=0),
    'owner': 'airflow',
}

def send_telegram_notify(message: str) -> None:
    logging.info(f'Message {message} was sended')

@task
def check_health_ratios() -> None:
   wallets = ["0x233D00f1201F9057Cc80981D6013247Df93A4E7F"]
   for wallet in wallets:
       logging.info(f'Check health ratio for wallet: {wallet}')

with DAG(
    'health_ratio_checks',
    default_args=default_args,
    description='Health ratio checker. It call blockchain and send notification if health ratio was exceeded.',
    schedule_interval=timedelta(days=1),
    tags=['health ratio', 'limits', 'risks'],
) as dag:
    pass
