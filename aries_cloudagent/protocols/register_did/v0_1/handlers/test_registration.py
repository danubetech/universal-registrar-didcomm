import requests
import json


def register_did(url):
    """Register a DID using a registrar service like uniregistrar."""
    params = {"driverId": "driver-universalregistrar/driver-did-key"}
    payload = {
        "jobId": None,
        "options": {
            "keyType": "Ed25519VerificationKey2018"
        },
        "secret": {},
        "didDocument": {
            "service": [],
            "verificationMethod": [],
            "authentication": []
        }
    }
    xpayload = json.dumps(payload)
    import pdb
    pdb.set_trace()
    response = requests.post(url, params=params, data=xpayload)
    if response.ok:
        # content = response.json()
        return response.json()
        # return content['didDocument']
    raise ValueError(f"Failed to register DID document using URL {url}")


response = register_did("https://uniregistrar.io/1.0/register")
print(response.text)
