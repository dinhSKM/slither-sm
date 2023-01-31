from typing import List, Dict

from prettytable import PrettyTable


# class Table:
#     def __init__(self, field_names: List[str]):
#         self._field_names = field_names
#         self._rows: List = []

#     def add_row(self, row: List[str]) -> None:
#         self._rows.append(row)

#     def __str__(self) -> str:
#         txt = "| "
#         for i in self._field_names:
#             txt += i + " |"
#         txt += "\n"
#         for row in self._rows:
#             txt += "| "
#             for item in row:
#                 txt += item + " |"
#             txt += "\n"


class MyPrettyTable:
    def __init__(self, field_names: List[str]):
        self._field_names = field_names
        self._rows: List = []

    def add_row(self, row: List[str]) -> None:
        self._rows.append(row)

    # def to_pretty_table(self) -> Table:
    #     table = Table(self._field_names)
    #     for row in self._rows:
    #         table.add_row(row)
    #     return table

    def to_json(self) -> Dict:
        return {"fields_names": self._field_names, "rows": self._rows}

    def __str__(self) -> str:
        txt = "|"
        for i in self._field_names:
            txt += i + "|"
        txt += "\n"
        txt += "|"
        for i in self._field_names:
            txt += "-" + "|"
        txt += "\n"

        for row in self._rows:
            txt += "|"
            for item in row:
                txt += str(item).replace("\n", " ").strip() + "|"
            txt += "\n"
        with open("print-report.md", "a") as myfile:
            myfile.write(txt + "\n")
        return str(txt)
