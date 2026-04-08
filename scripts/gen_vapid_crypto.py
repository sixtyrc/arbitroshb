import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_vapid_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Get private key bytes (raw d value)
    private_value = private_key.private_numbers().private_value
    private_bytes = private_value.to_bytes(32, 'big')

    # Get public key bytes (uncompressed format 0x04 + x + y)
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    def b64url(b):
        return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')

    print(f"VAPID_PRIVATE_KEY={b64url(private_bytes)}")
    print(f"VAPID_PUBLIC_KEY={b64url(public_bytes)}")

if __name__ == "__main__":
    generate_vapid_keys()
