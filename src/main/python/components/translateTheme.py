def translateTheme(themeName, leftToRight):
    themeMappingLeft = {
        "Alap téma": "default",
        "Sötét téma": "dark",
        "Nagy Kontrasztú": "highContrast"
    }

    themeMappingRight = {
        "default": "Alap téma",
        "dark": "Sötét téma",
        "highContrast": "Nagy Kontrasztú"
    }

    return themeMappingLeft.get(themeName, "") if leftToRight else themeMappingRight.get(themeName, "")
