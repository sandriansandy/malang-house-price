import pandas as pd
import numpy as np
import pickle
from typing import Literal


def load_model():
    return pickle.load(open('./rf_model_full.pkl', 'rb'))['model']

def add_kecamatan_onehot(df: pd.DataFrame, kecamatan_value: str) -> pd.DataFrame:
    kecamatan_columns = [
        'kecamatan_Kedungkandang', 'kecamatan_Sukun', 'kecamatan_Blimbing',
        'kecamatan_Klojen', 'kecamatan_Lowokwaru'
    ]
    
    valid_kecamatans = ['Kedungkandang', 'Sukun', 'Blimbing', 'Klojen', 'Lowokwaru']
    if kecamatan_value not in valid_kecamatans:
        raise ValueError(f"Kecamatan '{kecamatan_value}' tidak valid. Pilih dari: {valid_kecamatans}")
    
    for kec in valid_kecamatans:
        df[f'kecamatan_{kec}'] = 0
    
    df[f'kecamatan_{kecamatan_value}'] = 1
    
    if 'kecamatan' in df.columns:
        df = df.drop('kecamatan', axis=1)
    
    return df

def standardize_column_order(df: pd.DataFrame) -> pd.DataFrame:
    expected_columns = [
        'luas_tanah', 'luas_bangunan', 'kamar_mandi', 'kamar_tidur',
        'kecamatan_Kedungkandang', 'kecamatan_Sukun', 'kecamatan_Blimbing',
        'kecamatan_Klojen', 'kecamatan_Lowokwaru', 'bulan', 'jumlah_lantai',
        'kondisi_properti'
    ]
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0 
    
    return df[expected_columns]

def create_df_bangunan(input_data: dict) -> pd.DataFrame:
    input_df = pd.DataFrame({
        k: (v if isinstance(v, (list, tuple, pd.Series)) else [v])
        for k, v in input_data.items()
    })
    
    kecamatan_value = input_data["kecamatan"]
    input_df = add_kecamatan_onehot(input_df, kecamatan_value)
    
    input_df = standardize_column_order(input_df)
    
    return input_df

def create_df_tanah(input_data: dict) -> pd.DataFrame:
    input_df = pd.DataFrame({
        "luas_tanah": [input_data["luas_tanah"]],
        "luas_bangunan": [0],
        "kamar_mandi": [0],
        "kamar_tidur": [0],
        "kecamatan": [input_data["kecamatan"]],
        "bulan": [input_data["bulan"]],
        "jumlah_lantai": [0],
        "kondisi_properti": [input_data["kondisi_properti"]],
    })
    
    kecamatan_value = input_data["kecamatan"]
    input_df = add_kecamatan_onehot(input_df, kecamatan_value)
    
    input_df = standardize_column_order(input_df)
    
    return input_df

def convert_kondisi_to_code(kondisi_input):
    kondisi_mapping = {
        'Bagus': 0,
        'Baru': 1,
        'Butuh Renovasi': 2,
        'Renovasi Minimum': 3,
        'Renovasi Total': 4,
        'Sudah Renovasi': 5,
        'Tanah': 6
    }
    
    return kondisi_mapping.get(kondisi_input, kondisi_input)

def convert_month_to_number(month_input):
    month_mapping = {
        'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
        'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
        'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
    }
    
    return month_mapping.get(month_input, month_input)

def create_df(input_data: dict, category: Literal["Bangunan", "Tanah"]) -> pd.DataFrame:
    print(input_data['kondisi_properti'])
    input_data = input_data.copy()
    input_data['bulan'] = convert_month_to_number(input_data['bulan'])
    input_data['kondisi_properti'] = convert_kondisi_to_code(input_data['kondisi_properti'])

    if category == "Bangunan":
        return create_df_bangunan(input_data)
    else:
        return create_df_tanah(input_data)

def predict_price(input_data: dict, category: Literal["Bangunan", "Tanah"]):
    print(input_data)
    input_df = create_df(input_data, category)
    model = load_model()
    input_log = np.log1p(input_df)
    
    prediction_log = model.predict(input_log)
    prediction = np.expm1(prediction_log)
    return prediction[0]