# Interface Specification
The mesh nodes generally use the same gateway interface for both the Mesh and the Multi-Hop operation mode. Both modes use MQTT for communicating. In the mesh the broker is shared across all nodes such that each node acts both as a broker and a client.

## Security
The communication between the nodes and the gateway is to be secured by encrypting the messages with a symmetrical or asymmetrical algorithm. This will / has to be further discussed.

## Messages
The MQTT message structure is defined by the mesh. It at least has to support:
- Topic: the mqtt topic
- Payload: a variable length byte/string including these fields
  - message uid: an id that uniquely identifies the message (may be a combination of sender and timestamp)
  - sender uuid: a uuid for the node that sent the message
  - timestamp: the timestamp for when the message was sent

## Interface

The interface uses JSON for its payload.

### Measurements
Topic:
```
v1/backend/measurements
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
- `value` is the string representation of the value. _This is prone to change to a number instead (17 May, 23)._

The generic measurement used for:
- battery status
- signal strength
- temperature measurements
- pressure measurements
- ...
Nodes should publish messages to this topic to make the gateway forward them to the backend.

### Generic Message Acknowledge
Topic:
```
v1/acknowledges/{message uid}
```
Payload:
```
{
  ... (defined by mesh/multi-hop group, includes sender uuid and timestamp)
}
```

Acknowledges are published back to the mesh as soon as a message is received by the gateway.

### Monitoring
...

### OTA Updates
...
