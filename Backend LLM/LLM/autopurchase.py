import json
import time
import logging
from threading import Thread
# from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from crewai import Task, Crew
from agents import autopurchase_agent


def autopurchase(db):

    while(True):

        # Load the stock data from the JSON file
        # main_stock_data()

        with open('stock_data.json', 'r') as json_file:
            stock_data = json.load(json_file)


        # time.sleep((60*60*2)) for a constant loop put this around the code below
        try:
            docs = (
                db.collection("autopurchase").stream()
            )

            docs = list(docs)

            if docs:
                for doc in docs:
                    userid = doc.get('userid')
                    company = doc.get('company')
                    ticker = doc.get('ticker')
                    buy_percent = int(doc.get('buy_percent'))
                    sell_percent = int(doc.get('sell_percent'))
                    funds = int(doc.get('funds_dollar'))
                    shares_owned = 0
                    document_id = doc.id


                    company_stock = stock_data[company]
                    lastitemdate = list(company_stock)[-1]
                    closingorice = company_stock[lastitemdate]['Close']
                    autopurchase_task = Task(
                        description="From the data given here make a prediction as to whether it is a good idea to buy or sell the stock with the ticker of "+ ticker  +" and the previous 7 days data of "+ str(company_stock),
                        agent=autopurchase_agent,
                        expected_output="I expect the output to be given like this as whole numbers, just numbers even if its 0 and nothing more."
                                        "{"
                                        '"Buy"": "x%",'
                                        '"Sell": "z%"'
                                        "}"
                    )
                    crew = Crew(agents=[autopurchase_agent],
                                tasks=[autopurchase_task], verbose=True)
                    result = crew.kickoff()
                    result = str(result)
                    result = result.replace("%", "")
                    result = result.replace("-", "")
                    result = result.replace("+", "")
                    print(result)
                    jsonobject = json.loads(result)
                    agent_buy = int(jsonobject.get('Buy'))
                    agent_sell = int(jsonobject.get('Sell'))
                    #if the buy from agent is greater than the given from user, then go ahead and buy as many stocks as possible until you can buy anymore
                    #then save that into the firebase database

                    if int(agent_buy)>= buy_percent and funds > closingorice:
                        shares_owned  += funds / closingorice
                        funds -= shares_owned*closingorice
                        db.collection("autopurchase").document(document_id).set({ "shares_owned": shares_owned,'funds_dollar':funds}, merge=True)

                        #save share bought , ticker, user id into database so it can be retrieved for future use
                    else:
                        if agent_sell >= sell_percent and shares_owned > 0:
                            #get the share from database and sell them all
                            newfunds = closingorice * shares_owned
                            shares_owned = 0
                            docs = (
                                db.collection("admins").stream()
                            )

                            adminobject = 0
                            docs = list(docs)
                            for doc in docs:
                                if doc.id == userid:
                                    adminobject = doc
                                    break
                            capital = adminobject.get('capital')
                            capital += newfunds
                            db.collection("autopurchase").document(document_id).delete()
                            db.collection("admins").document(userid).set({'capital': capital})


        except Exception as e:
            logging.error(f"Error during task execution: {e}")
        time.sleep(1000)