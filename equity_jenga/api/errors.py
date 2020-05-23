"""
Generic Error
{ 
   "response_status": "error",
   "response_code": "500101",
   "response_msg": "Generic error. Please contact our support."
}
Syntax Error
400 Bad Request

{ 
   "response_status": "invalid_request_error",
   "response_code": "500102",
   "response_msg": "{$.message}"
}

401 Unauthorized

{ 
   "response_status": "unauthorized",
   "response_code": "500103",
   "response_msg": "Unauthorized - Please check your Bearer token."
}

404 Not Found

{ 
   "response_status": "not_found",
   "response_code": "500104",
   "response_msg": "Resource not found"
}

500 Internal Server Error

{ 
   "response_status": "internal_server_error",
   "response_code": "500105",
   "response_msg": "Internal Server Error - Please try again later."
}

Target Error

200 OK

{ 
   "response_status": "error",
   "response_code": "{$.response code}",
   "response_msg": "{$.message}"
}

Downstream Provider Error responses
error	900101	Invalid merchant Cipher Text
error	900101	Invalid merchant certificate
error	900101	invalid merchant public key configuration -- is empty
error	900101	Invalid merchant public key configuration ---Public key is null
error	900101	Invalid merchant code provided

Merchant Authorization
error	401101	Unauthorized
error	401102	Service Not available
error	401103	Service Not available

Merchant Account/ Profile Validation
error	104101	Validation of account failed
error	104102	Merchant daily transaction limit exceeded
error	104103	Insufficient Funds
error	104104	Invalid charge configuration
error	104105	Server Error
error	104106	Server error - could not save to database
error	104107	Invalid merchant configuration - No billing account found

RTGS
error	118102	Service Not Available
error	118108	The source account has insufficient balance amount
error	103101	Invalid Account Type.
error	103102	Invalid account number .
error	103104	Insufficient funds.
error	103105	Transfer Limit Exceeded .
error	103106	Request Failed, please contact Bank.
error	103107	Invalid Currency/Transaction Amount.
error	103108	System Failure please retry .
error	103109	System malfunction .

Send Money - Within Equity Bank and Equitel
error	400103	Failed, invalid destination bank account
error	400104	Failed, insufficient funds
error	400105	Failed, general error
error	400106	Failed, destination bank error.
error	400107	Failed, destination bank error. Cut-over in progress
error	400108	Failed, destination bank error. System malfunction
error	400109	Failed, destination bank error. Duplicate transmission
error	400111	Failed, missing parameter in integration to gateway system
error	400112	Failed, could not process this request. System failure.
error	400101	Duplicate Transaction/ Payment Reference
error	400113	Failed, sender daily limit exceeded
error	103120	Failed, banking service could not process the request
error	400114	Failed, unable to process request. Third party is unavailable
error	400115	Failed, unhandled error
error	400116	Failed, 12 digit transaction reference required
error	118110	Failed, maximum transfer amount is 999,999 per transaction

Pesalink
error	100116	Failed, pesalink or destination bank error
error	100124	Failed, invalid amount
error	100128	Failed, pesalink or destination bank error
error	100130	Failed, pesalink or destination bank error
error	100134	Failed, amount less than minimum allowed
error	100207	Failed, destination cannot be found for routing
error	100209	Failed, pesalink or destination bank error
error	100210	Failed, transaction timed out
error	100211	Failed, pesalink or destination bank error
error	100232	Failed, banking service could not process the request
error	400101	Duplicate Transaction/ Payment Reference
error	100222	Failed, suspected fraud
error	400102	Failed, invalid destination bank account
error	400103	Failed, invalid destination bank account
error	400104	Failed, insufficient funds
error	400105	Failed, general error
error	400106	Failed, destination bank error.
error	400107	Failed, destination bank error. Cut-over in progress
error	400108	Failed, destination bank error. System malfunction
error	400109	Failed, destination bank error. Duplicate transmission
error	400110	Failed, bank not on pesalink
error	400111	Failed, missing parameter in integration to gateway system
error	400112	Failed, could not process this request. System failure.
error	400113	Failed, sender daily limit exceeded
error	400114	Failed, unable to process request. Third party is unavailable
error	400115	Failed, unhandled error
error	400116	Failed, 12 digit transaction reference required

Purchase Airtime
error	107101	Service Not available
error	107102	Invalid Provider
error	107103	Invalid Parameters
error	107104	Invalid Mobile Number
error	107105	Invalid Service Type
error	107106	Invalid Amount
error	107107	Payment reference Number should be 12 digits
error	107108	Authentication Failed
error	107109	The maximum amount allowed for transfers per transaction is KES 8000
error	107110	Failed. Transaction has been reversed to your Account {account}. Ref.{reference}.
error	107111	Dear Customer, we are unable to complete your request at this time. Kindly try again later. Reference Number {ref}
error	107112	Failed.Transaction Ref.#RefNo# unsuccessful. Kindly call 100 for assistance
error	400101	Duplicate Transaction/ Payment Reference

Send Money - To Mobile Wallet ( Airtel and M-PESA )
error	400101	Duplicate Transaction/ Payment Reference
error	400104	Failed, insufficient funds
error	400105	Failed, general error
error	400112	Failed, could not process this request. System failure.
error	400113	Failed, sender daily limit exceeded
error	400114	Failed, unable to process request. Third party is unavailable
error	400115	Failed, unhandled error
error	400116	Failed, 12 digit transaction reference required
error	103120	Failed, banking service could not process the request
error	105154	Failed, we cannot process your request at the moment due to system failure at Airtel
error	105156	Failed, the number is not registered for Airtel money
error	105157	Failed, credit party customer type can’t be supported by the service
error	105158	Failed, Maximum transfer amount is 70000 per transaction
error	105160	Failed, invalid mobile wallet
error	118101	Customer not registered for Equitel Mobile Banking

Bill and Till Payments
error	102101	Missing parameter
error	102102	invalid Reference Number
error	102103	Invalid Biller Code/Till Number
error	102104	Invalid Bill Reference
error	102105	Reversal Failed
error	102106	Insufficient Balance, Invalid Account
error	102107	System Failure please retry
error	102108	Reversal Failed
error	102110	Service Not available
error	400101	Duplicate Transaction/ Payment Reference

Eazzypay Push
error	114101	Merchant not registered for service
error	114102	Amount is below minimum that is allowed for transaction.
error	114103	The maximum amount limit is reached
error	114104	Customer is not registered
error	114105	Maximum daily amount per-day limit is reached for this payment
error	114106	Maximum transactions per-day limit is reached for this payment
error	114107	Invalid parameters. Kindly check with bank team
error	400101	Duplicate Transaction/ Payment Reference

Lipa na M-Pesa Online
error	117101	Bad Request - Invalid TransactionType
error	117101	Bad Request - Invalid Password
error	117101	Bad Request - Invalid PartyB
error	117101	Bad Request - Invalid CallBackURL
error	117101	Bad Request - Invalid Remarks
error	117101	Bad Request - Invalid PartyA
error	117101	Bad Request - Invalid Amount
error	117102	[MerchantValidate] - Wrong credentials
error	117102	Request failed: Output data invalid
error	117104	Error Occured: Spike Arrest Violation
error	500101	Generic error. Please contact our support.

Get Payment Status
error	111101	Failed. Invalid input parameters
error	111102	Bad request - Transaction not found.

Refund Payment
error	113101	Service Not available
error	113102	Invalid request format
error	113103	Invalid Transaction Status code for Reverse the Transaction
error	113104	Service Not available
error	113105	Due to technical problem we are not able to process your request

Identity Verification
error	115101	ID number used for search contains invalid symbols
error	115102	Serial number used for search contains invalid symbols
error	115103	At least one of search parameters should be filled
error	115104	Search can’t be done if one of mandatory fields is empty. All input parameters should be filled
error	115105	There is no record found in IPRS corresponding search parameters
error	115106	Service Not available
error	115107	Service Not available
error	115108	Service Not available
error	115109	Service Not available
error	115110	Service Not available
error	115111	Passport number contains illegal symbols
error	115112	At least one of search parameters should be filled
error	115113	Search can’t be done if one of mandatory fields is empty. All input parameters should be filled
error	115114	User can’t invoke verification methods because he didn’t pass the authorization or don’t have sufficient privileges
error	115115	Service Not available
error	115116	The image sent doesn’t correspond to the fingerprint format
error	115117	Service Not available
error	115118	Service Not available
error	115119	Service Not available

Account Balance
error	8504	No record could be retrieved

Create Bill
error	106101	Unauthorized
error	109101	invalid charge configuration
error	109102	invalid channel code
error	109103	Bill already cleared
error	109104	Invalid service configuration
error	109105	Invalid charge channel configuration code
error	109106	Invalid merchant Outlet code specified
error	109107	Invalid merchant code
error	109108	Invalid request data. Please check your payload
error	109109	Service not available

Credit & Debit Card
error	101101	Transaction could not be processed
error	101102	Transaction declined – contact issuing bank
error	101103	No reply from Processing Host
error	101104	Card has expired
error	101105	Insufficient credit
error	101106	Error Communicating with Bank
error	101107	Message Detail Error (Invalid PAN, Invalid Expiry Date)
error	101108	Transaction declined –transaction type not supported
error	101109	Bank Declined Transaction – Do Not Contact Bank
error	116101	Payment Not Updated
error	109101	invalid charge configuration
error	109102	invalid channel code
error	109103	Bill already cleared
error	109104	Invalid service configuration
error	109105	Invalid charge channel configuration code
error	109106	Invalid merchant Outlet code specified
error	109107	Invalid merchant code
error	109108	Invalid request data. Please check your payload
error	109109	Service not available

Receive Payments - Mobile Wallets
error	114101	Merchant not registered for service
error	114102	Amount is below minimum that is allowed for transaction.
error	114103	The maximum amount limit is reached
error	114104	Customer is not registered
error	114105	Maximum daily amount per-day limit is reached for this payment
error	114106	Maximum transactions per-day limit is reached for this payment
error	114107	Invalid parameters. Kindly check with bank team
error	111101	Failed. Invalid input parameters.
error	111102	Bad request - Transaction not found
error	116101	Payment Not Updated

Query Payment
error	112101	Amount paid is less or more than bill amount
error	112102	No transaction found for order ref
error	112103	Bill not found
error	112104	Invalid merchant code
error	112105	invalid service map configuration
error	112106	Due to technical problem we are not able to process your request
error	112107	Invalid service configuration
error	112108	Bill already cleared

Query Bill
error	110101	Invalid merchant code
error	110102	Invalid request data. Please check your payload
error	110103	bill doesn’t exist
"""
