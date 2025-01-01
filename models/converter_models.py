from pydantic import BaseModel


class Detail(BaseModel):
    Amount: float
    AccountId: str | None = None
    Quantity: int
    Notes: str


class Payable(BaseModel):
    InvoiceNumber: str
    InvoiceDate: str
    DueDate: str
    TotalAmount: float
    Notes: str | None = None
    Iban: str
    Amount: float | None = None
    Currency: str
    Vendor: str
    VendorAddress: str
    Details: list[Detail]
