def get_pesalink_banks(phonenumber):
    pass

def transaction_status(self,requestId,transferDate):
    headers={
        "Authorization":self.authorization_token,
        "Content-Type":"application/json",
    }
    data={
        "requestId": requestID,
        "destination": {
            "type": "M-Pesa"
        },
        "transfer": {
            "date": transferDate
        }
    }
    pass
