# JSON Interface
The mesh nodes generally use the same gateway interface for both the Peer-to-Peer (P2P) and the Multi-Hop operation mode. The headers differ between the modes and the Multi-Hop mode has a response whereas the P2P mode can't respond as all nodes are anonymous in the network.

## Security
The communication between the nodes and the gateway is secured by encrypting the messages with a symmetrical or asymmetrical algorithm. This will / has to be further discussed.

## Peer-to-Peer
As part of the mesh the gateway will comply to the protocol used in the P2P mode for receiving and sending packages.

### Package Header
The package headers for P2P packages look like this:
```
{
  "senderUUID": int,
  "messageUUID": int,
  "sentAt": int,
  "message": MessageObject (see below)
}
```
- The `senderUUID` is currently defined to be an integer between 0 and 255 (1 byte). _(This is to be discussed with the Mesh group.)_
<!-- Dropped feature due to missing development resources, this has to be implemented later!
- The `senderKey` is used to authenticate the node. It is just the sender id signed with the private key of the node using SHA-256. The gateway keeps a list of all nodes public keys and verifies the signature with the public key.
-->
- The `messageUUID` is the UUID for this message.
- The `sentAt` is a 8-byte integer (long int) containing a UNIX timestamp.

## Multi-Hop

### Response
For Multi-Hop the gateway will address the targeted node or receive packages from it. After receiving a package from a node (meaning that it did at least reach the gateway) it responds with one of the following responses. These responses use status codes. When the gateway sends a package to a node the node is expected to also respond following this schema.

The general response pattern looks like this:
```
{
  "code": int,
  "status": string,
  "message": string
}
```

Positive status codes indicate success while negative status codes indicate a failure. The statuses and their codes are:
| code | status              | message       | Causes                                                                                      |
|------|---------------------|---------------|---------------------------------------------------------------------------------------------|
| 0    | ok                  | always `null` | success                                                                                     |
| 1    | no content          | string        | success with message                                                                        |
|      |                     |               |                                                                                             |
| -1   | node error          | string        | there was an error with the package that is the fault of the node (e.g. parsing error)      |
| -2   | unauthenticated     | string        | the node is not authentic (e.g. the signature is wrong)                                     |
|      |                     |               |                                                                                             |
| -10  | gateway error       | string        | there was an error in the gateway while processing the package (e.g. gateway unauthorized)  |
|      |                     |               |                                                                                             |
| -20  | backend error       | string        | there was an error in the backend while processing the package (i.e. internal server error) |
| -21  | backend unavailable | always `null` | the backend was not available while the package was sent                                    |

### Package Header
The package headers for Multi-Hop packages look like this:
```
{
  "senderUUID": int,
  "sentAt": int,
  "messageType": string
  "message": MessageObject (see below)
}
```
- The `senderUUID` is currently defined to be an integer between 0 and 255 (1 byte). _This is to be discussed with the Multi-Hop group._
<!-- Dropped feature due to missing development resources, this has to be implemented later!
- The `senderKey` is used to authenticate the node. It is just the sender id signed with the private key of the node using SHA-256. The gateway keeps a list of all nodes public keys and verifies the signature with the public key.
-->
- The `sentAt` is a 8-byte integer (long int) containing a UNIX timestamp.

## Message Types
Due to the fields in the header the nodes are identified and authenticated.

### Meassurement

```
"messageType": "meassurement"
"message": {
  "type": string,
  "value": string
}
```

The generic meassurement as discussed with the other teams. Use for:
- battery status
- signal strength
- temperature meassurements
- pressure measurements
- ...

### Time Sync

```
"message_type": "set_time"
"message": {
  "type": string,
  "value": string
}
```

The generic meassurement as discussed with the other teams.
