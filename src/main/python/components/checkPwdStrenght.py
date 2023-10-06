def calculateStrength(password):
    length = len(password)
    uppercase = any(i.isupper() for i in password)
    lowercase = any(i.islower() for i in password)
    digit = any(i.isdigit() for i in password)
    specialChar = any(not i.isalnum() for i in password)

    strength = 0

    if length >= 8:
        strength += 2
    elif length >= 6:
        strength += 1
    else:
        return 0

    if uppercase:
        strength += 1

    if lowercase:
        strength += 1

    if digit:
        strength += 1

    if specialChar:
        strength += 2

    return strength
