# fetch.py  (수정 버전)

import yfinance as yf
import pandas as pd
import os
from typing import List
from settings import initial

def fetch_stock_data(
        ticker: str,
        start: str,
        end: str,
        save_path: str = initial.RAW_DATA_DIR
) -> pd.DataFrame:
    print(f"[INFO] Fetching {ticker} ({start} → {end})")

    try:
        df = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=False,
            actions=True,
            group_by="column"     
        )

        if df.empty:
            print(f"[WARNING] No data for {ticker}")
            return None

       
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        required = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
        for col in required:
            if col not in df.columns:
                df[col] = 0.0
        df = df[required]

        df.index = pd.to_datetime(df.index).tz_localize("America/New_York", nonexistent='shift_forward')

        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, f"{ticker}.csv")
        df.to_csv(file_path, index_label="Date")  
        print(f" Saved  →  {file_path}")
        return df

    except Exception as e:
        print(f"[ERROR] {ticker}: {e}")
        return None


def fetch_multiple_stocks(
        tickers: List[str] = None,
        start: str = None,
        end:   str = None,
        save_path: str = None
):
    tickers   = tickers   or initial.TICKERS
    start     = start     or initial.START_DATE
    end       = end       or initial.END_DATE
    save_path = save_path or initial.RAW_DATA_DIR

    for t in tickers:
        fetch_stock_data(t, start, end, save_path)
