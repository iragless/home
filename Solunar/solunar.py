import json
from urllib.request import urlopen

# solunar api with urlopen("https://api.solunar.org/solunar/-34.99,138.52,20220907,10") as response:
with urlopen("https://api.sunrise-sunset.org/json?lat=-34.99&lng=138.52&date=today") as response: #sunrise api
    source = response.read()

data = json.loads(source)

while True:
    print(data['results'][input('?')])

