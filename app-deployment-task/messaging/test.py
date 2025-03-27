import requests

BASE_URL = "https://7892-197-210-76-101.ngrok-free.app"  

def test_sendmail():
    print("Testing /sendmail endpoint:")
    response = requests.get(f"{BASE_URL}/sendmail", params={"sendmail": "test@example.com"})
    print(response.json())

def test_talktome():
    print("\nTesting /talktome endpoint:")
    response = requests.get(f"{BASE_URL}/talktome")
    print(response.json())

def test_logs():
    print("\nTesting /logs endpoint:")
    response = requests.get(f"{BASE_URL}/logs")
    print(f"Total log lines: {len(response.json().get('logs', []))}")

def main():
    test_sendmail()
    test_talktome()
    test_logs()

if __name__ == "__main__":
    main()