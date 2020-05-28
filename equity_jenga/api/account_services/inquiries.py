import requests
import sys

sys.path.append("..")
try:
    from exceptions import handle_response
    from auth import JengaAuth
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

    def get_account_details(self, countryCode, accountNumber):
        """
        ========    ========    ============================================================
        account 	object  	account object
        number  	string  	account number
        currency	string  	account currency
        status	    string  	account status. Could be one of; Active,Inactive or Dormant
        customer	object  	customer list
        id	        string   	customer identifier
        name	    string  	customer account name
        type	    string  	customer type
        ========    ========    ============================================================
        """
        headers = self.authenticate(countryCode, accountNumber)
        if self.env == "sandbox":
            resource = f"/account-test/v2/search/{countryCode}/{accountNumber}"
            url = self.sandbox_url + resource
            response = requests.get(url, headers=headers)
            return handle_response(response)
