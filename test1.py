# import nest_asyncio
# nest_asyncio.apply()

# import marketfeed
# import asyncio

# client_id = "1104088864"
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI3NTE5ODQzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.XIKQpgBpDUa6CLjf67FjM-4c6lIfvURzU0Dob6RJIZUv3dyCmsZhXxiKMhSccdvCNdfPctU_vPSa6j8WclAfiA"

# instruments = [(0,"13",15)]
# subscription_code = marketfeed.Ticker

# # Usage Example
# async def on_connect(instance):
#     print("Connected to websocket")

# async def on_message(instance, message):
#     print("Received:", message)

# print("Subscription code :", subscription_code)
# feed = marketfeed.DhanFeed(client_id, access_token,instruments)
# asyncio.create_task(feed.run_forever())
# feed.run_forever()
# feed.subscribe_symbols(instruments)
# feed.disconnect()


from dhanhq import marketfeed

# Add your Dhan Client ID and Access Token
client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI3NTE5ODQzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.XIKQpgBpDUa6CLjf67FjM-4c6lIfvURzU0Dob6RJIZUv3dyCmsZhXxiKMhSccdvCNdfPctU_vPSa6j8WclAfiA"

# Structure for subscribing is (exchange_segment, "security_id", subscription_type)

instruments = [(marketfeed.NSE, "1333", marketfeed.Ticker),(marketfeed.NSE, "1333", marketfeed.Quote),(marketfeed.NSE, "1333", marketfeed.Depth),(marketfeed.NSE, "11915", marketfeed.Ticker),(marketfeed.NSE, "11915", marketfeed.Ticker)]


# Ticker - Ticker Data
# Quote - Quote Data
# Depth - Market Depth

# In case subscription_type is left as blank, by default Ticker mode will be subscribed.

try:
    data = marketfeed.DhanFeed(client_id, access_token, instruments)
    while True:
        data.run_forever()
        response = data.get_data()
        print(response)

except Exception as e:
    print(e)


# Subscribe instruments while connection is open
sub_instruments =
    [(marketfeed.NSE, "14436", marketfeed.Ticker)]

data.subscribe_symbols(sub_instruments)
# Close Connection
data.disconnect()

# Unsubscribe instruments which are already active on connection
unsub_instruments =
    [(marketfeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
