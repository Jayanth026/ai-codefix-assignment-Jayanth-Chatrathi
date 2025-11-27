import os
import time
import requests


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/local_fix")


TEST_CASES = [
    (
        "SQL Injection Java",
        {
            "language": "java",
            "cwe": "CWE-89",
            "vulnerability_type": "SQL Injection",
            "code": 'String query = "SELECT * FROM users WHERE id=" + userId;',
        },
    ),
    (
        "Hardcoded Secret Python",
        {
            "language": "python",
            "cwe": "CWE-798",
            "vulnerability_type": "Hardcoded Secret",
            "code": 'API_KEY = "1234567890SECRET"\nrequests.get("https://example.com", headers={"Authorization": API_KEY})',
        },
    ),
    (
        "Basic XSS JavaScript",
        {
            "language": "javascript",
            "cwe": "CWE-79",
            "vulnerability_type": "Cross-Site Scripting",
            "code": 'const userInput = location.search.substr(1);\ndocument.body.innerHTML = "Hello " + userInput;',
        },
    ),
]


def run_test_case(name: str, payload: dict):
    print(f"\n=== Test Case: {name} ===")
    start = time.time()
    try:
        resp = requests.post(API_URL, json=payload)
    except Exception as e:
        elapsed = (time.time() - start) * 1000.0
        print(f"Request failed after {elapsed:.2f} ms: {e}")
        return

    elapsed = (time.time() - start) * 1000.0
    print(f"Latency (client-side)   : {elapsed:.2f} ms")

    if resp.status_code != 200:
        print(f"Error: status={resp.status_code}, body={resp.text}")
        return

    data = resp.json()

    # These keys are provided by main.py
    print(f"Model latency (server)  : {data['latency_ms']} ms")
    print(f"Model used              : {data.get('model_used')}")
    token_usage = data.get("token_usage", {})
    print(f"Input tokens            : {token_usage.get('input_tokens')}")
    print(f"Output tokens           : {token_usage.get('output_tokens')}")

    print("Explanation:")
    print(data.get("explanation", ""))

    print("Diff:")
    print(data.get("diff", ""))

    print("Fixed code:")
    print(data.get("fixed_code", ""))


def main():
    for name, payload in TEST_CASES:
        run_test_case(name, payload)


if __name__ == "__main__":
    main()
