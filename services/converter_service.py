import base64

import xmltodict

from exceptions.rossum import NoRossumDataError
from models.converter_models import Detail, Payable


class ConverterService:
    @staticmethod
    def _standardize_text(text: str) -> str | None:
        return " ".join(text.split()).strip() if text else None

    @staticmethod
    def process_datapoint(datapoint: dict) -> dict:
        key = datapoint.get("@schema_id")
        if not key:
            return {}
        value = ConverterService._standardize_text(datapoint.get("#text"))
        return {key: value}

    @staticmethod
    def process_section(section: list[dict] | dict) -> dict:
        result = {}
        if isinstance(section, dict):
            return ConverterService.process_datapoint(section)
        for datapoint in section:
            if processed := ConverterService.process_datapoint(datapoint):
                result.update(processed)
        return result

    @staticmethod
    def parse_raw_xml(raw_xml: str) -> dict:
        parsed_xml = xmltodict.parse(raw_xml)
        if not parsed_xml["export"]["results"]:
            raise NoRossumDataError("No data found in the XML")
        sections = parsed_xml["export"]["results"]["annotation"]["content"]["section"]
        result = {}

        for section in sections:
            schema_id = section["@schema_id"]
            datapoints = section.get("datapoint")

            if (not datapoints) and (multivalue := section.get("multivalue")):
                items = [
                    ConverterService.process_section(item.get("datapoint"))
                    for item in multivalue.get("tuple")
                ]
                result[schema_id] = items
                continue
            elif not datapoints:
                continue
            result[schema_id] = ConverterService.process_section(datapoints)
        return result

    @staticmethod
    def _get_details(parsed_xml: dict) -> list[Detail]:
        return [
            Detail(
                Amount=d.get("item_amount_total"),
                AccountId=d.get("item_account_id"),
                Quantity=d.get("item_quantity"),
                Notes=d.get("item_description"),
            )
            for d in parsed_xml.get("line_items_section", [])
        ]

    @staticmethod
    def create_structured_dict(parsed_xml: dict) -> dict:
        return Payable(
            InvoiceNumber=parsed_xml.get("basic_info_section", {}).get("document_id"),
            InvoiceDate=parsed_xml.get("basic_info_section", {}).get("date_issue"),
            DueDate=parsed_xml.get("basic_info_section", {}).get("date_due"),
            TotalAmount=parsed_xml.get("amounts_section", {}).get("amount_total"),
            Notes=parsed_xml.get("other_section", {}).get("notes"),
            Iban=parsed_xml.get("payment_info_section", {}).get("iban"),
            Amount=parsed_xml.get("amounts_section", {}).get("amount_total_base"),
            Currency=parsed_xml.get("amounts_section", {}).get("currency").upper(),
            Vendor=parsed_xml.get("vendor_section", {}).get("sender_name"),
            VendorAddress=parsed_xml.get("vendor_section", {}).get("sender_address"),
            Details=ConverterService._get_details(parsed_xml),
        ).model_dump()

    @staticmethod
    def process_xml(raw_xml: str) -> str:
        parsed_xml = ConverterService.parse_raw_xml(raw_xml)
        structured_dict = ConverterService.create_structured_dict(parsed_xml)
        xml_res = xmltodict.unparse(
            {"InvoiceRegisters": {"Invoices": {"Payable": structured_dict}}},
            pretty=True,
        )
        return base64.b64encode(xml_res.encode()).decode()


if __name__ == "__main__":
    with open("../data/raw.xml") as file:
        r = ConverterService.process_xml(file.read())
        print(r)
