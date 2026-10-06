import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List


class ReceiptParser:

    def __init__(self, file_path: str):
        script_dir = Path(__file__).parent.resolve()
        target_path = script_dir / file_path

        if not target_path.exists():
            # Fall back to direct path if target_path does not exist
            target_path = Path(file_path)

        with open(target_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

    def clean_number(self, val_str: str) -> float:
        cleaned = val_str.replace(" ", "").replace(",", ".")
        return float(cleaned)

    def extract_header_info(self) -> Dict[str, Any]:
        bin_match = re.search(r"БИН\s+(\d+)", self.raw_text)
        cashier_match = re.search(r"Кассир\s+(.+)", self.raw_text)

        return {
            "bin": bin_match.group(1) if bin_match else None,
            "cashier": cashier_match.group(1).strip()
            if cashier_match
            else None,
        }

    def extract_datetime(self) -> Dict[str, str]:
        match = re.search(
            r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
            self.raw_text,
        )
        if match:
            return {
                "date": match.group(1),
                "time": match.group(2),
                "datetime": f"{match.group(1)} {match.group(2)}",
            }
        return {"date": None, "time": None, "datetime": None}

    def extract_payment_method(self) -> str:
        match = re.search(
            r"^(Банковская карта|Наличные|Карта):",
            self.raw_text,
            re.MULTILINE,
        )
        if match:
            return match.group(1)
        return "Unknown"

    def extract_total_amount(self) -> float:
        match = re.search(r"ИТОГО:\s*\n?\s*([\d\s]+,\d{2})", self.raw_text)
        if match:
            return self.clean_number(match.group(1))
        return 0.0

    def extract_items(self) -> List[Dict[str, Any]]:
        pattern = re.compile(
            r"^\s*(\d+)\.\s*\n"
            r"(.*?)\n"
            r"\s*([\d\s]+,\d{3})\s*x\s*([\d\s]+,\d{2})\s*\n"
            r"\s*([\d\s]+,\d{2})\s*\n"
            r"\s*Стоимость\s*\n"
            r"\s*([\d\s]+,\d{2})",
            re.MULTILINE | re.DOTALL,
        )

        items = []
        for match in pattern.finditer(self.raw_text):
            item_id = int(match.group(1))
            name = match.group(2).strip()
            quantity = self.clean_number(match.group(3))
            unit_price = self.clean_number(match.group(4))
            line_total = self.clean_number(match.group(6))

            items.append(
                {
                    "item_number": item_id,
                    "name": name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total,
                }
            )

        return items

    def parse(self) -> Dict[str, Any]:
        header = self.extract_header_info()
        datetime_info = self.extract_datetime()
        payment_method = self.extract_payment_method()
        receipt_total = self.extract_total_amount()
        items = self.extract_items()

        calculated_total = round(sum(item["line_total"] for item in items), 2)

        return {
            "store_info": {
                "company": "Филиал ТОО EUROPHARMA Астана",
                "bin": header["bin"],
                "cashier": header["cashier"],
            },
            "date": datetime_info["date"],
            "time": datetime_info["time"],
            "datetime": datetime_info["datetime"],
            "payment_method": payment_method,
            "calculated_total": calculated_total,
            "receipt_total": receipt_total,
            "total_matches": calculated_total == receipt_total,
            "products_count": len(items),
            "product_names": [item["name"] for item in items],
            "items": items,
        }


if __name__ == "__main__":
    parser = ReceiptParser("raw.txt")
    parsed_data = parser.parse()
    print(json.dumps(parsed_data, indent=2, ensure_ascii=False))