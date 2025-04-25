def calculate_actual_length(text: str) -> int:
    """
    Calculate the actual length of a string based on the given rules:
    1. 1 Chinese character counts as 2 characters.
    2. 1 English letter, 1 punctuation mark, or 1 space counts as 1 character.
    """
    import re

    # Regular expression to match Chinese characters
    chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")

    # Count Chinese characters
    chinese_char_count = len(chinese_char_pattern.findall(text))

    # Count other characters
    other_char_count = len(text) - chinese_char_count

    # Calculate total length
    total_length = chinese_char_count * 2 + other_char_count

    return total_length
