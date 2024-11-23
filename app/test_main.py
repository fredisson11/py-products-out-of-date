import pytest

from datetime import date
from unittest.mock import patch

from app.main import outdated_products


class TestOutdatedProducts:
    @pytest.fixture()
    def products_template(self) -> list:
        return [
            {
                "name": "salmon",
                "expiration_date": date(2022, 2, 10),
                "price": 600
            },
            {
                "name": "chicken",
                "expiration_date": date(2022, 2, 5),
                "price": 120
            },
            {
                "name": "duck",
                "expiration_date": date(2022, 2, 1),
                "price": 160
            }
        ]

    @pytest.mark.parametrize(
        "fake_today, result_list",
        [
            pytest.param(
                date(2022, 2, 6),
                ["chicken", "duck"],
                id="Some products outdated"
            ),
            pytest.param(
                date(2022, 2, 1),
                [],
                id="No products outdated"
            ),
            pytest.param(
                date(2022, 2, 11),
                ["salmon", "chicken", "duck"],
                id="All products outdated"
            ),
            pytest.param(
                date(2022, 2, 5),
                ["duck"],
                id="Boundary condition"
            ),
        ],
    )
    def test_outdated_products(self,
                               products_template: list,
                               fake_today: date,
                               result_list: list
                               ) -> None:
        with patch("app.main.datetime") as mock_datetime:
            mock_datetime.date.today.return_value = fake_today
            assert outdated_products(products_template) == result_list

    def test_outdated_products_empty_list(self) -> None:
        assert outdated_products([]) == []
