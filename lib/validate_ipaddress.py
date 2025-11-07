import ipaddress


class ValidateIPAddress:
    """Class to validate IP addresses."""

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Validates if the provided string is a valid IPv4 or IPv6 address."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
