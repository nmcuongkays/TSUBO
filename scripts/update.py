#!/usr/bin/env python3
import json, re, html, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CAMDIR = DATA / "camera"
DATA.mkdir(exist_ok=True)
CAMDIR.mkdir(exist_ok=True)

WATER_URL = "https://www.kasen.pref.gifu.lg.jp/h/Valley_6_450.html"
CAMERA_URL = "https://www.kasen.pref.gifu.lg.jp/h/Camera513_B.html"
JST = timezone(timedelta(hours=9))
UA = "Mozilla/5.0 (compatible; TsubogawaWatch/2.3; personal river monitor)"

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

def fetch(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read()
        if binary:
            return b
        charset = r.headers.get_content_charset()
    tried=[]
    for enc in ([charset] if charset else []) + ["utf-8","cp932","shift_jis","euc_jp"]:
        if not enc or enc in tried:
            continue
        tried.append(enc)
        try:
            return b.decode(enc)
        except Exception:
            pass
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
    if pos < 0:
        return ""
    end=text.find(next_name,pos+len(name)) if next_name else -1
    if end < 0:
        end=len(text)
    return text[pos:end]

def parse_rows(block, source_dt):
    rows=[]
    pat=re.compile(r"(?<!\d)(\d{1,2}:\d{2})\s+(-?\d+(?:\.\d+)?)\s*([↑↓→])")
    for tm,val,tr in pat.findall(block):
        dt=infer_dt(source_dt,tm)
        rows.append({
            "ts":dt.isoformat(timespec="seconds"),
            "level":float(val),
            "trend":tr,
            "source":"Gifu"
        })
    return rows

def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path, obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def update_water():
    raw=fetch(WATER_URL + "?_=" + str(int(datetime.now(JST).timestamp())))
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
    for x in rows:
        by_ts[x["ts"]]=x

    # We only display 24h, but retain 30h to safely span midnight / delayed updates.
    cutoff=source_dt-timedelta(hours=30)
    merged=[]
    for x in by_ts.values():
        try:
            dt=datetime.fromisoformat(x["ts"])
            if dt>=cutoff:
                merged.append(x)
        except Exception:
            pass
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
    return source_dt

def official_camera_url(dt):
    # Camera files are published in 10-minute slots.
    dt=dt.astimezone(JST).replace(second=0,microsecond=0)
    dt=dt.replace(minute=(dt.minute//10)*10)
    ymd=dt.strftime("%Y%m%d")
    stamp=dt.strftime("%Y%m%d%H%M00")
    return f"https://www.kasen.pref.gifu.lg.jp/h/cctv_image/513/{ymd}/{stamp}_513_fenl.jpg"

def image_filename(dt):
    dt=dt.astimezone(JST).replace(second=0,microsecond=0)
    dt=dt.replace(minute=(dt.minute//10)*10)
    return dt.strftime("%Y%m%d%H%M")+".jpg"

def try_download_camera(dt):
    url=official_camera_url(dt)
    fn=image_filename(dt)
    path=CAMDIR/fn
    if path.exists() and path.stat().st_size>1000:
        return {"ts":dt.astimezone(JST).replace(second=0,microsecond=0).isoformat(timespec="seconds"),
                "path":f"data/camera/{fn}","sourceUrl":url}
    try:
        img=fetch(url,binary=True,timeout=12)
        if len(img)<1000 or not img.startswith(b"\xff\xd8"):
            return None
        path.write_bytes(img)
        return {"ts":dt.astimezone(JST).replace(second=0,microsecond=0).isoformat(timespec="seconds"),
                "path":f"data/camera/{fn}","sourceUrl":url}
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None

def update_camera():
    raw=fetch(CAMERA_URL + "?_=" + str(int(datetime.now(JST).timestamp())))
    text,urls=parse_html(raw)
    tm=re.search(r"(20\d{2})/(\d{2})/(\d{2})\s+(\d{1,2}):(\d{2})\s*現在",text)
    if not tm:
        raise RuntimeError("Không tìm thấy thời gian camera Gifu")
    y,mo,d,h,mi=map(int,tm.groups())
    source_dt=datetime(y,mo,d,h,mi,tzinfo=JST)

    candidates=[]
    for u in urls:
        full=urllib.parse.urljoin(CAMERA_URL,u)
        if re.search(r"_fenl\.jpe?g(?:\?|$)",full,re.I):
            candidates.append(full)
    if not candidates:
        for u in re.findall(r"""(?:src|href)\s*=\s*["']([^"']+_fenl\.jpe?g[^"']*)["']""", raw, re.I):
            candidates.append(urllib.parse.urljoin(CAMERA_URL, html.unescape(u)))
    img_url=candidates[0] if candidates else official_camera_url(source_dt)

    # Save the exact latest image from the camera page.
    img=fetch(img_url,binary=True,timeout=20)
    if len(img)<1000 or not img.startswith(b"\xff\xd8"):
        raise RuntimeError("Ảnh camera mới nhất không hợp lệ")
    latest_name=image_filename(source_dt)
    (CAMDIR/latest_name).write_bytes(img)
    (DATA/"camera-latest.jpg").write_bytes(img)

    # Build/repair a 24-hour camera archive at times that appear on the water timeline.
    hist=load_json(DATA/"history.json",[])
    desired=set()
    desired.add(source_dt.replace(second=0,microsecond=0,minute=(source_dt.minute//10)*10))
    cutoff=source_dt-timedelta(hours=24,minutes=20)
    for x in hist:
        try:
            d=datetime.fromisoformat(x["ts"]).astimezone(JST)
            d=d.replace(second=0,microsecond=0,minute=(d.minute//10)*10)
            if d>=cutoff:
                desired.add(d)
        except Exception:
            pass

    # Try only missing desired points (usually <= 30 on first run, then 1 new point).
    for d in sorted(desired):
        fn=CAMDIR/image_filename(d)
        if not fn.exists():
            try_download_camera(d)

    # Purge images older than 26h to keep the repo small.
    purge_before=source_dt-timedelta(hours=26)
    for p in CAMDIR.glob("*.jpg"):
        try:
            d=datetime.strptime(p.stem,"%Y%m%d%H%M").replace(tzinfo=JST)
            if d<purge_before:
                p.unlink()
        except Exception:
            pass

    # Rebuild archive index from actual files.
    index=[]
    for p in CAMDIR.glob("*.jpg"):
        try:
            d=datetime.strptime(p.stem,"%Y%m%d%H%M").replace(tzinfo=JST)
            index.append({
                "ts":d.isoformat(timespec="seconds"),
                "path":f"data/camera/{p.name}",
                "sourceUrl":official_camera_url(d)
            })
        except Exception:
            pass
    index.sort(key=lambda x:x["ts"])
    save_json(DATA/"camera-history.json",index)

    save_json(DATA/"camera.json",{
      "station":"関","river":"津保川",
      "sourceUpdated":source_dt.isoformat(timespec="seconds"),
      "fetchedAt":datetime.now(JST).isoformat(timespec="seconds"),
      "sourceUrl":img_url,
      "path":f"data/camera/{latest_name}",
      "pageUrl":CAMERA_URL,
      "archiveCount":len(index)
    })
    print("camera",source_dt.isoformat(),"archive",len(index))

def save_health(errors):
    now=datetime.now(JST)
    save_json(DATA/"health.json",{
        "checkedAt":now.isoformat(timespec="seconds"),
        "ok":len(errors)==0,
        "errors":errors
    })

if __name__=="__main__":
    errors=[]
    try:
        update_water()
    except Exception as e:
        print("WATER ERROR:",repr(e))
        errors.append("water")
    try:
        update_camera()
    except Exception as e:
        print("CAMERA ERROR:",repr(e))
        errors.append("camera")
    save_health(errors)
    # Do not erase good previous data on a transient source failure.
    if len(errors)==2:
        raise SystemExit(1)
