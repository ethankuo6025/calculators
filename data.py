import os
import sqlite3
from datetime import timedelta
from sqlite3 import Connection

import pandas as pd
import yfinance as yf

DB_PATH = "prices.db"

def _connect() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS prices ("
        "date TEXT NOT NULL, "
        "ticker TEXT NOT NULL, "
        "close REAL NOT NULL, "
        "PRIMARY KEY (date, ticker))"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS meta ("
        "ticker TEXT PRIMARY KEY, "
        "start TEXT NOT NULL, "
        "end TEXT NOT NULL)"
    )
    return conn

def _store(conn: Connection, prices: pd.DataFrame) -> None:
    rows = prices.stack().reset_index()
    rows.columns = ["date", "ticker", "close"]
    rows["date"] = rows["date"].dt.strftime("%Y-%m-%d")

    conn.executemany(
        "INSERT OR REPLACE INTO prices (date, ticker, close) VALUES (?, ?, ?)",
        rows.itertuples(index=False, name=None),
    )
    conn.commit()

def _read_meta(conn: Connection) -> dict[str, tuple[pd.Timestamp, pd.Timestamp]]:
    meta = pd.read_sql("SELECT ticker, start, end FROM meta", conn, parse_dates=["start", "end"])
    return {row.ticker: (row.start, row.end) for row in meta.itertuples(index=False)}

def _set_meta(conn: Connection, ticker: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO meta (ticker, start, end) VALUES (?, ?, ?)",
        (ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")),
    )
    conn.commit()

def _download(tickers: list[str], **kwargs) -> pd.DataFrame:
    prices = yf.download(tickers, auto_adjust=True, **kwargs)["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(tickers[0])
    return prices

def get_prices(tickers: list[str], start: str) -> pd.DataFrame:
    conn = _connect()
    start_ts = pd.Timestamp(start)
    today = pd.Timestamp.today().normalize()
    meta = _read_meta(conn)

    # find missing tickers
    missing = [t for t in tickers if t not in meta]
    if missing:
        _store(conn, _download(missing, start=start))
        for ticker in missing:
            _set_meta(conn, ticker, start_ts, today)

    # check range of stored data
    for ticker in tickers:
        if ticker in missing:
            continue

        have_start, have_end = meta[ticker]

        if start_ts < have_start:
            _store(conn, _download([ticker], start=start, end=have_start))
            have_start = start_ts

        if today > have_end and today.weekday() < 5:
            _store(conn, _download([ticker], start=have_end + timedelta(days=1)))
            have_end = today

        if (have_start, have_end) != meta[ticker]:
            _set_meta(conn, ticker, have_start, have_end)

    # query
    tickers_str = ",".join("?" * len(tickers))
    df = pd.read_sql(
        f"SELECT date, ticker, close FROM prices WHERE ticker IN ({tickers_str})",
        conn,
        params=tickers,
        parse_dates=["date"],
    )
    conn.close()

    return df.pivot(index="date", columns="ticker", values="close")


def reset() -> None:
    if not os.path.exists(DB_PATH):
        return

    conn = _connect()
    tickers = pd.read_sql("SELECT DISTINCT ticker FROM prices", conn)["ticker"].tolist()
    conn.execute("DELETE FROM prices")
    conn.execute("DELETE FROM meta")
    conn.commit()

    if tickers:
        _store(conn, _download(tickers, period="max"))
        today = pd.Timestamp.today().normalize()
        min_dates = pd.read_sql(
            "SELECT ticker, MIN(date) AS min_date FROM prices GROUP BY ticker",
            conn,
            parse_dates=["min_date"],
        )
        for row in min_dates.itertuples(index=False):
            _set_meta(conn, row.ticker, row.min_date, today)

    conn.close()


if __name__ == "__main__":
    reset()
