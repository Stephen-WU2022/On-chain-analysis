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

####  _Erc20_Tx_

This module is for download Etherscan transaction details and method, including timestamp, from, to, value, hash, method.


```python
from onchain_analysis import Erc20_Tx

transaction = Erc20_Tx(etherscan_api_key = YOUR_API_KEY, 
                                        chromedriver_absolute_path = YOUR_DRIVER_PATH)

tx_details = transaction.get_erc20_transfer_by_address(contract_address = TOKEN_CONTRACT_ACCOUNT, 
                                                       address = EOA)

tx_method = transaction.tx_method(contract_address = TOKEN_CONTRACT_ACCOUNT,  
                                                     address = EOA)
```

The outcome would be two list contained the data.


####  _Tx_analysis_

This module is for analysis transaction receipt from _Erc20_Tx_, function including identifing the flow of token, filter of method value (transaction number) in-out flow, also provide some visualize tools.


Suppose a entity have mutiple addresses, and want to analyze this entity to a ERC20 token.
1. Get all address data from _Erc20_Tx_ and combine together
2. Transfer to Dataframe format

```python
from onchain_analysis import Tx_analysis

print(df)
```

| timestamp  | from | to  | value | hash | method |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 1555963003    | 0x29de....  | 0x05e7...   | 1     | 0x...    | Transfer     |
| 1555963861    | 0x29de....  | 0x05e7...   | 59999 | 0x...    | Transfer     |
| 1573245075    | 0x05e7....  | 0x9ef0...   | 1     | 0x...    | Lock     |


```python

all_methods = Tx_analysis.get_all_method(df)
```
This function wuold return all the method df contained
# 
```python

df = Tx_analysis.inflow_outflow(tx_receipts=df,clusters1_addresses= Entity1_addresses_list, clusters2_addresses: Entity2_addresses_list)
```
clusters1_addresses for the entity mutiple addresses 

clusters2_addresses for the second entity that want to specify the token flow in_out. (e.g Exchange)

Fundtion wuold add a new column _inflow_outflow_ in df with five different value. 
* _internal_Tx_: Transaction inside the entity 1 

* _inflow_: Token inflow to entity 1 

* _outflow_: Token outflow from entity 1 

* _inflow_from_clusters2_: Token inflow to entity 1 from entity 2 

* _outflow_to_clusters2_: Token outflow from entity 1 to entity 2 


| timestamp  | from | to  | value | hash | method | inflow_outflow |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 1555963003    | 0x29de....  | 0x05e7...   | 1     | 0x...    | Transfer | internal_Tx  |
| 1555963861    | 0x29de....  | 0x05e7...   | 59999 | 0x...    | Transfer | internal_Tx  |   
| 1573245075    | 0x05e7....  | 0x9ef0...   | 1     | 0x...    | Lock     | outflow    |  
# 
```python

df = Tx_analysis.methods_filter(df,'Lock','Transfer')
df = Tx_analysis.in_outflow_filter(df,outflow=True)
df = Tx_analysis.value_filter(df,min = 2)
```
Those three filter function are for specified some transaction. 
* _methods_filter_ 

| timestamp  | from | to  | value | hash | method | inflow_outflow |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 1555963003    | 0x29de....  | 0x05e7...   | 1     | 0x...    | Transfer | internal_Tx  |
| 1555963861    | 0x29de....  | 0x05e7...   | 59999 | 0x...    | Transfer | internal_Tx  |   
| 1573245075    | 0x05e7....  | 0x9ef0...   | 1     | 0x...    | Lock     | outflow    |  

* _in_outflow_filter_

| timestamp  | from | to  | value | hash | method | inflow_outflow |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 1573245075    | 0x05e7....  | 0x9ef0...   | 1     | 0x...    | Lock     | outflow    |  

* _value_filter_

| timestamp  | from | to  | value | hash | method | inflow_outflow |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 1555963861    | 0x29de....  | 0x05e7...   | 59999 | 0x...    | Transfer | internal_Tx  |   
# 
```python

plt.figure(figsize=(20, 10))
Tx_analysis.methods_bar_chart(df,label="Entity_name")
plt.grid()
plt.show()
```
_methods_bar_chart_ is for drawing a bar chart base on Matplotlib. 

Function accept the assigned color but need to match method type number and in Matplotlib support way




















