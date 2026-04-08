from pywebpush import vapid_auth_issue
import json

def generate_keys():
    keys = vapid_auth_issue()
    result = {
        "VAPID_PUBLIC_KEY": keys["public_key"],
        "VAPID_PRIVATE_KEY": keys["private_key"]
    }
    with open(".tmp/vapid_keys.json", "w") as f:
        json.dump(result, f, indent=4)
    print("VAPID Keys generated and saved to .tmp/vapid_keys.json")

if __name__ == "__main__":
    generate_keys()
