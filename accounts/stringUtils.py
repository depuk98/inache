

def reopen_number(string):
    # Check if the case contains an underscore '_'
    if "_" in string:
        # Split the case into two parts: the part before '_' and the part after '_'
        prefix, suffix = string.split("_")

        # Try converting the suffix to an integer and increment it by 1
        try:
            incremented_suffix = int(suffix) + 1
        except ValueError:
            # If the conversion to an integer fails, set the suffix to 1
            incremented_suffix = 1

        # Combine the prefix and the incremented suffix with an underscore
        new_a = f"{prefix}_{incremented_suffix}"
    else:
        # If the case has no underscore, add "_1" at the end
        new_a = f"{string}_1"

    return new_a

    