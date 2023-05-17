**Lora Gateway - MDMA SS23**
# Requirements

## Functional Requirements

The Gateway is responsible for enabling the communication between the mesh network (both Mesh mode and Multi-Hop mode). It is also a great place to manage the mesh itself (e.g. monitoring):
- Forwarding messages from the mesh to the backend, translating between protocols/interfaces
- Regularly fetching the backend for mesh node updates (OTA updates)
- _monitoring?_
- _backend responses?_

## Non-functional Requirements

- The communication with the mesh nodes has to be secure (authenticated, authorized and encrypted)
- The communication with the backend has to be secure (authenticated, authorized and encrypted)
- Using MQTT for communication with the mesh nodes (this has to be specified by the mesh groups)
- Messages are forwarded asynchronously (using MQTT)
- Errors are logged and then ignored, there is no further error handling
- The gateway application has to be easily expandable as it is prone to rapidly change.
- The gateway should be able to scale with the mesh network (so it should be possible to add nodes without any problems)
