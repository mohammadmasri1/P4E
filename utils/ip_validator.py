import ipaddress
from typing import Set

def is_valid_ip(ip: str) -> bool:
    """Validate if the given string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def check_ip_access(ip: str, allowed_ips: Set[str]) -> bool:
    """
    Check if an IP address is in the allowed list.
    Args:
        ip (str): IP address to check
        allowed_ips (Set[str]): Set of allowed IP addresses
    Returns:
        bool: True if IP is allowed, False otherwise
    """
    if not is_valid_ip(ip):
        return False
    return ip in allowed_ips
