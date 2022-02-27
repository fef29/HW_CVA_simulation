class YearFrac:

    @staticmethod
    def calculation(d1, d2, convention):

        if convention.upper() == "ACT/ACT":
            return (d2 - d1).days / 365

        elif convention.upper() == "ACT/360":
            return (d2 - d1).days / 360

        elif convention.upper() == "30/360":
            return (360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (min(30, d2.day) - min(30, d1.day))) / 360
