import requests
import pandas as pd 

url = "http://localhost:8051/data/trade/jp/?time=monthly&types=total&agr=false&group=false"
r = requests.get(url).json()
print(pd.DataFrame(r))