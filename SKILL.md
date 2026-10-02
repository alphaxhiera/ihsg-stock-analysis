---
name: ihsg-stock-analysis
description: Analyze Indonesian stocks (IHSG / IDX / BEI) and the Jakarta Composite Index — technical, fundamental, flow and risk analysis with a structured report. Use whenever the user mentions IHSG, IDX, BEI, saham, emiten, a 4-letter ticker (BBCA, BBRI, TLKM, GOTO, ADRO…), "analisa saham", "layak beli?", support/resistance, entry/stop-loss, dividend yield, or asks about the Indonesian market, even if they do not say "analysis".
version: 1.0.0
author: Community
license: MIT
metadata:
  hermes:
    tags: [finance, stocks, indonesia, ihsg, idx, technical-analysis, fundamental-analysis]
    category: finance
---

# IHSG / IDX Stock Analysis

Produce a structured, data-grounded analysis of an IDX-listed stock or of IHSG itself. This is educational analysis, not personalized investment advice.

## When to use

- User gives a ticker (e.g. `BBCA`, `BBRI.JK`) or company name and asks for analysis, outlook, entry/exit, valuation, or comparison.
- User asks about IHSG condition, sector rotation, foreign flow, or market outlook.
- User asks to screen/compare several emiten.

Reply in the user's language (Indonesian or English). Keep tickers uppercase, prices in IDR, and use Indonesian terms where the user does (ARA, ARB, lot, fraksi harga).

## Workflow

1. **Clarify only if essential.** Defaults: horizon = swing (days–weeks) if unspecified; state the assumption in one line. Don't interrogate the user.
2. **Fetch data** (never invent numbers):
   - Price/technicals: run `python scripts/ihsg_ta.py TICKER [--period 1y]` (uses yfinance, `.JK` suffix added automatically; `^JKSE` for IHSG). If unavailable, fall back to web search/fetch (IDX, Yahoo Finance, Stockbit, RTI, Bisnis, Kontan, CNBC Indonesia) and compute by hand.
   - Fundamentals: latest quarterly/annual report figures (revenue, net profit, margins, ROE, DER, EPS, BVPS, dividend). Prefer IDX disclosure / company IR over aggregators.
   - Catalysts: search for recent news, corporate actions (rights issue, buyback, stock split, dividend cum/ex dates, RUPS), regulator notices.
   - Market context: IHSG trend, USD/IDR, BI rate, foreign net buy/sell, commodity prices if relevant to the sector.
3. **Run the checks** in `references/checklist.md` (IDX-specific risks: board, UMA/FCA, liquidity, free float, tick size).
4. **Synthesize** into the report format below. Give a verdict with explicit conditions that would invalidate it.
5. **Cite sources and timestamps.** Say when data was fetched and flag anything stale (>1 trading day for price, >1 quarter for fundamentals).

## Analysis framework

**Technical (swing view)**
- Trend: price vs SMA20/50/200, EMA structure, higher-highs/lows.
- Momentum: RSI(14), MACD(12,26,9), divergences.
- Volatility: ATR(14), Bollinger width; use ATR for stop sizing.
- Volume: vs 20-day average, accumulation/distribution, value traded (liquidity).
- Levels: support/resistance from swing pivots (script output) plus round numbers. **Round every level to a valid IDX tick** (see `references/idx-rules.md`).

**Fundamental**
- Profitability and growth (YoY, QoQ), margin trend.
- Balance sheet: DER, net debt/EBITDA, interest coverage (banks: NPL, CAR, LDR, NIM, CASA).
- Valuation: PER, PBV, EV/EBITDA, dividend yield vs own 5y history and sector peers.
- Quality: cash flow vs earnings, related-party exposure, governance red flags, free float.

**Flow & sentiment**
- Foreign net buy/sell (trend, not a single day), broker summary if available, insider/major shareholder transactions (KSEI/OJK disclosures).

**Sector & macro**
- Rate sensitivity (banks, property), commodity linkage (coal, nickel, CPO), rupiah sensitivity (importers/exporters), policy risk (state-owned, regulated tariffs).

## Output format

```
# {TICKER} — {Company}  |  {date}, data as of {timestamp}
**Verdict:** Bullish / Neutral / Bearish  (horizon: …, confidence: Low/Med/High)

## Snapshot
Price, 1D/1M/YTD change, volume vs avg, market cap, PER, PBV, div. yield

## Technical
Trend · Momentum · Volume · Key levels (support / resistance, tick-valid)

## Fundamental
3–5 bullets with numbers and peer comparison

## Flow & Catalysts
Foreign flow, upcoming events (with dates), news

## Scenario plan (illustrative)
| Scenario | Trigger | Entry zone | Stop (ATR-based) | Target | R:R |
Bull / Base / Bear

## Risks
Top 3–5 specific risks, incl. IDX-specific ones

## What would change my view
Concrete invalidation conditions
```

For IHSG itself, replace Snapshot/Fundamental with index level, sector heatmap, foreign flow, top contributors/draggers, USD/IDR, and BI rate.
For multi-stock comparison, lead with a compact table (valuation, momentum, yield, liquidity) and rank with reasoning.

## Rules

- **No fabricated data.** If a figure can't be retrieved, say "not available" and explain impact.
- **No guarantees or hype.** Avoid "pasti naik", "guaranteed". Present probabilities and conditions.
- **Always include risk**: position sizing hint (e.g. risk ≤1–2% of capital per trade via stop distance), and that 1 lot = 100 shares.
- **Flag manipulation-prone setups**: small-cap, low free float, sudden volume spikes without news, UMA/FCA/special-monitoring board, suspension history. Advise caution rather than promoting them.
- **Don't act as a signal service for "gorengan"**; analyze objectively and highlight the risk.
- **Costs matter**: include approximate round-trip broker fee + 0.1% sell tax in net R:R (verify the user's broker rates).
- End with a one-line disclaimer: educational analysis, not investment advice (*bukan ajakan membeli/menjual*); DYOR and consider a licensed advisor.

## Resources

- `scripts/ihsg_ta.py` — fetch OHLCV and compute indicators, pivots, ATR-based stops; JSON or text output. Run `--help`.
- `references/idx-rules.md` — tick size, lots, auto-reject, trading hours, boards, settlement, fees. **Verify against idx.co.id; rules change.**
- `references/checklist.md` — pre-report checklist and sector-specific metrics.
