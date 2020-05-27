import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


def generate_key_pair():
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    import os

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    home_dir = os.path.expanduser("~")
    if not os.path.exists(home_dir + "/.JengaApi"):
        os.mkdir(home_dir + "/.JengaApi")
    keypath = os.path.join(home_dir, ".JengaApi", "keys")
    if not os.path.exists(keypath):
        os.mkdir(keypath)
        print(f"created {keypath}")

    with open(keypath + "/private_key.pem", "wb") as fl:
        fl.write(pem)
        print(f"created {keypath+'/private_key.pem'}")
    with open(keypath + "/public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.PKCS1,
            )
        )
        print(f"created {keypath+'/public_key.pem'}")
    with open(keypath + "/certificate.pem", "wb") as f:
        f.write(
            generate_self_signed_cert(
                private_key_file=keypath + "/private_key.pem")
        )
        print(f"created {keypath+'/certificate.pem'}")

    return private_key, public_key


def generate_self_signed_cert(private_key_file=None):
    """
    Create a self-signed x509 certificate with python cryptography library
    Generates self signed certificate for a hostname, and optional IP addresses.
    """
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from datetime import timedelta
    import datetime
    import socket

    if private_key_file is None:
        generate_key_pair()

    with open(private_key_file, "rb") as pem_data:
        private_key = serialization.load_pem_private_key(
            pem_data.read(), None, default_backend()
        )

    public_key = private_key.public_key()
    one_day = timedelta(1, 0, 0)

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, socket.gethostname())])
    )
    builder = builder.issuer_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, socket.gethostname())])
    )
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(
        datetime.datetime.today() + (one_day * 365 * 5))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            [
                x509.DNSName(socket.gethostname()),
                x509.DNSName("*.%s" % socket.gethostname()),
                x509.DNSName("localhost"),
                x509.DNSName("*.localhost"),
            ]
        ),
        critical=False,
    )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )
    cert_data = certificate.public_bytes(serialization.Encoding.PEM)
    return cert_data


class JengaAuth:
    def __init__(
        self,
        authorization_token: str,
        private_key: str,
        merchant_code: str,
        env: str,
        sandbox_url="https://sandbox.jengahq.io",
        live_url="",
        *args,
        **kwargs,
    ):
        """
        :authorization_token: the bearer token used to access the API
        :merchant_code: the merchant code provided by JengaHQ
        :private_key: the path to the merchant private key
        :env: the environment in which  the API is to be used
        :sandbox_url: the url used to access the Sandbox API
        :live_url: the url used to access the Production API

        """
        self.authorization_token = authorization_token
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.private_key = private_key
        self.merchant_code = merchant_code

    def signature(self, request_hash_fields: tuple):
        """
        Build a String of concatenated values of the request fields with
        following order: as specificied by the API endpoint
        The resulting text is then signed with Private Key and Base64 encoded.

        Takes a tuple of request fields in the order that they should be
        concatenated, hashes them with SHA-256,signs the resulting hash and
        returns a Base64 encoded string of the resulting signature
        """
        data = "".join(request_hash_fields).encode()
        private_key = open(self.private_key, "r").read()
        rsa_key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA256.new()
        digest.update(data)
        sign = signer.sign(digest)
        return base64.b64encode(sign)
