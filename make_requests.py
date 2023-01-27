import requests
import json

BASE_URL = 'http://localhost:8000/orders'

def create_boat_orders(url,product,price):
    data = json.dumps({"actual_price": price,
                        "item": product })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=data)
    print(response.json())


def read_all_orders(url):
    response = requests.request("GET", url)
    print(response.json())
    
def read_product_order(url,product):
    request_url = url+'/?product='+product
    response = requests.request("GET", request_url)
    print(response.json())
  
def read_an_order(url,order_number):
    request_url = url+'/'+str(order_number)
    response = requests.request("GET", request_url)
    print(response.json())
     
def update_an_order(url,order_number,new_price):
    request_url = url+'/'+str(order_number)
    data = json.dumps({"actual_price": new_price})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("PUT", request_url, headers=headers, data=data)
    print(response.json())
                            
def delete_an_order(url,order_number):  
    request_url = url+'/'+str(order_number)      
    response = requests.request("DELETE", request_url)   
    print(response.json())                 

def read_metrics(url):   
    request_url = url+'/metrics'
    response = requests.request("GET", request_url)
    print(response.json())




"""
Run Function Below for particular request to API endpoints
"""

# Read all orders
read_all_orders(BASE_URL)

# Read all orders from a particular product
# read_product_order(BASE_URL,"Catamaran")

# Read an order via order_id
# read_an_order(BASE_URL,10)

# Make post request
# create_boat_orders(BASE_URL,"Submarine",1800)

# Update an exiting order
# update_an_order(BASE_URL,15,2000)

# delete an order
# delete_an_order(BASE_URL,15)

# Get metrics of product orders 
# read_metrics(BASE_URL)
