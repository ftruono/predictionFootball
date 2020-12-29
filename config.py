#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "d85be113-3517-4cc4-864e-fbfde769ef95")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "H7.~ODxEa46~L4wu5c8uKM3P1~Rx4BV.m_")

    SUBSCRIPTION_ID = '2853834e-9533-4f4f-80cb-9fba1589b89c'
    RESOURCE_GROUP = 'DefaultResourceGroup-WEU'
    WORKSPACE_NAME = 'ML22'
    FILE_NAME='pre'

    JSON_FILE_NAME='metadata'
    MODEL_LINK_PREDICTION='http://2e7611b0-9187-498c-b5c1-b2c2df00254f.westeurope.azurecontainer.io/score'
