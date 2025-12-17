# Krantheon OS Demo API

Deterministic, production-style API for:

- Investigate IP threats (`investigate 8.8.8.8`)
- Show alerts (`show critical alerts`)
- Risk scoring (`risk score 1.1.1.1`)
- Compliance report (`compliance report`)
- Agency dashboard
- Athlete Hub marketplace
- HCA Registry (5.6M tokenized assets - demo)
- Campaigns summary

## Local Run
pip install -r requirements.txt
uvicorn app.main:app --reload
Open: http://localhost:8000/docs

## Docker
docker build -t krantheon-os-demo .
docker run -p 8000:8000 krantheon-os-demo

## Example Command Call
curl -X POST http://localhost:8000/api/command
-H "Content-Type: application/json"
-d '{"command":"investigate 8.8.8.8","session_id":"test"}'
undefined



