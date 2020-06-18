After installing the package, you need to generate a Public/Private Key Pair if you haven't done so already.
We provide you with a utility function to generate this pair which is stored in your home directory under a folder named **.JengaApi/keys**.
By default it is where we look for the Private key if you do not specify one when you create a JengaAPI object.
This works similarly to the **ssh-keygen** command from **SSH**.

To generate a Public/Private Key Pair using the command line tool call the script from the command line as below:

.. code-block:: console

    $ jenga_gen_key_pair

Then Proceed to copy the contents of **YOUR_HOME_DIRECTORY/.JengaApi/keys/publickey.pem** to your JengaHQ Portal.


Once you've done that you can now use the library in your code.

.. code-block:: python

    from equity_jenga import api
    jengaApi=api.auth.JengaAPI(
        api_key="Your-API-KEY-Here",
        password="YourPasswordHere",
        merchant_code="45678398098932",
        env="your environment here either sandbox or production default is sandbox"
    )

Or if you have private key else where specify the path

.. code-block:: python

    from equity_jenga import api
    jengaApi=api.auth.JengaAPI(
        api_key="Your-API-KEY-Here",
        password="YourPasswordHere",
        merchant_code="45678398098932",
        private_key="/path/to/privatekey.pem",
        env="your environment here either sandbox or production default is sandbox"
    )

Using the APIs provided by the JengaAPI class
=============================================

Account Services
-----------------

1. Account Available Balance

.. code-block:: python

    acc_balances=jengaApi.get_account_available_balance(countryCode="KE",accountId="090023816748923781")
    current=acc_balances.get("balances")[0].get("amount")
    available=acc_balances.get("balances")[1].get("amount")
    # convert the values to float from str
    current=float(current)
    available=float(available)
