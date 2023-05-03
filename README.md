# lora-gateway
The Repository for the LoRa Gateway we coded in Summer Semester 2023

# Requirements
1. Establish a secure and authorized connection with the backend
   - Authenticate against the backend
   - Check the identity of the backend (using certificates/SSL?)
2. Authenticate nodes
3. Translate packages from nodes to HTTP(S) requests
4. Translate responses from Server to nodes

# Interfaces
"JSON Interface" specifies the JSON interface the gateway provides. While being more verbose and heavier the JSON format allows for faster development, easier debugging and more flexibilty.

"Binary Interface" specifies an alternative binary interface for the gateway. This is more resource optimized and uses as few bytes as possible for communication.
