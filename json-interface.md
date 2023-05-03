# JSON Interface
The mesh nodes generally use the same gateway interface for both the Peer-to-Peer (P2P) and the Multi-Hop operation mode. The headers differ between the modes and the Multi-Hop mode has a response whereas the P2P mode can't respond as all nodes are anonymous in the network.

## Mesh
As part of the mesh the gateway will comply to the protocol used in the mesh for receiving and sending packages.

### Package Header
The package headers for P2P packages look like this:
```
{
  "sender_id": int,
  "message_id": int,
  "timestamp": int,
  "message": MessageObject (see below)
}
```
- The `sender_id` is currently defined to be an integer between 0 and 255 (1 byte). _This is to be discussed with the Mesh group._
- The `message_id` is a 32-bit integer.
- The `timestamp` is a 8-byte integer (long int) containing a UNIX timestamp.

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
| code | status              | message       |
|------|---------------------|---------------|
| 0    | ok                  | always `null` |
| 1    | no content          | string        |
|      |                     |               |
| -1   | node error          | string        |
| -2   | unauthorized        | string        |
|      |                     |               |
| -10  | gateway error       | string        |
|      |                     |               |
| -20  | backend error       | string        |
| -21  | backend unavailable | always `null` |

### Package Header
The package headers for Multi-Hop packages look like this:
```
{
  "sender_id": int,
  "timestamp": int,
  "message": MessageObject (see below)
}
```
- The `sender_id` is currently defined to be an integer between 0 and 255 (1 byte). _This is to be discussed with the Multi-Hop group._
- The `timestamp` is a 8-byte integer (long int) containing a UNIX timestamp.
