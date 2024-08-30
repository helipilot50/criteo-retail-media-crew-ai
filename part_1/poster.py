
# rest post request example

import requests

# Define the API endpoint
url = 'https://jsonplaceholder.typicode.com/posts'

# Data to be sent in the POST request
data = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.json())
