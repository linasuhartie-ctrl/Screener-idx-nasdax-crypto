# GPR Market Scanner — IDX, US, Crypto

Streamlit scanner using the existing GPR projection algorithm and Yahoo Finance/yfinance OHLCV data.

## Universe behavior
- **US:** downloads public Nasdaq Trader symbol directories (Nasdaq-listed + other-listed) and caches them for 6 hours.
- **Crypto:** queries Yahoo Finance's `all_cryptocurrencies_us` screener and keeps USD pairs; cached for 6 hours.
- **IDX:** attempts to read ticker-like symbols from the public IDX listed-share pages; if IDX doesn't expose a parseable table, falls back to the bundled list. The source label in the app tells you which path was used.

No public data source guarantees that every symbol is supported by Yahoo Finance or has enough candles for the selected timeframe. A symbol can appear in the universe and still fail analysis. Intraday histories have shorter coverage than daily histories. Scan in batches to reduce rate limiting; partial results remain in the current Streamlit session.

## Deploy
Keep `requirements.txt` in the repository root. If Streamlit Cloud currently runs `streamlit_app.py`, replace that file with the supplied `streamlit_app.py`; `app.py` is also included as an equivalent entrypoint. Commit both files and `requirements.txt`.

The GPR projection, ranking, GPR return, uncertainty estimate, selected-asset chart, and CSV export are retained. Uncertainty is model uncertainty, not a probability of profit or loss. Outputs are experimental and are not investment advice.
