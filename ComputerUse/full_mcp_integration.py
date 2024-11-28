import asyncio
import websockets
import json
import sys

class MCPIntegrationServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8767
        
    async def handle_connection(self, websocket):
        print("New client connected to integration server")
        try:
            async for message in websocket:
                try:
                    # Parse incoming message
                    command = json.loads(message)
                    
                    # Forward command to computer control server
                    async with websockets.connect(f'ws://{self.host}:{self.port}') as computer_ws:
                        await computer_ws.send(json.dumps(command))
                        response = await computer_ws.recv()
                        # Forward response back to client
                        await websocket.send(response)
                        
                except json.JSONDecodeError as e:
                    error_response = {
                        'status': 'error',
                        'message': f'Invalid JSON format: {str(e)}'
                    }
                    await websocket.send(json.dumps(error_response))
                except Exception as e:
                    error_response = {
                        'status': 'error',
                        'message': str(e)
                    }
                    await websocket.send(json.dumps(error_response))
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            print("Client disconnected from integration server")

    async def start_server(self):
        integration_port = 8768  # Different port from computer server
        server = await websockets.serve(
            self.handle_connection,
            self.host,
            integration_port
        )
        
        print(f"MCP Integration Server running on ws://{self.host}:{integration_port}")
        await server.wait_closed()

async def main():
    try:
        integration_server = MCPIntegrationServer()
        await integration_server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())