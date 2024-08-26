import os
import numpy as np

from chapter_2.tests.utils import fetchToken
from chapter_2.tools.charts import BarChartTool
from chapter_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool

def start_date(li):
    return li['attributes']['startDate']
def end_date(li):
    return li['attributes']['endDate']
def budget(li):
    if li['attributes']['budget']:
        return li['attributes']['budget']['amount']
    else:
        return 0

def test_analytics_bar_chart():
    token = fetchToken()
    file_name = 'output/test_lineitem_bar_chart.png' 
    if os.path.exists(file_name):
        os.remove(file_name)

    campaign_id = "83603916384092160"
    
    preferred = PreferredLineitemsTool(token=token)
    auction = AuctionLineitemsTool(token=token)
    # preferred_api_result = preferred._run(campaignId=campaign_id)
    # prefered_lineitems = preferred_api_result['data']
    auction_api_result = auction._run(campaignId=campaign_id)
    auction_lineitems = auction_api_result['data']
    print(auction_lineitems)
    dates = map(start_date, auction_lineitems)
    print(list(dates))
    auction_budgets = map(budget, auction_lineitems)
    print(list(auction_budgets))
    # all_lineitems = np.concatenate((prefered_lineitems, auction_lineitems), axis=0)
    # print(all_lineitems)

    bar = BarChartTool()
    chart = bar._run(categories=list(dates), 
                    values=[list(auction_budgets)],
                    x_label='Dates',
                    y_label='Budget',
                    labels=["Auction"],
                    title='Lineitem Budgets', 
                    file_name=file_name)
    assert os.path.exists(file_name)
    assert chart is not None