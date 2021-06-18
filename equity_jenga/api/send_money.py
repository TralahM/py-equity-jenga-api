"""Send Money Module."""
TransferTypes = {
    "InternalFundsTransfer": "InternalFundsTransfer",
    "MobileWallet": "MobileWallet",
    "RTGS": "RTGS",
    "SWIFT": "SWIFT",
    "EFT": "EFT",
    "PesaLink": "PesaLink",
}
DestinationTypes = {
    "mobile": "mobile",
    "bank": "bank",
}


class Source:
    """Internal Funds Transfer Source."""

    def __init__(self, account_number, name, country_code="KE"):
        """Create Source object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
            },
        }


class Dest:
    """Destination for send money."""

    def __init__(self, account_number, name, country_code="KE", type="bank"):
        """Create Dest object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code
        self.type = type

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
                "type": self.type,
            },
        }


class Transfer:
    """Funds Transfer."""

    def __init__(
        self,
        amount,
        reference,
        currencyCode,
        date,
        description,
        type="InternalFundsTransfer",
    ):
        """Create  Transfer object."""
        self.currencyCode = currencyCode
        self.amount = amount
        self.reference = reference
        self.date = date
        self.description = description
        self.type = type

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "currencyCode": self.currencyCode,
                "reference": self.reference,
                "date": self.date,
                "description": self.description,
                "amount": self.amount,
                "type": self.type,
            },
        }


class PesalinkMobileDest(Dest):
    """PesalinkMobile Destination."""

    def __init__(self, mobile_number, name, bankCode, country_code="KE"):
        """Create Dest object."""
        self.mobileNumber = mobile_number
        self.name = name
        self.countryCode = country_code
        self.type = "mobile"
        self.bankCode = bankCode

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "mobileNumber": self.mobileNumber,
                "bankCode": self.bankCode,
                "type": self.type,
            },
        }


class MobileDest(Dest):
    """Mobile Destination."""

    def __init__(
        self,
        mobile_number,
        name,
        walletName="Mpesa",
        country_code="KE",
    ):
        """Create Dest object."""
        self.mobileNumber = mobile_number
        self.name = name
        self.countryCode = country_code
        self.type = "mobile"
        self.walletName = walletName

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "mobileNumber": self.mobileNumber,
                "walletName": self.walletName,
                "type": self.type,
            },
        }


class PesalinkTransfer(Transfer):
    """Mobile Transfer."""

    def __init__(
        self,
        amount,
        reference,
        currencyCode,
        date,
        description,
        type="PesaLink",
    ):
        """Create  Transfer object."""
        self.currencyCode = currencyCode
        self.amount = amount
        self.reference = reference
        self.date = date
        self.description = description
        self.type = type


class MobileTransfer(Transfer):
    """Mobile Transfer."""

    def __init__(
        self,
        amount,
        reference,
        currencyCode,
        date,
        description,
        type="MobileWallet",
    ):
        """Create  Transfer object."""
        self.currencyCode = currencyCode
        self.amount = amount
        self.reference = reference
        self.date = date
        self.description = description
        self.type = type


class EFTTransfer(Transfer):
    """EFT Transfer."""

    def __init__(
        self,
        amount,
        reference,
        currencyCode,
        date,
        description,
        type="EFT",
    ):
        """Create  Transfer object."""
        self.currencyCode = currencyCode
        self.amount = amount
        self.reference = reference
        self.date = date
        self.description = description
        self.type = type


class SWIFTransfer(Transfer):
    """SWIFT Transfer."""

    def __init__(
        self,
        amount,
        reference,
        currencyCode,
        date,
        description,
        chargeOption="OTHER",
        type="SWIFT",
    ):
        """Create SWIFT Transfer object."""
        super().__init__(
            amount,
            reference,
            currencyCode,
            date,
            description,
            type=type,
        )
        self.chargeOption = chargeOption

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "currencyCode": self.currencyCode,
                "reference": self.reference,
                "date": self.date,
                "description": self.description,
                "amount": self.amount,
                "type": self.type,
                "chargeOption": self.chargeOption,
            },
        }


class RTGSDest(Dest):
    """RTGS Destination."""

    def __init__(self, account_number, name, bankCode, country_code="KE"):
        """Create Dest object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code
        self.type = "bank"
        self.bankCode = bankCode

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
                "type": self.type,
                "bankCode": self.bankCode,
            },
        }


class EFTDest(Dest):
    """EFT Destination."""

    def __init__(
        self,
        account_number,
        name,
        bankCode,
        branchCode,
        country_code="KE",
    ):
        """Create Dest object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code
        self.type = "bank"
        self.bankCode = bankCode
        self.branchCode = branchCode

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
                "type": self.type,
                "bankCode": self.bankCode,
                "branchCode": self.branchCode,
            },
        }


class PesalinkDest(Dest):
    """Pesa Link Bank Account Destination."""

    def __init__(
        self,
        account_number,
        mobile_number,
        name,
        bankCode,
        country_code="KE",
    ):
        """Create Dest object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code
        self.type = "bank"
        self.bankCode = bankCode
        self.mobileNumber = mobile_number

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
                "mobileNumber": self.mobileNumber,
                "type": self.type,
                "bankCode": self.bankCode,
            },
        }


class SWIFTDest(Dest):
    """SWIFT Destination."""

    def __init__(
        self,
        account_number,
        name,
        bankBic,
        addressline1,
        country_code="KE",
    ):
        """Create Dest object."""
        self.accountNumber = account_number
        self.name = name
        self.countryCode = country_code
        self.type = "bank"
        self.bankBic = bankBic
        self.addressline1 = addressline1

    def to_json(self):
        """Convert to json."""
        return {
            "source": {
                "countryCode": self.countryCode,
                "name": self.name,
                "accountNumber": self.accountNumber,
                "type": self.type,
                "bankBic": self.bankBic,
                "addressline1": self.addressline1,
            },
        }


def transfer_payload(src: Source, dst: Dest, transfer: Transfer) -> dict:
    """Return internal funds transfer payload."""
    payload = {}
    payload.update(src.to_json())
    payload.update(dst.to_json())
    payload.update(transfer.to_json())
    return payload


class IFT:
    """Within Equity bank Funds Tranfer."""

    def __init__(self, source: Source, dest: Dest, transfer: Transfer):
        """Create IFT."""
        self.source = source
        self.dest = dest
        self.transfer = transfer

    @property
    def body_payload(self):
        """Return Body Payload."""
        payload = {}
        payload.update(self.source.to_json())
        payload.update(self.dest.to_json())
        payload.update(self.transfer.to_json())
        return payload

    @property
    def sigkey(self):
        """Return text to generate signature."""
        return (
            self.source.accountNumber,
            self.transfer.amount,
            self.transfer.currencyCode,
            self.transfer.reference,
        )


class IFTMobile(IFT):
    """Within Equity to mobile funds transfer."""

    def __init__(self, source: Source, dest: MobileDest, transfer: Transfer):
        """Create IFT."""
        self.source = source
        self.dest = dest
        self.transfer = transfer

    @property
    def sigkey(self):
        """Return text to generate signature."""
        if self.dest.walletName != "Equitel":
            return (
                self.transfer.amount,
                self.transfer.currencyCode,
                self.transfer.reference,
                self.source.accountNumber,
            )
        return (
            self.source.accountNumber,
            self.transfer.amount,
            self.transfer.currencyCode,
            self.transfer.reference,
        )


class RTGS(IFT):
    """RTGS Funds Transfer."""

    @property
    def sigkey(self):
        """Return text to generate signature."""
        return (
            self.transfer.reference,
            self.transfer.date,
            self.source.accountNumber,
            self.dest.accountNumber,
            self.transfer.amount,
        )


class SWIFT(RTGS):
    """SWIFT Funds Transfer."""

    pass


class EFT(IFT):
    """EFT Funds Transfer."""

    def __init__(self, source: Source, dest: EFTDest, transfer: Transfer):
        """Create IFT."""
        self.source = source
        self.dest = dest
        self.transfer = transfer

    @property
    def sigkey(self):
        """Return text to generate signature."""
        return (
            self.transfer.reference,
            self.source.accountNumber,
            self.dest.accountNumber,
            self.transfer.amount,
            self.dest.bankCode,
        )


class Pesalink(IFT):
    """Pesalink Funds Transfer."""

    @property
    def sigkey(self):
        """Return text to generate signature."""
        return (
            self.transfer.amount,
            self.transfer.currencyCode,
            self.transfer.reference,
            self.dest.name,
            self.source.accountNumber,
        )
