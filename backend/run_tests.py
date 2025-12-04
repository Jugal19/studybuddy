import json
import requests

with open("tests.json", "r") as f:
    tests = json.load(f)

passed = 0
total = len(tests)

print("Running offline evaluation...\n")

for i, t in enumerate(tests, start=1):
    res = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": t["input"], "subject": t["subject"]}
    ).json()

    reply = res.get("reply", "").lower()
    expect = t["expect"].lower()

    if expect in reply:
        print(f"[PASS] {i}. \"{t['input']}\" → found '{expect}'")
        passed += 1
    else:
        print(f"[FAIL] {i}. \"{t['input']}\" → expected '{expect}'")
        print("Model replied:", reply[:200], "...\n")

print(f"\nPass rate: {passed}/{total} ({passed/total*100:.1f}%)")

if passed == total:
    print("\nAll tests passed! 🎉")