**Lora Gateway - MDMA SS23**
# Metrics

The gateway sends these metrics every 60 seconds:

## System Metrics

| key ('type') | 'value' type | minimum | maximum | format             | semantic                                                          |
|--------------|--------------|---------|---------|--------------------|-------------------------------------------------------------------|
| cpu_load     | float        | 0.0     | 100.0   | percent            | the cpu load                                                      |
| ram_usage    | float        | 0.0     | 100.0   | percent            | the ram usage                                                     |
| started_at   | string       |         |         | ISO-8601 timestamp | the time the gateway program started running                      |
| system_time  | string       |         |         | ISO-8601 timestamp | the current system time on the gateway at the time of the request |
| system       | string       |         |         |                    | the operating system version running the gateway                  |

Additionally the backend may track the following metrics:
- the last time the backend received had a connection to the gateway (this should be at least every minute for the gateways system info)

## Network Metrics

| key ('type')          | value type | minimum | maximum | format             | semantic                                                     |
|-----------------------|------------|---------|---------|--------------------|--------------------------------------------------------------|
| received_packages     | integer    | 0       |         |                    | the number of packages the gateway received from the mesh    |
| sent_packages         | integer    | 0       |         |                    | the number of packages sent by the gateway to the mesh       |
| last_package_received | string     |         |         | ISO-8601 timestamp | the time the gateway received the last package from the mesh |
| last_package_sent     | string     |         |         | ISO-8601 timestamp | the time the gateway sent the last package to the mesh       |

