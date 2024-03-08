def translateTheme(themeName, leftToRight):
    themeMappingLeft = {
        "Alap Kék": "default",
        "Alap Sötétkék": "dark",
        "Élénk Sárga": "yellow",
        "Vidám Zöld": "green",
        "Nagy Kontrasztú": "highContrast"
    }

    themeMappingRight = {
        "default": "Alap Kék",
        "dark": "Alap Sötétkék",
        "yellow": "Élénk Sárga",
        "green": "Vidám Zöld",
        "highContrast": "Nagy Kontrasztú"
    }

    return themeMappingLeft.get(themeName, "") if leftToRight else themeMappingRight.get(themeName, "")
