import re

regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"  # noqa: E501
match_iso8601 = re.compile(regex).match


def validate_iso8601(str_val):
    try:
        if match_iso8601(str_val) is not None:
            return True
    except:  # noqa: E722
        pass
    return False
