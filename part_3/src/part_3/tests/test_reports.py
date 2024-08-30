from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import CampaignsTool
from part_3.tests.utils import fetchToken
from part_3.tests.utils import write_data

from part_3.tools.analytics import CampaignAnalyticsTool, ReportDownloadTool, ReportStatusTool

import time


def test_create_summary_report():
    token = fetchToken()
    assert token is not None

    # tools
    accounts = AccountsTool(token=token)
    campaigns = CampaignsTool(token=token)
    campaigns_analytics = CampaignAnalyticsTool(token=token)
    status = ReportStatusTool(token=token)
    downloader= ReportDownloadTool(token=token)

    # accounts
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    # campaigns for first account
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    assert len(campaigns_api_result["data"]) > 0
    campaign_list = campaigns_api_result["data"]
    campaign_ids = [campaign["id"] for campaign in campaign_list]

    summary_api_result = campaigns_analytics._run(
        campaignIds=campaign_ids, startDate="2020-01-01", endDate="2020-12-31"
    )
    assert summary_api_result is not None
    assert summary_api_result["data"] is not None
    data = summary_api_result["data"]
    write_data(data, "test_summary_create.json")

    assert data["id"] is not None
    reportId = data["id"]
    assert data["attributes"]["status"] is not None

    report_status = data["attributes"]["status"]
    status_counter = 0

    while report_status == "pending":
        time.sleep(60)
        status_counter += 1

        status_result = status._run(
            reportId=reportId
        )
        assert status_result is not None
        assert status_result["data"] is not None
        data = status_result["data"]
        report_status = data["attributes"]["status"]

        write_data(data, f"test_summary_status_{reportId}_{status_counter}.json")
    
    assert report_status == "success"

    download_result = downloader._run(reportId=reportId, path=f"outpur/test_summary_download_{reportId}.json")
    assert download_result is not None
    


