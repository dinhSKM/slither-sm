"""
    Module printing summary of the contract
"""

from slither.core.declarations import Function
from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.myprettytable import MyPrettyTable


class PublicModifiers(AbstractPrinter):

    ARGUMENT = "public-modifiers"
    HELP = "Print the modifiers called by each function"

    WIKI = "https://github.com/trailofbits/slither/wiki/Printer-documentation#modifiers"

    def output(self, _filename):
        """
        _filename is not used
        Args:
            _filename(string)
        """

        all_txt = ""
        all_tables = []

        for contract in self.slither.contracts_derived:
            txt = f"\nContract {contract.name}"
            table = MyPrettyTable(["Function","Visibility", "Modifiers"])
            for function in contract.functions:
                if function.is_empty is not None:
                    if function.name not in  ["constructor", "initialize"] and function.visibility in ["public", "external"] and function.modifiers == [] and not function.pure and not function.view:
                        table.add_row([function.name, function.visibility ,[m.name for m in set(function.modifiers)]])
            txt += "\n" + str(table)
            self.info(txt)
            all_txt += txt
            all_tables.append((contract.name, table))

        res = self.generate_output(all_txt)
        for name, table in all_tables:
            res.add_pretty_table(table, name)

        return res
