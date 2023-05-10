# JSON Interface
The mesh nodes generally use the same gateway interface for both the Mesh and the Multi-Hop operation mode. Both modes use MQTT for communicating. In the mesh the broker is shared across all nodes such that each node acts both as a broker and a client.

## Security
The communication between the nodes and the gateway is to be secured by encrypting the messages with a symmetrical or asymmetrical algorithm. This will / has to be further discussed.

## Messages
The MQTT message structure is defined by the mesh. It at least has to support:
- Topic: the mqtt topic
- Payload: a variable length byte/string including these fields
  - sender uuid: a uuid for the node that sent the message
  - timestamp: the timestamp for when the message was sent

## Interface

### Meassurements
Topic:
```
v1/backend/meassurements
```
Payload:
```
{
  ... (defined by mesh/multi-hop group, includes sender uuid and timestamp)
  "content": {
    "type": string,
    "value": string
  }
}
```
- `type` is any string as discussed with the other teams.
- `value` is the string representation of the value. _This is prone to change to a number instead (10 May, 23)._

The generic meassurement used for:
- battery status
- signal strength
- temperature meassurements
- pressure measurements
- ...
Nodes should publish messages to this topic to make the gateway forward them to the backend.

### Response
Topic:
```
v1/backend/responses/{node id}
```
Payload:
```
{
  ... (defined by mesh/multi-hop group, includes sender uuid and timestamp)
  "content": {
    "statusCode": integer,
    "status": string,
    "message": string
  }
}
```
- `statusCode` is a integer HTTP status code (200, 422, ...)
- `status` is the string representation of the HTTP status code (OK, Unprocessable Entity, ...)
- `message` is the body of the HTTP response. May be an empty string.

Responses are published by the gateway after the server responded.
