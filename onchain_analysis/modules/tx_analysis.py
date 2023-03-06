import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from typing import Optional




class Tx_analysis:


    def __init__(self):
        """Transaction assort constructor
        """


    @staticmethod
    def get_all_method(tx_receipts: pd.core.frame.DataFrame):
        return list(set(tx_receipts['method']))


    @staticmethod
    def inflow_outflow(tx_receipts: pd.core.frame.DataFrame,
                       clusters1_addresses: list,
                       clusters2_addresses: Optional[list] = []) -> pd.core.frame.DataFrame:
        """

        :param tx_receipts: data contain transaction receipts in Dataframe form
        :param clusters1_addresses: a bunch of the entity/whales's addresses
        :param clusters2_addresses: the specific clusters (ex. Exchange) interact with
        :return New column with value  'internal_Tx', 'inflow', 'outflow', 'inflow_from_clusters2', 'outflow_to_clusters2'
        """
        cd = [
            tx_receipts['to'].isin(clusters1_addresses) & tx_receipts['from'].isin(clusters1_addresses),
            tx_receipts['to'].isin(clusters1_addresses) & ~tx_receipts['from'].isin(clusters1_addresses),
            ~tx_receipts['to'].isin(clusters1_addresses) & tx_receipts['from'].isin(clusters1_addresses),
            tx_receipts['to'].isin(clusters1_addresses) & tx_receipts['from'].isin(clusters2_addresses),
            tx_receipts['to'].isin(clusters2_addresses) & tx_receipts['from'].isin(clusters1_addresses),
        ]
        value = [
            'internal_Tx',
            'inflow',
            'outflow',
            'inflow_from_clusters2',
            'outflow_to_clusters2'
        ]
        tx_receipts['inflow_outflow'] = np.select(cd, value)
        return tx_receipts


    @staticmethod
    def methods_filter(tx_receipts: pd.core.frame.DataFrame, *methods):
        """

        :param tx_receipts: data contain transaction receipts in Dataframe format
        :param methods: the methods set as filter
        :return: Transaction receipts specified by the methods
        """

        df = pd.DataFrame(columns=tx_receipts.columns)
        for method in methods:
            df = pd.concat([df, (tx_receipts.loc[tx_receipts['method'] == method])], ignore_index=True)
        return df


    @staticmethod
    def in_outflow_filter(tx_receipts: pd.core.frame.DataFrame,
                          inflow: Optional[bool] = False,
                          outflow: Optional[bool] = False,
                          internal_Tx: Optional[bool] = False,
                          inflow_from_clusters2: Optional[bool] = False,
                          outflow_to_clusters2: Optional[bool] = False):
        """

        :param tx_receipts: data contain transaction receipts in Dataframe form
        :param inflow: token flow set as filter, default as False
        :param outflow: token flow set as filter, default as False
        :param internal_Tx: token flow set as filter, default as False
        :param inflow_from_clusters2: token flow set as filter, default as False
        :param outflow_to_clusters2: token flow set as filter, default as False
        :return: Transaction receipts specified by the in_out flow
        """
        flows = {'inflow': inflow, 'outflow': outflow, 'internal_Tx': internal_Tx,
                 'inflow_from_clusters2': inflow_from_clusters2,
                 'outflow_to_clusters2': outflow_to_clusters2}
        df = pd.DataFrame(columns=tx_receipts.columns)
        for name, flow in flows.items():
            if flow:
                result = pd.concat([df, (tx_receipts.loc[tx_receipts['inflow_outflow'] == name])], ignore_index=True)
        return result


    @staticmethod
    def value_filter(tx_receipts: pd.core.frame.DataFrame, min: Optional[float] = 0, max: Optional[float] = None):
        """

        :param tx_receipts: data contain transaction receipts in Dataframe form
        :param min: minimum value, below this num would abandon
        :param max: max value, maxmum value, above this num would abandon
        :return: Transaction receipts specified by the value range
        """
        if max:
            assert max > min
            return tx_receipts.loc[tx_receipts['value'] > min & tx_receipts['value'] < max]
        else:
            return tx_receipts.loc[tx_receipts['value'] > min]

    ### Visualize, currently under development


    @staticmethod
    def methods_bar_chart(tx_receipts: pd.core.frame.DataFrame,label: str,
                          colors: Optional[list] = None,
                          width: Optional[float] = 8.64 * 10 ** 4):
        """

        :param label: The name of address entity
        :param colors: list with Color Format recognized by Matplotlib, require match methods number
        :param width: the bar's width, default 86400 for using timestamp as x-axis
        :return: bar chart
        """
        methods = Tx_analysis.get_all_method(tx_receipts)
        if colors:
            if len(colors) != len(methods):
                raise Exception("Color amount insufficient, require match methods amount")
        else:
            colors = cm.rainbow(np.linspace(0, 1, int(len(methods))))
        for color, method in zip(colors, methods):
            plt.bar(x=tx_receipts.loc[tx_receipts['method'] == method]['timestamp'],
                    height=tx_receipts.loc[tx_receipts['method'] == method]['value'],
                    width=8.64 * 10 ** 4, label=f"{label}-{method}", color = color)


    @staticmethod
    def colors_generater(num: int)->list:
        """
        :param num: number of color
        :return:  list contain rainbow colors
        """
        return cm.rainbow(np.linspace(0, 1, num))

