import requests
import pandas as pd
import time

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
market_depth_url = "https://api.dhan.co/v2/marketfeed/quote"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'MCX_COMM':[436966,436967,436968,437018,437019,437020]
}

while True:
    response_quote = requests.post(url = market_depth_url,headers = header,json = data)
    result_depth = response_quote.json()['data']["MCX_COMM"]
    print(result_depth)
    time.sleep(1)
