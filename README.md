# On chain analysis 

This is a tool for on-chain data analysis. Get the data you want from blockchain and analyze.

For now supporting Ethereum.

## Feature

* Check erc20 token transaction details and method (lock, stake...) filtered by token contract account and EOA
* Analyze transaction receipt by identify the flow of token, mutiple filter for method value (transaction number) in-out flow, visualize tool

## Start

Before proceeding, you should register an account on Etherscan and generate API KEY, also install Selenium and Chrome driver for web scraping, Pandas, Numpy and Matplotlib for transaction analysis.

* Git clone


## Usage

####  _Erc20 transaction_

This module is for download Etherscan transaction details and method, including timestamp, from, to, value, hash, method.


```python
import onchain_analysis

transaction = onchain_analysis.Erc20_Tx(etherscan_api_key = YOUR_API_KEY, 
                                        chromedriver_absolute_path = YOUR_DRIVER_PATH)

tx_details = transaction.get_erc20_transfer_by_address(contract_address = TOKEN_CONTRACT_ACCOUNT, 
                                                       address = EOA)

tx_method = transaction.tx_method(contract_address = TOKEN_CONTRACT_ACCOUNT,  
                                                     address = EOA)
```

The outcome would be two list contained the data.


####  _Tx analysis_

This module is for analysis transaction receipt from _Erc20 transaction_, function including identifing the flow of token, filter of method value (transaction number) in-out flow, also provide some visualize tools.


Suppose you have the data from _Erc20 transaction_ and then transfer to Dataframe form

| timestamp  | from | to  | value | hash | method |
|:-------------:|:-------------:|:-------------:|:-------------:|
| left foo      | right foo     | left foo      | right foo     |
| left bar      | right bar     | left foo      | right foo     |
| left baz      | right baz     | left foo      | right foo     |
```python
import onchain_analysis


```

























