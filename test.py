import requests

url = "http://localhost:8666/patients_dvh"
params = {"endpoint": "http://graphdb:7200/repositories/protrait"}

url2 = "http://localhost:8666/dvh_curve"
params2 = {"endpoint": "http://host.docker.internal:7200/repositories/protrait"}
p_id = "hypog01-FR-04-0002-P-L"
url3 = f"http://localhost:8000/patients/{p_id}"
params3 = {"endpoint": "http://host.docker.internal:7200/repositories/protrait"}
url4 = f"http://localhost:8666/clinical"


url5 = "http://localhost:8666/clinical_patient"
params5 = {"endpoint": "http://graphdb:7200/repositories/protrait_c"}

response = requests.get(url,params)
print(response.status_code)
if response.status_code != 200 and response.status_code != 201 and response.status_code != 204:
    print(f"Error: {response.status_code} - {response.text}")
    exit(1)
else:
    data = response.json()  # This converts response.content from bytes to a dict
    print(data)
    # Now access the list of patient IDs
#print(data["patients"]["x.type"])
