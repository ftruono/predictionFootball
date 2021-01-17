#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    #ML-Configuration
    TENANT_ID=os.environ.get("TenantId","c30767db-3dda-4dd4-8a4d-097d22cb99d3")
    SUBSCRIPTION_ID = os.environ.get("SubscriptionId", '2853834e-9533-4f4f-80cb-9fba1589b89c')
    RESOURCE_GROUP = os.environ.get("ResourceGroup", "f.truono5_rg_Linux_centralus")
    WORKSPACE_NAME = os.environ.get("WorkspaceName", "ML22")

    FILE_NAME = os.environ.get("csvFileName", "pre")
    JSON_FILE_NAME = os.environ.get("jsonFileName", 'metadata')
    MODEL_LINK_PREDICTION = os.environ.get("modelLink", "")

    #Auth Configuration
    CLIENT_ID=os.environ.get("ClientId","8e8ad129-6308-4a63-984f-f9f117388e62")
    CLIENT_SECRET=os.environ.get("ClientSecret","H~2-KInUEysuHqq19D33noyt_L0N~mBN.J")

    #LUIS Configuration
    LUIS_APPID=os.environ.get("LuisAppId","a0edec6c-a603-477b-8285-15bbe0915ece")
    LUIS_KEY1=os.environ.get("LuisKey1","e1eaf55999604f2eb4db53b9c6d53a43")
    LUIS_KEY2 = os.environ.get("LuisKey2", "")
    LUIS_ENDPOINT=os.environ.get("LuisEndPoint","https://luisservice0.cognitiveservices.azure.com/")

