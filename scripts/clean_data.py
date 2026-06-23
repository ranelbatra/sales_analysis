import numpy as np
import pandas as pd
df=pd.read_csv('C:\\Users\\japnoor.kaur\\Desktop\\sales_analysis\\data\\iowa_liquor_sales_target_raw.csv')

df=df.dropna(subset=['invoice_id'], how='all')

df=df.drop_duplicates(subset='invoice_id')
print(df['invoice_id'].nunique())

text_cols=df.select_dtypes(include='object').columns
df[text_cols]=df[text_cols].apply(lambda x: x.str.strip().str.upper())

df['invoice_id']=df['invoice_id'].astype(str)
print(df['invoice_id'].dtypes)
df['invoice_id']=df['invoice_id'].str.replace('S', 'INV-')

df['store_city']=df['store_city'].str.strip().str.upper()
df['county_name']=df['county_name'].str.strip().str.upper()
df['category_name']=df['category_name'].str.strip().str.upper()
df['vendor_name']=df['vendor_name'].str.strip().str.upper()
df['im_desc']=df['im_desc'].str.strip().str.upper()

df['sales_dollars']=df['sales_dollars'].replace('[\$,]', '', regex=True).astype(float)
print(df['sales_dollars'].head(15))

df['store_zip_code']=df['store_zip_code'].str.replace(r'-\d+', '', regex=True)
print(df.at[144, 'store_zip_code'])

print(df.isnull().sum())
store_zip_code_map={
    'ALTOONA': 50009,
    'AMES': 50010,
    'ANKENY': 50021,
    'CEDAR FALLS': 50613,
    'CEDAR RAPIDS': 52402,
    'CORALVILLE': 52241,
    'COUNCIL BLUFFS': 51503,
    'DES MOINES': 50322,
    'DUBUQUE': 52003,
    'FORT DODGE': 50501,
    'IOWA CITY': 52240,
    'SIOUX CITY': 51106,
    'URBANDALE': 50322,
    'WAUKEE': 50263,
    'WEST BURLINGTON': 52655,
    'WEST DES MOINES': 50266,
    'WATERLOO': 50702
}
df['store_zip_code']=df['store_zip_code'].fillna(df['store_city'].map(store_zip_code_map))
print(df.isnull().sum())

county_fips_code_map={
    'ALTOONA': 19153,
    'AMES': 19169,
    'ANKENY': 19153,
    'CEDAR FALLS': 19013,
    'CEDAR RAPIDS': 19113,
    'CORALVILLE': 19103,
    'COUNCIL BLUFFS': 19155,
    'DES MOINES': 19153,
    'DUBUQUE': 19061,
    'FORT DODGE': 19187,
    'IOWA CITY': 19103,
    'SIOUX CITY': 19193,
    'URBANDALE': 19153,
    'WAUKEE': 19049,
    'WEST BURLINGTON': 19057,
    'WEST DES MOINES': 19153,
    'WATERLOO': 19013
}
df['county_fips_code']=df['county_fips_code'].fillna(df['store_city'].map(county_fips_code_map))
print(df.isnull().sum())

county_name_map={
    19153: 'POLK',
    19169: 'STORY',
    19013: 'BLACK HAWK',
    19113: 'LINN',
    19155: 'POTTAWATTAMIE',
    19061: 'DUBUQUE',
    19187: 'WEBSTER',
    19103: 'JOHNSON',
    19193: 'WOODBURY',
    19049: 'DALLAS',
    19057: 'DES MOINES'
}
df['county_name']=df['county_name'].fillna(df['county_fips_code'].map(county_name_map))


print(
    df[df['category_code'].isin([1081500, 1081400])]
    .groupby('category_name')['category_code']
    .value_counts()
)

df['category_name']=df['category_name'].str.strip()
df['category_name']=df['category_name'].str.strip().str.replace('SPIRITS', 'SPIRIT')
df['category_name']=df['category_name'].str.strip().str.replace('LIQUERS', 'LIQUER')
df['category_name']=df['category_name'].str.strip().str.replace('IMPORTED VODKA - MISC', 'IMPORTED FLAVORED VODKA')
category_code_map={
    'AMERICAN FLAVORED VODKA': 1031200,
    '100 PROOF VODKA': 1031100,
    '100% AGAVE TEQUILA': 1022200,
    'AGED DARK RUM': 1062300,
    'AMERICAN AMARETTO': 1081010,
    'AMERICAN BRANDIES': 1051100,
    'AMERICAN COCKTAILS': 1071100,
    'AMERICAN CORDIALS & LIQUEURS': 1081300,
    'AMERICAN DISTILLED SPIRIT SPECIALTY': 1081300,
    'AMERICAN DRY GINS': 1041100,
    'AMERICAN GRAPE BRANDIES': 1051010,
    'AMERICAN SCHNAPPS': 1081400,
    'AMERICAN VODKAS': 1031100,
    'APPLE SCHNAPPS': 1081305,
    'BLENDED WHISKIES': 1011100,
    'BOTTLED IN BOND BOURBON': 1011400,
    'BUTTERSCOTCH SCHNAPPS': 1081312,
    'CANADIAN WHISKIES': 1012100,
    'COCKTAILS/RTD': 1071100,
    'COFFEE LIQUEURS': 1081030,
    'CORN WHISKIES': 1011600,
    'CREAM LIQUEURS': 1081200,
    'DECANTERS & SPECIALTY PACKAGES': 1701100,
    'DISTILLED SPIRIT SPECIALTY': 1081700,
    'FLAVORED GIN': 1041200,
    'FLAVORED RUM': 1062500,
    'GOLD RUM': 1062100,
    'IMPORTED AMARETTO': 1081015,
    'IMPORTED BRANDIES': 1052100,
    'IMPORTED CORDIALS & LIQUEUS': 1082100,
    'IMPORTED DISTILLED SPIRIT SPECIALTY': 1092100,
    'IMPORTED DRY GINS': 1042100,
    'IMPORTED FLAVORED VODKA': 1032200,
    'IMPORTED GRAPE BRANDIES': 1052010,
    'IMPORTED SCHNAPPS': 1082200,
    'IMPORTED VODKAS': 1032100,
    'IOWA DISTILLERIES': 1091400,
    'IRISH WHISKIES': 1012400,
    'JAMAICA RUM': 1062100,
    'JAPANESE WHISKY': 1012400,
    'LOW PROOF VODKA': 1031110,
    'MEZCAL': 1022300,
    'MISC. AMERICAN CORDIALS & LIQUEURS': 1081900,
    'MISC. IMPORTED CORDIALS & LIQUEURS': 1082900,
    'MISCELLANEOUS SCHNAPPS': 1081380,
    'MIXTO TEQUILA': 1022100,
    'PEACH SCHNAPPS': 1081330,
    'PEPPERMINT SCHNAPPS': 1081300,
    'PUERTO RICO & VIRGIN ISLANDS RUM': 1062200,
    'SCOTCH WHISKIES': 1012200,
    'SINGLE BARREL BOURBON WHISKIES': 1011300,
    'SINGLE MALT SCOTCH': 1012210,
    'SPICED RUM': 1062400,
    'STRAIGHT BOURBON WHISKIES': 1011200,
    'STRAIGHT RYE WHISKIES': 1011600,
    'TEMPORARY & SPECIALTY PACKAGES': 1700000,
    'TENNESSEE WHISKIES': 1011400,
    'TEQUILA': 1022100,
    'TRIPLE SEC': 1081500,
    'VODKA 80 PROOF': 1031080,
    'VODKA FLAVORED': 1031200,
    'WHISKEY LIQUEUR': 1081600,
    'WHITE RUM': 1062200,
}
df['category_code']=df['category_code'].fillna(df['category_name'].map(category_code_map))
df=df.dropna(subset=['category_code'])

category_name_map={
    1031200: 'VODKA FLAVORED',
    1031100: '100 PROOF VODKA',
    1022200: '100% AGAVE TEQUILA',
    1062300: 'AGED DARK RUM',
    1081010: 'AMERICAN AMARETTO',
    1051100: 'AMERICAN BRANDIES',
    1071100: 'AMERICAN COCKTAILS',
    1081300: 'AMERICAN CORDIALS & LIQUEURS',
    1081300: 'AMERICAN DISTILLED SPIRIT SPECIALTY',
    1041100: 'AMERICAN DRY GINS',
    1051010: 'AMERICAN GRAPE BRANDIES',
    1081400: 'AMERICAN SCHNAPPS',
    1031100: 'AMERICAN VODKAS',
    1081305: 'APPLE SCHNAPPS',
    1011100: 'BLENDED WHISKIES',
    1011400: 'BOTTLED IN BOND BOURBON',
    1081312: 'BUTTERSCOTCH SCHNAPPS',
    1012100: 'CANADIAN WHISKIES',
    1071100: 'COCKTAILS/RTD',
    1081030: 'COFFEE LIQUEURS',
    1011600: 'CORN WHISKIES',
    1081200: 'CREAM LIQUEURS',
    1701100: 'DECANTERS & SPECIALTY PACKAGES',
    1081700: 'DISTILLED SPIRIT SPECIALTY',
    1041200: 'FLAVORED GIN',
    1062500: 'FLAVORED RUM',
    1062100: 'GOLD RUM',
    1081015: 'IMPORTED AMARETTO',
    1052100: 'IMPORTED BRANDIES',
    1082100: 'IMPORTED CORDIALS & LIQUEURS',
    1092100: 'IMPORTED DISTILLED SPIRIT SPECIALTY',
    1042100: 'IMPORTED DRY GINS',
    1032200: 'IMPORTED FLAVORED VODKA',
    1052010: 'IMPORTED GRAPE BRANDIES',
    1082200: 'IMPORTED SCHNAPPS',
    1032100: 'IMPORTED VODKAS',
    1091400: 'IOWA DISTILLERIES',
    1012400: 'IRISH WHISKIES',
    1062100: 'JAMAICA RUM',
    1012400: 'JAPANESE WHISKY',
    1031110: 'LOW PROOF VODKA',
    1022300: 'MEZCAL',
    1081900: 'MISC. AMERICAN CORDIALS & LIQUEURS',
    1082900: 'MISC. IMPORTED CORDIALS & LIQUEURS',
    1081380: 'MISCELLANEOUS SCHNAPPS',
    1022100: 'MIXTO TEQUILA',
    1081330: 'PEACH SCHNAPPS',
    1081300: 'PEPPERMINT SCHNAPPS',
    1062200: 'PUERTO RICO & VIRGIN ISLANDS RUM',
    1012200: 'SCOTCH WHISKIES',
    1011300: 'SINGLE BARREL BOURBON WHISKIES',
    1012210: 'SINGLE MALT SCOTCH',
    1062400: 'SPICED RUM',
    1011200: 'STRAIGHT BOURBON WHISKIES',
    1011600: 'STRAIGHT RYE WHISKIES',
    1700000: 'TEMPORARY & SPECIALTY PACKAGES',
    1011400: 'TENNESSEE WHISKIES',
    1022100: 'TEQUILA',
    1081500: 'TRIPLE SEC',
    1031080: 'VODKA 80 PROOF',
    1031200: 'VODKA FLAVORED',
    1081600: 'WHISKEY LIQUEUR',
    1062200: 'WHITE RUM',
}
df['category_name']=df['category_name'].fillna(df['category_code'].map(category_name_map))
print(df.isnull().sum())

df['vendor_name']=df['vendor_name'].str.upper()
df['vendor_name']=df['vendor_name'].str.strip().str.replace('BACARDI USA INC', 'BACARDI U.S.A., INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('BROWN FORMAN CORP.', 'BROWN-FORMAN CORPORATION')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('CEDAR RIDGE VINEYARDS LL', 'CEDAR RIDGE VINEYARDS,LLC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('CONSTELLATION BRANDS INC', 'CONSTELLATION WINE COMPANY, INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('DISARONNO INTERNATIONAL', 'DISARONNO INTERNATIONAL LLC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('DISARONNO INTERNATIONAL LLC LLC', 'DISARONNO INTERNATIONAL LLC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('E AND J GALLO WINERY', 'E & J GALLO WINERY')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('LAIRD AND COMPANY', 'LAIRD & COMPANY')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('LUXCO INC', 'LUXCO-ST LOUIS')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('MCCORMICK DISTILLING CO.', 'MCCORMICK DISTILLING COMPANY')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('MOET HENNESSY USA', 'MOET HENNESSY USA, INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('MOET HENNESSY USA, INC., INC.', 'MOET HENNESSY USA, INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PERNOD RICARD USA', 'PERNOD RICARD USA/AUSTIN NICHOLS')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PERNOD RICARD USA/AUSTIN NICHOLS/AUSTIN NICHOLS', 'PERNOD RICARD USA/AUSTIN NICHOLS')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PHILLIPS BEVERAGE', 'PHILLIPS BEVERAGE COMPANY')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PHILLIPS BEVERAGE COMPANY COMPANY','PHILLIPS BEVERAGE COMPANY')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PRESTIGE WINE AND SPIRITS GROUP', 'PRESTIGE WINE & SPIRITS GROUP / UNITED STATES DISTILLED PRODUCTS CO')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PRESTIGE WINE & SPIRITS GROUP', 'PRESTIGE WINE & SPIRITS GROUP / UNITED STATES DISTILLED PRODUCTS CO')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('PRESTIGE WINE & SPIRITS GROUP / UNITED STATES DISTILLED PRODUCTS CO / UNITED STATES DISTILLED PRODUCTS CO', 'PRESTIGE WINE & SPIRITS GROUP / UNITED STATES DISTILLED PRODUCTS CO')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('Rï¿½MY COINTREAU USA', 'REMY COINTREAU USA INC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('REMY COINTREAU USA         .', 'REMY COINTREAU USA INC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('SAZERAC CO., INC.', 'SAZERAC COMPANY  INC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('SAZERAC NORTH AMERICA', 'SAZERAC COMPANY  INC')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('WILSON DANIELS LTD', 'WILSON DANIELS LTD.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('WILSON DANIELS LTD..', 'WILSON DANIELS LTD.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('WILLIAM GRANT & SONS INC', 'WILLIAM GRANT AND SONS, INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('FIFTH GENERATION INC', 'FIFTH GENERATION INC.')
df['vendor_name']=df['vendor_name'].str.strip().str.replace('FIFTH GENERATION INC..', 'FIFTH GENERATION INC.')
vendor_number_map={
    'ARTISAN GRAIN DISTILLERY': 101,
    'BACARDI U.S.A., INC.': 35,
    'BROWN-FORMAN CORPORATION': 85,
    'CAMPARI AMERICA': 619,
    'CAMPARI(SKYY)': 461,
    'CASTLE BRANDS': 91,
    'CEDAR RIDGE VINEYARDS,LLC': 125,
    'CHARLES JACQUIN/INDEPENDENT SPIRITS': 284,
    'CHATHAM IMPORTS INC': 287,
    'CONSTELLATION WINE COMPANY, INC.': 115,
    'DAVOS BRANDS LLC': 469,
    'DEHNER DISTILLERY': 229,
    'DIAGEO AMERICAS': 260,
    'DISARONNO INTERNATIONAL LLC': 130,
    'DUNKEL CORPORATION': 154,
    'DV SPIRITS LLC': 342,
    'E & J GALLO WINERY': 205,
    'EDRINGTON GROUP USA LLC': 266,
    'FIFTH GENERATION DISTILLED SPIRITS, INC.': 982,
    'FIFTH GENERATION INC.': 301,
    'FOUR ROSES DISTILLERY': 184,
    'FRANK-LIN DISTILLERS PRODUCTS LTD.': 198,
    'GEMINI SPIRITS': 330,
    'HEAVEN HILL BRANDS': 259,
    'WILSON DANIELS LTD.': 255,
    'SKYY SPIRITS INC': 461,
    'JIM BEAM BRANDS': 65,
    'PIEDMONT DISTILLERS': 384,
    'PROXIMO': 395,
    'LUXCO-ST LOUIS': 434,
    'WILLIAM GRANT AND SONS, INC.': 240,
    'MHW LTD': 305,
    'SAZERAC COMPANY  INC': 421,
    'PERNOD RICARD USA/AUSTIN NICHOLS': 370,
    'KIRIN BEER & SPIRITS OF AMERICA INC / FOUR ROSES DISTILLERY': 830,
    'PHILLIPS BEVERAGE COMPANY': 380,
    'MAST-JAGERMEISTER US, INC': 192,
    'MOET HENNESSY USA, INC.': 420,
    'ZING ZANG, LLC': 902,
    'LAIRD & COMPANY': 297,
    'PRESTIGE WINE & SPIRITS GROUP / UNITED STATES DISTILLED PRODUCTS CO': 322,
    'SOVEREIGN BRANDS, LLC': 482,
    'SAZERAC NORTH AMERICA': 55,
    'PATRON SPIRITS COMPANY': 410,
    'REMY COINTREAU USA INC': 389,
    'INTERCONTINENTAL PACKAGING COMPANY/PRESTIGE BEVERAGE GROUP': 772,
    'MISSISSIPPI RIVER DISTIL': 306,
    'MCCORMICK DISTILLING COMPANY': 300,
    'MPL BRANDS NV INC/ PATCO BRANDS': 620,
    'JINRO AMERICA INC': 293,
    'SHAW-ROSS INTERNATIONAL': 460,
    'STOLI GROUP': 277,
    'TY KU LLC': 469,
    'JEM BEVERAGE COMPANY': 521,
    'PARK STREET IMPORTS': 368,
    'WINESOURCE INTERNATIONAL INC.': 755,
    'VBJ BEVERAGES LLC': 269,
    'HOTALING & CO': 391,
    'SWELL LIQUOR LLC': 195,
    'HOOD RIVER DISTILLERS, INC.': 971,
    'RUSSIAN STANDARD VODKA, USA': 239,
    'WESTERN SPIRITS BEVERAGE CO. LLC': 492,
    'OLE SMOKY DISTILLERY, LLC': 346,
    'IMPERIAL BRANDS, INC.': 267,
    'INFINIUM SPIRITS': 255,
    'SIDNEY FRANK IMPORTING CO.': 192,
    'THE PATRON SPIRITS COMPANY': 410
}
df['vendor_number']=df['vendor_number'].fillna(df['vendor_name'].map(vendor_number_map))

print(df[df['vendor_number'].isnull()])

print(df.groupby('item_no')['pack'].value_counts())
pack_map=df.groupby('item_no')['pack'].first()
df['pack']=df['pack'].fillna(df['item_no'].map(pack_map))
print(df.isnull().sum())

print(df['ordered_on'].head(15))
df['ordered_on']=df['ordered_on'].str.strip().str.replace('/', '-', regex=True)
df['ordered_on']=pd.to_datetime(df['ordered_on'], errors='coerce')
print(df['ordered_on'].head(15))