#!/usr/bin/env python3
import json, re, html, urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

WATER_URL = "https://www.kasen.pref.gifu.lg.jp/h/Valley_6_450.html"
CAMERA_URL = "https://www.kasen.pref.gifu.lg.jp/h/Camera513_B.html"
JST = timezone(timedelta(hours=9))
UA = "Mozilla/5.0 (compatible; TsubogawaWatch/2.0; personal river monitor)"

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.urls = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("br","tr","p","div","hr","table","h1","h2","h3"):
            self.text.append("\n")
        for k in ("src","href"):
            if d.get(k):
                self.urls.append(d[k])
    def handle_endtag(self, tag):
        if tag in ("tr","p","div","table","h1","h2","h3"):
            self.text.append("\n")
    def handle_data(self, data):
        self.text.append(data)

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent":UA, "Cache-Control":"no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        b = r.read()
        if binary:
            return b
        charset = r.headers.get_content_charset()
    tried=[]
    for enc in ([charset] if charset else []) + ["utf-8","cp932","shift_jis","euc_jp"]:
        if not enc or enc in tried: continue
        tried.append(enc)
        try: return b.decode(enc)
        except Exception: pass
    return b.decode("utf-8","replace")

def parse_html(s):
    p=Extractor()
    p.feed(s)
    text=html.unescape("".join(p.text)).replace("\u3000"," ").replace("\xa0"," ")
    text="\n".join(re.sub(r"[ \t]+"," ",x).strip() for x in text.splitlines())
    return text, p.urls

def infer_dt(source_dt, hhmm):
    h,m=map(int,hhmm.split(":"))
    d=source_dt.replace(hour=h,minute=m,second=0,microsecond=0)
    if d > source_dt + timedelta(minutes=5):
        d -= timedelta(days=1)
    return d

def section(text, name, next_name=None):
    pos=text.find(name)
    if pos < 0: return ""
    end=text.find(next_name,pos+len(name)) if next_name else -1
    if end < 0: end=len(text)
    return text[pos:end]

def parse_rows(block, source_dt):
    rows=[]
    pat=re.compile(r"(?<!\d)(\d{1,2}:\d{2})\s+(-?\d+(?:\.\d+)?)\s*([↑↓→])")
    for tm,val,tr in pat.findall(block):
        dt=infer_dt(source_dt,tm)
        rows.append({"ts":dt.isoformat(timespec="seconds"),"level":float(val),"trend":tr,"source":"Gifu"})
    return rows

def load_json(path, default):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return default

def save_json(path, obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def update_water():
    raw=fetch(WATER_URL)
    text,_=parse_html(raw)
    m=re.search(r"(20\d{2})/(\d{2})/(\d{2})\s+(\d{1,2}):(\d{2})\s*現在",text)
    if not m:
        raise RuntimeError("Không tìm thấy thời gian cập nhật Gifu")
    y,mo,d,h,mi=map(int,m.groups())
    source_dt=datetime(y,mo,d,h,mi,tzinfo=JST)

    one=section(text,"1時間履歴","24時間履歴")
    day=section(text,"24時間履歴")
    rows=parse_rows(day,source_dt)+parse_rows(one,source_dt)
    if not rows:
        raise RuntimeError("Không tìm thấy các dòng mực nước")

    old=load_json(DATA/"history.json",[])
    by_ts={x["ts"]:x for x in old if isinstance(x,dict) and "ts" in x}
    for x in rows: by_ts[x["ts"]]=x

    cutoff=source_dt-timedelta(days=45)
    merged=[]
    for x in by_ts.values():
        try:
            dt=datetime.fromisoformat(x["ts"])
            if dt>=cutoff: merged.append(x)
        except Exception: pass
    merged.sort(key=lambda x:x["ts"])
    save_json(DATA/"history.json",merged)

    cur=max(rows,key=lambda x:x["ts"])
    out={
      "station":"関","river":"津保川","level":cur["level"],"trend":cur["trend"],
      "sourceUpdated":source_dt.isoformat(timespec="seconds"),
      "fetchedAt":datetime.now(JST).isoformat(timespec="seconds"),
      "thresholds":{"standby":3.0,"attention":4.0,"evacuation":5.7,"danger":5.8},
      "sourceUrl":WATER_URL
    }
    save_json(DATA/"latest.json",out)
    print("water",cur["level"],cur["ts"],"points",len(merged))

def update_camera():
    raw=fetch(CAMERA_URL)
    text,urls=parse_html(raw)
    tm=re.search(r"(20\d{2})/(\d{2})/(\d{2})\s+(\d{1,2}):(\d{2})\s*現在",text)
    source_dt=None
    if tm:
        y,mo,d,h,mi=map(int,tm.groups())
        source_dt=datetime(y,mo,d,h,mi,tzinfo=JST)

    candidates=[]
    for u in urls:
        full=urllib.parse.urljoin(CAMERA_URL,u)
        if re.search(r"_fenl\.jpe?g(?:\?|$)",full,re.I):
            candidates.append(full)
    if not candidates and source_dt:
        stamp=source_dt.strftime("%Y%m%d%H%M00")
        ymd=source_dt.strftime("%Y%m%d")
        candidates=[f"https://www.kasen.pref.gifu.lg.jp/h/cctv_image/513/{ymd}/{stamp}_513_fenl.jpg"]

    if not candidates:
        raise RuntimeError("Không tìm thấy URL ảnh camera lớn")

    img_url=candidates[0]
    prev=load_json(DATA/"camera.json",{})
    stamp=source_dt.isoformat(timespec="seconds") if source_dt else None
    image_path=DATA/"camera-latest.jpg"
    if prev.get("sourceUrl") != img_url or not image_path.exists():
        img=fetch(img_url,binary=True)
        if len(img)<1000:
            raise RuntimeError("Ảnh camera tải về quá nhỏ")
        image_path.write_bytes(img)

    save_json(DATA/"camera.json",{
      "station":"関","river":"津保川",
      "sourceUpdated":stamp,
      "fetchedAt":datetime.now(JST).isoformat(timespec="seconds"),
      "sourceUrl":img_url,
      "pageUrl":CAMERA_URL
    })
    print("camera",stamp,img_url)

if __name__=="__main__":
    errors=[]
    try: update_water()
    except Exception as e:
        print("WATER ERROR:",repr(e)); errors.append("water")
    try: update_camera()
    except Exception as e:
        print("CAMERA ERROR:",repr(e)); errors.append("camera")
    # Keep prior data if one source temporarily fails.
    if len(errors)==2:
        raise SystemExit(1)
