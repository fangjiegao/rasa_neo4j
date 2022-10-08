# coding=utf-8

REQUEST_URL = "http://localhost:5005/webhooks/rest/webhook"
HEADERS = {'Content-Type': 'application/json; charset=utf-8'}

# curl -H "Content-Type:application/json" -H "Data_Type:msg" -XPOST --data '{"sender": "gfj", "message": "今天南京天气"}' http://localhost:5005/webhooks/rest/webhook | native2ascii -encoding UTF-8 -reverse
