def convertibleToInt(variable):
    try:
        variable = int(variable)
        return True
    except ValueError:
        return False
