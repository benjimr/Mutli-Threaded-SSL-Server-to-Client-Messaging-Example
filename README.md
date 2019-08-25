Simple example of a server designed to accept connections from many clients, and message all connected clients, like a notification system. Using SSL for security.

## Steps 

1. Server starts a listener thread, then waits for client connections.
   * Setup SSL context for client authentication.
   * Load certificates/keys.
   * Create socket, bind to address, begin listening.
   * Wrap the unsecure socket using the SSL context.

2. Client starts and connects to server.
   * Setup SSL context for server authentication.
   * Load certificate. 
   * Create socket.
   * Wrap unsecured socket using the SSL context
   * Connect to server.

3. Server accepts connection and begins a dedicated handler thread.
   * Listener thread creates handler thread.
   * Handler thread takes over the connection.
   * Listener thread waits for next client.
   * Handler thread waits for a message from the main thread.

4. User inputs message to main thread.
   * Main thread takes input and provides it to handler threads.
   * Handler threads maintain a local deque of messages in case one thread falls behind, the others don't have to wait to send the next message.

5. Handler sends messages over socket.

6. Client displays all received messages.
