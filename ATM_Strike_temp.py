import my_lib
import time
from dhanhq import marketfeed

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

index_security_ids = {
    "MIDCPNIFTY" : 442,
    "BANKEX" : 69,
    "FINNIFTY" : 27,
    "BANKNIFTY" : 25,
    "NIFTY" : 13,
    "SENSEX" : 51
}


underlying = "MIDCPNIFTY"

start = time.time()
current_atm_strike = my_lib.curent_atm_strike(client_id=client_id,access_token=access_token,underlying_security_id=index_security_ids[underlying])
print(f"Current_ATM_Strike = {current_atm_strike} ,Time Taken = {time.time()-start}")



