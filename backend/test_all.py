import urllib.request
import json
import uuid

def upload_file(source_id, file_path, filename):
    boundary = uuid.uuid4().hex
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

    body = bytearray()
    # data_source_id part
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(b'Content-Disposition: form-data; name="data_source_id"\r\n\r\n')
    body.extend(f'{source_id}\r\n'.encode('utf-8'))

    # file part
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode('utf-8'))
    body.extend(b'Content-Type: text/csv\r\n\r\n')
    with open(file_path, 'rb') as f:
        body.extend(f.read())
    body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode('utf-8'))

    req = urllib.request.Request('http://127.0.0.1:8000/api/uploads/upload/', data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as res:
            print(f'Upload {filename} status: {res.status}')
            print(f'Upload {filename} response: {res.read().decode("utf-8")}')
    except Exception as e:
        print(f'Upload {filename} failed: {e}')

# Fetch sources
req = urllib.request.Request('http://127.0.0.1:8000/api/sources/')
with urllib.request.urlopen(req) as res:
    sources = json.loads(res.read().decode('utf-8'))

utility_id = next(s['id'] for s in sources if s['source_type'] == 'UTILITY')
travel_id = next(s['id'] for s in sources if s['source_type'] == 'TRAVEL')

upload_file(utility_id, '../samples/utility_sample.csv', 'utility_sample.csv')
upload_file(travel_id, '../samples/travel_sample.csv', 'travel_sample.csv')

# Fetch activities
req = urllib.request.Request('http://127.0.0.1:8000/api/activities/')
with urllib.request.urlopen(req) as res:
    activities = json.loads(res.read().decode('utf-8'))

print(f'\nTotal {len(activities)} activities in the database now.')
for a in activities[-5:]: # show last 5
    print(f"- {a['activity_type']} ({a['normalized_quantity']} {a['normalized_unit']}) - Scope: {a['scope']}")
