import socket
import requests
import logging

class NetworkManager:
    def __init__(self):
        self.session = requests.Session()
    
    def check_internet_connection(self) -> bool:
        """
        Check if there is an active internet connection.
        
        Returns:
            bool: True if internet is connected, False otherwise
        """
        try:
            # Try to connect to a reliable host
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            # Optional: Also check if we can reach alttpr.com
            requests.get("https://alttpr.com/", timeout=5)
            return True
        except (socket.error, requests.RequestException) as e:
            logging.error(f"Internet connection check failed: {e}")
            return False