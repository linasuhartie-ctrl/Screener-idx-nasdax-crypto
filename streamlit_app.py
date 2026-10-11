import os
import math
import time
from typing import Any

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="GPR Market Scanner", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "300"))

FALLBACK_CODES = """
AADI AALI ABBA ABDA ABMM ACES ACRO ACST ADCP ADES ADHI ADMF ADMG ADMR ADRO
AGAR AGII AIMS AISA AKKU AKPI AKRA AKSI ALDO ALKA ALMI ALTO AMAG AMAN AMAR
AMFG AMIN AMMN AMMS AMOR ANJT ANTM APII APIC APLI APMI ARCI ARGO ARII ARKA
ARKO ARNA ARTA ARTO ASBI ASDM ASGR ASII ASJT ASLC ASLI ASMI ASPI ASRI ASRM
ASSA ATAP AUTO AVIA AWAN AYLS BAPA BAPI BATA BAYU BBCA BBHI BBKP BBLD BBNI
BBRI BBSI BBTN BBYB BCAP BCIC BCIP BDMN BEBS BEEF BEKS BELI BELL BESS BEST
BFIN BGTG BHAT BHIT BIKA BIMA BINA BINO BIPP BIRD BISI BJBR BJTM BKDP BKSL
BKSW BLTA BLTZ BMAS BMRI BMTR BNBA BNGA BNII BNLI BOBA BOGA BOLA BOLT BRAM
BREN BRIS BRMS BRNA BRPT BSDE BSIM BSSR BTEK BTEL BTON BTPN BTPS BUDI BULL
BUMI BUVA BYAN CAMP CARE CASH CASS CBMF CBPE CCSI CEKA CENT CFIN CHEM CINT
CITA CITY CLAY CLEO CMNP CMOA CMNT CPRO CPIN CPRI CSAP CSIS CTBN CTTH CTRA
CTRA CUAN CYBR DADA DART DAYA DCII DEFI DEPO DEWA DGIK DGNS DGWG DILD DKFT
DMAS DMMX DMND DNAR DOID DPNS DPUM DRMA DSFI DSNG DSSA DUTI DVLA DWGL EAST
ECII EDGE EKAD ELIT ELSA ELTY EMDE EMTK ENAK ENRG ENZO EPAC ERAA ERAL ESIP
ESSA ESTI ETWA EURO EXCL FAPA FAST FILM FIRE FISH FITT FLMC FMII FOLK FOOD
FORU FPNI FUTR GAMA GDST GDYR GEMA GEMS GGRM GGRP GHON GIAA GJTL GLVA GMFI
GMTD GOLD GOOD GPRA GPSO GRPM GSMF GTBO GTRA GTSI GULA GUNA GWSA HADE HAIS
HATM HBAT HDFA HDTX HEAL HELI HERO HEXA HITS HKMU HOME HOTL HRME HRTA HRUM
IATA IBFN IBST IBOS ICCA ICON IDEA IFII IKAI IKAN IKBI IKPM IMAS IMJS IMPC
INAF INAI INCI INCO INDF INDR INDS INDX INDY INKP INOV INPC INPP INRU INTA
INTD INTP IPCC IPCM IPOL IPPE IPTV IRRA IRSX ISAT ISSP ITIC ITMA ITMG JARR
JAST JATI JAWA JECC JGLE JIHD JKON JMAS JPFA JRPT JSKY JSMR JTPE KAEF KAYU
KBAG KBLI KBLM KBRI KDSI KDTN KEEN KEJU KIAS KIJA KINO KIOS KKGI KLBF KMDS
KMTR KOBX KOIN KONI KOPI KPIG KREN KRYA LABA LAJU LAND LAPD LCAS LCKM LEAD
LINK LMAS LMPI LOPI LPCK LPKR LPPF LRNA LSIP LTLS LUCY MAGP MAIN MAPA MAPB
MAPI MARK MASA MASB MAYA MBAP MBSS MBTO MCAS MCOL MDIA MDKA MDKI MDLN MDRN
MEDC MEGA MERK META MFMI MGNA MGRO MICE MIDI MIKA MINA MIRA MITI MKNT MKPI
MLBI MLIA MLPL MLPT MLPT MLPT MMIX MMLP MMSI MNCN MPPA MPMX MREI MSIN MTDL
MTEL MTLA MTMH MTPS MTRA MTWI MULT MYOH MYOR MYTX NASI NATO NELY NEST NETV
NICL NIKL NIPS NISP NOBU NRCA NSSS NUSA OASA OBMD OCAP OKAS OMRE OPMS PADI
PALM PAMG PANI PANR PANS PBID PBRX PBSA PCAR PDES PEGE PEHA PGAS PGEO PGLI
PGUN PICO PJAA PKPK PLAN PLIN PMJS PMMP PMUI PNBN PNBS PNGO PNIN PNSE POLI
POLL POLU PORT POWR PPRE PPRO PRDA PRIM PSAB PSAT PSDN PSKT PTPP PUDP PURA
PURE PWON PYFA RAJA RALS RANC RBMS RDTX REAL RELI RICY RIGS RISE RMBA RMKE
ROCK RODA ROTI RUIS RUNS SAFE SAME SAMF SAPX SATU SBAT SBCS SBMA SCCO SCMA
SCNP SDMU SDPC SDRA SGRO SHID SHIP SICO SIDO SILO SIMA SIMP SIPD SKBM SKLT
SKRN SLIS SMAR SMBR SMCB SMDM SMDR SMGA SMGR SMIL SMKL SMKM SMMT SMRA SMSM
SNLK SOCI SOFA SOHO SOSS SOTS SPMA SPTO SQMI SRAJ SRTG SSIA SSMS SSTM STAR
STTP SUNI SUPR SURE SWAT SWID TALF TAMU TBIG TBLA TBMS TCID TCPI TDPM TELE
TFAS TGKA TGRA TIFA TINS TIRA TKIM TLKM TLDN TMAS TMPO TNCA TOBA TOPS TOTL
TOTO TOWR TPIA TPMA TRGU TRIL TRIM TRIN TRIO TRIS TRJA TRON TRUE TSCP TUGU
TYRE UANG UCID ULTJ UNIC UNIT UNTR UNVR VICI VINS VKTR VRNA WAPO WEGE WEHA
WIFI WIKA WINR WINS WIRG WMPP WMUU WTON YPAS ZATA ZBRA ZINC ZONE
""".split()
FALLBACK_CODES = list(dict.fromkeys(FALLBACK_CODES))

# Curated universes: convenient starting lists, not a claim of complete live listings.
US_CODES = """
AAPL MSFT NVDA AMZN GOOGL META AVGO TSLA BRK-B JPM WMT LLY V MA XOM ORCL COST NFLX JNJ HD PG ABBV BAC KO CRM CVX AMD TMUS MRK WFC CSCO ACN IBM MCD LIN ABT GE NOW PEP TMO DIS QCOM TXN CAT AMGN INTU DHR VZ PM RTX UNH COP GS SPGI ISRG AMAT BKNG LOW PFE C SCHW BLK ANET MU LRCX ADI SYK PANW KLAC HON DE CAT UBER NKE PLTR ARM SHOP SNOW CRWD DDOG NET COIN HOOD SQ PYPL TGT F GM FDX UPS BA INTC CMCSA T RBLX ABNB DASH MAR ROST CHTR MDT BMY GILD CVS ELV CI REGN ZTS SO DUK NEE CEG FSLR ENPH OXY SLB HAL EOG PSX MPC VLO KMI OKE PBR BABA BIDU JD PDD TSM ASML SAP SONY TM HMC NVO AZN SHEL RIO BHP VALE
""".split()
CRYPTO_CODES = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "ADA-USD", "TRX-USD",
    "AVAX-USD", "LINK-USD", "DOT-USD", "BCH-USD", "LTC-USD", "SHIB-USD", "TON-USD", "SUI-USD",
    "NEAR-USD", "APT-USD", "ICP-USD", "ETC-USD", "XLM-USD", "HBAR-USD", "FIL-USD", "ATOM-USD",
    "ARB-USD", "OP-USD", "INJ-USD", "AAVE-USD", "UNI-USD", "RENDER-USD", "FET-USD", "MKR-USD",
    "PEPE-USD", "TAO-USD", "IMX-USD", "GRT-USD", "ALGO-USD", "VET-USD", "EOS-USD", "XTZ-USD"
]

def normalize_yf_history(raw: pd.DataFrame) -> pd.DataFrame:
    if raw is None or raw.empty:
        return pd.DataFrame()
    df = raw.copy()
    if isinstance(df.columns, pd.MultiIndex):
        # Single-symbol history should be flattened, but tolerate yfinance's multi-index output.
        df.columns = [str(col[0]) if isinstance(col, tuple) else str(col) for col in df.columns]
    df = df.reset_index()
    aliases = {"Date": "time", "Datetime": "time", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}
    df = df.rename(columns=aliases)
    if "close" not in df.columns:
        return pd.DataFrame()
    for col in ("open", "high", "low"):
        if col not in df.columns:
            df[col] = df["close"]
    if "volume" not in df.columns:
        df["volume"] = 0.0
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
        df = df.sort_values("time")
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["close"]).reset_index(drop=True)


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def get_history_cached(market: str, code: str, timeframe: str, cache_buster: int = 0) -> pd.DataFrame:
    interval_map = {"5m": "5m", "15m": "15m", "1h": "1h", "1d": "1d"}
    period_map = {"5m": "60d", "15m": "60d", "1h": "730d", "1d": "5y"}
    ticker = f"{code}.JK" if market == "IDX" else code
    try:
        raw = yf.Ticker(ticker).history(
            period=period_map.get(timeframe, "5y"),
            interval=interval_map.get(timeframe, "1d"),
            auto_adjust=False,
            actions=False,
            timeout=20,
        )
    except Exception as exc:
        raise RuntimeError(f"Yahoo Finance: {type(exc).__name__}: {str(exc)[:130]}") from exc
    return normalize_yf_history(raw)


def ema(series, length):
    return series.ewm(span=length, adjust=False, min_periods=1).mean()


def matern32_kernel(x, z, amplitude, scale):
    d = x - z
    distance2 = d[0]**2 + 0.8*d[1]**2 + 0.6*d[2]**2 + 0.8*d[3]**2 + 0.6*d[4]**2
    u = math.sqrt(3.0 * max(float(distance2), 0.0)) / scale
    return amplitude * (1.0 + u) * math.exp(-u)


def gpr_project(df, horizon=10, training=30, momentum_len=5, vol_len=14,
                ema_fast=8, ema_slow=21, kernel_scale=1.5, noise_ratio=0.30,
                volume_fade=0.65, atr_width=0.70):
    min_needed = max(training + vol_len + ema_slow + 10, 60)
    if len(df) < min_needed:
        raise ValueError(f"Data candle hanya {len(df)}; perlu minimal sekitar {min_needed}.")
    close = df["close"].astype(float).to_numpy()
    volume = df["volume"].fillna(0).astype(float).to_numpy()
    high = df["high"].astype(float).to_numpy()
    low = df["low"].astype(float).to_numpy()

    logret = np.full(len(close), np.nan)
    logret[1:] = np.log(np.maximum(close[1:], 1e-12) / np.maximum(close[:-1], 1e-12))
    ret_series = pd.Series(logret)
    momentum = ret_series.ewm(span=momentum_len, adjust=False, min_periods=1).mean().to_numpy()
    volatility = ret_series.rolling(vol_len, min_periods=vol_len).std(ddof=1).to_numpy()
    vol_base = pd.Series(volatility).rolling(training, min_periods=training).mean().to_numpy()
    avg_volume = pd.Series(volume).rolling(vol_len, min_periods=1).mean().to_numpy()
    rel_volume = np.zeros(len(close))
    valid = (volume > 0) & (avg_volume > 0)
    rel_volume[valid] = np.log(volume[valid] / avg_volume[valid])
    fast = ema(pd.Series(close), ema_fast).to_numpy()
    slow = ema(pd.Series(close), ema_slow).to_numpy()
    direction = (fast - slow) / np.maximum(close, 1e-12)

    prev_close = np.r_[np.nan, close[:-1]]
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    tr[0] = high[0] - low[0]
    atr = pd.Series(tr).ewm(alpha=1/vol_len, adjust=False, min_periods=vol_len).mean().to_numpy()

    idx = len(df) - 1
    vol_ref = max(float(vol_base[idx]) if np.isfinite(vol_base[idx]) else 0.0, 0.0001)
    if not np.isfinite(volatility[idx]) or not np.isfinite(atr[idx]) or not np.isfinite(logret[idx]):
        raise ValueError("Indikator belum siap pada candle terakhir.")

    X, y = [], []
    for r in range(training):
        target_idx = idx - training + 1 + r
        feature_idx = target_idx - 1
        if feature_idx < 1 or not np.isfinite(logret[target_idx]):
            continue
        X.append([
            logret[feature_idx] / vol_ref,
            momentum[feature_idx] / vol_ref,
            rel_volume[feature_idx],
            (volatility[feature_idx] / vol_ref - 1.0) if np.isfinite(volatility[feature_idx]) else 0.0,
            direction[feature_idx] / vol_ref,
        ])
        y.append(logret[target_idx])

    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n = len(y)
    if n < max(20, training - 3):
        raise ValueError("Observasi training valid terlalu sedikit.")

    signal_var = max(float(np.mean(y*y)), 1e-8)
    noise_var = signal_var * noise_ratio + 1e-10
    K = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1):
            value = matern32_kernel(X[i], X[j], signal_var, kernel_scale)
            if i == j:
                value += noise_var
            K[i, j] = K[j, i] = value
    try:
        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
    except np.linalg.LinAlgError:
        raise ValueError("Matriks GPR tidak stabil.")

    price_start = float(close[idx])
    price_prev = price_start
    ret_prev = float(logret[idx])
    mom_prev = float(momentum[idx])
    fast_prev, slow_prev = float(fast[idx]), float(slow[idx])
    volume_prev = float(rel_volume[idx])
    vol_prev = float(volatility[idx])
    cumulative_return = 0.0
    predictions = []
    # Approximate GPR posterior uncertainty for each predicted log-return.
    # The cumulative value assumes forecast errors are independent across steps;
    # it is a model-uncertainty estimate, NOT a probability of loss or success.
    cumulative_variance = 0.0

    for h in range(horizon):
        fade = volume_fade ** h
        assumed_vol = vol_ref + (vol_prev - vol_ref) * fade
        x_star = np.array([
            ret_prev / vol_ref,
            mom_prev / vol_ref,
            volume_prev * fade,
            assumed_vol / vol_ref - 1.0,
            ((fast_prev - slow_prev) / max(price_prev, 1e-12)) / vol_ref,
        ])
        kstar = np.array([matern32_kernel(X[i], x_star, signal_var, kernel_scale) for i in range(n)])
        pred_ret = float(kstar @ alpha)
        try:
            solved = np.linalg.solve(L, kstar)
            predictive_variance = max(float(signal_var - solved @ solved), 0.0)
        except (np.linalg.LinAlgError, ValueError):
            predictive_variance = 0.0
        cumulative_variance += predictive_variance
        cumulative_return += pred_ret
        price_pred = price_start * math.exp(cumulative_return)
        distance = atr_width * float(atr[idx]) * math.sqrt(h + 1.0)
        predictions.append({
            "step": h + 1,
            "price": round(price_pred, 4),
            "return_pct": round((price_pred / price_start - 1.0) * 100.0, 3),
            "upper": round(price_pred + distance, 4),
            "lower": round(max(0.0001, price_pred - distance), 4),
        })
        price_prev = price_pred
        ret_prev = pred_ret
        a_m = 2.0 / (momentum_len + 1.0)
        mom_prev = a_m * pred_ret + (1.0-a_m) * mom_prev
        a_f = 2.0 / (ema_fast + 1.0)
        a_s = 2.0 / (ema_slow + 1.0)
        fast_prev = a_f * price_pred + (1.0-a_f) * fast_prev
        slow_prev = a_s * price_pred + (1.0-a_s) * slow_prev

    latest_price = float(close[idx])
    trend = "BULLISH" if fast[idx] > slow[idx] else "BEARISH"
    mom_now = float(momentum[idx]) if np.isfinite(momentum[idx]) else 0.0
    vol_now = float(volume[idx])
    vol_avg = float(avg_volume[idx]) if np.isfinite(avg_volume[idx]) else 0.0
    rel_vol = vol_now / vol_avg if vol_avg > 0 else 0.0
    final = predictions[-1]

    return {
        "price": round(latest_price, 4),
        "trend": trend,
        "momentum": "POSITIVE" if mom_now > 0 else "NEGATIVE",
        "relative_volume": round(rel_vol, 2),
        "gpr_return_pct": final["return_pct"],
        "uncertainty_pct": round(math.sqrt(max(cumulative_variance, 0.0)) * 100.0, 2),
        "projected_price": final["price"],
        "upper": final["upper"],
        "lower": final["lower"],
        "horizon": horizon,
        "predictions": predictions,
        "as_of": str(df.iloc[idx].get("time", "")),
        "bars": len(df),
    }




def analyze_one(market: str, code: str, timeframe: str, horizon: int) -> dict:
    hist = get_history_cached(market, code, timeframe, int(time.time() // CACHE_SECONDS))
    if hist.empty:
        raise ValueError("Data historis kosong/tidak tersedia dari Yahoo Finance.")
    result = gpr_project(hist, horizon=horizon)
    result["code"] = code
    result["market"] = market
    score = max(0, min(100,
        35 * (1 if result["trend"] == "BULLISH" else 0)
        + 20 * (1 if result["momentum"] == "POSITIVE" else 0)
        + 20 * min(result["relative_volume"] / 2.0, 1.0)
        + 25 * max(0, min(result["gpr_return_pct"] / 5.0, 1.0))
    ))
    result["score"] = round(score, 1)
    result["signal"] = ("KANDIDAT" if result["trend"] == "BULLISH" and result["momentum"] == "POSITIVE" and result["gpr_return_pct"] > 0 else "PANTAU" if result["gpr_return_pct"] > 0 else "HINDARI")
    return result


@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def fetch_us_universe():
    """Fetch current US-listed symbols from Nasdaq Trader's public directories."""
    urls = [
        "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt",
        "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt",
    ]
    symbols = []
    headers = {"User-Agent": "Mozilla/5.0 GPR-Market-Scanner/1.0"}
    for url in urls:
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()
        lines = response.text.splitlines()
        if not lines:
            continue
        header = lines[0].split("|")
        symbol_idx = 0
        test_idx = header.index("Test Issue") if "Test Issue" in header else None
        for line in lines[1:]:
            if not line or line.startswith("File Creation Time"):
                continue
            fields = line.split("|")
            if len(fields) <= symbol_idx:
                continue
            symbol = fields[symbol_idx].strip()
            if test_idx is not None and len(fields) > test_idx and fields[test_idx].strip() == "Y":
                continue
            # Yahoo uses '-' for share-class dots (e.g. BRK-B); discard malformed directory rows.
            if symbol and symbol not in {"Symbol", "ACT Symbol"} and all(c.isalnum() or c in ".-^" for c in symbol):
                symbols.append(symbol.replace(".", "-"))
    symbols = list(dict.fromkeys(symbols))
    if len(symbols) < 1000:
        raise RuntimeError("Direktori saham AS tidak lengkap/berhasil diunduh.")
    return symbols


@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def fetch_crypto_universe():
    """Fetch Yahoo Finance's current all-cryptocurrencies screener universe."""
    symbols = []
    headers = {"User-Agent": "Mozilla/5.0 GPR-Market-Scanner/1.0"}
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
    # Yahoo's screener returns up to 250 results per request; paginate until exhausted.
    for offset in range(0, 10000, 250):
        params = {"formatted": "false", "count": 250, "start": offset, "scrIds": "all_cryptocurrencies_us"}
        response = requests.get(url, params=params, timeout=20, headers=headers)
        response.raise_for_status()
        payload = response.json()
        results = payload.get("finance", {}).get("result") or []
        if not results:
            break
        quotes = results[0].get("quotes", [])
        batch = [q.get("symbol", "").strip() for q in quotes if q.get("symbol")]
        symbols.extend(batch)
        total = int(results[0].get("total", len(symbols)))
        if not batch or offset + len(batch) >= total:
            break
    symbols = [x for x in dict.fromkeys(symbols) if x.endswith("-USD")]
    if len(symbols) < 100:
        raise RuntimeError("Screener kripto Yahoo tidak mengembalikan daftar lengkap.")
    return symbols


@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def fetch_idx_universe():
    """Fetch IDX tickers from structured company-list tables; never scrape arbitrary 4-letter words."""
    urls = [
        "https://www.idx.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/",
        "https://block.idx.id/id/data-pasar/data-saham/daftar-saham/",
        "https://www.idx.co.id/id/data-pasar/ringkasan-perdagangan/ringkasan-saham/",
    ]
    headers = {"User-Agent": "Mozilla/5.0 GPR-Market-Scanner/1.0"}
    found = []
    for url in urls:
        try:
            response = requests.get(url, timeout=20, headers=headers)
            response.raise_for_status()
            # Parse table rows/columns only. Regex over the whole HTML wrongly counts
            # unrelated four-letter words as tickers (the source of the inflated 1,404).
            tables = pd.read_html(response.text)
            for table in tables:
                if table.empty:
                    continue
                cols = [str(c).strip().lower() for c in table.columns]
                ticker_col = None
                for i, col in enumerate(cols):
                    if any(word in col for word in ("kode", "code", "ticker", "symbol")):
                        ticker_col = i
                        break
                if ticker_col is None:
                    # Some IDX tables have a generic first column containing ranking,
                    # followed by the ticker code in the second column.
                    for i in range(min(3, len(cols))):
                        sample = table.iloc[:, i].astype(str).str.strip().str.upper()
                        matches = sample.str.fullmatch(r"[A-Z]{4,5}").sum()
                        if matches >= 5:
                            ticker_col = i
                            break
                if ticker_col is None:
                    continue
                for value in table.iloc[:, ticker_col].astype(str):
                    symbol = value.strip().upper()
                    if symbol in {"KODE", "CODE", "TICKER", "SYMBOL", "NAN", "NONE"}:
                        continue
                    if __import__("re").fullmatch(r"[A-Z]{4,5}", symbol):
                        found.append(symbol)
        except Exception:
            continue
    found = list(dict.fromkeys(found))
    # Accept live source only when it looks like a complete directory, not a single
    # paginated table or a page whose HTML did not render the data.
    if 800 <= len(found) <= 1200:
        return found, f"Direktori tabel IDX terstruktur ({len(found)} kode unik; refresh tiap 6 jam)"
    # Fallback is intentionally labeled; never pretend it is a complete current IDX list.
    fallback = list(dict.fromkeys(FALLBACK_CODES))
    return fallback, f"Fallback BEI ({len(fallback)} kode unik); direktori IDX lengkap gagal dimuat, daftar perlu diverifikasi"


def get_universe(market: str):
    if market == "IDX":
        try:
            codes, source = fetch_idx_universe()
            return codes, source
        except Exception:
            return FALLBACK_CODES.copy(), "Fallback BEI bawaan aplikasi; gagal mengambil direktori IDX"
    if market == "US":
        try:
            return fetch_us_universe(), "Direktori Nasdaq Trader: saham/simbol AS lintas bursa; refresh otomatis tiap 6 jam"
        except Exception:
            return list(dict.fromkeys(US_CODES)), "Fallback saham AS pilihan; gagal mengambil direktori live"
    try:
        return fetch_crypto_universe(), "Yahoo Finance All Cryptocurrencies USD; refresh otomatis tiap 6 jam"
    except Exception:
        return CRYPTO_CODES.copy(), "Fallback kripto pilihan; gagal mengambil screener live"


# ---------------------------- UI ----------------------------
st.markdown("""
<style>
.block-container {padding-top:1rem; padding-bottom:3rem; max-width:1500px;}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
[data-testid="stMetric"] {background:#111c2e; border:1px solid #26354a; padding:12px 14px; border-radius:12px;}
div.stButton > button {border-radius:10px; min-height:42px; font-weight:600;}
[data-testid="stDataFrame"] {border:1px solid #26354a; border-radius:12px; overflow:hidden;}
.note {font-size:0.88rem; color:#9ca3af;}
</style>
""", unsafe_allow_html=True)

st.title("📈 GPR MARKET SCANNER")
st.caption("Satu dashboard untuk saham BEI, saham Amerika, dan aset kripto")

with st.sidebar:
    st.subheader("Pengaturan scanner")
    market = st.selectbox("Pasar", ["IDX", "US", "Crypto"], format_func=lambda x: {"IDX":"🇮🇩 Saham Indonesia (BEI)", "US":"🇺🇸 Saham Amerika", "Crypto":"₿ Cryptocurrency"}[x])
    timeframe_label = st.selectbox("Timeframe", ["Harian", "1 jam", "15 menit", "5 menit"], index=0)
    timeframe = {"Harian":"1d", "1 jam":"1h", "15 menit":"15m", "5 menit":"5m"}[timeframe_label]
    horizon = st.selectbox("Horizon proyeksi (candle)", [3, 5, 10, 20], index=2)
    scan_size_label = st.selectbox("Target jumlah aset", ["50", "100", "300", "500", "Semua tersedia"], index=0)
    batch_size = st.selectbox("Ukuran batch manual", [100, 200, 300, 400, 500], index=0, help="Jumlah aset yang diproses setiap klik.")
    auto_scan = st.checkbox("Otomatis scan sampai target", value=False, help="Jika aktif, tombol scan akan melanjutkan batch 100 aset demi 100 aset sampai target selesai.")
    min_score = st.slider("Skor minimum ranking", 40, 80, 80, 5)
    st.caption("Filter skor hanya memengaruhi ranking, bukan jumlah aset yang dianalisis.")
    start_new = st.button("↻ Mulai scan baru", use_container_width=True)
    scan_next = st.button("▶ Mulai / lanjutkan scan", type="primary", use_container_width=True)

codes, universe_source = get_universe(market)
target_count = len(codes) if scan_size_label == "Semua tersedia" else min(int(scan_size_label), len(codes))

# Store scan state separately per market/timeframe so changing market doesn't mix results.
state_key = f"{market}_{timeframe}_{horizon}"
if "scanner_states" not in st.session_state:
    st.session_state.scanner_states = {}
if state_key not in st.session_state.scanner_states:
    st.session_state.scanner_states[state_key] = {"cursor":0, "results":[], "errors":[], "target":target_count, "source":universe_source}
state = st.session_state.scanner_states[state_key]
if start_new:
    state = {"cursor":0, "results":[], "errors":[], "target":target_count, "source":universe_source}
    st.session_state.scanner_states[state_key] = state
    st.rerun()
# Respect the latest target selection while preserving progress.
state["target"] = target_count

left, mid, right = st.columns([1.2, 1.2, 2.2])
left.metric("Aset tersedia", len(codes))
mid.metric("Target scan", target_count)
right.markdown(f"**Sumber data:** Yahoo Finance  \n<span class='note'>{universe_source}</span>", unsafe_allow_html=True)

st.info("IDX diambil dari kolom kode saham pada tabel publik (bukan hasil pencarian teks seluruh halaman). Jika direktori lengkap gagal dimuat, aplikasi memakai daftar cadangan dan menandainya. Scan manual tersedia per 100/200/300/400/500 aset; mode otomatis melanjutkan per 100 sampai target, sehingga bisa berjalan lama dan terkena rate limit.")

if scan_next:
    if state["cursor"] >= target_count:
        st.success("Target scan sudah selesai. Tekan 'Mulai scan baru' jika ingin mengulang.")
    else:
        # Manual mode processes the selected batch. Auto mode repeatedly processes
        # batches of 100 until target is reached, preserving progress after each asset.
        step_size = 100 if auto_scan else int(batch_size)
        progress = st.progress(min(state["cursor"] / max(1, target_count), 1.0), text="Menyiapkan scan…")
        status = st.empty()
        while state["cursor"] < target_count:
            batch_start = state["cursor"]
            stop = min(batch_start + step_size, target_count)
            for idx in range(batch_start, stop):
                code = codes[idx]
                known = {x["code"] for x in state["results"]} | {x["code"] for x in state["errors"]}
                if code not in known:
                    try:
                        row = analyze_one(market, code, timeframe, int(horizon))
                        state["results"].append(row)
                    except Exception as exc:
                        state["errors"].append({"code":code, "error":str(exc)[:200]})
                state["cursor"] = idx + 1
                progress.progress(state["cursor"] / max(1, target_count), text=f"Memproses {state['cursor']}/{target_count}: {code}")
                status.info(f"Progres {state['cursor']}/{target_count} · berhasil {len(state['results'])} · gagal {len(state['errors'])}")
                time.sleep(0.15)
            state["results"].sort(key=lambda x:(x["score"],x["gpr_return_pct"]), reverse=True)
            if not auto_scan:
                break
        if state["cursor"] >= target_count:
            status.success(f"Scan selesai. Progres {state['cursor']}/{target_count} aset.")
        else:
            status.success(f"Batch selesai. Progres {state['cursor']}/{target_count} aset. Tekan lanjutkan untuk batch berikutnya.")

results = state["results"]
errors = state["errors"]
qualified = [x for x in results if float(x.get("score",0)) >= min_score]
candidates = [x for x in qualified if x.get("signal") == "KANDIDAT"]
best_return = max((float(x["gpr_return_pct"]) for x in qualified), default=None)

m1,m2,m3,m4 = st.columns(4)
m1.metric("Berhasil dianalisis", len(results))
m2.metric("Lolos skor", len(qualified))
m3.metric("Kandidat", len(candidates))
m4.metric("GPR Return tertinggi", f"{best_return:+.2f}%" if best_return is not None else "—")

rank_tab, detail_tab, status_tab = st.tabs(["🏆 Ranking", "📈 Detail aset", "🧾 Status & error"])
with rank_tab:
    query = st.text_input("Cari simbol", placeholder="Contoh: BBCA, AAPL, BTC-USD")
    view = [x for x in qualified if query.strip().upper() in x["code"].upper()]
    view.sort(key=lambda x:(x["score"],x["gpr_return_pct"]), reverse=True)
    if view:
        table = []
        for rank, item in enumerate(view,1):
            score = float(item["score"])
            table.append({
                "Rank":rank, "Pasar":item["market"], "Kode":item["code"],
                "Kategori":"HIGH" if score>=80 else "MEDIUM–HIGH" if score>=60 else "MEDIUM",
                "Skor":score, "GPR Return (%)":item["gpr_return_pct"],
                "Uncertainty (%)":item.get("uncertainty_pct", np.nan),
                "Tren":item["trend"], "Momentum":item["momentum"],
                "Rel. Volume":item["relative_volume"], "Sinyal":item["signal"], "Harga":item["price"]
            })
        table_df = pd.DataFrame(table)
        st.dataframe(table_df, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Unduh ranking CSV", table_df.to_csv(index=False).encode("utf-8"), file_name=f"gpr_ranking_{market.lower()}.csv", mime="text/csv")
    else:
        st.info("Belum ada aset yang lolos skor. Jalankan batch atau turunkan skor minimum.")
with detail_tab:
    if results:
        codes_ready = [x["code"] for x in results]
        selected = st.selectbox("Pilih aset", codes_ready)
        item = next(x for x in results if x["code"] == selected)
        a,b,c,d = st.columns(4)
        a.metric("Harga terakhir", f"{item['price']:,.4f}")
        b.metric("Tren", item["trend"])
        c.metric("GPR Return", f"{item['gpr_return_pct']:+.2f}%")
        d.metric("Uncertainty", f"{item.get('uncertainty_pct', float('nan')):.2f}%")
        preds = item.get("predictions",[])
        if preds:
            chart = pd.DataFrame({"Candle":["Sekarang"]+[f"+{p['step']}" for p in preds], "Harga":[item["price"]]+[p["price"] for p in preds]}).set_index("Candle")
            st.line_chart(chart)
            st.dataframe(pd.DataFrame(preds), use_container_width=True, hide_index=True)
    else:
        st.info("Scan batch pertama untuk melihat detail aset.")
with status_tab:
    st.write(f"**Pasar:** {market}")
    st.write(f"**Provider:** Yahoo Finance via yfinance")
    st.write(f"**Universe:** {universe_source}")
    st.write(f"**Progres:** {state['cursor']} / {target_count}")
    st.write(f"**Berhasil:** {len(results)} · **Gagal:** {len(errors)} · **Belum diproses:** {max(0,target_count-state['cursor'])}")
    if errors:
        error_df = pd.DataFrame(errors)
        error_df["jenis_error"] = error_df["error"].apply(lambda e: "Data kosong/tidak tersedia" if "kosong" in str(e).lower() else "Data candle kurang" if "minimal" in str(e).lower() else "Rate limit/koneksi" if "429" in str(e) or "timeout" in str(e).lower() or "too many" in str(e).lower() else "Error lainnya")
        st.dataframe(error_df, use_container_width=True, hide_index=True)
    st.caption("Uncertainty adalah estimasi ketidakpastian model, bukan probabilitas keuntungan/kerugian. Hasil GPR bersifat eksperimental, bukan saran investasi.")
