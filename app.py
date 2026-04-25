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
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='public', static_url_path='')
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

@app.route("/",defaults={"path":""})
@app.route("/<path:path>")
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder,path)):
        return send_from_directory(app.static_folder,path)
    return send_from_directory(app.static_folder,"index.html")

if __name__=="__main__":
    port=int(os.environ.get("PORT",5001))
    app.run(host="0.0.0.0",port=port,debug=False)
