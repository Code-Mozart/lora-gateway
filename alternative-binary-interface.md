# Binary interface
The mesh nodes use the same gateway interface for both the Mesh and the Multi-Hop.

## Mesh
As part of the mesh the gateway will comply to the protocol used in the mesh for receiving and sending packages.

## Multi-Hop
For multihop the gateway will address the targeted node or receive packages from it. After receiving a package from a node (meaning that it did at least reach the gateway) it responds with one of the following responses. These responses use status codes. When the gateway sends a package to a node the node is expected to also respond following this schema.

The general response pattern looks like this:
```
status code       signed byte (-128..127)    1 byte
message           ascii-encoded char array   variable length, null-terminated
```

Positive status codes indicate success while negative status codes indicate a failure. The status codes are:
```
CODE  MEANING              MESSAGE

0     no content           no
1     ok                   yes

-1    node error           yes
-2    unauthorized         yes

-10   gateway error        yes

-20   server error         yes
-21   server unavailable   no
```

Example:
```
f6 4e 6f 74 20 69 6d 70 6c 65 6d 65 6e 74 65 64 00

0xf6 = -10 is the status code "gateway error"
the bytes after that each encode a ascii char and make up the message "Not implemented"
the trailing 0x00 is a null character ("\0") terminating the message
```

## Gateway Interface
The specification of the supported messages between the gateway and the mesh. This applies to both the Mesh and the Multi-Hop.

### Header
The header for messages always looks the same:
```
operation type    1 byte      either M (0x4d) for the Mesh or H (0x48) for Multi-Hop.
message id        4 byte      uuid32 (randomly generated id)
timestamp         8 byte      long unix timestamp
```
The `operation type` would not be necessary if it is decided which one will be used and would then be ommitted.

### Endpoints
...

