"""
Example Request

..code-block:: console

    curl -X POST \
        -d '{
    "source": {
        "countryCode": "KE",
        "name": "Tom Doe",
        "accountNumber": "0011547896523"
    },
    "destination": {
        "type": "mobile",
        "countryCode": "KE",
        "name": "John Doe",
        "mobileNumber": "0763555619",
        "walletName": "Equitel"
    },
    "transfer": {
        "type": "MobileWallet",
        "amount": "20",
        "currencyCode": "KES",
        "reference": "692194625798",
        "date": "2019-05-01",
        "description": "Some remarks here"
    }
    }'  \
        -H 'Authorization: Bearer {access_token}'  \
        -H 'Content-Type: application/json'  \
        -H 'signature: e967CLKebZyLfa73/YYltjW5M4cHoyWeHi/5VDKJ64gOwKBvzHJRqJJrBBc34v2m4jyKkDMBtfRJeFlxbNisMAeBtkw0TRcD2LThFK27EOqLM3m8rQYa+7CJ2FhPhK+iOa4RUY+vTfkRX5JXuqOW7a3GHds8qyPaPe19cKUY33eAJL3upXnGnA3/PEhzjhb0pqk2zCI7aRzvjjVUGwUdT6LO73NVhDSWvGpLEsP0dH/stC5BoTPNNt9nY8yvGUPV7fmaPSIFn68W4L04WgePQdYkmD1UPApGcrl+L2ALY3lPaRfI6/N+0Y3NIWQyLgix+69k7V4EGolqejWdion+9A=='  \
        -L 'https://sandbox.jengahq.io/transaction-test/v2/remittance'

Example Request

..code-block:: json

    {
        "transactionId": "45865",
        "status": "SUCCESS"
    }


"""
MobileWalletDestination = {
    "type": "mobile",
    "countryCode": "KE",
    "name": "John Doe",
    "mobileNumber": "0763555619",
    "walletName": "Equitel",
}

PesaLinkMobileDestination = {
    "type": "mobile",
    "countryCode": "KE",
    "name": "Tom Doe",
    "bankCode": "01",
    "mobileNumber": "0722000000",
}

RTGSDestination = {
    "type": "bank",
    "countryCode": "KE",
    "name": "Tom Doe",
    "bankCode": "70",
    "accountNumber": "12365489",
}

PesaLinkDestination = {
    "type": "bank",
    "countryCode": "KE",
    "name": "Tom Doe",
    "bankCode": "63",
    "accountNumber": "0090207635001",
}

ETSDestination = {
    "type": "bank",
    "countryCode": "KE",
    "name": "Tom Doe",
    "bankCode": "01",
    "branchCode": "112",
    "accountNumber": "54545",
}

SWIFTDestination = {
    "type": "bank",
    "countryCode": "JP",
    "name": "Tom Doe",
    "bankBic": "BOTKJPJTXXX",
    "accountNumber": "12365489",
    "addressline1": "Post Box 56",
}
