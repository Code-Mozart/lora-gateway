**Lora Gateway - MDMA SS23**
# Interface Specification
The mesh nodes generally use the same gateway interface for both the Mesh and the Multi-Hop operation mode. Both modes use MQTT for communicating. In the mesh the broker is shared across all nodes such that each node acts both as a broker and a client.

## Security
The communication between the nodes and the gateway is to be secured by encrypting the messages with a symmetrical or asymmetrical algorithm. This will / has to be further discussed.

## Messages
The MQTT message structure is defined by the mesh. It at least has to support:
- Topic: the mqtt topic
- Payload: a variable length byte/string including these fields
  - message uid: an id that uniquely identifies the message (may be a combination of sender and timestamp)
  - sender uid: a uid for the node that sent the message
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
  ... (defined by mesh/multi-hop group, includes sender uid and timestamp)
  "content": {
    "type": string,
    "value": string
  }
}
```
- `type` is any string as discussed with the other teams.
- `value` is the string representation of the value.

The generic measurement used for:
- battery status
- signal strength
- temperature measurements
- pressure measurements
- ...
Nodes should publish messages to this topic to make the gateway forward them to the backend.

### Register new Node
Only used for Multi-Hop-Mode

Topic:
```
v1/registrations
```
Payload:
```
{
  ... (defined by mesh/multi-hop group, includes sender uid and timestamp)
  content: {
    "uuid": string
  }
}
```

## OTA Updates

### Patch Block
Does not use JSON.
```
BYTES       CONTENT         DESCRIPTION
1           0xFF            Escape Symbol
2                           Version number
2                           Number of blocks
2                           Block index
1-237                       Block content (Fixed block size)
```

The block size is defined due to limitations from the packet size and headers in the Multi-Hop mode.

### Missing Patch Block
Topic:
```
v1/updates/missing
```
Payload:
```
{
  ... (defined by mesh/multi-hop group, includes sender uuid and timestamp)
  "content": {
    "missingBlockIndex": int
  }
}
```
