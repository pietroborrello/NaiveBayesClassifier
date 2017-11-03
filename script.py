import requests

s = "https://flatscience.flatearth.fluxfingers.net/"

for i in range(99999):
    site = s+ ''.join(map(lambda c: c+'/', str(i)))
    code = requests.get(site).status_code
    if code != 404:
        print site
    code = requests.get(site+'/ded').status_code
    if code != 404:
        print site
