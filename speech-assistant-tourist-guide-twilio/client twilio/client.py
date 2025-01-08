# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'sid'
auth_token = 'token'
client = Client(account_sid, auth_token)

call = client.calls.create(
    from_="+12315998232",
    to="+33752052082",
    url="https://topical-reindeer-broadly.ngrok-free.app/incoming-call"
)

print(call.sid)