import requests

url = "http://localhost:8000/patients"
params = {"endpoint": "http://host.docker.internal:7200/repositories/protrait"}

url2 = "http://localhost:8000/dvh_curve"
params = {"endpoint": "http://host.docker.internal:7200/repositories/protrait"}
response = requests.get(url2, params=params)
print(response.status_code)
data = response.json()  # This converts response.content from bytes to a dict
print(data)
# Now access the list of patient IDs
#print(data["patients"]["x.type"])
