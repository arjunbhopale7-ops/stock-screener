"""
Arjun's Stock Screener — Hosted Backend
Runs on Render.com — always on, no Mac needed
"""
import ssl, os, warnings, time, json
warnings.filterwarnings('ignore')
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['PYTHONHTTPSVERIFY'] = '0'

import requests, urllib3
urllib3.disable_warnings()
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

TWELVE_KEY = os.environ.get("TWELVE_DATA_KEY","cc5706080270455db629d72dacf4dad6")
TD_BASE    = "https://api.twelvedata.com"

SESSION = requests.Session()
SESSION.verify = False
SESSION.headers.update({'User-Agent':'Mozilla/5.0','Accept':'application/json'})

NAME_TO_SYMBOL = {
    "PAYTM":"ONE97","ONE97":"ONE97","ZOMATO":"ZOMATO","NYKAA":"FSN","FSN":"FSN",
    "POLICYBAZAAR":"POLICYBZR","POLICYBZR":"POLICYBZR","DMART":"DMART",
    "HDFC BANK":"HDFCBANK","HDFCBANK":"HDFCBANK","HDFC":"HDFCBANK",
    "ICICI BANK":"ICICIBANK","ICICIBANK":"ICICIBANK","ICICI":"ICICIBANK",
    "SBI":"SBIN","SBIN":"SBIN","KOTAK":"KOTAKBANK","KOTAKBANK":"KOTAKBANK",
    "AXIS BANK":"AXISBANK","AXISBANK":"AXISBANK","AXIS":"AXISBANK",
    "RELIANCE":"RELIANCE","RIL":"RELIANCE","TCS":"TCS",
    "INFOSYS":"INFY","INFY":"INFY","WIPRO":"WIPRO",
    "HCL":"HCLTECH","HCLTECH":"HCLTECH","TECHM":"TECHM",
    "BAJAJ FINANCE":"BAJFINANCE","BAJFINANCE":"BAJFINANCE",
    "ASIAN PAINTS":"ASIANPAINT","ASIANPAINT":"ASIANPAINT",
    "MARUTI":"MARUTI","TATA MOTORS":"TATAMOTORS","TATAMOTORS":"TATAMOTORS",
    "TITAN":"TITAN","NESTLE":"NESTLEIND","NESTLEIND":"NESTLEIND",
    "HUL":"HINDUNILVR","HINDUNILVR":"HINDUNILVR","ITC":"ITC",
    "AIRTEL":"BHARTIARTL","BHARTIARTL":"BHARTIARTL",
    "ONGC":"ONGC","NTPC":"NTPC","POWERGRID":"POWERGRID","POWER GRID":"POWERGRID",
    "COAL INDIA":"COALINDIA","COALINDIA":"COALINDIA",
    "TATA STEEL":"TATASTEEL","TATASTEEL":"TATASTEEL",
    "JSW STEEL":"JSWSTEEL","JSWSTEEL":"JSWSTEEL","HINDALCO":"HINDALCO",
    "SUN PHARMA":"SUNPHARMA","SUNPHARMA":"SUNPHARMA",
    "DR REDDY":"DRREDDY","DRREDDY":"DRREDDY","CIPLA":"CIPLA","MANKIND":"MANKIND",
    "LAURUS":"LAURUSLABS","LAURUSLABS":"LAURUSLABS","LAURUS LABS":"LAURUSLABS",
    "DIXON":"DIXON","KAYNES":"KAYNES","POLYCAB":"POLYCAB","HAVELLS":"HAVELLS",
    "PERSISTENT":"PERSISTENT","COFORGE":"COFORGE","MPHASIS":"MPHASIS",
    "BEL":"BEL","HAL":"HAL","IREDA":"IREDA",
    "WAAREE":"WAAREEENER","WAAREEENER":"WAAREEENER",
    "ADANI":"ADANIENT","ADANIENT":"ADANIENT",
    "IRCTC":"IRCTC","IRFC":"IRFC","RVNL":"RVNL",
    "INDIGO":"INDIGO","APARINDS":"APARINDS","APAR":"APARINDS",
    "DEEPAK NITRITE":"DEEPAKNTR","DEEPAKNTR":"DEEPAKNTR",
    "ALKYLAMINE":"ALKYLAMINE","CDSL":"CDSL","BSE":"BSE","MCX":"MCX",
    "ANGELONE":"ANGELONE","ANGEL ONE":"ANGELONE",
    "AU BANK":"AUBANK","AUBANK":"AUBANK",
    "IDFC FIRST":"IDFCFIRSTB","IDFCFIRSTB":"IDFCFIRSTB",
    "BANDHAN":"BANDHANBNK","BANDHANBNK":"BANDHANBNK",
    "FEDERAL BANK":"FEDERALBNK","FEDERALBNK":"FEDERALBNK",
    "INDUSIND":"INDUSINDBK","INDUSINDBK":"INDUSINDBK",
    "YES BANK":"YESBANK","YESBANK":"YESBANK",
    "EICHER":"EICHERMOT","EICHERMOT":"EICHERMOT","ROYAL ENFIELD":"EICHERMOT",
    "HERO":"HEROMOTOCO","HEROMOTOCO":"HEROMOTOCO",
    "TVS":"TVSMOTOR","TVSMOTOR":"TVSMOTOR",
    "TATA POWER":"TATAPOWER","TATAPOWER":"TATAPOWER",
    "MUTHOOT":"MUTHOOTFIN","MUTHOOTFIN":"MUTHOOTFIN",
    "DLF":"DLF","GODREJ PROPERTIES":"GODREJPROP","GODREJPROP":"GODREJPROP",
    "LODHA":"LODHA","PRESTIGE":"PRESTIGE",
    "ABB":"ABB","SIEMENS":"SIEMENS","THERMAX":"THERMAX",
    "PI INDUSTRIES":"PIIND","PIIND":"PIIND","UPL":"UPL",
    "IGL":"IGL","GAIL":"GAIL","PETRONET":"PETRONET",
    "VEDANTA":"VEDL","VEDL":"VEDL","NMDC":"NMDC","SAIL":"SAIL","BHEL":"BHEL",
    "NAUKRI":"NAUKRI","INFOEDGE":"NAUKRI","INDIAMART":"INDIAMART",
    "JUBILANT FOOD":"JUBLFOOD","JUBLFOOD":"JUBLFOOD","DOMINOS":"JUBLFOOD",
    "VARUN BEVERAGES":"VBL","VBL":"VBL",
    "TATA CONSUMER":"TATACONSUM","TATACONSUM":"TATACONSUM",
    "DABUR":"DABUR","MARICO":"MARICO","COLGATE":"COLPAL","COLPAL":"COLPAL",
    "APOLLO HOSPITALS":"APOLLOHOSP","APOLLOHOSP":"APOLLOHOSP",
    "ULTRATECH":"ULTRACEMCO","ULTRACEMCO":"ULTRACEMCO",
    "SHREE CEMENT":"SHREECEM","SHREECEM":"SHREECEM","ACC":"ACC",
    "AMBUJA":"AMBUJACEM","AMBUJACEM":"AMBUJACEM",
    "MTAR":"MTAR","DATAPATTNS":"DATAPATTNS","DATA PATTERNS":"DATAPATTNS",
    "COCHIN SHIPYARD":"COCHINSHIP","COCHINSHIP":"COCHINSHIP",
    "MAZAGON DOCK":"MAZDOCK","MAZDOCK":"MAZDOCK",
    "GRSE":"GRSE","BEML":"BEML","MIDHANI":"MIDHANI",
    "HAPPSTMNDS":"HAPPSTMNDS","HAPPIEST MINDS":"HAPPSTMNDS",
    "ROUTE":"ROUTE","MAPMYINDIA":"MAPMYINDIA",
    "DELHIVERY":"DELHIVERY","BLUEDART":"BLUEDART","BLUE DART":"BLUEDART",
    "BATA":"BATA","TRENT":"TRENT","PAGEIND":"PAGEIND",
    "SULA":"SULA","LALPATHLAB":"LALPATHLAB","DR LAL":"LALPATHLAB",
    "METROPOLIS":"METROPOLIS","SOLARINDS":"SOLARINDS",
    "PIDILITIND":"PIDILITIND","PIDILITE":"PIDILITIND",
    "BERGEPAINT":"BERGEPAINT","BERGER PAINTS":"BERGEPAINT",
    "TORNTPHARM":"TORNTPHARM","TORRENT PHARMA":"TORNTPHARM",
    "IPCALAB":"IPCALAB","IPCA":"IPCALAB","GRANULES":"GRANULES",
    "DIVISLAB":"DIVISLAB","DIVI":"DIVISLAB","DIVIS":"DIVISLAB",
    "ABBOTINDIA":"ABBOTINDIA","ABBOTT":"ABBOTINDIA",
}

def resolve(s):
    c = s.strip().upper().replace(".NS","").replace(".BO","")
    if c in NAME_TO_SYMBOL: return NAME_TO_SYMBOL[c]
    cn = c.replace(" ","")
    for k,v in NAME_TO_SYMBOL.items():
        if cn==k.replace(" ",""): return v
    for k,v in NAME_TO_SYMBOL.items():
        if cn in k.replace(" ","") or k.replace(" ","") in cn: return v
    return c

SECTOR_PE = {
    "Technology":28,"Information Technology":28,"Financial Services":18,
    "Banking":14,"Consumer Cyclical":35,"Consumer Defensive":42,
    "Healthcare":30,"Industrials":32,"Energy":12,"Basic Materials":18,
    "Real Estate":25,"Communication Services":22,"Utilities":20,"default":25
}

PRESETS = {
    "growth10":["DIXON","KAYNES","ZOMATO","IREDA","PERSISTENT","COFORGE","MANKIND","APARINDS","POLYCAB","LAURUSLABS"],
    "nifty10":["RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","SBIN","BHARTIARTL","ITC","KOTAKBANK"],
    "pharma":["SUNPHARMA","DRREDDY","CIPLA","MANKIND","ALKEM","TORNTPHARM","ABBOTINDIA","IPCALAB","LALPATHLAB","DIVISLAB"],
    "banking":["HDFCBANK","ICICIBANK","KOTAKBANK","AXISBANK","SBIN","INDUSINDBK","FEDERALBNK","IDFCFIRSTB","BANDHANBNK","AUBANK"],
    "defence":["BEL","HAL","BEML","DATAPATTNS","MTAR","COCHINSHIP","MAZDOCK","GRSE","MIDHANI","RVNL"],
}

def _s(v,d=0):
    try: return float(v) if v else d
    except: return d

def td(ep,params):
    params["apikey"]=TWELVE_KEY
    try:
        r=SESSION.get(f"{TD_BASE}/{ep}",params=params,timeout=15)
        if r.status_code==200: return r.json()
    except: pass
    return {}

def score_stock(symbol):
    sym = resolve(symbol)
    result = {"symbol":sym,"original_input":symbol.upper(),"name":sym,
              "fetch_time":datetime.now().strftime("%d %b %Y, %H:%M IST"),
              "error":None,"sector":"Unknown","industry":"Unknown"}

    # Quote
    q = td("quote",{"symbol":f"{sym}:NSE","interval":"1day"})
    if not q or not q.get("close"):
        result["error"]=f"No data for '{symbol}'. Try the NSE symbol directly."
        return result

    price = _s(q.get("close"))
    prev  = _s(q.get("previous_close"),price)
    result.update({
        "price":round(price,2),"prev_close":round(prev,2),
        "day_change_pct":round((price-prev)/prev*100,2) if prev else 0,
        "name":q.get("name",sym),"exchange":"NSE"
    })

    # Time series for 52W range
    ts = td("time_series",{"symbol":f"{sym}:NSE","interval":"1day","outputsize":252})
    if ts.get("values"):
        closes=[_s(v["close"]) for v in ts["values"] if v.get("close")]
        vols=[_s(v.get("volume",0)) for v in ts["values"]]
        if closes:
            hi,lo=max(closes),min(closes)
            result.update({
                "52w_high":round(hi,2),"52w_low":round(lo,2),
                "52w_range_pct":round((price-lo)/(hi-lo)*100,1) if hi>lo else 50,
                "pct_from_52w_high":round((hi-price)/hi*100,1) if hi else 0,
            })
        if len(vols)>=20:
            result["volume_ratio"]=round(sum(vols[:5])/5/(sum(vols[:20])/20),2)

    # RSI
    rsi_d=td("rsi",{"symbol":f"{sym}:NSE","interval":"1day","time_period":14,"outputsize":1})
    if rsi_d.get("values"): result["rsi"]=round(_s(rsi_d["values"][0]["rsi"]),1)

    # MACD
    macd_d=td("macd",{"symbol":f"{sym}:NSE","interval":"1day","fast_period":12,"slow_period":26,"signal_period":9,"outputsize":1})
    if macd_d.get("values"):
        v=macd_d["values"][0]
        m,s=_s(v.get("macd")),_s(v.get("macd_signal"))
        result["macd_crossover"]="Bullish" if m>s else "Bearish"

    # EMA 200
    ema_d=td("ema",{"symbol":f"{sym}:NSE","interval":"1day","time_period":200,"outputsize":1})
    if ema_d.get("values"):
        ema=_s(ema_d["values"][0]["ema"])
        result.update({"200dma":round(ema,2),"above_200dma":price>ema,
                       "vs_200dma_pct":round((price-ema)/ema*100,1)})

    # Statistics (fundamentals)
    stats=td("statistics",{"symbol":f"{sym}:NSE"})
    if stats and "valuations_metrics" in stats:
        vm=stats["valuations_metrics"]
        fs=stats.get("financials",stats.get("financial_summary",{}))
        result.update({
            "pe_ratio":_s(vm.get("pe_ratio") or vm.get("trailing_pe")) or None,
            "peg_ratio":_s(vm.get("peg_ratio")) or None,
            "market_cap_cr":round(_s(vm.get("market_capitalization"))/1e7,0),
            "roe":round(_s(fs.get("return_on_equity_ttm"))*100,1),
            "revenue_growth":round(_s(fs.get("quarterly_revenue_growth_yoy"))*100,1),
            "earnings_growth":round(_s(fs.get("quarterly_earnings_growth_yoy"))*100,1),
            "op_margin":round(_s(fs.get("operating_margin_ttm"))*100,1),
            "dividend_yield":round(_s(fs.get("forward_annual_dividend_yield"))*100,2),
        })

    # Profile
    prof=td("profile",{"symbol":f"{sym}:NSE"})
    if prof and prof.get("name"):
        result.update({"name":prof.get("name",sym),"sector":prof.get("sector","Unknown"),
                       "industry":prof.get("industry_group",prof.get("industry","Unknown"))})

    # Derived fields
    de=result.get("de_ratio",0) or 0
    result["de_flag"]="✅ Healthy" if de<0.5 else "🟡 Moderate" if de<1.0 else "🟠 Elevated" if de<1.5 else "🔴 High Risk"
    dy=result.get("dividend_yield",0) or 0
    result["div_sustainability"]="Reinvestment-focused" if dy==0 else "✅ Highly Sustainable" if dy<2 else "🟡 Sustainable" if dy<5 else "🔴 Review Needed"

    sec=result.get("sector","default")
    spe=SECTOR_PE.get(sec,SECTOR_PE["default"])
    result["sector_pe"]=spe
    pe=result.get("pe_ratio")
    if pe and spe:
        prem=(pe-spe)/spe*100
        result["pe_vs_sector_pct"]=round(prem,1)
        result["pe_verdict"]="Undervalued" if prem<-15 else "Overvalued" if prem>15 else "Fairly Valued"
    else:
        result["pe_vs_sector_pct"]=None; result["pe_verdict"]="N/A"

    # Scoring
    rg=result.get("revenue_growth",0) or 0; eg=result.get("earnings_growth",0) or 0
    roe=result.get("roe",0) or 0; om=result.get("op_margin",0) or 0
    rsi=result.get("rsi") or 50; a200=result.get("above_200dma")
    macd=result.get("macd_crossover")=="Bullish"
    pfh=result.get("pct_from_52w_high",20) or 20; rng=result.get("52w_range_pct",50) or 50
    volr=result.get("volume_ratio",1.0) or 1.0; peg=result.get("peg_ratio")

    p1=min((5 if rg>25 else 3 if rg>12 else 1)+(5 if eg>30 else 3 if eg>15 else 1)+(5 if rg>20 and eg>15 else 3 if rg>10 else 1)+(5 if rg>20 else 3 if rg>10 else 1),20)
    p2=max(min((5 if roe>22 else 3 if roe>13 else 1)+(5)+(5 if de<0.5 else 3 if de<1.5 else 1)+(5 if om>20 else 3 if om>10 else 2 if om>0 else 0),20),0)
    p3=min((5 if om>40 else 3 if om>20 else 0)+(5 if sec in["Technology","Financial Services","Banking"]else 0)+(5 if sec in["Healthcare","Utilities","Energy"]else 0)+3,20)
    p4=0
    if pe and pe>0:
        if peg: p4+=(5 if peg<1.5 else 3 if peg<2.5 else 1)
        else: p4+=2
        prem2=(pe-spe)/spe*100; p4+=(5 if prem2<-15 else 3 if prem2<15 else 1)
    else: p4+=4
    p4=min(max(p4+(5 if pfh>25 else 3 if pfh>10 else 1)+(5 if 30<=rng<=65 else 3 if rng<80 else 1),0),20)
    p5=min((4 if a200 else 2 if a200 is None else 0)+(4 if 40<=rsi<=60 else 2 if rsi<=72 else 0)+(4 if macd else 2)+(4 if volr>=1.5 else 2)+(4 if 30<=rng<=65 else 2),20)
    p6=min((8 if eg>20 else 4 if eg>0 else 0)+(8 if rg>20 else 4 if rg>0 else 0)+(4 if a200 else 2),20)
    risk=min(2+(2 if pe and pe>spe*3 else 0)+(1 if de>1.5 else 0)+(2 if eg<0 else 0)+(1 if a200 is False else 0)+(1 if pfh<5 else 0),10)
    p7=max(20-risk*2,0)
    p8=min(10+(6 if sec in["Technology","Healthcare"]else 8 if sec in["Industrials","Energy"]else 5 if sec in["Banking","Financial Services"]else 4),20)

    total=round(p1+p2+p3+p4+p5+p6+p7+p8,1)
    result.update({"p1_growth":p1,"p2_quality":p2,"p3_moat":p3,"p4_valuation":p4,
                   "p5_technical":p5,"p6_sentiment":p6,"p7_risk":p7,"p8_macro":p8,
                   "total_score":total,"total_pct":round(total/160*100,1),
                   "risk_score":risk,"risk_label":"Low" if risk<=3 else "Moderate" if risk<=5 else "High" if risk<=7 else "Very High"})

    if total>=128: result["verdict"],result["verdict_emoji"]="Strong Buy","🟢"
    elif total>=104: result["verdict"],result["verdict_emoji"]="Buy","🔵"
    elif total>=80: result["verdict"],result["verdict_emoji"]="Watch","🟡"
    else: result["verdict"],result["verdict_emoji"]="Avoid","🔴"

    if price>0:
        result.update({"entry_low":round(price*.97,1),"entry_high":round(price*1.01,1),
                       "stop_loss":round(price*.91,1),"bull_target":round(price*1.5,1),
                       "bear_target":round(price*.82,1),"bull_return_pct":round(50,1),"rrr":round(50/9,1)})
    return result

@app.route("/api/screen",methods=["POST"])
def screen():
    body=request.json or {}
    symbols=body.get("symbols",[])
    preset=body.get("preset")
    if preset and preset in PRESETS: symbols=PRESETS[preset]
    if not symbols: return jsonify({"error":"No symbols"}),400
    symbols=[resolve(s) for s in symbols[:15]]
    results=[]
    for sym in symbols:
        try:
            results.append(score_stock(sym)); time.sleep(0.5)
        except Exception as e:
            results.append({"symbol":sym,"error":str(e),"verdict":"Error","verdict_emoji":"⚠️","total_score":0})
    results.sort(key=lambda x:x.get("total_score",0),reverse=True)
    return jsonify({"results":results})

@app.route("/api/presets")
def presets(): return jsonify({"presets":list(PRESETS.keys())})

@app.route("/api/health")
def health(): return jsonify({"status":"ok","time":datetime.now().isoformat()})

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arjun's Stock Screener</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swapfamily=DM+Sans:wght@300;400;500;600https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swapfamily=DM+Mono:wght@400;500https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swapdisplay=swap" rel="stylesheet">
<style>
:root{
  --bg:#faf6ef;--bg2:#f4ede1;--bg3:#ede3d4;--bg4:#e4d7c4;
  --border:#d4c5ae;--border2:#bfad96;
  --text:#2a1f12;--text2:#7a6348;--text3:#a8906f;
  --cyan:#8b6840;--cyan2:#6b4e2c;
  --green:#4a7c59;--red:#a84444;--yellow:#b87820;--orange:#a8601a;
  --purple:#6b5a8a;
  --mono:'DM Mono',monospace;
  --sans:'DM Sans',sans-serif;
  --display:'Cormorant Garamond',serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:14px;display:flex;flex-direction:column}

/* Subtle paper texture */
body::after{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");pointer-events:none;z-index:9999;opacity:.5}

/* ── TOPBAR ── */
.topbar{display:flex;align-items:center;gap:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--border);flex-shrink:0;padding:0 20px;gap:16px}
.app-logo{font-family:var(--display);font-size:28px;color:var(--cyan);letter-spacing:1px;font-weight:600;font-style:italic}
.app-tagline{font-size:11px;color:var(--text3);font-family:var(--mono);letter-spacing:.5px}
.spacer{flex:1}
.top-clock{font-family:var(--mono);font-size:13px;color:var(--cyan);opacity:.7}
.conn-indicator{display:flex;align-items:center;gap:6px;font-family:var(--mono);font-size:11px;color:var(--text3)}
.conn-dot{width:7px;height:7px;border-radius:50%;background:var(--text3);transition:all .3s}
.conn-dot.live{background:var(--green);box-shadow:0 0 6px rgba(74,124,89,.5);animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}

/* ── MAIN LAYOUT ── */
.layout{display:flex;flex:1;overflow:hidden}

/* ── SIDEBAR ── */
.sidebar{width:260px;flex-shrink:0;background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto}
.sidebar-section{padding:16px}
.sidebar-label{font-family:var(--mono);font-size:9px;text-transform:uppercase;letter-spacing:2px;color:var(--text3);margin-bottom:10px}

.search-wrap{position:relative;margin-bottom:8px}
.search-input{width:100%;background:var(--bg3);border:1px solid var(--border2);border-radius:8px;padding:10px 14px;color:var(--text);font-family:var(--mono);font-size:12px;outline:none;transition:all .2s}
.search-input:focus{border-color:var(--cyan);box-shadow:0 0 0 2px rgba(139,104,64,.15)}
.search-input::placeholder{color:var(--text3)}

.screen-btn{width:100%;background:linear-gradient(135deg,var(--cyan),var(--cyan2));color:#faf6ef;border:none;border-radius:8px;padding:11px;font-family:var(--display);font-size:16px;letter-spacing:1px;cursor:pointer;transition:all .2s;margin-bottom:16px;font-weight:600}
.screen-btn:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(139,104,64,.25)}
.screen-btn:active{transform:translateY(0)}
.screen-btn:disabled{opacity:.4;cursor:not-allowed;transform:none}

.divider{border:none;border-top:1px solid var(--border);margin:12px 0}

.preset-btn{width:100%;background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:9px 12px;color:var(--text2);font-family:var(--sans);font-size:12px;cursor:pointer;text-align:left;transition:all .2s;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center}
.preset-btn:hover,.preset-btn.active{border-color:var(--cyan);color:var(--cyan);background:rgba(139,104,64,.08)}
.preset-count{font-family:var(--mono);font-size:10px;color:var(--text3)}

/* Recent searches */
.recent-list{display:flex;flex-direction:column;gap:4px}
.recent-item{background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-family:var(--mono);font-size:11px;color:var(--text2);cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:all .15s}
.recent-item:hover{border-color:var(--border2);color:var(--text)}
.recent-verdict{font-size:10px}

/* ── MAIN PANEL ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden}

/* ── STATES ── */
.state-idle,.state-loading,.state-results,.state-error{
  flex:1;display:none;flex-direction:column;overflow:hidden
}
.state-idle.show,.state-loading.show,.state-results.show,.state-error.show{display:flex}

/* Idle */
.state-idle{align-items:center;justify-content:center}
.idle-hero{text-align:center}
.idle-title{font-family:var(--display);font-size:80px;color:var(--cyan);letter-spacing:2px;line-height:1;font-weight:500;font-style:italic;margin-bottom:12px}
.idle-sub{font-size:15px;color:var(--text2);max-width:400px;margin:0 auto 32px;line-height:1.6}
.idle-hint{font-family:var(--mono);font-size:11px;color:var(--text3)}
.idle-keys{display:flex;gap:8px;justify-content:center;margin-top:12px;flex-wrap:wrap}
.key{background:var(--bg3);border:1px solid var(--border2);border-radius:5px;padding:4px 10px;font-family:var(--mono);font-size:11px;color:var(--text2)}

/* Loading */
.state-loading{align-items:center;justify-content:center;gap:24px}
.loading-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:300px}
.loading-cell{height:4px;background:var(--border2);border-radius:2px;overflow:hidden}
.loading-cell .fill{height:100%;background:var(--cyan);width:0%;border-radius:2px;transition:width .3s}
.loading-text{font-family:var(--mono);font-size:13px;color:var(--cyan);text-align:center}
.loading-sub{font-size:12px;color:var(--text3);text-align:center;font-family:var(--mono)}

/* Error */
.state-error{align-items:center;justify-content:center}
.error-box{background:rgba(255,59,92,.06);border:1px solid rgba(255,59,92,.25);border-radius:14px;padding:32px;max-width:500px;text-align:center}
.error-title{font-family:var(--display);font-size:28px;color:var(--red);letter-spacing:1px;margin-bottom:8px}
.error-msg{font-size:13px;color:var(--text2);line-height:1.7}

/* Results */
.state-results{overflow-y:auto}
.results-inner{padding:20px}

/* Summary bar */
.summary-bar{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;align-items:center}
.summary-title{font-family:var(--display);font-size:22px;color:#fff;letter-spacing:1px}
.summary-chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{padding:4px 12px;border-radius:20px;font-family:var(--mono);font-size:11px}
.chip-sb{background:rgba(5,245,158,.1);color:var(--green);border:1px solid rgba(5,245,158,.25)}
.chip-b{background:rgba(0,240,255,.08);color:var(--cyan);border:1px solid rgba(0,240,255,.25)}
.chip-w{background:rgba(255,193,7,.08);color:var(--yellow);border:1px solid rgba(255,193,7,.25)}
.chip-a{background:rgba(255,59,92,.08);color:var(--red);border:1px solid rgba(255,59,92,.25)}
.refresh-btn{margin-left:auto;background:var(--bg3);border:1px solid var(--border2);border-radius:8px;padding:7px 14px;color:var(--text2);font-family:var(--mono);font-size:11px;cursor:pointer;transition:all .2s}
.refresh-btn:hover{border-color:var(--cyan);color:var(--cyan)}

/* Summary table */
.table-wrap{background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:24px;overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:800px}
thead tr{background:var(--bg3)}
th{padding:10px 14px;text-align:left;font-family:var(--mono);font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);border-bottom:1px solid var(--border);white-space:nowrap}
td{padding:12px 14px;border-bottom:1px solid var(--border);vertical-align:middle}
tbody tr:last-child td{border-bottom:none}
tbody tr{transition:background .12s;cursor:pointer}
tbody tr:hover{background:rgba(0,240,255,.025)}

.ticker-cell .sym{font-family:var(--mono);font-size:14px;font-weight:600;color:var(--cyan)}
.ticker-cell .co{font-size:11px;color:var(--text3);margin-top:1px}
.score-pill{background:var(--bg4);border:1px solid var(--border2);color:var(--cyan);font-family:var(--mono);font-size:12px;font-weight:600;padding:3px 9px;border-radius:6px;letter-spacing:.3px}
.verdict-pill{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;font-family:var(--mono);white-space:nowrap}
.vp-sb{background:rgba(5,245,158,.1);color:var(--green);border:1px solid rgba(5,245,158,.25)}
.vp-b{background:rgba(0,240,255,.08);color:var(--cyan);border:1px solid rgba(0,240,255,.25)}
.vp-w{background:rgba(255,193,7,.08);color:var(--yellow);border:1px solid rgba(255,193,7,.25)}
.vp-a{background:rgba(255,59,92,.08);color:var(--red);border:1px solid rgba(255,59,92,.25)}
.risk-pill{font-family:var(--mono);font-size:11px;font-weight:700;padding:2px 8px;border-radius:5px}
.rp-low{background:rgba(5,245,158,.1);color:var(--green)}
.rp-med{background:rgba(255,193,7,.1);color:var(--yellow)}
.rp-high{background:rgba(255,123,0,.1);color:var(--orange)}
.rp-vhigh{background:rgba(255,59,92,.1);color:var(--red)}
.muted{color:var(--text3);font-size:11px}
.pos{color:var(--green)}.neg{color:var(--red)}.neu{color:var(--yellow)}

/* Detail cards */
.cards-label{font-family:var(--mono);font-size:9px;text-transform:uppercase;letter-spacing:2px;color:var(--cyan);margin-bottom:14px;display:flex;align-items:center;gap:8px}
.cards-label::before{content:'';display:inline-block;width:3px;height:12px;background:var(--cyan);border-radius:2px}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:16px}

.card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;overflow:hidden;animation:fadeUp .3s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.card:hover{border-color:var(--border2)}

.card-head{padding:16px 20px 14px;background:var(--bg3);border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:flex-start}
.card-sym{font-family:var(--display);font-size:22px;color:#fff;letter-spacing:1px}
.card-co{font-size:11px;color:var(--text3);margin-top:2px}
.card-price{font-family:var(--mono);font-size:20px;font-weight:600;color:var(--cyan);text-align:right}
.card-chg{font-size:11px;margin-top:2px;text-align:right}

.card-body{padding:16px 20px}

/* Pillar bars */
.pillar-row{display:flex;align-items:center;gap:8px;margin-bottom:7px}
.p-name{font-size:10px;color:var(--text2);width:140px;flex-shrink:0;font-family:var(--mono)}
.p-track{flex:1;height:5px;background:var(--bg4);border-radius:3px}
.p-fill{height:5px;border-radius:3px}
.p-pts{font-family:var(--mono);font-size:10px;color:var(--text3);width:28px;text-align:right}
.score-total{display:flex;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid var(--border)}
.score-total-val{font-family:var(--mono);font-size:18px;font-weight:600;color:var(--cyan)}

/* Metric boxes */
.metrics-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:14px 0}
.m-box{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:9px 11px}
.m-label{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:var(--text3);font-family:var(--mono)}
.m-val{font-family:var(--mono);font-size:13px;font-weight:600;margin-top:3px}
.m-sub{font-size:9px;color:var(--text3);margin-top:1px}

/* Trade boxes */
.trade-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:14px 0}
.t-box{border-radius:9px;padding:10px 12px;border:1px solid}
.t-entry{background:rgba(0,240,255,.04);border-color:rgba(0,240,255,.2)}
.t-stop{background:rgba(255,59,92,.04);border-color:rgba(255,59,92,.2)}
.t-bull{background:rgba(5,245,158,.04);border-color:rgba(5,245,158,.2)}
.t-bear{background:rgba(255,123,0,.04);border-color:rgba(255,123,0,.2)}
.t-rrr{background:rgba(157,111,255,.04);border-color:rgba(157,111,255,.2)}
.t-risk{background:rgba(255,193,7,.04);border-color:rgba(255,193,7,.2)}
.t-label{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:var(--text3);font-family:var(--mono)}
.t-val{font-family:var(--mono);font-size:14px;font-weight:700;margin-top:3px}
.t-sub{font-size:10px;color:var(--text2);margin-top:2px}

.sub-label{font-family:var(--mono);font-size:9px;text-transform:uppercase;letter-spacing:2px;color:var(--text3);margin:12px 0 6px}
.note-box{background:rgba(255,193,7,.05);border:1px solid rgba(255,193,7,.15);border-radius:8px;padding:9px 12px;font-size:11px;color:var(--yellow);margin-bottom:12px;font-family:var(--mono)}
.disclaimer{font-size:11px;color:var(--text3);line-height:1.7;padding:16px 20px;border-top:1px solid var(--border);font-family:var(--mono)}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="app-logo">₹ SCREENER</div>
  <div class="app-tagline">8-Pillar Framework · NSE/BSE · Extended Swing</div>
  <div class="spacer"></div>
  <div class="conn-indicator">
    <div class="conn-dot" id="connDot"></div>
    <span id="connText">connecting...</span>
  </div>
  <div class="top-clock" id="clock" style="margin-left:16px"></div>
</div>

<!-- LAYOUT -->
<div class="layout">

  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="sidebar-section">
      <div class="sidebar-label">Screen Stocks</div>
      <div class="search-wrap">
        <input class="search-input" id="searchInput" type="text"
          placeholder="RELIANCE TCS ZOMATO DIXON..."
          onkeydown="if(event.key==='Enter')runScreen()">
      </div>
      <button class="screen-btn" id="screenBtn" onclick="runScreen()">▶ SCREEN NOW</button>

      <div class="sidebar-label">Quick Presets</div>
      <button class="preset-btn" onclick="loadPreset('growth10',this)">
        Growth 10 <span class="preset-count">High-growth</span>
      </button>
      <button class="preset-btn" onclick="loadPreset('nifty10',this)">
        Nifty Top 10 <span class="preset-count">Large-cap</span>
      </button>
      <button class="preset-btn" onclick="loadPreset('pharma',this)">
        Pharma <span class="preset-count">Healthcare</span>
      </button>
      <button class="preset-btn" onclick="loadPreset('banking',this)">
        Banking <span class="preset-count">Finance</span>
      </button>
      <button class="preset-btn" onclick="loadPreset('defence',this)">
        Defence <span class="preset-count">PSU/Govt</span>
      </button>
    </div>

    <hr class="divider" style="margin:0 16px">

    <div class="sidebar-section" id="recentSection" style="display:none">
      <div class="sidebar-label">Recent Searches</div>
      <div class="recent-list" id="recentList"></div>
    </div>

    <div style="flex:1"></div>
    <div class="disclaimer">
      ⚠️ Not financial advice.<br>
      Verify on screener.in & TradingView.<br>
      SEBI disclaimer applies.
    </div>
  </div>

  <!-- MAIN PANEL -->
  <div class="main">

    <!-- IDLE STATE -->
    <div class="state-idle show" id="stateIdle">
      <div class="idle-hero">
        <div class="idle-title">READY</div>
        <div class="idle-sub">Type stock symbols on the left and press Screen Now — or pick a preset watchlist</div>
        <div class="idle-hint">Examples you can try right now:</div>
        <div class="idle-keys">
          <span class="key">RELIANCE</span>
          <span class="key">TCS</span>
          <span class="key">ZOMATO</span>
          <span class="key">DIXON</span>
          <span class="key">HDFCBANK</span>
          <span class="key">BEL</span>
        </div>
      </div>
    </div>

    <!-- LOADING STATE -->
    <div class="state-loading" id="stateLoading">
      <div class="loading-grid" id="loadingGrid">
        <div class="loading-cell"><div class="fill" id="lf1"></div></div>
        <div class="loading-cell"><div class="fill" id="lf2"></div></div>
        <div class="loading-cell"><div class="fill" id="lf3"></div></div>
        <div class="loading-cell"><div class="fill" id="lf4"></div></div>
      </div>
      <div class="loading-text" id="loadingText">Fetching live market data...</div>
      <div class="loading-sub" id="loadingSub">Connecting to NSE/BSE · Calculating RSI, MACD, 200 DMA</div>
    </div>

    <!-- ERROR STATE -->
    <div class="state-error" id="stateError">
      <div class="error-box">
        <div class="error-title">CONNECTION ERROR</div>
        <div class="error-msg" id="errorMsg">
          Cannot reach the backend server.<br><br>
          Make sure you launched the app using <strong>StockScreener.command</strong><br>
          and not by opening this HTML file directly.
        </div>
      </div>
    </div>

    <!-- RESULTS STATE -->
    <div class="state-results" id="stateResults">
      <div class="results-inner">

        <div class="summary-bar">
          <div class="summary-title" id="summaryTitle">Results</div>
          <div class="summary-chips" id="summaryChips"></div>
          <button class="refresh-btn" onclick="runScreen()">↻ Refresh</button>
        </div>

        <!-- Summary table -->
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th><th>Stock</th><th>Score /160</th><th>Verdict</th>
                <th>P/E vs Sector</th><th>D/E</th><th>Div Yield</th><th>Moat</th><th>Risk</th>
              </tr>
            </thead>
            <tbody id="summaryBody"></tbody>
          </table>
        </div>

        <div class="cards-label">Detailed Analysis — Click any row above to jump</div>
        <div class="cards-grid" id="cardsGrid"></div>

      </div>
    </div>

  </div>
</div>

<script>
const API = '';
let lastSymbols = [];
let recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');

// Clock
setInterval(()=>{
  const n=new Date();
  document.getElementById('clock').textContent=
    n.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit',second:'2-digit'})+' IST';
},1000);

// Connection check
async function checkConn(){
  try{
    const r=await fetch(`${API}/api/health`,{signal:AbortSignal.timeout(3000)});
    if(r.ok){
      document.getElementById('connDot').className='conn-dot live';
      document.getElementById('connText').textContent='LIVE';
      document.getElementById('connText').style.color='var(--green)';
    }else throw new Error();
  }catch{
    document.getElementById('connDot').className='conn-dot';
    document.getElementById('connText').textContent='offline';
    document.getElementById('connText').style.color='var(--red)';
  }
}
checkConn(); setInterval(checkConn,30000);

function showState(name){
  ['Idle','Loading','Error','Results'].forEach(s=>{
    document.getElementById(`state${s}`).classList.toggle('show',s===name);
  });
}

function loadPreset(preset,btn){
  document.querySelectorAll('.preset-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('searchInput').value='';
  runScreenWithPayload({preset});
}

function runScreen(){
  const val=document.getElementById('searchInput').value.trim();
  if(!val){showState('Idle');return;}
  const symbols=val.split(/[\\s,]+/).filter(Boolean).map(s=>s.toUpperCase());
  runScreenWithPayload({symbols});
}

async function runScreenWithPayload(payload){
  const btn=document.getElementById('screenBtn');
  btn.disabled=true; btn.textContent='⏳ SCREENING...';
  showState('Loading');

  const msgs=['Fetching live prices from NSE/BSE...','Calculating RSI, MACD, 200 DMA...','Running 8-pillar scoring...','Computing entry zones & targets...','Almost done — finalising verdicts...'];
  let mi=0;
  const interval=setInterval(()=>{
    document.getElementById('loadingText').textContent=msgs[mi%msgs.length];
    mi++;
    ['lf1','lf2','lf3','lf4'].forEach((id,i)=>{
      setTimeout(()=>{document.getElementById(id).style.width=Math.random()*100+'%';},i*150);
    });
  },2500);

  try{
    const r=await fetch(`${API}/api/screen`,{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload)
    });
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const data=await r.json();
    clearInterval(interval);
    renderResults(data.results, payload);
    saveRecent(payload, data.results);
  }catch(e){
    clearInterval(interval);
    document.getElementById('errorMsg').innerHTML=
      `Cannot connect to the backend.<br><br>`+
      `<strong>Fix:</strong> Close this window and double-click<br>`+
      `<code style="background:rgba(255,255,255,.05);padding:2px 6px;border-radius:4px">StockScreener.command</code><br><br>`+
      `Then this app will reopen automatically with full data.`;
    showState('Error');
  }

  btn.disabled=false; btn.textContent='▶ SCREEN NOW';
}

function fmt(v,d=1,pre='',suf='',na='N/A'){
  if(v===null||v===undefined) return na;
  return `${pre}${Number(v).toFixed(d)}${suf}`;
}
function vc(v){
  const s=(v||'').split(' ')[0];
  return s==='Strong'?'vp-sb':s==='Buy'?'vp-b':s==='Watch'?'vp-w':'vp-a';
}
function rc(r){return r<=3?'rp-low':r<=5?'rp-med':r<=7?'rp-high':'rp-vhigh';}
function pillarColor(i){return['#00f0ff','#05f59e','#9d6fff','#ffc107','#00bcd4','#ff9100','#ef5350','#4db6ac'][i%8];}

function renderResults(results, payload){
  // Summary chips
  const verdicts={};
  results.forEach(r=>{if(!r.error) verdicts[r.verdict]=(verdicts[r.verdict]||0)+1;});
  let chips='';
  if(verdicts['Strong Buy']) chips+=`<span class="chip chip-sb">🟢 ${verdicts['Strong Buy']} Strong Buy</span>`;
  if(verdicts['Buy'])        chips+=`<span class="chip chip-b">🔵 ${verdicts['Buy']} Buy</span>`;
  if(verdicts['Watch'])      chips+=`<span class="chip chip-w">🟡 ${verdicts['Watch']} Watch</span>`;
  if(verdicts['Avoid'])      chips+=`<span class="chip chip-a">🔴 ${verdicts['Avoid']} Avoid</span>`;
  document.getElementById('summaryChips').innerHTML=chips;

  const n=results.filter(r=>!r.error).length;
  document.getElementById('summaryTitle').textContent=`${n} Stocks Screened`;

  // Summary table
  const tbody=document.getElementById('summaryBody');
  tbody.innerHTML='';
  results.forEach((s,i)=>{
    if(s.error){
      tbody.innerHTML+=`<tr><td>${i+1}</td><td class="ticker-cell"><div class="sym">${s.symbol}</div></td><td colspan="7" style="color:var(--red);font-family:var(--mono);font-size:11px">⚠️ ${s.error}</td></tr>`;
      return;
    }
    const pe=fmt(s.pe_ratio);
    const secpe=fmt(s.sector_pe,0);
    const peV=s.pe_verdict||'N/A';
    const pec=peV==='Undervalued'?'pos':peV==='Overvalued'?'neg':'neu';
    tbody.innerHTML+=`
    <tr onclick="document.getElementById('card-${s.symbol}').scrollIntoView({behavior:'smooth',block:'start'})">
      <td style="font-family:var(--mono);color:var(--text3)">#${i+1}</td>
      <td class="ticker-cell"><div class="sym">${s.symbol}</div><div class="co">${(s.name||s.symbol).substring(0,22)}</div></td>
      <td><span class="score-pill">${s.total_score}/160</span></td>
      <td><span class="verdict-pill ${vc(s.verdict)}">${s.verdict_emoji} ${s.verdict}</span></td>
      <td>${pe} <span class="muted">vs ${secpe}</span><br><span class="${pec}" style="font-size:10px">${peV}</span></td>
      <td style="font-size:12px">${s.de_flag||'N/A'}</td>
      <td style="font-family:var(--mono)">${fmt(s.dividend_yield,2,'','%')}</td>
      <td style="font-size:11px">${getMoat(s)}</td>
      <td><span class="risk-pill ${rc(s.risk_score||5)}">${s.risk_score||'?'}/10</span></td>
    </tr>`;
  });

  // Detail cards
  const grid=document.getElementById('cardsGrid');
  grid.innerHTML='';
  results.forEach((s,ci)=>{
    if(s.error){
      grid.innerHTML+=`<div class="card" id="card-${s.symbol}" style="animation-delay:${ci*.05}s"><div class="card-head"><div><div class="card-sym">${s.symbol}</div></div></div><div class="card-body" style="color:var(--red);font-family:var(--mono);font-size:12px">⚠️ ${s.error}</div></div>`;
      return;
    }
    const price=s.price||0;
    const chg=s.day_change_pct||0;
    const chgCls=chg>=0?'pos':'neg';
    const pillars=[
      {n:'Growth Engine',s:s.p1_growth},{n:'Financial Quality',s:s.p2_quality},
      {n:'Competitive Moat',s:s.p3_moat},{n:'Valuation & P/E',s:s.p4_valuation},
      {n:'Technical Setup',s:s.p5_technical},{n:'Inst. Sentiment',s:s.p6_sentiment},
      {n:'Risk Assessment',s:s.p7_risk},{n:'Macro Tailwind',s:s.p8_macro},
    ];
    const note=s._note?`<div class="note-box">⏳ ${s._note}</div>`:'';
    const bullCls=(s.bull_return_pct||0)>0?'pos':'neg';
    const rrrCls=(s.rrr||0)>=3?'pos':(s.rrr||0)>=2?'neu':'neg';

    grid.innerHTML+=`
    <div class="card" id="card-${s.symbol}" style="animation-delay:${ci*.05}s">
      <div class="card-head">
        <div>
          <div class="card-sym">${s.symbol} <span class="verdict-pill ${vc(s.verdict)}" style="font-size:11px;margin-left:8px;vertical-align:middle">${s.verdict_emoji} ${s.verdict}</span></div>
          <div class="card-co">${s.name||s.symbol} · ${s.sector||'Unknown'} · NSE</div>
        </div>
        <div>
          <div class="card-price">₹${price.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2})}</div>
          <div class="card-chg"><span class="${chgCls}">${chg>=0?'+':''}${chg}%</span> <span class="muted">₹${(s.market_cap_cr||0).toLocaleString('en-IN')} Cr</span></div>
        </div>
      </div>
      <div class="card-body">
        ${note}
        <div class="sub-label">8-Pillar Scores</div>
        ${pillars.map((p,i)=>`<div class="pillar-row"><span class="p-name">P${i+1} ${p.n}</span><div class="p-track"><div class="p-fill" style="width:${(p.s/20)*100}%;background:${pillarColor(i)}"></div></div><span class="p-pts">${Math.round(p.s||0)}/20</span></div>`).join('')}
        <div class="score-total"><span style="font-size:12px;color:var(--text2)">Composite Score</span><span class="score-total-val">${s.total_score}/160 (${s.total_pct}%)</span></div>

        <div class="metrics-grid">
          <div class="m-box"><div class="m-label">P/E Ratio</div><div class="m-val" style="color:var(--cyan)">${fmt(s.pe_ratio)}</div><div class="m-sub">Sector: ${fmt(s.sector_pe,0)}</div></div>
          <div class="m-box"><div class="m-label">P/E Verdict</div><div class="m-val" style="color:${s.pe_verdict==='Undervalued'?'var(--green)':s.pe_verdict==='Overvalued'?'var(--red)':'var(--yellow)'};font-size:11px">${s.pe_verdict||'N/A'}</div><div class="m-sub">${fmt(s.pe_vs_sector_pct,1,'','%','—')} vs sector</div></div>
          <div class="m-box"><div class="m-label">ROE</div><div class="m-val" style="color:${(s.roe||0)>22?'var(--green)':(s.roe||0)>13?'var(--yellow)':'var(--red)'}">${fmt(s.roe,1,'','%')}</div></div>
          <div class="m-box"><div class="m-label">D/E Health</div><div class="m-val" style="font-size:11px">${s.de_flag||'N/A'}</div><div class="m-sub">${fmt(s.de_ratio,2)}</div></div>
          <div class="m-box"><div class="m-label">RSI (14d)</div><div class="m-val" style="color:${40<=(s.rsi||0)&&(s.rsi||0)<=60?'var(--green)':(s.rsi||0)>72?'var(--red)':'var(--yellow)'}">${fmt(s.rsi,1,'','','—')}</div></div>
          <div class="m-box"><div class="m-label">MACD</div><div class="m-val" style="color:${s.macd_crossover==='Bullish'?'var(--green)':'var(--red)'};font-size:12px">${s.macd_crossover||'N/A'}</div></div>
          <div class="m-box"><div class="m-label">200 DMA</div><div class="m-val" style="color:${s.above_200dma?'var(--green)':s.above_200dma===false?'var(--red)':'var(--text2)'};font-size:12px">${s.above_200dma===true?'Above ✅':s.above_200dma===false?'Below ⚠️':'N/A'}</div><div class="m-sub">${s.vs_200dma_pct!=null?fmt(s.vs_200dma_pct,1,'','%'):'—'}</div></div>
          <div class="m-box"><div class="m-label">52W Range</div><div class="m-val" style="color:var(--yellow)">${fmt(s['52w_range_pct'],0,'','%')}</div><div class="m-sub">${fmt(s.pct_from_52w_high,1,'','%')} from high</div></div>
        </div>

        <div class="sub-label">Trade Setup</div>
        <div class="trade-grid">
          <div class="t-box t-entry"><div class="t-label">Entry Zone</div><div class="t-val" style="color:var(--cyan)">₹${(s.entry_low||0).toLocaleString('en-IN',{maximumFractionDigits:1})}</div><div class="t-sub">to ₹${(s.entry_high||0).toLocaleString('en-IN',{maximumFractionDigits:1})}</div></div>
          <div class="t-box t-stop"><div class="t-label">Stop Loss</div><div class="t-val" style="color:var(--red)">₹${(s.stop_loss||0).toLocaleString('en-IN',{maximumFractionDigits:1})}</div><div class="t-sub">~9% below entry</div></div>
          <div class="t-box t-rrr"><div class="t-label">Risk/Reward</div><div class="t-val" style="color:var(--purple)">${s.rrr||0}x</div><div class="t-sub ${rrrCls}">${(s.rrr||0)>=3?'✅ Excellent':(s.rrr||0)>=2?'✓ Acceptable':'⚠️ Weak'}</div></div>
          <div class="t-box t-bull"><div class="t-label">Bull Target 12M</div><div class="t-val" style="color:var(--green)">₹${(s.bull_target||0).toLocaleString('en-IN',{maximumFractionDigits:1})}</div><div class="t-sub ${bullCls}">+${s.bull_return_pct||0}% upside</div></div>
          <div class="t-box t-bear"><div class="t-label">Bear Target</div><div class="t-val" style="color:var(--orange)">₹${(s.bear_target||0).toLocaleString('en-IN',{maximumFractionDigits:1})}</div></div>
          <div class="t-box t-risk"><div class="t-label">Risk Rating</div><div class="t-val" style="color:var(--yellow)">${s.risk_score||0}/10</div><div class="t-sub">${s.risk_label||'—'}</div></div>
        </div>
      </div>
    </div>`;
  });

  showState('Results');
}

function getMoat(s){
  const p3=s.p3_moat||0;
  if(p3>=16) return '🏰 Strong';
  if(p3>=10) return '🛡️ Moderate';
  return '🪨 Weak';
}

function saveRecent(payload, results){
  const top=results.filter(r=>!r.error)[0];
  if(!top) return;
  const entry={
    label: payload.preset ? payload.preset.toUpperCase() : (payload.symbols||[]).join(' '),
    verdict: top.verdict_emoji+' '+top.verdict,
    payload,
    time: new Date().toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'})
  };
  recentSearches.unshift(entry);
  recentSearches = recentSearches.slice(0,8);
  localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
  renderRecent();
}

function renderRecent(){
  if(!recentSearches.length) return;
  document.getElementById('recentSection').style.display='block';
  const list=document.getElementById('recentList');
  list.innerHTML=recentSearches.map((r,i)=>`
    <div class="recent-item" onclick="runScreenWithPayload(${JSON.stringify(r.payload).replace(/"/g,'&quot;')})">
      <div>
        <div style="font-size:12px;color:var(--text)">${r.label.substring(0,22)}</div>
        <div style="font-size:10px;color:var(--text3)">${r.time}</div>
      </div>
      <div class="recent-verdict">${r.verdict}</div>
    </div>`).join('');
}
renderRecent();
</script>
</body>
</html>
"""

@app.route("/",defaults={"path":""})
@app.route("/<path:path>")
def serve(path):
    if path.startswith("api"):
        return jsonify({"error":"not found"}), 404
    from flask import Response
    return Response(HTML_PAGE, mimetype="text/html")

if __name__=="__main__":
    port=int(os.environ.get("PORT",5001))
    app.run(host="0.0.0.0",port=port,debug=False)

# ── KEEP ALIVE — prevents Render free tier from sleeping ─────────────────────
import threading

def keep_alive():
    """Ping self every 14 minutes to prevent sleep"""
    import time
    time.sleep(60)  # wait for app to fully start
    while True:
        try:
            url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5001")
            SESSION.get(f"{url}/api/health", timeout=10)
        except:
            pass
        time.sleep(840)  # 14 minutes

threading.Thread(target=keep_alive, daemon=True).start()

# This line is already there — checking the serve route exists
