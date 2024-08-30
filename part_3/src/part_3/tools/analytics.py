from typing import List
from crewai_tools import BaseTool

import requests
import os
import json
import pprint

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]

# See: https://developers.criteo.com/retail-media/docs/analytics

# The Criteo Retail Media Analytics API allows you to scale operations programmatically
# through our API and integrate Retail Media Platform (RMP) capabilities into your preferred UI or workflow tools.
# With the Criteo Retail Media API You will be able to download campaign and line item performance reports, including:
# - Product-level performance and attributed transaction logs
# - Report attribution windows and time zones are fully customizable
# Quick Start
# 1. Request a report
# 2. Poll for report status
# 3. Upon success, download the report output

# https://developers.criteo.com/retail-media/docs/overview


class CampaignAnalyticsTool(BaseTool):
    name: str = "Retail Media campaign analytics API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns a report for the requested campaign id and date range"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, campaignIds: List[str], startDate: str, endDate: str):
        # print("campaignIds", campaignIds)
        # print("startDate", startDate)
        # print("endDate", endDate)
        url = f"{self.base_url}reports/campaigns"
        # https://api.criteo.com/2024-01/retail-media/reports/campaigns
        # print("url", url)
        # print("token", self.token)
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "accept": "application/json"}
        payload = {"data" : {
                "type": "RetailMediaReportRequest",
                "attributes": {
                    "ids": campaignIds,
                    "format": "json-compact",
                    "reportType": "summary",
                    "clickAttributionWindow": "none",
                    "viewAttributionWindow": "none",
                    "timeZone": "UTC",
                },
            }
        }
        # print("payload", payload)
        response = requests.post(
            url,
            headers=headers,
            # json=json.dumps(payload),
            json=payload
        )
        
        # print("response", response)
        response_as_json = response.json()
        # print("response_as_json", response_as_json )
        # # response.raise_for_status()
        return response_as_json


class LineitemAnalyticsTool(BaseTool):
    name: str = "Retail Media lineitem analytics API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the analytic for the requested lineitems"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, lineitemIds: List[str], startDate: str, endDate: str):
        headers = {"Authorization": "Bearer " + self.token}
        data= {
                "type": "RetailMediaReportRequest",
                "attributes": {
                    "id": lineitemIds,
                    "metrics": ["impressions"],
                    "dimensions": ["date"],
                    "reportType": "summary",
                    "startDate": startDate,
                    "endDate": endDate,
                    "timeZone": "America/New_York",
                    "campaignType": "sponsoredProducts",
                    "salesChannel": "offline",
                },
            }
        response = requests.request(
            "POST",
            f"{self.base_url}reports/line-items",
            headers=headers,
            body=data,
        )
        response.raise_for_status()
        return response.json()


class ReportStatusTool(BaseTool):
    name: str = "Retail Media report status API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the status for the report using reportId"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, reportId: str):
        headers = {"Authorization": "Bearer " + self.token}

        response = requests.get(
            f"{self.base_url}reports/{reportId}/status",
            headers=headers,
        )
        print("status response", response)
        return response.json()


class ReportDownloadTool(BaseTool):
    name: str = "Retail Media report download API Caller"
    description: str = "Calls the Retail Media  REST API to download a report using reportId"
    base_url: str = base_url_env
    token: str

    def _run(self, reportId: str, path: str):

        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request(
            "GET",
            f"{self.base_url}reports/{reportId}/output",
            headers=headers,
        )
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Report downloaded successfully and saved as {path}")
        return response.json()
