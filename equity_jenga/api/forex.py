import requests
from .auth import JengaAuth
from .exceptions import handle_response


class Forex(JengaAuth):
    """
    The Foreign Exchange Rates API Provides Easy Access To The Equity Bank
    Daily Currency Conversion Rate For Major Currencies
    """

    def authenticate(self) -> dict:
        return {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
        }

    def forex_rates(self, countryCode: str, currencyCode: str) -> dict:
        """
        Params

        :countryCode:: the country for which rates are being requested.
            Valid values are KE, TZ, UG, RW.

        :currencyCode:: the currency code of the currency
            that is being converted from in ISO 4217 format

        Example Request

        .. code-block:: json

            {
            "countryCode": "KE",
            "currencyCode": "USD"
            }


        Example Response
        :currencyRates:: list of conversion rates for major currencies

        .. code-block:: json

            {
            "currencyRates":[],
            "fromCurrency": "KES",
            "rate":101.3,
            "toCurrency": "USD"
            }


        """
        headers = self.authenticate()
        data = {
            "countryCode": countryCode,
            "currencyCode": currencyCode,
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/foreignexchangerates"
            response = requests.post(url=url, headers=headers, data=data)
            return handle_response(response)
        pass
