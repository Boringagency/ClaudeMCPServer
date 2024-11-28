#!/usr/bin/env python3
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class CurlServer(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Default curl command
            curl_command = [
                'curl',
                '-X', 'POST',
                'http://localhost:8000/process',
                '-H', 'accept: application/json',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    "date_column": "Start Time",
                    "model_column": "Device Brand",
                    "csv_file_paths": "S5_S8_2024_11_20_15_27_33.csv,S5_S8_2024_11_25_10_10_12.csv"
                })
            ]
            
            # Execute curl command
            logger.info(f"Executing curl command: {' '.join(curl_command)}")
            process = subprocess.Popen(
                curl_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            # Check if there was an error
            if process.returncode != 0:
                logger.error(f"Curl command failed with error: {stderr.decode()}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Curl command failed",
                    "details": stderr.decode()
                }).encode())
                return
                
            # Send successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Try to parse the response as JSON
            try:
                response_data = json.loads(stdout.decode())
                self.wfile.write(json.dumps(response_data).encode())
            except json.JSONDecodeError:
                self.wfile.write(stdout)
                
            logger.info("Successfully processed request")
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Internal server error",
                "details": str(e)
            }).encode())

    def do_GET(self):
        # Simple health check endpoint
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "healthy",
            "message": "Curl server is running"
        }).encode())

def run_server(port=9000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CurlServer)
    logger.info(f"Starting curl server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()