# import date
# from date import datetime
import requests

# url = "https://api.upstox.com/v2/market/holidays/:2024-06-17" # wrong remove the column
# url = "https://api.upstox.com/v2/market/holidays/today" # not working correct this to dynamically pass or check the date 
# url = "https://api.upstox.com/v2/market/holidays/2024-05-30" # works in this format 
url = "https://api.upstox.com/v2/market/holidays/"

payload={}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text) # this also works

text_type = response.text

print(type(text_type) ,"  " , text_type,"\n")

# print(response.json())

json_type = response.json()

print("\n \n 999999999   ", type(json_type) , " " , json_type)