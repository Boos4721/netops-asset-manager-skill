import ssl
import socket
import datetime
import json
import sys

def get_ssl_expiry(hostname, port=443):
    """
    Get SSL certificate expiry date for a given hostname.
    """
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert['notAfter']
                expiry_date = datetime.datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.datetime.utcnow()).days
                return {
                    "hostname": hostname,
                    "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                    "days_left": days_left,
                    "status": "Healthy" if days_left > 15 else "Critical"
                }
    except Exception as e:
        return {"hostname": hostname, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(get_ssl_expiry(sys.argv[1]), indent=2))
    else:
        print("Usage: python3 ssl_check.py <domain_name>")
