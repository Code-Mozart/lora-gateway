# JSON Interface
The mesh nodes use the same gateway interface for both the Mesh and the Multi-Hop.

## Mesh
As part of the mesh the gateway will comply to the protocol used in the mesh for receiving and sending packages.

## Multi-Hop
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
| Code | Status              | Message       |
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
