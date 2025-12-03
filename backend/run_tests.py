import json
import requests

with open("tests.json", "r") as f:
    tests = json.load(f)

passed = 0

for t in tests:
    res = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": t["input"], "subject": t["subject"]}
    ).json()

    reply = res.get("reply", "").lower()
    if t["expect"].lower() in reply:
        passed += 1

print(f"Pass rate: {passed}/{len(tests)} ({passed/len(tests)*100:.1f}%)")
