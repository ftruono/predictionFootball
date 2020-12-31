# Prediction Football Bot

This bot use custom deployed ml to predict the match of ligue Serie A

This bot has been created using [Bot Framework](https://dev.botframework.com) and use resource of azure ml
## Prerequisites

This sample **requires** prerequisites in order to run.

### Install Python 3.6

## Running the sample
- Run `pip install -r requirements.txt` to install all dependencies
- Set your tenant id, in file config.py TENANT_ID
- Add in ml studio, two file: one tabular mode (pre.csv) and metadata.json. The first one contains the pre-processed csv, the second one contains
the encoded list team. If you want customize this property is necessary modify config.py
- Deploy the model on machine learning studio. Create an environment constant called modelLink that contains the deployed model
- To login in ml resource is necessary create an user on Azure Active Directory and link to machine learning resource to sum up update the two environment constant: clientId, clientSecret  
- Run `python app.py`


## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- Enter a Bot URL of `http://localhost:3978/api/messages`