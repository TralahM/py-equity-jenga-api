class JengaAuth:
    def __init__(self, sandbox_url, live_url, *args, **kwargs):
        ...

    def authenticate(self):
        """
        Headers
        Authorization: the bearer token used to access the API
        signature: A SHA-256 signature to proof that this request is coming from the merchant.
        Build a String of concatenated values of the request fields with the following order: countryCode, accountNumber.
        The resulting text is then signed with Private Key and Base64 encoded.
        
        The Authentication Method should be implemented by each child to meet the required auth for its use case
        as some require additional fields to be included in the generation of the signature

        """
        pass
