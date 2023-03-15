import requests
import threading


def post_request(url, body, request_type):
    
    headers = {
           'Content-Type': 'application/json',
         }
    response = requests.request(request_type, url, headers=headers, json=body)
    return response
    
def fire_and_forget(url, body, request_type):
    threading.Thread(target=post_request, args=(url, body, request_type)).start()
