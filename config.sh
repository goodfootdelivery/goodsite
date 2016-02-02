#!/bin/bash

# Set Bash Variables for api testing purposes

API='http://127.0.0.1:8000/delivery/'
echo "API Root set at: $API"

# Address View Set
address=$API
address+='addresses/'
echo "Address Views set at: $address"

# User View Set
user=$API
user+='users/'
echo "User Views set at: $user"

# Order View Set
order=$API
order+='orders/'
echo "Order Views set at: $order"

echo 'Completed'
