"""
Example Request

..code-block:: console

    curl -X POST \
        -d '{
    "source": {
        "countryCode": "KE",
        "name": "John Doe",
        "accountNumber": "0011547896523"
    },
    "destination": {
        "type": "bank",
        "countryCode": "KE",
        "name": "Tom Doe",
        "accountNumber": "0060161911111"
    },
    "transfer": {
        "type": "InternalFundsTransfer",
        "amount": "100.00",
        "currencyCode": "KES",
        "reference": "742194625798",
        "date": "2019-05-01",
        "description": "Some remarks here"
    }
    }'  \
        -H 'Authorization: Bearer {access_token}'  \
        -H 'Content-Type: application/json'  \
        -H 'signature: e967CLKebZyLfa73/YYltjW5M4cHoyWeHi/5VDKJ64gOwKBvzHJRqJJrBBc34v2m4jyKkDMBtfRJeFlxbNisMAeBtkw0TRcD2LThFK27EOqLM3m8rQYa+7CJ2FhPhK+iOa4RUY+vTfkRX5JXuqOW7a3GHds8qyPaPe19cKUY33eAJL3upXnGnA3/PEhzjhb0pqk2zCI7aRzvjjVUGwUdT6LO73NVhDSWvGpLEsP0dH/stC5BoTPNNt9nY8yvGUPV7fmaPSIFn68W4L04WgePQdYkmD1UPApGcrl+L2ALY3lPaRfI6/N+0Y3NIWQyLgix+69k7V4EGolqejWdion+9A=='  \
        -L 'https://sandbox.jengahq.io/transaction-test/v2/remittance'



Example Response

..code-block:: json

    {
        "transactionId": "1452854",
        "status": "SUCCESS"
    }


"""
InternalTransferSrc={
    "countryCode":"KE",
    "name":"John Doe",
    "accountNumber":"0011547896523",
}
InternalTransferDestination= {
      "type": "bank",
      "countryCode": "KE",
      "name": "Tom Doe",
      "accountNumber": "0060161911111",
}
InternalTransfer = {
      "type": "InternalFundsTransfer",
      "amount": "100.00",
      "currencyCode": "KES",
      "reference": "742194625798",
      "date": "2019-05-01",
      "description": "Some remarks here",
}
