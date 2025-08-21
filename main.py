import datetime

import requests
from bs4 import BeautifulSoup
from InquirerPy import inquirer

from app.config import settings
from app.core.paths import Path, Paths
from app.core.router import Route, Router
from app.core.serializers import PaymentItemSerializer, PaymentResponse
from app.core.utils import clear_screen
from app.logs.logger import logger


class App:

    def __init__(self, credentials_from_env: bool = False):
        entrypoint_response: requests.Response = self.session.get(
            self.paths.get_url_of("entrypoint")
        )
        soup = BeautifulSoup(entrypoint_response.text, "html.parser")

        data = {inp.get("name"): inp.get("value") for inp in soup.find_all("input")}
        if credentials_from_env:
            data["login"] = settings.USER_LOGIN
            data["password"] = settings.USER_PASSWORD
        else:
            login = input("Enter your login: ")
            password = input("Enter your password: ")
            # some validation
            data["login"] = login
            data["password"] = password

        login_response = self.session.post(self.paths.get_url_of("login"), data)
        if login_response.status_code == 200:
            logger.info("Successfully logged in")
        else:
            logger.error("Something went wrong at login proccess")

    def get_payment_details(
        self,
        start_date: datetime.date = datetime.date.today() - datetime.timedelta(days=30),
        end_date: datetime.date = datetime.date.today(),
    ):
        self.payment_data = PaymentResponse(start_date=start_date, end_date=end_date)
        response = self.session.get(
            self.paths.get_url_of("payments"),
            params={
                "StartDate": start_date.strftime("%d.%m.%Y"),
                "EndDate": end_date.strftime("%d.%m.%Y"),
            },
        )

        if response.status_code == 200:
            logger.info("Successfully get payment data")
            try:
                table = BeautifulSoup(response.text, "html.parser").find_all(
                    attrs={"class": "table-values"}
                )

                for table_row in table:
                    for tr in table_row.find_all("tr"):
                        tr_data = list(tr.children)
                        self.payment_data.append(PaymentItemSerializer(tr_data))
                logger.info("Successfully parsed response content")
                print(
                    f"\n*** Data from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')} ***\n",
                    self.payment_data.table,
                    end="\n\n",
                )
            except Exception as e:
                logger.error(f"Something went wrong at parsing process: {e}")

    session = requests.Session()

    router = Router(Route("main", lambda e: e), Route("payments", get_payment_details))

    page = router.get_route("main")

    paths = Paths(
        Path("entrypoint", ""),
        Path("login", "/User"),
        Path("payments", "/Payment/Details"),
    )

    LOGIN_FIELD = "login"
    PASSWORD_FIELD = "password"

    payment_data = PaymentResponse()

    def run(self):
        while True:
            page = self.page.name
            match page:
                case "main":
                    options = ["payments"]

                case _:
                    options = ["main"]

            selected_route = inquirer.select(
                message="Go to route:",
                choices=options,
            ).execute()

            route_kwargs = {}
            match selected_route:
                case "payments":
                    custom_date_range = inquirer.confirm(
                        message="Want to add your own date range?"
                    ).execute()
                    if custom_date_range:
                        try:
                            route_kwargs["start_date"] = datetime.datetime.strptime(
                                inquirer.text(
                                    message="Enter start date of range (DD.MM.YYYY):"
                                ).execute(),
                                "%d.%m.%Y",
                            ).date()
                            route_kwargs["end_date"] = datetime.datetime.strptime(
                                inquirer.text(
                                    message="Enter end date of range (DD.MM.YYYY):"
                                ).execute(),
                                "%d.%m.%Y",
                            ).date()
                        except Exception as e:
                            logger.error(f"Something went wrong: {e}")

            clear_screen()
            self.router.go_to(selected_route, self, route_kwargs)
            inquirer.confirm(message="Next").execute()
            clear_screen()


if __name__ == "__main__":
    clear_screen()
    credentials_from_env = inquirer.confirm(
        message="Take credential from environment variable?"
    ).execute()
    clear_screen()
    app = App(credentials_from_env=credentials_from_env)
    app.run()
