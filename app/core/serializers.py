import datetime
from typing import List, Tuple

from bs4.element import PageElement
from tabulate import tabulate

from app.core.utils import clear_string


class PaymentItemSerializer:
    def __init__(self, tr: PageElement):
        self.datetime: datetime.datetime = datetime.datetime.strptime(
            clear_string(tr[1].text), "%d.%m.%Y %H:%M:%S"
        )
        self.sum: float = float(
            clear_string(tr[3].text).replace("manat", "").replace(",", ".").strip()
        )
        self.type: str = clear_string(tr[5].text)
        self.dealer: str = clear_string(tr[7].text)
        self.tax: float = float(clear_string(tr[9].text).replace(",", "."))

    @property
    def fields_list(self) -> Tuple[str]:
        # (datetime, sum, type, dealer, tax)
        return tuple(
            [
                self.datetime.strftime("%d.%m.%Y %H:%M:%S"),
                f"{self.sum:.2f}",
                self.type,
                self.dealer,
                f"{self.tax:.2f}",
            ]
        )


class PaymentResponse:
    def __init__(
        self,
        *args: List[PaymentItemSerializer],
        start_date: datetime.date = datetime.date.today() - datetime.timedelta(days=30),
        end_date: datetime.date = datetime.date.today(),
    ):
        self.data: List[PaymentItemSerializer] = list(args)
        self.start_date: datetime.date = start_date
        self.end_date: datetime = end_date

    def append(self, item: PaymentItemSerializer):
        self.data.append(item)

    @property
    def rows(self) -> Tuple[Tuple]:
        return tuple([row.fields_list for row in self.data])

    @property
    def table(self):
        data = list(self.rows)
        data.insert(0, ("Datetime", "Sum (TMT)", "Type", "Dealer", "Tax (TMT)")),
        return tabulate(
            data,
            headers="firstrow",
            tablefmt="grid",
        )
