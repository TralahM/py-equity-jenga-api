import requests
import sys

sys.path.append("..")
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

    def get(self, countryCode, accountId) -> dict:
        """
        200 Success Response Schema

        Field Name	Field Type	Field Description
        currency	string	account currency
        balances	array	array of balances
        amount	string	account balance
        type	string	account balance type
        """
        headers = self.authenticate(countryCode, accountId)
        if self.env == "sandox":
            resource = f"/account-test/v2/accounts/balances/{countryCode}/{accountId}"
            url = self.sandbox_url + resource
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return handle_response(response)
