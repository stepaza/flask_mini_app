import requests
import json

api_url = "http://localhost:5000/todo/api/v1.0/tasks"

#####################################
### Test GET request
print('Testing GET request...')
get_resp = requests.get(url=api_url + '/' + '1', auth = ('miguel', 'python')) # Same as: auth = requests.auth.HTTPBasicAuth('user', 'pwd')
print(f"HTML Code: {get_resp}")
print(f"Text:\n{get_resp.text}")

#####################################
### Test POST request
print('##########################################################################')
print('Testing POST request...')

new_data = {"title":"Read a book as part of the new task !"}
new_data_json = json.dumps(new_data)

headers= {"Content-Type": "application/json"}

post_resp = requests.post(url=api_url, headers = headers, data = new_data_json, auth = ('miguel', 'python'))

print(f"HTML Code: {post_resp}")
print(f"Text:\n{post_resp.text}")

#####################################
### Test DELETE request
print('##########################################################################')
print('Testing DELETE request...')

delete_resp = requests.delete(url=api_url + '/' + '3', auth = ('miguel', 'python'))
print(f"HTML Code: {delete_resp}")
print(f"Text:\n{delete_resp.text}")

#####################################
### Test PUT request
print('##########################################################################')
print('Testing PUT request...')

update_data = {"title":"Update the book title as part of the new task !", 'description' : "This is an updated description", 'done': True}
update_data_json = json.dumps(update_data)

headers= {"Content-Type": "application/json"}

put_resp = requests.put(url=api_url + '/' + '2', headers = headers, data = update_data_json, auth = ('miguel', 'python'))

print(f"HTML Code: {put_resp}")
print(f"Text:\n{put_resp.text}")

print('#####################################\n\nSuccessfully tested all methods !')

