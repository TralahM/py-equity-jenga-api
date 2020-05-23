"""
This web service enables your application to query the various registrar of persons in the various countries in East Africa.
Currently available for Kenya and Rwanda only.

https://sandbox.jengahq.io/customer-test/v2/identity/verify
"""
from .auth import JengaAuth


class IDSearchVerification(JengaAuth):
    def authenticate(self):
        """
        Headers:

        Authorization* string
        the bearer token used to access the API

        Content-Type: string
        the content type of the payload

        signature: string
        A SHA-256 signature to proof that this request is coming from the merchant.
        Build a String of concatenated values of the request fields with the following order: merchantcode documentNumber countryCode.
        The resulting text is then signed with Private Key and Base64 encoded.
        """
        pass

    def verify(identity: dict):
        """
        Params:
        identitiy:
            documentType: string
            the document type of the customer.
            for example ID, PASSPORT, ALIENID

            firstName: string
            first name as per identity document type

            lastName: string
            last name as per identity document type

            dateOfBirth: string optional
            date in YYYY-MM-DD format

            documentNumber: string
            the document id number

            countryCode: string
            the country in which the document relates to (only KE and RW enabled for now)


        Example Reponse
        .. code-block: json

            {
                "identity": {
                    "customer": {
                        "fullName": "John Doe ",
                        "firstName": "John",
                        "middlename": "",
                        "lastName": "Doe",
                        "ShortName": "John",
                        "birthDate": "1900-01-01T00:00:00",
                        "birthCityName": "",
                        "deathDate": "",
                        "gender": "",
                        "faceImage": "/9j/4AAQSkZJRgABAAEAYABgA+H8qr6n4e1O71SGFbV/sEOF3O6/N/eb71d/FGkaBVXaq9KfRRRRRUMsKSIdyr0r/9k=",
                        "occupation": "",
                        "nationality": "Refugee"
                    },
                    "documentType": "ALIEN ID",
                    "documentNumber": "654321",
                    "documentSerialNumber": "100500425",
                    "documentIssueDate": "2002-11-29T12:00:00",
                    "documentExpirationDate": "2004-11-28T12:00:00",
                    "IssuedBy": "REPUBLIC OF KENYA",
                    "additionalIdentityDetails": [
                        {
                            "documentNumber": "",
                            "documentType": "",
                            "issuedBy": ""
                        }
                    ],
                    "address": {
                        "provinceName": " ",
                        "districtName": "",
                        "locationName": "",
                        "subLocationName": "",
                        "villageName": ""
                    }
                }
            }
        """
