import base64

import pytest
import xmltodict

from exceptions.rossum import NoRossumDataError
from services.converter_service import ConverterService


def test_parse_raw_xml(raw_xml):
    parsed_xml = ConverterService.parse_raw_xml(raw_xml)
    assert parsed_xml == {
        "amounts_section": {
            "amount_total": "1045383.35",
            "amount_total_base": "909029.00",
            "amount_total_tax": "136354.35",
            "currency": "czk",
        },
        "basic_info_section": {
            "date_due": "2022-02-28",
            "date_issue": "2022-01-04",
            "document_id": "43543687",
            "document_type": "tax_invoice",
            "language": "eng",
            "order_id": "PO5475375",
        },
        "line_items_section": [
            {
                "item_amount": "2.90",
                "item_amount_base": None,
                "item_amount_total": "14500.00",
                "item_code": None,
                "item_description": "Rohlík 30 g",
                "item_quantity": "5000",
                "item_uom": None,
            },
            {
                "item_amount": "43.90",
                "item_amount_base": None,
                "item_amount_total": "133895.00",
                "item_code": None,
                "item_description": "Chléb kváskový 450 g",
                "item_quantity": "3050",
                "item_uom": None,
            },
            {
                "item_amount": "5.90",
                "item_amount_base": None,
                "item_amount_total": "26550.00",
                "item_code": None,
                "item_description": "Houska celozrná 30 g",
                "item_quantity": "4500",
                "item_uom": None,
            },
            {
                "item_amount": "18.90",
                "item_amount_base": None,
                "item_amount_total": "160650.00",
                "item_code": None,
                "item_description": "Makový šáteček 120 g",
                "item_quantity": "8500",
                "item_uom": None,
            },
            {
                "item_amount": "125.67",
                "item_amount_base": None,
                "item_amount_total": "25134.00",
                "item_code": None,
                "item_description": "Vánočka 750 g",
                "item_quantity": "200",
                "item_uom": None,
            },
            {
                "item_amount": "178.60",
                "item_amount_base": None,
                "item_amount_total": "89300.00",
                "item_code": None,
                "item_description": "Tvarohová buchta, plech 750 g",
                "item_quantity": "500",
                "item_uom": None,
            },
            {
                "item_amount": "45.90",
                "item_amount_base": None,
                "item_amount_total": "459000.00",
                "item_code": None,
                "item_description": "Pražský koláč 230 g",
                "item_quantity": "10000",
                "item_uom": None,
            },
        ],
        "other_section": {"notes": None},
        "payment_info_section": {
            "account_num": "45-567894324",
            "bic": "CZMOUTYDD",
            "iban": "CZ22 3405 6455 6789 4324",
            "spec_sym": None,
            "var_sym": None,
        },
        "vendor_section": {
            "recipient_address": "Moscow 119333 Russia",
            "recipient_delivery_address": "65/8 Ulitsa Gavrilova Moscow 119567 Russia",
            "recipient_delivery_name": "Kurtky&Kurtki",
            "recipient_ic": None,
            "recipient_name": None,
            "recipient_vat_id": "582902578",
            "sender_address": "Pivovarská 34 Kozmice Česká republika",
            "sender_ic": "67890324",
            "sender_name": "Kurtky&Kurtki",
            "sender_vat_id": "CZ67890324",
        },
    }


def test_parse_raw_xml_no_data():
    with pytest.raises(NoRossumDataError):
        ConverterService.parse_raw_xml("<export><results></results></export>")


def test_create_structured_dict(raw_xml):
    parsed_xml = ConverterService.parse_raw_xml(raw_xml)
    structured_dict = ConverterService.create_structured_dict(parsed_xml)
    assert structured_dict == {
        "Amount": 909029.0,
        "Currency": "CZK",
        "Details": [
            {
                "AccountId": None,
                "Amount": 14500.0,
                "Notes": "Rohlík 30 g",
                "Quantity": 5000,
            },
            {
                "AccountId": None,
                "Amount": 133895.0,
                "Notes": "Chléb kváskový 450 g",
                "Quantity": 3050,
            },
            {
                "AccountId": None,
                "Amount": 26550.0,
                "Notes": "Houska celozrná 30 g",
                "Quantity": 4500,
            },
            {
                "AccountId": None,
                "Amount": 160650.0,
                "Notes": "Makový šáteček 120 g",
                "Quantity": 8500,
            },
            {
                "AccountId": None,
                "Amount": 25134.0,
                "Notes": "Vánočka 750 g",
                "Quantity": 200,
            },
            {
                "AccountId": None,
                "Amount": 89300.0,
                "Notes": "Tvarohová buchta, plech 750 g",
                "Quantity": 500,
            },
            {
                "AccountId": None,
                "Amount": 459000.0,
                "Notes": "Pražský koláč 230 g",
                "Quantity": 10000,
            },
        ],
        "DueDate": "2022-02-28",
        "Iban": "CZ22 3405 6455 6789 4324",
        "InvoiceDate": "2022-01-04",
        "InvoiceNumber": "43543687",
        "Notes": None,
        "TotalAmount": 1045383.35,
        "Vendor": "Kurtky&Kurtki",
        "VendorAddress": "Pivovarská 34 Kozmice Česká republika",
    }


def test_process_xml(raw_xml):
    result = ConverterService.process_xml(raw_xml)
    decoded_result = base64.b64decode(result).decode()
    parsed_result = xmltodict.parse(decoded_result)
    assert (
        result
        == "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPEludm9pY2VSZWdpc3RlcnM+Cgk8SW52b2ljZXM+CgkJPFBheWFibGU+CgkJCTxJbnZvaWNlTnVtYmVyPjQzNTQzNjg3PC9JbnZvaWNlTnVtYmVyPgoJCQk8SW52b2ljZURhdGU+MjAyMi0wMS0wNDwvSW52b2ljZURhdGU+CgkJCTxEdWVEYXRlPjIwMjItMDItMjg8L0R1ZURhdGU+CgkJCTxUb3RhbEFtb3VudD4xMDQ1MzgzLjM1PC9Ub3RhbEFtb3VudD4KCQkJPE5vdGVzPjwvTm90ZXM+CgkJCTxJYmFuPkNaMjIgMzQwNSA2NDU1IDY3ODkgNDMyNDwvSWJhbj4KCQkJPEFtb3VudD45MDkwMjkuMDwvQW1vdW50PgoJCQk8Q3VycmVuY3k+Q1pLPC9DdXJyZW5jeT4KCQkJPFZlbmRvcj5LdXJ0a3kmYW1wO0t1cnRraTwvVmVuZG9yPgoJCQk8VmVuZG9yQWRkcmVzcz5QaXZvdmFyc2vDoSAzNCBLb3ptaWNlIMSMZXNrw6EgcmVwdWJsaWthPC9WZW5kb3JBZGRyZXNzPgoJCQk8RGV0YWlscz4KCQkJCTxBbW91bnQ+MTQ1MDAuMDwvQW1vdW50PgoJCQkJPEFjY291bnRJZD48L0FjY291bnRJZD4KCQkJCTxRdWFudGl0eT41MDAwPC9RdWFudGl0eT4KCQkJCTxOb3Rlcz5Sb2hsw61rIDMwIGc8L05vdGVzPgoJCQk8L0RldGFpbHM+CgkJCTxEZXRhaWxzPgoJCQkJPEFtb3VudD4xMzM4OTUuMDwvQW1vdW50PgoJCQkJPEFjY291bnRJZD48L0FjY291bnRJZD4KCQkJCTxRdWFudGl0eT4zMDUwPC9RdWFudGl0eT4KCQkJCTxOb3Rlcz5DaGzDqWIga3bDoXNrb3bDvSA0NTAgZzwvTm90ZXM+CgkJCTwvRGV0YWlscz4KCQkJPERldGFpbHM+CgkJCQk8QW1vdW50PjI2NTUwLjA8L0Ftb3VudD4KCQkJCTxBY2NvdW50SWQ+PC9BY2NvdW50SWQ+CgkJCQk8UXVhbnRpdHk+NDUwMDwvUXVhbnRpdHk+CgkJCQk8Tm90ZXM+SG91c2thIGNlbG96cm7DoSAzMCBnPC9Ob3Rlcz4KCQkJPC9EZXRhaWxzPgoJCQk8RGV0YWlscz4KCQkJCTxBbW91bnQ+MTYwNjUwLjA8L0Ftb3VudD4KCQkJCTxBY2NvdW50SWQ+PC9BY2NvdW50SWQ+CgkJCQk8UXVhbnRpdHk+ODUwMDwvUXVhbnRpdHk+CgkJCQk8Tm90ZXM+TWFrb3bDvSDFocOhdGXEjWVrIDEyMCBnPC9Ob3Rlcz4KCQkJPC9EZXRhaWxzPgoJCQk8RGV0YWlscz4KCQkJCTxBbW91bnQ+MjUxMzQuMDwvQW1vdW50PgoJCQkJPEFjY291bnRJZD48L0FjY291bnRJZD4KCQkJCTxRdWFudGl0eT4yMDA8L1F1YW50aXR5PgoJCQkJPE5vdGVzPlbDoW5vxI1rYSA3NTAgZzwvTm90ZXM+CgkJCTwvRGV0YWlscz4KCQkJPERldGFpbHM+CgkJCQk8QW1vdW50Pjg5MzAwLjA8L0Ftb3VudD4KCQkJCTxBY2NvdW50SWQ+PC9BY2NvdW50SWQ+CgkJCQk8UXVhbnRpdHk+NTAwPC9RdWFudGl0eT4KCQkJCTxOb3Rlcz5UdmFyb2hvdsOhIGJ1Y2h0YSwgcGxlY2ggNzUwIGc8L05vdGVzPgoJCQk8L0RldGFpbHM+CgkJCTxEZXRhaWxzPgoJCQkJPEFtb3VudD40NTkwMDAuMDwvQW1vdW50PgoJCQkJPEFjY291bnRJZD48L0FjY291bnRJZD4KCQkJCTxRdWFudGl0eT4xMDAwMDwvUXVhbnRpdHk+CgkJCQk8Tm90ZXM+UHJhxb5za8O9IGtvbMOhxI0gMjMwIGc8L05vdGVzPgoJCQk8L0RldGFpbHM+CgkJPC9QYXlhYmxlPgoJPC9JbnZvaWNlcz4KPC9JbnZvaWNlUmVnaXN0ZXJzPg=="
    )
    assert parsed_result == {
        "InvoiceRegisters": {
            "Invoices": {
                "Payable": {
                    "Amount": "909029.0",
                    "Currency": "CZK",
                    "Details": [
                        {
                            "AccountId": None,
                            "Amount": "14500.0",
                            "Notes": "Rohlík 30 g",
                            "Quantity": "5000",
                        },
                        {
                            "AccountId": None,
                            "Amount": "133895.0",
                            "Notes": "Chléb kváskový 450 g",
                            "Quantity": "3050",
                        },
                        {
                            "AccountId": None,
                            "Amount": "26550.0",
                            "Notes": "Houska celozrná 30 g",
                            "Quantity": "4500",
                        },
                        {
                            "AccountId": None,
                            "Amount": "160650.0",
                            "Notes": "Makový šáteček 120 g",
                            "Quantity": "8500",
                        },
                        {
                            "AccountId": None,
                            "Amount": "25134.0",
                            "Notes": "Vánočka 750 g",
                            "Quantity": "200",
                        },
                        {
                            "AccountId": None,
                            "Amount": "89300.0",
                            "Notes": "Tvarohová buchta, plech 750 g",
                            "Quantity": "500",
                        },
                        {
                            "AccountId": None,
                            "Amount": "459000.0",
                            "Notes": "Pražský koláč 230 g",
                            "Quantity": "10000",
                        },
                    ],
                    "DueDate": "2022-02-28",
                    "Iban": "CZ22 3405 6455 6789 4324",
                    "InvoiceDate": "2022-01-04",
                    "InvoiceNumber": "43543687",
                    "Notes": None,
                    "TotalAmount": "1045383.35",
                    "Vendor": "Kurtky&Kurtki",
                    "VendorAddress": "Pivovarská 34 Kozmice Česká republika",
                }
            }
        }
    }


def test_process_xml_output(raw_xml, expected_xml):
    result = ConverterService.process_xml(raw_xml)
    decoded_result = base64.b64decode(result).decode()
    result_dict = xmltodict.parse(decoded_result)
    expected_dict = xmltodict.parse(expected_xml)

    assert result_dict == expected_dict
