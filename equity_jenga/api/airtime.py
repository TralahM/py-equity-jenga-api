import requests
from .auth import JengaAuth
from .exceptions import handle_response, generate_reference


class Airtime(JengaAuth):
    """
    This gives an application the ability to purchase airtime from any telco in
    East and Central Africa.
    """

    def authenticate(
        self,
        merchantCode: str,
        airtimeTelco: str,
        airtimeAmount: str,
        airtimeReference: str,
    ) -> dict:
        fields = (merchantCode, airtimeTelco, airtimeAmount, airtimeReference)
        return {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
            "signature": self.signature(fields),
        }

    def purchase_airtime(self, customer: dict, airtime: dict) -> dict:
        """
        Example Request
        :countryCode:: the telco's ISO country code
        :mobileNumber:: the mobile number you are purchasing airtime for

        :Telco:: the telco/provider. For example: Equitel, Safaricom , Airtel.
        :reference:: your transaction references. Should always be a 12 digit string
        :amount:: the airtime amount string

        .. code-block:: json

            {
                "customer": {
                    "countryCode": "KE",
                    "mobileNumber": "0765555131"
                },
                "airtime": {
                    "amount": "100",
                    "reference": "692194625798",
                    "telco": "Equitel"
                }
            }


        Example Response

        .. code-block:: json

            {
                "referenceNumber": "4568899373748",
                "status": "SUCCESS"
            }

        """
        airtime["reference"] = generate_reference()
        payload = {
            "customer": customer,
            "airtime": airtime,
        }
        headers = self.authenticate(
            merchantCode=self.merchant_code,
            airtimeTelco=airtime.get("telco"),
            airtimeAmount=airtime.get("amount"),
            airtimeReference=airtime.get("reference"),
        )
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/airtime"
            response = requests.post(url=url, headers=headers, data=payload)
            return handle_response(response)
        pass
