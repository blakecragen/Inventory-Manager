import re

class UnitConverter:
    # Base: ounce
    unit_to_oz = {
        'oz': 1,
        'g': 0.035274,
        'kg': 35.274,
        'lb': 16,
        'cup': 8,
        'cups': 8,
        'ml': 0.033814,
        'l': 33.814
    }

    @classmethod
    def parse_amount(cls, amount_str):
        match = re.match(r'^\s*([\d.]+)\s*([a-zA-Z]+)\s*$', amount_str)
        if not match:
            raise ValueError(f"Invalid amount format: '{amount_str}'")
        quantity = float(match.group(1))
        unit = match.group(2).lower()
        if unit not in cls.unit_to_oz:
            raise ValueError(f"Unsupported unit: {unit}")
        return quantity, unit

    @classmethod
    def to_oz(cls, amount_str):
        quantity, unit = cls.parse_amount(amount_str)
        return quantity * cls.unit_to_oz[unit]

    @classmethod
    def from_oz(cls, oz_value, target_unit):
        if target_unit not in cls.unit_to_oz:
            raise ValueError(f"Unsupported unit: {target_unit}")
        result = oz_value / cls.unit_to_oz[target_unit]
        return f"{round(result, 2)} {target_unit}"

    @classmethod
    def add(cls, current_str, add_str):
        cur_qty, cur_unit = cls.parse_amount(current_str)
        cur_oz = cur_qty * cls.unit_to_oz[cur_unit]
        add_oz = cls.to_oz(add_str)
        result_oz = cur_oz + add_oz
        return cls.from_oz(result_oz, cur_unit)

    @classmethod
    def subtract(cls, current_str, subtract_str):
        cur_qty, cur_unit = cls.parse_amount(current_str)
        cur_oz = cur_qty * cls.unit_to_oz[cur_unit]
        sub_oz = cls.to_oz(subtract_str)
        result_oz = cur_oz - sub_oz
        if result_oz < 0:
            raise ValueError("Resulting amount is negative.")
        return cls.from_oz(result_oz, cur_unit)
