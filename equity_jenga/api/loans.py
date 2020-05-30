import requests
from .auth import JengaAuth
from .exceptions import handle_response


class CreditScore(JengaAuth):
    """
    This API (first of its kind) aggregates all the Credit Reference Bureaus
    in East Africa as well as Equity Bank's own internal scoring to
    give a response on the credit worthiness (or not) of an individual.
    No need to perform countless integrations.
    This web service does it for you.
    """

    def authenticate(
        self, dateOfBirth: str, merchantCode: str, documentNumber: str
    ) -> dict:
        return {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
            "signature": self.signature((dateOfBirth, merchantCode, documentNumber)),
        }

    def credit_score(self, customer: list, bureau: dict, loan: dict) -> dict:
        """
        Example Request Payload
        customer,bureau,loan

        .. code-block:: json

            {
                "customer": [{
                    "id": "",
                    "fullName": "",
                    "firstName": "",
                    "lastName": "",
                    "shortName": "",
                    "title": "",
                    "mobileNumber": "",
                    "dateOfBirth": "1999-01-31",
                    "identityDocument": {
                        "documentType": "NationalID",
                        "documentNumber": "12365478"
                    }
                }],
                "bureau": {
                    "reportType": "Mobile",
                    "countryCode": "KE"
                },
                "loan": {
                    "amount": "5000"
                }
            }

        Example Response

        .. code-block:: json

            {
                "Person": {
                    "PersonName": {},
                    "IdentityDocument": {
                        "IdentityDocumentID": "1234568",
                        "IdentityDocumentType": "National ID"
                    }
                },
                "CreditAccountsSummary": [
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "17012014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "65000.00000",
                            "65000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "5000.00000",
                        "LastPaymentReceivedDate": "20062014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "09",
                        "AccountOpenDate": "09062011",
                        "AccountOwnership": "true",
                        "Balance": "106458.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "200000.00000",
                            "200000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "1667.00000",
                        "LastPaymentReceivedDate": "15062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "14052014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6960.00000",
                        "LastPaymentReceivedDate": "15122014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "22092014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "1000.00000",
                            "1000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "1000.00000",
                        "LastPaymentReceivedDate": "15102014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31102014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "29122014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16032015",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31032015",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "20032015",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16012016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31012016",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "N:000019:01:2015",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "06012015",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "300000.00000",
                            "300000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "20562.00000",
                        "LastPaymentReceivedDate": "27102017",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "068-P-12365478",
                            "AccountCurrency": {}
                        },
                        "AccountType": "04",
                        "AccountOpenDate": "13102011",
                        "AccountOwnership": "true",
                        "Balance": "39844.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "40000.00000",
                            "40000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2500.00000",
                        "LastPaymentReceivedDate": "16072018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "068-P-25417854",
                            "AccountCurrency": {}
                        },
                        "AccountType": "04",
                        "AccountOpenDate": "19082015",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "50000.00000",
                            "50000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2500.00000",
                        "LastPaymentReceivedDate": "13022018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "02022016",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16122016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31012017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "2569774",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "02062016",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "3000.00000",
                            "3000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "3726.00000",
                        "LastPaymentReceivedDate": "26122016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "11110571749286",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "14022017",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "120000.00000",
                            "120000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "10000.00000",
                        "LastPaymentReceivedDate": "15112017",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "JKCBDL1724301111",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "30082017",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "None",
                        "LastPaymentReceivedDate": "None",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "13122017",
                        "AccountStatus": "A",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "BCKMLD1802229762",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "08042018",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "None",
                        "LastPaymentReceivedDate": "11062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "21062018",
                        "AccountStatus": "A",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MKDLCB1814647289",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "26052018",
                        "AccountOwnership": "false",
                        "Balance": "5400.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "5400.00000",
                        "LastPaymentReceivedDate": "26052018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31052018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MKCDLB1818039369",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "29062018",
                        "AccountOwnership": "false",
                        "Balance": "2150.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "2150.00000",
                            "2150.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2150.00000",
                        "LastPaymentReceivedDate": "29062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MDLBBCK1821123688",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "29072018",
                        "AccountOwnership": "false",
                        "Balance": "2150.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "2150.00000",
                            "2150.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2150.00000",
                        "LastPaymentReceivedDate": "30072018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    }
                ],
                "CreditBureau": {
                    "score": "772",
                    "creditApplications90Days": "0",
                    "creditApplications180Days": "0",
                    "creditApplications365Days": "0",
                    "crbEnqiry90Days": "0",
                    "crbEnqiry180Days": "0",
                    "crbEnqiry365Days": "0",
                    "BouncedCheques90Days": "0",
                    "BouncedCheques180Days": "0",
                    "BouncedCheques365Days": "0",
                    "AcctNonPerformingCurrent": "0",
                    "AcctNonPerformingHisto": "0",
                    "AcctPerformingCurrent": "15",
                    "AcctPerformingHisto": "NaN",
                    "IsFraud": "false",
                    "isGuarantor": "false",
                    "delinquency_code": "No delinquency"
                }
            }

        """
        payload = {"customer": customer, "bureau": bureau, "loan": loan}
        headers = self.authenticate(
            dateOfBirth=payload.get("customer")[0].get("dateOfBirth"),
            merchantCode=self.merchant_code,
            documentNumber=payload.get("customer")[0]
            .get("identityDocument")
            .get("documentNumber"),
        )
        if self.env == "sandbox":
            url = self.sandbox_url + "/customer-test/v2/creditinfo"
            response = requests.post(url=url, headers=headers, data=payload)
            return handle_response(response)
        pass
