import urllib.request
import urllib.parse
import json
import mimetypes
import uuid

# Fetch sources
req = urllib.request.Request('http://127.0.0.1:8000/api/sources/')
with urllib.request.urlopen(req) as res:
    sources = json.loads(res.read().decode('utf-8'))

sap_id = next(s['id'] for s in sources if s['source_type'] == 'SAP')

# Upload file using multipart/form-data
boundary = uuid.uuid4().hex
headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

body = bytearray()
# data_source_id part
body.extend(f'--{boundary}\r\n'.encode('utf-8'))
body.extend(b'Content-Disposition: form-data; name="data_source_id"\r\n\r\n')
body.extend(f'{sap_id}\r\n'.encode('utf-8'))

# file part
body.extend(f'--{boundary}\r\n'.encode('utf-8'))
body.extend(b'Content-Disposition: form-data; name="file"; filename="sap_sample.csv"\r\n')
body.extend(b'Content-Type: text/csv\r\n\r\n')
with open('../samples/sap_sample.csv', 'rb') as f:
    body.extend(f.read())
body.extend(b'\r\n')
body.extend(f'--{boundary}--\r\n'.encode('utf-8'))

req = urllib.request.Request('http://127.0.0.1:8000/api/uploads/upload/', data=body, headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as res:
        print('Upload status:', res.status)
        print('Upload response:', res.read().decode('utf-8'))
except Exception as e:
    print('Upload failed:', e)

# Fetch activities
req = urllib.request.Request('http://127.0.0.1:8000/api/activities/')
with urllib.request.urlopen(req) as res:
    activities = json.loads(res.read().decode('utf-8'))

print(f'Found {len(activities)} activities in the database.')
for a in activities:
    print(f"- {a['activity_type']} ({a['normalized_quantity']} {a['normalized_unit']}) - Status: {a['status']}")
