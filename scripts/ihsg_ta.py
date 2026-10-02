#!/usr/bin/env python3
"""IHSG / IDX technical snapshot.

Usage:
  python ihsg_ta.py BBCA                # -> BBCA.JK, 1y daily
  python ihsg_ta.py ^JKSE --period 2y   # IHSG
  python ihsg_ta.py BBRI --json
  python ihsg_ta.py X --csv prices.csv  # offline: Date,Open,High,Low,Close,Volume

Requires: pandas, numpy; yfinance for online fetch (pip install yfinance).
Educational use only. Not investment advice.
"""
import argparse, json, sys
import numpy as np
import pandas as pd


def tick_size(p):
    if p < 200: return 1
    if p < 500: return 2
    if p < 2000: return 5
    if p < 5000: return 10
    return 25


def round_tick(p, mode="nearest"):
    t = tick_size(p)
    f = {"nearest": round, "down": np.floor, "up": np.ceil}[mode]
    return float(f(p / t) * t)


def fetch(ticker, period):
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("yfinance not installed. Run: pip install yfinance (or use --csv)")
    sym = ticker.upper()
    if not sym.startswith("^") and not sym.endswith(".JK"):
        sym += ".JK"
    df = yf.Ticker(sym).history(period=period, interval="1d", auto_adjust=False)
    if df.empty:
        sys.exit(f"No data for {sym}. Check the ticker or network access.")
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return sym, df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def atr(df, n=14):
    pc = df["Close"].shift()
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - pc).abs(), (df["Low"] - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def pivots(df, w=5, k=3):
    hi, lo = df["High"], df["Low"]
    ph = [hi.iloc[i] for i in range(w, len(df) - w) if hi.iloc[i] == hi.iloc[i - w:i + w + 1].max()]
    pl = [lo.iloc[i] for i in range(w, len(df) - w) if lo.iloc[i] == lo.iloc[i - w:i + w + 1].min()]
    last = df["Close"].iloc[-1]
    res = sorted({round_tick(x) for x in ph if x > last})[:k]
    sup = sorted({round_tick(x) for x in pl if x < last}, reverse=True)[:k]
    return sup, res


def analyze(df):
    c = df["Close"]
    out = {}
    last = float(c.iloc[-1])
    for n in (20, 50, 200):
        out[f"sma{n}"] = float(c.rolling(n).mean().iloc[-1]) if len(c) >= n else None
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    sig = macd.ewm(span=9, adjust=False).mean()
    out["macd"], out["macd_signal"], out["macd_hist"] = float(macd.iloc[-1]), float(sig.iloc[-1]), float((macd - sig).iloc[-1])
    out["rsi14"] = float(rsi(c).iloc[-1])
    a = float(atr(df).iloc[-1]); out["atr14"] = a; out["atr_pct"] = a / last * 100
    m, s = c.rolling(20).mean(), c.rolling(20).std()
    ub, lb = float((m + 2 * s).iloc[-1]), float((m - 2 * s).iloc[-1])
    out["bb_upper"], out["bb_lower"], out["bb_pctb"] = ub, lb, (last - lb) / (ub - lb)
    v = df["Volume"]
    out["vol_ratio_20d"] = float(v.iloc[-1] / v.rolling(20).mean().iloc[-1])
    out["avg_value_20d_idr_bn"] = float((c * v).rolling(20).mean().iloc[-1] / 1e9)
    out["high_52w"], out["low_52w"] = float(df["High"].tail(252).max()), float(df["Low"].tail(252).min())
    out["ret_1m_pct"] = float((last / c.iloc[-21] - 1) * 100) if len(c) > 21 else None
    out["ret_3m_pct"] = float((last / c.iloc[-63] - 1) * 100) if len(c) > 63 else None
    out["support"], out["resistance"] = pivots(df)
    s50, s200 = out["sma50"], out["sma200"]
    if s50 and s200:
        out["trend"] = "uptrend" if last > s50 > s200 else "downtrend" if last < s50 < s200 else "mixed/range"
    else:
        out["trend"] = "insufficient data"
    out["stop_1p5atr"] = round_tick(last - 1.5 * a, "down")
    out["stop_2atr"] = round_tick(last - 2 * a, "down")
    out["target_2r"] = round_tick(last + 2 * 1.5 * a, "up")
    out["last"], out["tick"] = last, tick_size(last)
    out["liquidity_flag"] = "LOW (<IDR 1bn/day)" if out["avg_value_20d_idr_bn"] < 1 else "ok"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--period", default="1y")
    ap.add_argument("--csv")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.csv:
        df = pd.read_csv(a.csv, index_col=0, parse_dates=True); sym = a.ticker or "CSV"
    elif a.ticker:
        sym, df = fetch(a.ticker, a.period)
    else:
        ap.error("ticker or --csv required")
    r = analyze(df); r["symbol"] = sym; r["as_of"] = str(df.index[-1].date())
    if a.json:
        print(json.dumps(r, indent=2, default=float)); return
    print(f"{sym} as of {r['as_of']}  last={r['last']:,.0f} (tick {r['tick']})  trend={r['trend']}")
    for k in ("sma20", "sma50", "sma200", "rsi14", "macd_hist", "atr14", "atr_pct", "bb_pctb",
              "vol_ratio_20d", "avg_value_20d_idr_bn", "ret_1m_pct", "ret_3m_pct", "high_52w", "low_52w",
              "stop_1p5atr", "stop_2atr", "target_2r"):
        v = r[k]; print(f"  {k:22s} {v:,.2f}" if isinstance(v, float) else f"  {k:22s} {v}")
    print("  support               ", r["support"]); print("  resistance            ", r["resistance"])
    print("  liquidity             ", r["liquidity_flag"])


if __name__ == "__main__":
    main()
