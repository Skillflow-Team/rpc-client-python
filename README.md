# Turing Python Client Library

This library provides a straightforward interface for interacting with the
Turing RPC Server. It simplifies the process of sending questions and receiving
answers.

## Project Installation

## Project Structure

The client library is structured into modules within the `core` directory for
clarity and ease of use:

- `models/`: Contains the data structures and domain models, such as `Question`.
- `client/`: Houses the logic to handle communication with the RPC server.
- `errors.py`: Defines custom exception classes that the client may raise during
  operation.

Here is the layout of the project:

```
my_rpc_client/
│
├── core/
│ ├── models/
│ │ └──── # Domain models such as the Question class
│ │
│ ├── client/
│ │ └──── # Handles the communication with the RPC server
│ │
│ └── errors.py
│    └─── # Custom exception classes for the client library
│
├── tests/
│ ├── test_models/
│ │ └──── # Unit tests for the domain models
│ │
│ └── test_client/
│   └──── # Unit tests for the RPC client functionality
│
├── examples/
│ └── # Example scripts on how to use the library
│
```
