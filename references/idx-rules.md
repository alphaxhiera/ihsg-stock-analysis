# IDX Market Rules (reference)

> Rules change. Before quoting ARA/ARB limits, trading hours or fees as fact, verify at idx.co.id or recent news. Treat values below as defaults.

## Basics
- Currency IDR. **1 lot = 100 shares.** Settlement T+2 (regular market).
- Index: IHSG = `^JKSE` (Yahoo). Tickers on Yahoo use `.JK` (e.g. `BBCA.JK`). Other indices: LQ45, IDX30, KOMPAS100, IDX80, sectoral IDX-IC.

## Tick size (fraksi harga, regular board)
| Price (IDR) | Tick |
|---|---|
| < 200 | 1 |
| 200 – < 500 | 2 |
| 500 – < 2,000 | 5 |
| 2,000 – < 5,000 | 10 |
| ≥ 5,000 | 25 |

Round every entry/stop/target to a valid tick.

## Auto rejection (ARA/ARB)
Daily price limits vary by price band, board and period (and have been adjusted by IDX/OJK in recent years, including temporary measures during volatility). Always check the current rule. Special monitoring board and IPO/new-listing days have different limits.

## Trading hours (WIB, indicative)
- Mon–Thu: session I 09:00–12:00, session II 13:30–15:49, pre-closing ~15:50–16:00.
- Fri: session I 09:00–11:30, session II 14:00–15:49, pre-closing ~15:50–16:00.
- Verify; hours are adjusted around holidays and Ramadan.

## Boards
- Regular (Papan Utama / Pengembangan / Akselerasi), Special Monitoring Board (Papan Pemantauan Khusus, full call auction), plus UMA (unusual market activity) and FCA notices. Treat any of these as a risk flag.
- Suspensions (suspensi) can freeze the position for days to months.

## Costs (typical, verify per broker)
- Buy ≈ 0.10–0.15% · Sell ≈ 0.20–0.25% (incl. 0.10% final sell tax).
- Dividends: 10% final tax for residents (check current).

## Corporate actions & calendar
- Key dates: cum-date, ex-date, recording date, payment date. Price adjusts on ex-date.
- Watch: RUPS, rights issue (HMETD), stock split/reverse split, buyback, tender offer, delisting notices.

## Data caveats
- Yahoo `.JK` data can lag, miss splits, or have gaps; cross-check against IDX for critical decisions.
- Volume in shares (divide by 100 for lots). Liquidity: prefer average daily traded value > IDR 5–10 bn for tradable entries; flag below IDR 1 bn.
