import requests
import sys

sys.path.append("..")
try:
    from exceptions import handle_response
    from auth import JengaAuth
except ModuleNotFoundError as e:
    print(e)


class MiniStatement(JengaAuth):
    def authenticate(self, countryCode, accountNumber):
        self.countryCode = countryCode
        self.accountNumber = accountNumber
        return {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((countryCode, accountNumber)),
        }

    def retrieve(self, countryCode, accountNumber):
        """
        =============   ========    ============================================================
        accountNumber  	string  	account number
        currency	    string  	account currency
        balance  	    string  	account balance
        transactions	array	    transactions list
        date        	string	    transaction date
        chequeNumber	string	    cheque number. Applicable to current accounts only
        description 	string	    transaction description
        amount	        string	    transaction amount
        type	        string	    transaction type
        =============   ========    ============================================================
        """
        headers = self.authenticate(countryCode, accountNumber)
        if self.env == "sandbox":
            resource = (
                f"/account-test/v2/accounts/ministatement/{countryCode}/{accountNumber}"
            )
            url = self.sandbox_url + resource
            response = requests.get(url, headers=headers)
            return handle_response(response)


class FullStatement(JengaAuth):
    def authenticate(self, accountNumber, countryCode, toDate):
        self.countryCode = countryCode
        self.accountNumber = accountNumber
        self.toDate = toDate
        return {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((accountNumber, countryCode, toDate)),
        }

    def retrieve(self, payload):
        """
        Example Payload

        .. code-block:: json

            {
                "countryCode": "KE",
                "accountNumber": "0011547896523",
                "fromDate": "2018-01-18",
                "toDate": "2018-04-19",
                "limit": 20,
                "reference": "",
                "serial": "",
                "postedDateTime": "",
                "date": "",
                "runningBalance": {
                    "currency": "",
                    "amount": 0.0
                }
            }

        Example Response

        .. code-block:: json

            {
                "accountNumber": "0011547896523",
                "currency": "KES",
                "balance": 997382.57,
                "transactions": [
                    {
                        "reference": 541,
                        "date": "2018-07-13T00:00:00.000",
                        "description": "EQUITEL-BUNDLE/254764555383/8755",
                        "amount": 900,
                        "serial": 1,
                        "postedDateTime": "2018-07-13T09:51:27.000",
                        "type": "Debit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1344.57
                        }
                    },
                    {
                        "reference": "S4921027",
                        "date": "2018-07-18T00:00:00.000",
                        "description": "EAZZY-AIRTIME/EQUITEL/254764555383/100000939918/18",
                        "amount": 200,
                        "serial": 1,
                        "postedDateTime": "2018-07-18T16:27:18.000",
                        "type": "Debit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1144.57
                        }
                    },
                    {
                        "reference": 5436,
                        "date": "2018-07-19T00:00:00.000",
                        "description": "CREDIT TRANSFER",
                        "amount": 1000000,
                        "serial": 2,
                        "postedDateTime": "2018-07-19T12:01:47.000",
                        "type": "Credit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1001144.57
                        }
                    }
                ]
            }

        """

        accountNumber = payload.get("accountNumber")
        countryCode = payload.get("countryCode")
        toDate = payload.get("toDate")
        headers = self.authenticate(accountNumber, countryCode, toDate)
        if self.env == "sandbox":
            resource = f"/account-test/v2/accounts/fullstatement/"
            url = self.sandbox_url + resource
            response = requests.post(url, headers=headers, data=payload)
            return handle_response(response)
