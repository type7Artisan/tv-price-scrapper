from typing import Dict, Any
from dataclasses import dataclass
from decimal import Decimal
import re

@dataclass
class ProductValidationError(Exception):
    message: str
    details: Dict[str, Any] = None

class ProductValidator:
    @staticmethod
    def validate_price(price: str) -> bool:
        try:
            cleaned_price = re.sub(r'[^\d.]', '', price)
            price_decimal = Decimal(cleaned_price)
            return 0 < price_decimal < 100000  # Reasonable price range for TVs
        except:
            return False

    @staticmethod
    def validate_product_data(product_data: Dict) -> None:
        required_fields = ['brand', 'website', 'title', 'price']
        
        for field in required_fields:
            if field not in product_data:
                raise ProductValidationError(f"Missing required field: {field}")
        
        if not ProductValidator.validate_price(product_data['price']):
            raise ProductValidationError(
                "Invalid price format or value",
                {"price": product_data['price']}
            ) 