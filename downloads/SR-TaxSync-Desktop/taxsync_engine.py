# S&R TaxSync Desktop Python Core Engine v2.4
import sys
import os
import json
import xml.etree.ElementTree as ET

class TaxSyncEngine:
    def __init__(self, license_key="SRTX-PRO-2026-OFFLINE"):
        self.license_key = license_key

    def calculate_btw(self, base_amount, rate=0.21, voorbelasting=0.0):
        vat_amount = round(base_amount * rate, 2)
        total_payable = round(max(0.0, vat_amount - voorbelasting), 2)
        return {
            "base_amount": base_amount,
            "rate": rate,
            "vat_amount": vat_amount,
            "voorbelasting": voorbelasting,
            "net_payable": total_payable
        }

    def generate_xml(self, client_name, fiscal_id, calc_result):
        root = ET.Element("BelastingdienstAangifte")
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "Vendor").text = "S&R CoreSync For Intelligent Solutions"
        ET.SubElement(header, "License").text = self.license_key

        declarant = ET.SubElement(root, "Declarant")
        ET.SubElement(declarant, "Company").text = client_name
        ET.SubElement(declarant, "FiscalID").text = fiscal_id

        data = ET.SubElement(root, "Amounts")
        ET.SubElement(data, "Base").text = str(calc_result["base_amount"])
        ET.SubElement(data, "VAT").text = str(calc_result["vat_amount"])
        ET.SubElement(data, "NetPayable").text = str(calc_result["net_payable"])

        tree = ET.ElementTree(root)
        filename = f"BTW_{fiscal_id}.xml"
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"[OK] Generated XML Tax File: {filename}")
        return filename

if __name__ == "__main__":
    print("=== S&R TaxSync Desktop Engine Running ===")
    app = TaxSyncEngine()
    res = app.calculate_btw(10000, 0.21, 500)
    print("Calculation Result:", json.dumps(res, indent=2))
