import ipaddress

class Ip_Validator:
    """ Class that helps to manage validations for IP addresses """
    
    def validate_ip_address(ip_string) -> bool:
        """ Validates a given IP address by creating an ipaddress object """
        try:
            ipaddress.ip_address(ip_string)
        except ValueError:
            return False   
        
        return True