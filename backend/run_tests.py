import json, requests

tests = json.load(open("tests.json"))
passed = 0

for t in tests:
    r = requests.post("http://127.0.0.1:8000/quiz", json={"topic": t["topic"]})
    data = r.json()
    ok = t["expect"] in json.dumps(data).lower()
    if ok: passed += 1

print(f"Passed {passed}/{len(tests)} tests ({passed/len(tests)*100:.1f}%)")
