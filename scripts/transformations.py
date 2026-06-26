import numpy as np
import pandas as pd

df=pd.read_csv('C:/Users/japnoor.kaur/Desktop/sales_analysis/data/clean_output.csv')

df['sales_bottles_per_pack']=df['sales_bottles']*df['pack']

print(df.head(10))

import pandas as pd


def transform_data(df):

    df['store_zip_code'] = (
        df['store_zip_code']
        .fillna(df['store_city'].map(store_zip_code_map))
    )

    df['county_fips_code'] = (
        df['county_fips_code']
        .fillna(df['store_city'].map(county_fips_code_map))
    )

    df['county_name'] = (
        df['county_name']
        .fillna(df['county_fips_code'].map(county_name_map))
    )

    df['category_code'] = (
        df['category_code']
        .fillna(df['category_name'].map(category_code_map))
    )

    df = df.dropna(subset=['category_code'])

    df['category_name'] = (
        df['category_name']
        .fillna(df['category_code'].map(category_name_map))
    )

    df['vendor_number'] = (
        df['vendor_number']
        .fillna(df['vendor_name'].map(vendor_number_map))
    )

    pack_map = df.groupby('item_no')['pack'].first()
    df['pack'] = df['pack'].fillna(
        df['item_no'].map(pack_map)
    )

    df['ordered_on'] = (
        df['ordered_on']
        .str.replace('/', '-', regex=True)
    )

    df['ordered_on'] = pd.to_datetime(
        df['ordered_on'],
        errors='coerce'
    )

    numeric_cols = [
        'store_no',
        'store_zip_code',
        'county_fips_code',
        'vendor_number',
        'item_no',
        'pack',
        'bottle_volume_ml',
        'sales_bottles',
        'sales_dollars',
        'sales_liters',
        'sales_gallons'
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        ).abs()

    return df