#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    SUBSCRIPTION_ID = os.environ.get("SubscriptionId", '2853834e-9533-4f4f-80cb-9fba1589b89c')
    RESOURCE_GROUP = os.environ.get("ResourceGroup", "DefaultResourceGroup-WEU")
    WORKSPACE_NAME = os.environ.get("WorkspaceName", "ML22")
    FILE_NAME = os.environ.get("csvFileName", "pre")

    JSON_FILE_NAME = os.environ.get("jsonFileName", 'metadata')
    MODEL_LINK_PREDICTION = os.environ.get("modelLink", "")
