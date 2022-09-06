import json
from urllib.request import urlopen

with urlopen("https://api.solunar.org/solunar/42.66,-84.07,20180207,-4") as response:
    source = response.read()

data = json.loads(source)

print(json.dumps(data, indent=2))

