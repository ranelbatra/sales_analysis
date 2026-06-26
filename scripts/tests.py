import pandas as pd
df=pd.read_csv('C:/Users/japnoor.kaur/Desktop/sales_analysis/data/clean_output.csv')
assert df['sales_dollars'].isnull().sum() == 0

def test_fill_missing_zip_code():
    """Missing ZIP code should be filled using store_city mapping."""
    df = pd.DataFrame({
        "store_city": ["AMES"],
        "store_zip_code": [None]
    })

    result = transform_data(df)

    assert result.loc[0, "store_zip_code"] == 50010


def test_fill_missing_county_fips():
    """Missing county_fips_code should be filled."""
    df = pd.DataFrame({
        "store_city": ["DES MOINES"],
        "county_fips_code": [None]
    })

    result = transform_data(df)

    assert result.loc[0, "county_fips_code"] == 19153


def test_fill_missing_county_name():
    """County name should be derived from county_fips_code."""
    df = pd.DataFrame({
        "county_fips_code": [19153],
        "county_name": [None]
    })

    result = transform_data(df)

    assert result.loc[0, "county_name"] == "POLK"


def test_invalid_date_becomes_nat():
    """Invalid dates should become NaT."""
    df = pd.DataFrame({
        "ordered_on": ["2026-13-45"]
    })

    result = transform_data(df)

    assert pd.isna(result.loc[0, "ordered_on"])


def test_valid_date_conversion():
    """Valid dates should become datetime."""
    df = pd.DataFrame({
        "ordered_on": ["01/15/2026"]
    })

    result = transform_data(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["ordered_on"]
    )


def test_negative_numeric_values():
    """Negative numbers should become positive."""
    df = pd.DataFrame({
        "sales_dollars": [-100.5],
        "sales_bottles": [-12]
    })

    result = transform_data(df)

    assert result.loc[0, "sales_dollars"] == 100.5
    assert result.loc[0, "sales_bottles"] == 12


def test_non_numeric_values_become_nan():
    """Invalid numeric strings should become NaN."""
    df = pd.DataFrame({
        "sales_dollars": ["abc"]
    })

    result = transform_data(df)

    assert pd.isna(result.loc[0, "sales_dollars"])


def test_unknown_city_remains_null():
    """Unknown cities should not cause errors."""
    df = pd.DataFrame({
        "store_city": ["UNKNOWN CITY"],
        "store_zip_code": [None]
    })

    result = transform_data(df)

    assert pd.isna(result.loc[0, "store_zip_code"])


def test_fill_pack_from_item_no():
    """Missing pack should be filled using item_no mapping."""
    df = pd.DataFrame({
        "item_no": [1001, 1001],
        "pack": [12, None]
    })

    result = transform_data(df)

    assert result.loc[1, "pack"] == 12


def test_empty_dataframe():
    """Transformation should handle empty DataFrames."""
    df = pd.DataFrame()

    result = transform_data(df)

    assert result.empty

