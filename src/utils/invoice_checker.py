from decimal import Decimal, InvalidOperation
from typing import Dict, List, Any, Union


def validate_invoice_data(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the mathematical consistency of invoice data with exact precision.
    Uses Decimal for precise calculations to avoid floating point errors.

    Args:
        invoice_data (dict): Invoice data in JSON format

    Returns:
        dict: Validation results with 'is_valid' boolean and list of 'errors'
    """
    errors = []

    def to_decimal(
        value: Any, field_name: str, require_type: type = None
    ) -> Union[Decimal, None]:
        """Convert value to Decimal for exact calculations, with optional strict type enforcement"""
        if value is None:
            return None

        if require_type is not None and not isinstance(value, require_type):
            if isinstance(require_type, tuple):
                type_names = ", ".join([t.__name__ for t in require_type])
            else:
                type_names = require_type.__name__
            errors.append(f"Field '{field_name}' must be of type {type_names}")
            return None

        try:
            # Handle string representations of numbers only if not enforcing type
            if require_type is None and isinstance(value, str):
                value = value.strip()
                if value == "":
                    return None
                return Decimal(value)

            # Handle numeric types
            if isinstance(value, (int, float)):
                return Decimal(str(value))

            errors.append(f"Field '{field_name}' must be numeric")
            return None

        except (InvalidOperation, ValueError, TypeError):
            errors.append(f"Field '{field_name}' contains invalid numeric value")
            return None

    def validate_numeric_field(
        field_name: str,
        value: Any,
        allow_negative: bool = False,
        min_value: Union[Decimal, int, float] = None,
        max_value: Union[Decimal, int, float] = None,
        require_type: type = None,
    ) -> bool:
        """Helper function to validate numeric fields with exact precision and optional strict type"""
        if value is None:
            return True  # None values are handled separately

        decimal_value = to_decimal(value, field_name, require_type=require_type)
        if decimal_value is None:
            return False  # Error already added by to_decimal

        # Check sign constraint
        if not allow_negative and decimal_value < 0:
            errors.append(f"Field '{field_name}' must be positive")
            return False

        # Check range constraints
        if min_value is not None:
            min_decimal = Decimal(str(min_value))
            if decimal_value < min_decimal:
                errors.append(f"Field '{field_name}' must be at least {min_decimal}")
                return False

        if max_value is not None:
            max_decimal = Decimal(str(max_value))
            if decimal_value > max_decimal:
                errors.append(f"Field '{field_name}' must be at most {max_decimal}")
                return False

        return True

    def safe_get_decimal(
        data: Dict[str, Any], key: str, context: str = "", require_type: type = None
    ) -> Union[Decimal, None]:
        """Safely get and convert a value to Decimal, with optional strict type enforcement"""
        if key not in data or data[key] is None:
            return None

        field_name = f"{context}.{key}" if context else key
        return to_decimal(data[key], field_name, require_type=require_type)

    # 1. Validate required fields are present and not empty
    required_fields = ["invoice_number", "invoice_date", "total"]
    for field in required_fields:
        if field not in invoice_data or invoice_data[field] is None:
            errors.append(f"Missing required field: {field}")
        elif isinstance(invoice_data[field], str) and invoice_data[field].strip() == "":
            errors.append(f"Required field '{field}' cannot be empty")

    # 2. Validate supplier information
    if "supplier" not in invoice_data or invoice_data["supplier"] is None:
        errors.append("Missing required field: supplier")
    elif not isinstance(invoice_data["supplier"], dict):
        errors.append("Field 'supplier' must be an object")
    else:
        supplier = invoice_data["supplier"]
        if "name" not in supplier or supplier["name"] is None:
            errors.append("Missing required field: supplier.name")
        elif isinstance(supplier["name"], str) and supplier["name"].strip() == "":
            errors.append("Field 'supplier.name' cannot be empty")

    # 3. Validate client information
    if "client" not in invoice_data or invoice_data["client"] is None:
        errors.append("Missing required field: client")
    elif not isinstance(invoice_data["client"], dict):
        errors.append("Field 'client' must be an object")
    else:
        client = invoice_data["client"]
        if "name" not in client or client["name"] is None:
            errors.append("Missing required field: client.name")
        elif isinstance(client["name"], str) and client["name"].strip() == "":
            errors.append("Field 'client.name' cannot be empty")

    # 4. Validate items array structure
    if "items" not in invoice_data or invoice_data["items"] is None:
        errors.append("Missing required field: items")
    elif not isinstance(invoice_data["items"], list):
        errors.append("Field 'items' must be an array")
    elif len(invoice_data["items"]) == 0:
        errors.append("Invoice must contain at least one item")
    else:
        # Validate each item structure
        for i, item in enumerate(invoice_data["items"]):
            if not isinstance(item, dict):
                errors.append(f"Item {i+1} must be an object")
                continue

            required_item_fields = [
                "description",
                "quantity",
                "unit_price",
                "total_price",
            ]
            missing_fields = [
                field
                for field in required_item_fields
                if field not in item or item[field] is None
            ]
            for field in missing_fields:
                errors.append(f"Item {i+1}: missing required field '{field}'")
            # Only run further validation if all required fields are present
            if not missing_fields:
                if (
                    "description" in item
                    and isinstance(item["description"], str)
                    and item["description"].strip() == ""
                ):
                    errors.append(f"Item {i+1}: description cannot be empty")

    # 5. Validate currency if present
    if "currency" in invoice_data and invoice_data["currency"] is not None:
        if not isinstance(invoice_data["currency"], str):
            errors.append("Currency must be a string")
        elif invoice_data["currency"].strip() == "":
            errors.append("Currency cannot be empty")

    # 6. Validate core numeric fields
    validate_numeric_field(
        "subtotal", invoice_data.get("subtotal"), require_type=(int, float, Decimal)
    )
    validate_numeric_field(
        "total", invoice_data.get("total"), require_type=(int, float, Decimal)
    )
    validate_numeric_field(
        "tax", invoice_data.get("tax"), require_type=(int, float, Decimal)
    )
    validate_numeric_field(
        "shipping_cost",
        invoice_data.get("shipping_cost"),
        require_type=(int, float, Decimal),
    )
    validate_numeric_field(
        "discount", invoice_data.get("discount"), require_type=(int, float, Decimal)
    )
    validate_numeric_field(
        "discount_percentage",
        invoice_data.get("discount_percentage"),
        min_value=0,
        max_value=100,
        require_type=(int, float, Decimal),
    )
    validate_numeric_field(
        "rounding_adjustment",
        invoice_data.get("rounding_adjustment"),
        allow_negative=True,
        require_type=(int, float, Decimal),
    )

    # 7. Validate line items and their calculations
    client_valid = (
        "client" in invoice_data
        and isinstance(invoice_data["client"], dict)
        and invoice_data["client"] is not None
        and "name" in invoice_data["client"]
        and invoice_data["client"]["name"] is not None
        and (
            not isinstance(invoice_data["client"]["name"], str)
            or invoice_data["client"]["name"].strip() != ""
        )
    )
    if (
        "items" in invoice_data
        and isinstance(invoice_data["items"], list)
        and client_valid
    ):
        for i, item in enumerate(invoice_data["items"]):
            if not isinstance(item, dict):
                continue  # Error already added above
            # Only run numeric validation if all required fields are present
            required_item_fields = [
                "description",
                "quantity",
                "unit_price",
                "total_price",
            ]
            if any(
                field not in item or item[field] is None
                for field in required_item_fields
            ):
                continue
            item_context = f"Item {i+1}"
            # quantity must be int only
            if not isinstance(item.get("quantity"), int):
                errors.append(f"{item_context}.quantity must be an integer")
            else:
                validate_numeric_field(
                    f"{item_context}.quantity",
                    item.get("quantity"),
                    min_value=1,
                    require_type=int,
                )
            validate_numeric_field(
                f"{item_context}.unit_price",
                item.get("unit_price"),
                min_value=Decimal("0.001"),
                require_type=(int, float, Decimal),
            )
            validate_numeric_field(
                f"{item_context}.total_price",
                item.get("total_price"),
                require_type=(int, float, Decimal),
            )
            # Perform exact calculation check
            quantity = (
                item.get("quantity") if isinstance(item.get("quantity"), int) else None
            )
            unit_price = safe_get_decimal(
                item, "unit_price", item_context, require_type=(int, float, Decimal)
            )
            total_price = safe_get_decimal(
                item, "total_price", item_context, require_type=(int, float, Decimal)
            )
            if all(val is not None for val in [quantity, unit_price, total_price]):
                expected_total = Decimal(quantity) * unit_price
                if expected_total != total_price:
                    errors.append(
                        f"Item {i+1}: quantity ({quantity}) × unit_price ({unit_price}) = {expected_total}, "
                        f"but total_price is {total_price}"
                    )

    # 8. Validate subtotal equals sum of line items (exact calculation)
    subtotal = safe_get_decimal(invoice_data, "subtotal")
    if (
        subtotal is not None
        and "items" in invoice_data
        and isinstance(invoice_data["items"], list)
    ):
        calculated_subtotal = Decimal("0")
        valid_items_count = 0

        for i, item in enumerate(invoice_data["items"]):
            if isinstance(item, dict):
                item_total = safe_get_decimal(item, "total_price", f"Item {i+1}")
                if item_total is not None:
                    calculated_subtotal += item_total
                    valid_items_count += 1

        if valid_items_count > 0 and calculated_subtotal != subtotal:
            errors.append(
                f"Subtotal mismatch: sum of line items ({calculated_subtotal}) ≠ subtotal ({subtotal})"
            )

    # 9. Validate total calculation (exact calculation)
    total = safe_get_decimal(invoice_data, "total")
    if total is not None:
        # Start with subtotal or calculate from items
        calculated_total = Decimal("0")

        if subtotal is not None:
            calculated_total = subtotal
        elif "items" in invoice_data and isinstance(invoice_data["items"], list):
            for i, item in enumerate(invoice_data["items"]):
                if isinstance(item, dict):
                    item_total = safe_get_decimal(item, "total_price", f"Item {i+1}")
                    if item_total is not None:
                        calculated_total += item_total

        # Apply discount (exact calculation)
        discount = safe_get_decimal(invoice_data, "discount")
        discount_percentage = safe_get_decimal(invoice_data, "discount_percentage")

        if discount is not None:
            if discount_percentage is not None:
                # Both discount amount and percentage present - verify consistency first
                expected_discount = calculated_total * (
                    discount_percentage / Decimal("100")
                )
                if expected_discount != discount:
                    errors.append(f"Discount inconsistency")
            calculated_total -= discount
        elif discount_percentage is not None:
            # Only percentage present, calculate discount
            discount_amount = calculated_total * (discount_percentage / Decimal("100"))
            calculated_total -= discount_amount

        # Add tax (exact calculation)
        tax = safe_get_decimal(invoice_data, "tax")
        if tax is not None:
            calculated_total += tax

        # Add shipping cost (exact calculation)
        shipping_cost = safe_get_decimal(invoice_data, "shipping_cost")
        if shipping_cost is not None:
            calculated_total += shipping_cost

        # Apply rounding adjustment (exact calculation)
        rounding_adjustment = safe_get_decimal(invoice_data, "rounding_adjustment")
        if rounding_adjustment is not None:
            calculated_total += rounding_adjustment

        # Check exact match
        if calculated_total != total:
            errors.append(
                f"Total calculation mismatch: calculated total ({calculated_total}) ≠ given total ({total})"
            )

    return {"is_valid": len(errors) == 0, "errors": errors, "total_errors": len(errors)}
