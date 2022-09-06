import json
from urllib.request import urlopen

with urlopen("https://api.solunar.org/solunar/-34.99,138.52,20220907,10") as response:
    source = response.read()

data = json.loads(source)

print(json.dumps(data, indent=2))

