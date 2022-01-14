# e-comm-chatobot-luis
## This chatbot project creates a bot for a bakery shop.
### The bot offers following helps to the user:
#### 1. Create an order
#### 2. View orders
#### 3. Cancel an existing order

## Azure Bot Framework and LUIS 

#### For creating LUIS app use the json provided in data folder.
#### Guide to create a LUIS app is at https://docs.microsoft.com/en-us/azure/cognitive-services/luis/luis-how-to-start-new-app
#### When you create your LUIS app importing the JSON provided in data folder you will see the project has Create Order Intent
#### and few entities alreay created for you.
#### Order entity is ML structured entity. It is the main entity which we will be using in our project to map the order details.
#### In the LUIS app go to the Manage Tab and select Authorization Resource. 
#### On Authorization Resource screen you will find the URL.
#### Copy the URL, trim the last part of the URL i.e. "YOR_QUERY_HERE". paste the URL in Config file attribute LUIS_URL
