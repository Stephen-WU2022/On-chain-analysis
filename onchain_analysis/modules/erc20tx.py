import json
import requests
import selenium
import time
from onchain_analysis.modules import tools
from onchain_analysis import configs
from importlib import resources
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from enums.erc20_enum import Erc20tx_enum as erc20_enum


class Erc20_Tx:


    def __init__(self, etherscan_api_key: Optional[str] = None,
                 chromedriver_absolute_path: Optional[str] = None
    ):
        """Erc20  transcation  constructor
        :param etherscan_api_key: Api Key
        :param chromedriver_absolute_path: chrome driver absolute path for selenium
        """
        self.api_key = etherscan_api_key
        self.driver_path = chromedriver_absolute_path
        self.erc20_config = self._load_config()


    @staticmethod
    def _get_config_path():
        with resources.path(configs, "Erc20_tx.json") as path:
            config_path = str(path)
        return config_path


    @staticmethod
    def _load_config() -> dict:
        with open(Erc20_Tx._get_config_path(), "r") as f:
            return json.load(f)


    @staticmethod
    def _tx_method_url(contract_address: str, address: str) -> str:
        return Erc20_Tx._load_config()["transaction_method"]["URL"].format(contract_address, address)


    def __selnium_option(self):
        arguments = self.erc20_config["transaction_method"]
        chrome_options = Options()
        for i in arguments["chrome_options"]:
            chrome_options.add_argument(i)
        chrome_options.add_argument("user-agent={}".format(arguments['User_Agent']))
        return  chrome_options


    def tx_method(self,
                  contract_address: str,
                  address: str,
                  chromedriver_absolute_path: Optional[str] = None) -> list:
        """

        :param contract_address: Erc20 token's contract address
        :param address: ethereum normal address
        :param chromedriver_absolute_path: chrome driver absolute path for selenium
        :return: list contain transaction hash & method
        """

        if not self.driver_path  and not chromedriver_absolute_path :
            raise Exception("Require chrome driver absolute path for Selenium")
        return self.__run_method(driver_path= list(filter(None,[self.driver_path, chromedriver_absolute_path]))[0],
                          url = Erc20_Tx._tx_method_url(contract_address, address))


    def __run_method(self, driver_path: str, url: str):
        driver = webdriver.Chrome(service=Service(driver_path), options=self.__selnium_option())
        driver.get(url)
        self.__locate_iframe(driver)
        self.page_nums = self.__page_nums(driver)
        return   self.__get_method(limit = self.page_nums, driver = driver)


    def __locate_iframe(self, driver: selenium.webdriver.chrome.webdriver.WebDriver):
        driver.switch_to.frame(self.erc20_config["transaction_method"]["iframe_id"])


    def __page_nums(self, driver: selenium.webdriver.chrome.webdriver.WebDriver):
        return float(driver.find_elements(By.XPATH, self.erc20_config["transaction_method"]["page_number_XPATH"])[0].text[-1])


    def __get_table(self, driver: selenium.webdriver.chrome.webdriver.WebDriver):
        table = driver.find_element(By.XPATH, self.erc20_config["transaction_method"]["table_XPATH"]).text.split("\n")
        return [table[i*7:i*7+2] for i in range(int(len(table)/7))]


    def __next_page(self, driver: selenium.webdriver.chrome.webdriver.WebDriver):
        driver.find_element(By.XPATH, self.erc20_config["transaction_method"]["next_page_XPATH"]).click()
        time.sleep(self.erc20_config['transaction_method']['web_rendering_time'])

    @tools.Tools.counter
    def __get_method(self, **kwargs) -> list :
        page = kwargs["num_of_times"]
        last_page = kwargs['limit']
        if page + 1 < last_page:
            table = self.__get_table(kwargs['driver'])
            self.__next_page(kwargs['driver'])
            return table
        elif page + 1 == last_page:
            return self.__get_table(kwargs['driver'])
        else:
            pass


    def get_erc20_transfer_by_address(self,
                                      contract_address: str,
                                      address: str,
                                      start_datetime: Optional[str] = None,
                                      end_datetime: Optional[str] = None,
                                      etherscan_api_key: Optional[str] = None):
        """

        :param contract_address: Erc20 token's contract address
        :param address:  ethereum normal address
        :param start_datetime: "%Y-%m-%d %H:%M:%S", note UTC+00:00 (ex. 2020-01-01 00:00:00)
        :param end_datetime: "%Y-%m-%d %H:%M:%S", note UTC+00:00 (ex. 2020-01-01 00:00:00)
        :param etherscan_api_key: Your Etherscan API KEY
        :return: list contain 'ERC20 - Token Transfer Events' by Address include (timeStamp, from, to, value, hash)
        """
        if not self.api_key  and not etherscan_api_key:
            raise Exception("API KEY must be specified")
        api_key = list(filter(None,[self.api_key, etherscan_api_key]))[0]
        if not contract_address and not address:
            raise Exception("Contract address & address must be specified")
        start_block = "0" if not start_datetime else self.__datetime_to_blockno(start_datetime)
        end_block = "27025780" if not end_datetime else self.__datetime_to_blockno(end_datetime)
        return self.__restructure(self.__run_transfer(contract_address, address, api_key, start_block, end_block))


    def __datetime_to_blockno(self, datetime: str, api_key: str) -> str :
        timestamp = tools.Tools.datetime_to_timestamp(datetime)
        return requests.get(url = str(self.timestamp_to_blockno_url().format(timestamp, api_key))).json()['result']


    def __timestamp_to_blockno_url(self):
        api_config = self.erc20_config["etherscan_api"]
        return (
            f"{erc20_enum.base}"
            f"{erc20_enum.module}"
            f"{api_config['module']['block']}"
            f"{erc20_enum.action}"
            f"{api_config['action']['getblocknobytime']}"
            f"{erc20_enum.timestamp}"
            "{}"
            f"{erc20_enum.closest}"
            f"{api_config['closest']}"
            f"{erc20_enum.api_key}"
            "{}"
        )


    def __erc20_transfer_byaddress_url(self):
        api_config = self.erc20_config["etherscan_api"]
        return (
            f"{erc20_enum.base}"
            f"{erc20_enum.module}"
            f"{api_config['module']['account']}"
            f"{erc20_enum.action}"
            f"{api_config['action']['tokentx']}"
            f"{erc20_enum.contract_address}"
            "{}"
            f"{erc20_enum.address}"
            "{}"
            f"{erc20_enum.offset}"
            f"{api_config['offset']}"
            f"{erc20_enum.star_block}"
            "{}"
            f"{erc20_enum.end_block}"
            "{}"
            f"{erc20_enum.sort}"
            f"{api_config['sort']}"
            f"{erc20_enum.api_key}"
            "{}"
            f"{erc20_enum.page}"
            "{}"
        )


    def __run_transfer(self,
                       contract_address: str,
                       address: str,
                       etherscan_api_key: str,
                       start_block: str,
                       end_block: str
                       ):
        result = []
        page = 1
        while True:
            URL = self.__erc20_transfer_byaddress_url().format(contract_address,
                                                               address,
                                                               start_block,
                                                               end_block,
                                                               etherscan_api_key,
                                                               page)
            r = requests.get(url=URL).json()['result']
            if len(r) > 10000:
                page += 1
                result.extend(r)
            else:
                result.extend(r)
                break
        return result


    def __restructure(self, data: list):
        result = [["timeStamp", "from", "to", "value", "hash"]]
        result.extend([[i["timeStamp"], i["from"], i["to"], i["value"], i["hash"]] for i in data])
        return result




























