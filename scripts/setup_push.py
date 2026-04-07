import pywebpush

def generate_vapid():
    private_key_b64 = pywebpush.WebPush.generate_vapid_key()
    # It returns a base64 encoded string or similar depending on the lib version
    # Actually pywebpush usually needs to generate the info
    print("VAPID Keys Generated:")
    # We will use this in .env
    pass

# We'll use a simpler way since pywebpush.WebPush doesn't directly have generate_vapid_key in all versions
# Better: use a script to print them
import os
from pywebpush import webpush

if __name__ == "__main__":
    # Generate keys
    # Note: version 1.14+ often uses this
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    
    # Base64 URL safe without padding
    import base64
    def b64url(data):
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    # Convert to keys
    # Actually, pywebpush has its own utility sometimes. Let's just output them as required by django-push-notifications
    print("Please use a VAPID generator or I can output some random valid ones for test.")
