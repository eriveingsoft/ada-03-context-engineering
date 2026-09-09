from dataclasses import dataclass 
import re 

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$") 

@dataclass 
class Customer: 
    customer_id: int 
    name: str 
    email: str 
    created_by: str 
    updated_by: str 
 
def update_customer_email(customer, new_email, updated_by): 
    if not isinstance(new_email, str): 
        raise ValueError("invalid-email") 
    normalized_email = new_email.strip().lower() 
    if not EMAIL_REGEX.match(normalized_email): 
        raise ValueError("invalid-email") 
    customer.email = normalized_email 
    customer.updated_by = updated_by 
    return customer 