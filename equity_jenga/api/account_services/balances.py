import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from exceptions import handle_response
    from auth import JengaAuth
except ModuleNotFoundError as e:
    print(e)


class AccountBalance(JengaAuth):
    def authenticate(self, countryCode, accountId) -> dict:
        self.countryCode = countryCode
        self.accountId = accountId
        return {
            "Authorization": self.authorization_token,
            "signature": self.signature((countryCode, accountId)),
        }

    def available(self, countryCode, accountId) -> dict:
        """
        Retrieve the current and available balance of an account

        200 Success Response Schema

        .. code-block:: json

            {
                "currency": "KES",
                "balances": [
                    {
                        "amount": "997382.57",
                        "type": "Current"
                    },
                    {
                        "amount": "997382.57",
                        "type": "Available"
                    }
                ]
            }

        """
        headers = self.authenticate(countryCode, accountId)
        if self.env == "sandbox":
            resource = f"/account-test/v2/accounts/balances/{countryCode}/{accountId}"
            url = self.sandbox_url + resource
            response = requests.get(url, headers=headers)
            return handle_response(response)

    def get_opening_and_closing(self, accountId, countryCode, date):
        """
        Example Request

        .. code-block:: json

            {
            "countryCode": "KE",
            "accountId": "0011547896523",
            "date": "2017-09-29"
            }


        Example Response

        .. code-block:: json

                {
                    "balances": [
                        {
                            "type": "Closing Balance",
                            "amount": "10810.00"
                        },
                        {
                            "type": "Opening Balance",
                            "amount": "103.00"
                        }
                    ]
                }

        """
        headers = {
            "Authorization": self.authorization_token,
            "signature": self.signature((accountId, countryCode, date)),
        }
        data = {
            "countryCode": countryCode,
            "accountId": accountId,
            "date": date,
        }
        if self.env == "sandbox":
            resource = f"/account-test/v2/accounts/accountbalance/query"
            url = self.sandbox_url + resource
            response = requests.post(url, headers=headers, data=data)
            return handle_response(response)
