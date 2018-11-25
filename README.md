# ultra-protocol
A text-based protocol made for CS studies at PUT

## Communication between clients via the server (n: 1), based on the plain text protocol.

#### Protocol:
* connectionless,
* all data sent in text form (sequence of ASCII characters),
* every message with a time stamp,
* header element structure defined as `#key#$#value#`
(example) `#operation#$#add#`
* case sensitive identification,


#### Required fields:
* operation field - `O`,
* answer field - `o`,
* ID field - `I`.
* additional fields defined by the programmer.

#### Software features:
##### 1. Client:
* establishing a connection with the server,
* obtaining a session identifier,
* sending a single natural number L,
* sending numeric values that are "answers": the client has to guess the number drawn by the server.
* ending the call.
##### 2. Server:
* generating a session identifier,
* drawing a secret number from the interval (L1; L2),
* sending the range in which the number to be guessed is included,
* informing customers whether the value was guessed.

#### Additional info:
* session ID should be sent during communication,
* each message sent should be confirmed by the other side.


## Protocol structure
### Required fields
| field     | key | values                                                  |
| --------- | --- | ------------------------------------------------------- |
| Operation | `O` | `connecting`, `range`, `guess`, `session`, `response`   |
| Response  | `o` | `L`, `L1:L2`, `=`, `>`, `<`                             |
| ID        | `I` | `session_id`                                            |
### Additional fields
| field     | key | values                                                  |
| --------- | --- | ------------------------------------------------------- |
| Flags     | `f` | `syn`, `ack`, `push`                                    |
| Flag No.  | `n` | `numeric_flag_id`                                       |
| Time      | `t` | `timestamp`                                             |

## Communication scheme

##### 1. Client initializes connection
##### 2. Server confirms and send `session_id`
##### 3. Server sends `L1`, `L2` data to client
##### 4. Client confirms receiving
##### 5. Client sends `L`
##### 6. Server confirm receiving
##### 7. Server send response to client
