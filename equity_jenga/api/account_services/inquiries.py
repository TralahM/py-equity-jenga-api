import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from auth import JengaAuth
    from exceptions import handle_response
except ModuleNotFoundError as e:
    print(e)


class AccountInquiry(JengaAuth):
    def authenticate(self, countryCode, accountNumber):
        self.countryCode = countryCode
        self.accountNumber = accountNumber
        return {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((countryCode, accountNumber)),
        }

    def account_details(self, countryCode, accountNumber):
        """
        Example Response

        .. code-block:: json

            {
                "account": {
                    "number": "0011547896523",
                    "branchCode": "017",
                    "currency": "KES",
                    "status": "Active"
                },
                "customer": [
                    {
                        "id": "100200300",
                        "name": "A N.Other",
                        "type": "Retail"
                    }
                ]
            }


        """
        headers = self.authenticate(countryCode, accountNumber)
        if self.env == "sandbox":
            resource = f"/account-test/v2/search/{countryCode}/{accountNumber}"
            url = self.sandbox_url + resource
            response = requests.get(url, headers=headers)
            return handle_response(response)
