#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = "d85be113-3517-4cc4-864e-fbfde769ef95"
    APP_PASSWORD = "x51~S2t3.InM.SOw5o~E-Slp.4xs3.HSgc"

    SUBSCRIPTION_ID = '2853834e-9533-4f4f-80cb-9fba1589b89c'
    RESOURCE_GROUP = 'resourcegrouplinux'
    WORKSPACE_NAME = 'ML22'
    FILE_NAME = 'pre'

    JSON_FILE_NAME = 'metadata'
    MODEL_LINK_PREDICTION = 'http://051310e9-4932-434d-9104-f6c895e9e701.westeurope.azurecontainer.io/score'
