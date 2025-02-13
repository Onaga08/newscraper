from urllib.parse import urljoin
import logging
import re
import json
from datetime import datetime
from scrapy.selector.unified import SelectorList

# Set up logging
# logging.basicConfig(
#     filename=f"logs/scrapy-{datetime.now().strftime(r'%Y-%m-%d-%H-%M-%S-%f')}.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

def apply_operation(element, operation_name, additional_info=None):
    if not additional_info:
        additional_info = {}

    if element is None:
        return None

    # If element is a SelectorList, extract the first element
    if isinstance(element, SelectorList):
        element = element.get(default=None)

    # Operation to join base URL with relative URLs
    if operation_name == "join_url":
        base_url = additional_info.get("base_url", "")
        return urljoin(base_url, element)

    # Extract the nth element from a list
    if operation_name == "get_nth_element":
        index = additional_info.get("index", 0)
        try:
            return element[index]
        except IndexError:
            return None

    # Check if the element is present
    elif operation_name == "is_present":
        return element is not None and len(element) > 0

    # Strip extra spaces or characters from a string
    elif operation_name == "strip":
        chars = additional_info.get("chars", None)
        if isinstance(element, str):
            return element.strip(chars)
        return None

    # Replace one substring with another
    elif operation_name == "replace":
        if isinstance(element, str):
            return element.replace(additional_info["old"], additional_info["new"])
        return None

    # Count the number of elements in a list
    elif operation_name == "count_elements":
        return len(element) if element is not None else 0

    # Clean up HTML span tags
    elif operation_name == "merge_offer_strings":
        if element is not None:
            span_pattern = r"<span[^>]*>"
            return re.sub(span_pattern, "", element).replace("</span>", "")

    # Check if the element contains specific text
    elif operation_name == "check_text":
        if not element:
            return False
        text = additional_info.get("text", "")
        return True if re.search(text, element) else False

    # Extract the first integer found in the string
    elif operation_name == "extract_first_int":
        return int(re.search("\d+", element).group()) if element is not None else None

    # Convert string to a float, removing commas first
    elif operation_name == "convert_to_float":
        if isinstance(element, str):
            element = element.replace(",", "")  # remove commas
            try:
                return float(element)
            except ValueError:
                return None
        return None

    # Convert element to a boolean value
    elif operation_name == "is_true":
        return bool(element)

    # Split a string by a comma and count the resulting parts
    elif operation_name == "explode_count_elements":
        return len(element.split(",")) if element else 0

    # Split a string by a specified delimiter
    elif operation_name == "split_string":
        if isinstance(element, str):
            split_by = additional_info.get("split_by", " ")
            return element.split(split_by)
        return None

    # Convert text to lowercase
    elif operation_name == "lowercase":
        if isinstance(element, str):
            return element.lower()
        return None

    # Convert element (list or dict) to a JSON string
    elif operation_name == "convert_to_json":
        if isinstance(element, list) or isinstance(element, dict):
            return json.dumps(element)
        return element


    # Default return (if no operation is matched)
    else:
        return element

def process_dependent_operations(value, result):
    if not result:
        return None
    operation = value.get("operation")
    dep_key = value["dependencies"][0]
    if operation == "extract_float":
        if result[dep_key]:
            return float(result[dep_key].split(" ")[0])
    elif operation == "calculate_discount_percentage":
        if result[dep_key]:
            return int(result[dep_key].replace("% off", "").strip())
    else:
        return None

def process_element_data(element, selectors, meta):
    result = {}

    for key, value in selectors.items():
        if "xpath" in value:
            if not element:
                result[key] = None
            else:
                xpath_element = element.xpath(value["xpath"])
                if "operations" in value:
                    for op in value["operations"]:
                        xpath_element = apply_operation(
                            xpath_element, op["name"], op.get("additional_info")
                        )
                    result[key] = xpath_element
                else:
                    result[key] = xpath_element.get()
        elif "operation" in value:
            result[key] = process_dependent_operations(value, result)

    # Remove excluded elements
    for key, value in selectors.items():
        if value.get("exclude", False):
            result.pop(key, None)

    return result
