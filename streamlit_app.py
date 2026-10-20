import os
import math
import time
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="GPR Market Scanner", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "300"))

# Cleaned fallback codes without duplicates
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
CUAN CYBR DADA DART DAYA DCII DEFI DEPO DEWA DGIK DGNS DGWG DILD DKFT
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
MLBI MLIA MLPL MLPT MMIX MMLP MMSI MNCN MPPA MPMX MREI MSIN MTDL MTEL MTLA
MTMH MTPS MTRA MTWI MULT MYOH MYOR MYTX NASI NATO NELY NEST NETV NICL NIKL
NIPS NISP NOBU NRCA NSSS NUSA OASA OBMD OCAP OKAS OMRE OPMS PADI PALM PAMG
PANI PANR PANS PBID PBRX PBSA PCAR PDES PEGE PEHA PGAS PGEO PGLI PGUN PICO
PJAA PKPK PLAN PLIN PMJS PMMP PMUI PNBN PNBS PNGO PNIN PNSE POLI POLL POLU
PORT POWR PPRE PPRO PRDA PRIM PSAB PSAT PSDN PSKT PTPP PUDP PURA PURE PWON
PYFA RAJA RALS RANC RBMS RDTX REAL RELI RICY RIGS RISE RMBA RMKE ROCK RODA
ROTI RUIS RUNS SAFE SAME SAMF SAPX SATU SBAT SBCS SBMA SCCO SCMA SCNP SDMU
SDPC SDRA SGRO SHID SHIP SICO SIDO SILO SIMA SIMP SIPD SKBM SKLT SKRN SLIS
SMAR SMBR SMCB SMDM SMDR SMGA SMGR SMIL SMKL SMKM SMMT SMRA SMSM SNLK SOCI
SOFA SOHO SOSS SOTS SPMA SPTO SQMI SRAJ SRTG SSIA SSMS SSTM STAR STTP SUNI
SUPR SURE SWAT SWID TALF TAMU TBIG TBLA TBMS TCID TCPI TDPM TELE TFAS TGKA
TGRA TIFA TINS TIRA TKIM TLKM TLDN TMAS TMPO TNCA TOBA TOPS TOTL TOTO TOWR
TPIA TPMA TRGU TRIL TRIM TRIN TRIO TRIS TRJA TRON TRUE TSCP TUGU TYRE UANG
UCID ULTJ UNIC UNIT UNTR UNVR VICI VINS VKTR VRNA WAPO WEGE WEHA WIFI WIKA
WINR WINS WIRG WMPP WMUU WTON YPAS ZATA ZBRA ZINC ZONE
""".split()
FALLBACK_CODES = list(dict.fromkeys(FALLBACK_CODES))

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


def pine_rma(values, length):
    values = np.asarray(values, dtype=float)
    out = np.full(len(values), np.nan, dtype=float)
    if length <= 0 or len(values) < length:
        return out
    valid_idx = np.flatnonzero(np.isfinite(values))
    if len(valid_idx) < length:
        return out
    seed_indices = valid_idx[:length]
    seed_end = int(seed_indices[-1])
    out[seed_end] = float(np.mean(values[seed_indices]))
    alpha = 1.0 / length
    for i in range(seed_end + 1, len(values)):
        if np.isfinite(values[i]):
            prev = out[i - 1]
            if not np.isfinite(prev):
                prior = values[max(0, i-length+1):i+1]
                if np.isfinite(prior).sum() == length:
                    out[i] = float(np.mean(prior))
            else:
                out[i] = alpha * values[i] + (1.0-alpha) * prev
    return out


def gpr_profile(timeframe):
    if timeframe in ("5m", "15m"):
        return dict(training=30, momentum_len=6, vol_len=24, ema_fast=8, ema_slow=26,
                    kernel_scale=1.8, noise_ratio=0.85, volume_fade=0.35)
    if timeframe == "1h":
        return dict(training=35, momentum_len=5, vol_len=20, ema_fast=8, ema_slow=21,
                    kernel_scale=1.6, noise_ratio=0.65, volume_fade=0.50)
    return dict(training=30, momentum_len=5, vol_len=14, ema_fast=8, ema_slow=21,
                kernel_scale=1.5, noise_ratio=0.30, volume_fade=0.65)


def gpr_project(df, horizon=10, training=30, momentum_len=5, vol_len=14,
                ema_fast=8, ema_slow=21, kernel_scale=1.5, noise_ratio=0.30,
                volume_fade=0.65, band_mode="Pita GPR", band_sigma=1.96, atr_width=0.70,
                validation_candles=3):
    
    min_needed = max(training + vol_len + ema_slow + 10, 60)
    idx = len(df) - 1 - validation_candles 
    
    if idx < min_needed:
        raise ValueError(f"Data candle hanya {len(df)}; perlu minimal {min_needed + validation_candles}.")
        
    close = df["close"].astype(float).to_numpy()
    volume = df["volume"].fillna(0).astype(float).to_numpy()
    high = df["high"].astype(float).to_numpy()
    low = df["low"].astype(float).to_numpy()

    logret = np.full(len(close), np.nan)
    logret[1:] = np.log(np.maximum(close[1:], 1e-12) / np.maximum(close[:-1], 1e-12))
    ret_series = pd.Series(logret)
    momentum = ret_series.ewm(span=momentum_len, adjust=False, min_periods=1).mean().to_numpy()
    volatility = ret_series.rolling(vol_len, min_periods=vol_len).std(ddof=0).to_numpy()
    vol_base = pd.Series(volatility).rolling(training, min_periods=training).mean().to_numpy()
    avg_volume = pd.Series(volume).rolling(vol_len, min_periods=vol_len).mean().to_numpy()
    rel_volume = np.zeros(len(close))
    valid = (volume > 0) & (avg_volume > 0) & np.isfinite(avg_volume)
    rel_volume[valid] = np.log(volume[valid] / avg_volume[valid])
    fast = ema(pd.Series(close), ema_fast).to_numpy()
    slow = ema(pd.Series(close), ema_slow).to_numpy()
    direction = (fast - slow) / np.maximum(close, 1e-12)

    prev_close = np.r_[np.nan, close[:-1]]
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    tr[0] = high[0] - low[0]
    atr = pine_rma(tr, vol_len)

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
            volatility[feature_idx] / vol_ref - 1.0,
            direction[feature_idx] / vol_ref,
        ])
        y.append(logret[target_idx])

    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n = len(y)
    
    signal_var = max(float(np.mean(y*y)), 1e-8)
    noise_var = signal_var * noise_ratio + 1e-10
    K = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1):
            value = matern32_kernel(X[i], X[j], signal_var, kernel_scale)
            if i == j:
                value += noise_var
            K[i, j] = K[j, i] = value

    K += np.eye(n) * 1e-6
    try:
        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
    except np.linalg.LinAlgError:
        try:
            K += np.eye(n) * 1e-4
            L = np.linalg.cholesky(K)
            alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
        except np.linalg.LinAlgError:
            raise ValueError("Matriks GPR tidak stabil secara numerik.")

    price_start = float(close[idx])
    price_prev = price_start
    ret_prev = float(logret[idx])
    mom_prev = float(momentum[idx])
    fast_prev, slow_prev = float(fast[idx]), float(slow[idx])
    volume_prev = float(rel_volume[idx])
    vol_prev = float(volatility[idx])
    cumulative_return = 0.0
    cumulative_variance = 0.0
    predictions = []

    total_steps = horizon + validation_candles 

    for h in range(total_steps):
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
            predictive_variance = max(float(signal_var + noise_var - solved @ solved), 1e-12)
        except (np.linalg.LinAlgError, ValueError):
            predictive_variance = 1e-12
            
        cumulative_variance += predictive_variance
        cumulative_return += pred_ret
        price_pred = price_start * math.exp(cumulative_return)
        sigma_cum = math.sqrt(max(cumulative_variance, 0.0))
        
        if band_mode == "Kanal ATR":
            distance = atr_width * float(atr[idx]) * math.sqrt(h + 1.0)
            upper = price_pred + distance
            lower = max(1e-12, price_pred - distance)
        else:
            upper = price_pred * math.exp(band_sigma * sigma_cum)
            lower = price_pred * math.exp(-band_sigma * sigma_cum)
            
        real_idx = idx + h + 1
        actual_price = float(close[real_idx]) if real_idx < len(df) else None

        predictions.append({
            "step": h + 1,
            "is_future": actual_price is None,
            "price": round(price_pred, 6),
            "actual_price": round(actual_price, 6) if actual_price is not None else None,
            "upper": round(upper, 6),
            "lower": round(lower, 6),
            "sigma_cum": sigma_cum,
        })
        price_prev = price_pred
        ret_prev = pred_ret
        a_m = 2.0 / (momentum_len + 1.0)
        mom_prev = a_m * pred_ret + (1.0-a_m) * mom_prev
        a_f = 2.0 / (ema_fast + 1.0)
        a_s = 2.0 / (ema_slow + 1.0)
        fast_prev = a_f * price_pred + (1.0-a_f) * fast_prev
        slow_prev = a_s * price_pred + (1.0-a_s) * slow_prev

    latest_actual_price = float(close[-1])
    trend = "BULLISH" if fast[-1] > slow[-1] else "BEARISH"
    mom_now = float(momentum[-1]) if np.isfinite(momentum[-1]) else 0.0
    vol_now = float(volume[-1])
    vol_avg = float(avg_volume[-1]) if np.isfinite(avg_volume[-1]) else 0.0
    rel_vol = vol_now / vol_avg if vol_avg > 0 else 0.0
    
    final = predictions[-1]
    sigma_cum_final = math.sqrt(max(cumulative_variance, 0.0))
    uncertainty = 100.0 * sigma_cum_final / (abs(cumulative_return) + sigma_cum_final + 1e-10)
    
    # Validation Logic (T-3)
    validation_errors = []
    hits = 0
    for p in predictions:
        if not p["is_future"] and p["actual_price"] is not None:
            err = abs(p["price"] - p["actual_price"]) / max(p["actual_price"], 1e-12)
            validation_errors.append(err)
            if p["lower"] <= p["actual_price"] <= p["upper"]:
                hits += 1
                
    val_count = len(validation_errors)
    validation_mape = (sum(validation_errors) / val_count) if val_count > 0 else 1.0
    validation_hit_rate = (hits / val_count) if val_count > 0 else 0.0

    return_from_now = (final["price"] / latest_actual_price - 1.0) * 100.0

    return {
        "price": round(latest_actual_price, 6),
        "projection_start_price": round(price_start, 6),
        "trend": trend,
        "momentum": "POSITIVE" if mom_now > 0 else "NEGATIVE",
        "relative_volume": round(rel_vol, 2),
        "gpr_return_pct": round(return_from_now, 3),
        "uncertainty_pct": round(uncertainty, 2),
        "cumulative_sigma": sigma_cum_final,
        "projected_price": final["price"],
        "horizon": horizon,
        "validation_mape": validation_mape,
        "validation_hit_rate": validation_hit_rate,
        "predictions": predictions,
    }

def analyze_one(market: str, code: str, timeframe: str, horizon: int) -> dict:
    hist = get_history_cached(market, code, timeframe, int(time.time() // CACHE_SECONDS))
    if hist.empty:
        raise ValueError("Data historis kosong/tidak tersedia dari Yahoo Finance.")
        
    params = gpr_profile(timeframe)
    result = gpr_project(hist, horizon=horizon, validation_candles=3, **params)
    result["code"] = code
    result["market"] = market
    
    # RUMUS SKORING BARU
    hit_score = result["validation_hit_rate"] * 30
    mape_score = max(0, 20 - (result["validation_mape"] * 100 * 4))
    trend_score = 15 if result["trend"] == "BULLISH" else 0
    mom_score = 10 if result["momentum"] == "POSITIVE" else 0
    ret_score = 25 * max(0, min(result["gpr_return_pct"] / 5.0, 1.0))
    
    score = max(0, min(100, hit_score + mape_score + trend_score + mom_score + ret_score))
    result["score"] = round(score, 1)
    
    if result["trend"] == "BULLISH" and result["gpr_return_pct"] > 0 and result["validation_hit_rate"] >= 0.66:
        result["signal"] = "KANDIDAT"
    elif result["gpr_return_pct"] > 0:
        result["signal"] = "PANTAU"
    else:
        result["signal"] = "HINDARI"
        
    return result


@st.cache_data(ttl=7 * 24 * 60 * 60, show_spinner=False)
def fetch_us_universe():
    """Mengambil saham S&P 500 dan Nasdaq 100 (~550 emiten besar), cocok untuk Gotrade"""
    # Ambil S&P 500
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        sp500_tables = pd.read_html(sp500_url)
        sp500_symbols = sp500_tables[0]['Symbol'].str.replace('.', '-', regex=False).tolist()
    except Exception:
        sp500_symbols = []
        
    # Ambil Nasdaq 100
    ndx_url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    try:
        ndx_tables = pd.read_html(ndx_url)
        ndx_symbols = []
        for df in ndx_tables:
            if 'Ticker' in df.columns:
                ndx_symbols = df['Ticker'].str.replace('.', '-', regex=False).tolist()
                break
    except Exception:
        ndx_symbols = []
        
    symbols = list(dict.fromkeys(sp500_symbols + ndx_symbols))
    
    if len(symbols) < 100:
        # Fallback manual apabila Wikipedia gagal ditarik
        return US_CODES
        
    return symbols


@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def fetch_crypto_universe():
    symbols = []
    headers = {"User-Agent": "Mozilla/5.0 GPR-Market-Scanner/1.0"}
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
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
    url = "https://www.idx.co.id/primary/ListedCompany/GetCompanyProfiles"
    params = {"start": 0, "length": 9999, "code": ""}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/",
    }
    payload = None
    errors = []
    try:
        from curl_cffi import requests as curl_requests
        response = curl_requests.get(url, params=params, headers=headers, impersonate="chrome", timeout=30)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        errors.append(f"browser-like request: {type(exc).__name__}")
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            errors.append(f"standard request: {type(exc).__name__}")
            payload = None
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        records = payload["data"]
        total = int(payload.get("recordsTotal") or payload.get("recordsFiltered") or len(records))
        found = []
        for row in records:
            if not isinstance(row, dict):
                continue
            symbol = str(row.get("KodeEmiten", row.get("kodeEmiten", ""))).strip().upper()
            if __import__("re").fullmatch(r"[A-Z0-9]{4,5}", symbol):
                found.append(symbol)
        found = list(dict.fromkeys(found))
        if total >= 800 and len(found) >= min(total, 800) and len(found) >= total * 0.90:
            return found, f"API direktori resmi IDX ({len(found)}/{total} kode; cache 6 jam)"
        errors.append(f"API hanya mengembalikan {len(found)} dari {total} data")
    fallback = list(dict.fromkeys(FALLBACK_CODES))
    reason = "; ".join(errors) if errors else "format respons IDX tidak sesuai"
    return fallback, f"FALLBACK BEI ({len(fallback)} kode) — direktori resmi gagal dimuat ({reason}); universe tidak lengkap"


def get_universe(market: str):
    if market == "IDX":
        try:
            codes, source = fetch_idx_universe()
            return codes, source
        except Exception:
            return FALLBACK_CODES.copy(), "Fallback BEI bawaan aplikasi; gagal mengambil direktori IDX"
    if market == "US":
        try:
            return fetch_us_universe(), "Indeks S&P 500 & Nasdaq 100 (~550 saham terbesar, cocok untuk Gotrade)"
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
st.caption("Satu dashboard untuk saham BEI, saham Amerika (Gotrade Ready), dan aset kripto dengan Validasi T-3")

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

state["target"] = target_count

left, mid, right = st.columns([1.2, 1.2, 2.2])
left.metric("Aset tersedia", len(codes))
mid.metric("Target scan", target_count)
right.markdown(f"**Sumber data:** Yahoo Finance  \n<span class='note'>{universe_source}</span>", unsafe_allow_html=True)

def _worker_task(code):
    time.sleep(0.05)
    try:
        row = analyze_one(market, code, timeframe, int(horizon))
        return "SUCCESS", code, row
    except Exception as exc:
        return "ERROR", code, str(exc)[:200]

if scan_next:
    if state["cursor"] >= target_count:
        st.success("Target scan sudah selesai. Tekan 'Mulai scan baru' jika ingin mengulang.")
    else:
        step_size = 100 if auto_scan else int(batch_size)
        progress = st.progress(min(state["cursor"] / max(1, target_count), 1.0), text="Menyiapkan multi-threaded scan…")
        status = st.empty()

        while state["cursor"] < target_count:
            batch_start = state["cursor"]
            stop = min(batch_start + step_size, target_count)
            batch_codes = codes[batch_start:stop]
            
            known = {x["code"] for x in state["results"]} | {x["code"] for x in state["errors"]}
            to_process = [c for c in batch_codes if c not in known]

            if to_process:
                with ThreadPoolExecutor(max_workers=8) as executor:
                    futures = {executor.submit(_worker_task, code): code for code in to_process}
                    for future in as_completed(futures):
                        status_type, code, payload = future.result()
                        if status_type == "SUCCESS":
                            state["results"].append(payload)
                        else:
                            state["errors"].append({"code": code, "error": payload})
                        
                        state["cursor"] += 1
                        current_c = min(state["cursor"], target_count)
                        progress.progress(current_c / max(1, target_count), text=f"Memproses {current_c}/{target_count}: {code}")
                        status.info(f"Progres {current_c}/{target_count} · berhasil {len(state['results'])} · gagal {len(state['errors'])}")
            else:
                state["cursor"] = stop

            state["results"].sort(key=lambda x: (x["score"], x["gpr_return_pct"]), reverse=True)
            if not auto_scan:
                break

        if state["cursor"] >= target_count:
            status.success(f"Scan selesai. Progres {state['cursor']}/{target_count} aset.")
        else:
            status.success(f"Batch selesai. Progres {state['cursor']}/{target_count} aset. Tekan lanjutkan untuk batch berikutnya.")

results = state["results"]
errors = state["errors"]
qualified = [x for x in results if float(x.get("score", 0)) >= min_score]
candidates = [x for x in qualified if x.get("signal") == "KANDIDAT"]
best_return = max((float(x["gpr_return_pct"]) for x in qualified), default=None)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Berhasil dianalisis", len(results))
m2.metric("Lolos skor", len(qualified))
m3.metric("Kandidat", len(candidates))
m4.metric("GPR Return tertinggi", f"{best_return:+.2f}%" if best_return is not None else "—")

rank_tab, detail_tab, status_tab = st.tabs(["🏆 Ranking", "📈 Detail aset", "🧾 Status & error"])
with rank_tab:
    query = st.text_input("Cari simbol", placeholder="Contoh: BBCA, AAPL, BTC-USD")
    view = [x for x in qualified if query.strip().upper() in x["code"].upper()]
    view.sort(key=lambda x: (x["score"], x["gpr_return_pct"]), reverse=True)
    if view:
        table = []
        for rank, item in enumerate(view, 1):
            score = float(item["score"])
            err_str = f"Err: {item['validation_mape']*100:.1f}%"
            hit_str = f"{int(item['validation_hit_rate']*100)}%"
            
            table.append({
                "Rank": rank, "Pasar": item["market"], "Kode": item["code"],
                "Skor": score, 
                "Akurasi (T-3)": f"{hit_str} ({err_str})",
                "GPR Return (%)": item["gpr_return_pct"],
                "Tren": item["trend"], "Momentum": item["momentum"],
                "Sinyal": item["signal"], "Harga": item["price"]
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
        a, b, c, d = st.columns(4)
        a.metric("Harga saat ini", f"{item['price']:,.4f}")
        b.metric("Tren saat ini", item["trend"])
        c.metric("Potensi Return (dari skrg)", f"{item['gpr_return_pct']:+.2f}%")
        d.metric("Ketidakpastian", f"{item.get('uncertainty_pct', float('nan')):.2f}%")
        
        preds = item.get("predictions", [])
        if preds:
            st.markdown("##### Visualisasi Validasi (T-3) & Proyeksi Masa Depan")
            chart_data = []
            
            chart_data.append({
                "Candle": "Start (T-3)", 
                "Proyeksi GPR": item["projection_start_price"],
                "Harga Asli": item["projection_start_price"],
                "Batas Atas": item["projection_start_price"],
                "Batas Bawah": item["projection_start_price"],
            })
            
            valid_count = sum(1 for p in preds if not p["is_future"])
            for p in preds:
                if p["is_future"]:
                    lbl = f"Future +{p['step'] - valid_count}"
                else:
                    jarak = valid_count - p['step']
                    lbl = f"Valid T-{jarak}" if jarak > 0 else "Hari Ini (T0)"
                    
                chart_data.append({
                    "Candle": lbl,
                    "Proyeksi GPR": p["price"],
                    "Harga Asli": p["actual_price"],
                    "Batas Atas": p["upper"],
                    "Batas Bawah": p["lower"],
                })
            
            df_chart = pd.DataFrame(chart_data).set_index("Candle")
            st.line_chart(df_chart)
            
            view_df = pd.DataFrame(preds)
            view_df = view_df.drop(columns=["is_future", "sigma_cum"], errors="ignore")
            st.dataframe(view_df, use_container_width=True, hide_index=True)
    else:
        st.info("Scan batch pertama untuk melihat detail aset.")

with status_tab:
    st.write(f"**Pasar:** {market}")
    st.write(f"**Provider:** Yahoo Finance via yfinance")
    st.write(f"**Universe:** {universe_source}")
    st.write(f"**Progres:** {state['cursor']} / {target_count}")
    st.write(f"**Berhasil:** {len(results)} · **Gagal:** {len(errors)} · **Belum diproses:** {max(0, target_count - state['cursor'])}")
    if errors:
        error_df = pd.DataFrame(errors)
        error_df["jenis_error"] = error_df["error"].apply(lambda e: "Data kosong/tidak tersedia" if "kosong" in str(e).lower() else "Data candle kurang" if "minimal" in str(e).lower() else "Rate limit/koneksi" if "429" in str(e) or "timeout" in str(e).lower() or "too many" in str(e).lower() else "Error lainnya")
        st.dataframe(error_df, use_container_width=True, hide_index=True)
    st.caption("Uncertainty adalah estimasi ketidakpastian model, bukan probabilitas keuntungan/kerugian. Hasil GPR bersifat eksperimental, bukan saran investasi.")
