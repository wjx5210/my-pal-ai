import pytest
from app.data_validator import validate_pal_data


def test_valid_pal_data():

    pals = [
        {
            "name": "测试帕鲁",
            "element": [],
            "summary": "",
            "work_suitability": {},
            "combat": {},
            "drops": [],
            "locations": [],
            "recommended_stage": "",
            "recommendation": "",
            "tips": ""
        }
    ]


    assert validate_pal_data(pals) is True


def test_missing_field():

    pals = [
        {
            "name": "错误帕鲁"
        }
    ]


    with pytest.raises(ValueError):

        validate_pal_data(pals)