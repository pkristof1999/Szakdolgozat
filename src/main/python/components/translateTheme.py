def translateTheme(themeName, leftToRight):
    themeMappingLeft = {
        "Alap téma": "default",
        "Sötét téma": "dark"
    }

    themeMappingRight = {
        "default": "Alap téma",
        "dark": "Sötét téma"
    }

    return themeMappingLeft.get(themeName, "") if leftToRight else themeMappingRight.get(themeName, "")
