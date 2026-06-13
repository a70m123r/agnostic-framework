"""
P-L6 — intervention damping (tsunami-subdued, measured) — FETCH stage.

Probe: en.wikipedia article-protection events = public intervention timestamps
mid-attention-storm (NESTED_PONDS B10: engineered hydraulics). Measure post-peak
decay of protected storms vs MATCHED UNPROTECTED storms (same period, similar
peak magnitude + pre-peak shape) to separate intervention damping from natural
mean-reversion (protection is endogenous: applied at/near peak).

Register: exploratory instrument, read-only, real fetched data only, cached to disk.
UA: agnostic-framework-research/0.1 (research instrument)

-------------------- PRE-REGISTERED PARAMETERS (fixed before any decay fit) ----
Protection-event window : 2026-03-01 .. 2026-05-10 (so +31d of pageviews exist)
Event filter            : letype=protect, ns=0, action in {protect, modify},
                          must carry an EDIT restriction (move-only excluded)
Pageview series         : per-article, en.wikipedia, all-access, agent=USER, daily,
                          prot-60d .. prot+31d (zero-filled missing days)
Peak location           : argmax over [prot-25, prot+10]; must land in
                          [prot-14, prot+7] (else early/late-peak, excluded)
Baseline                : median(views[peak-45 .. peak-15])
Storm criteria          : peak >= 5 x max(baseline,1)  AND  peak-baseline >= 2000
Decay fit               : OLS slope of ln(excess) over k = 1..14 post-peak
                          (excess = views - baseline; >=7 valid days, excess>=max(5, 1% of peak excess))
Weekly-cycle-robust     : R7 = excess(peak+7)/excess(peak), R14 same (same weekday)
Growth fit (pre-peak)   : OLS slope of ln(excess) over k = -5..0 (>=3 valid days)
Controls                : from daily top-1000 on each treated peak date; views in
                          [0.4, 2.5] x treated peak; never in the protection log
                          window; no protect log event within [D-365, D+40];
                          currently-unprotected preferred (flags recorded);
                          same storm criteria; peak within +-3d of top date
Matching                : caliper |dlog10 peak_excess| <= 0.35, up to 3 nearest
                          controls per treated (distance = magnitude + growth shape)
--------------------------------------------------------------------------------
Confound handling folded in from the fresh scan (2026-06):
- McGrady 2025: stratify by protection level (semi/EC/full) + trigger keywords.
- Buntain/Snegovaya 2025: post window 31d (90d ideal; disclosed limitation).
- Okamura 2026 weekly periodicity: R7/R14 same-weekday ratios as primary robust metric.
- Cima 2025 heterogeneity: full distribution + Streisand (rebound) counts reported.
- agent=user excludes spider/automated traffic.
"""
import json, os, sys, time, hashlib, datetime as dt
import urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

UA    = "agnostic-framework-research/0.1 (research instrument)"
BASE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "cache", "pl6")
DATA  = os.path.join(BASE, "data", "pl6")
os.makedirs(CACHE, exist_ok=True); os.makedirs(DATA, exist_ok=True)

PROT_START   = dt.date(2026, 3, 1)
PROT_END     = dt.date(2026, 5, 10)
PV_PRE_D     = 60
PV_POST_D    = 31
PEAK_LO, PEAK_HI = -14, 7         # admissible peak vs protection day
PEAK_EXT_LO, PEAK_EXT_HI = -25, 10  # extended argmax window (early/late guard)
BASE_LO, BASE_HI = -45, -15       # baseline window relative to peak
STORM_RATIO  = 5.0
STORM_EXCESS = 2000
CTRL_BAND    = (0.4, 2.5)
CTRL_CAND_PER_T = 8
WORKERS      = 5

NS_PREFIXES = ("Special:", "Wikipedia:", "File:", "Portal:", "Help:", "Category:",
               "Template:", "Draft:", "User:", "Talk:", "Module:", "MediaWiki:",
               "TimedText:", "Book:", "Gadget:", "Education_Program:",
               "Wikipedia_talk:", "User_talk:", "Template_talk:", "File_talk:",
               "Category_talk:", "Portal_talk:", "Module_talk:", "Help_talk:",
               "Draft_talk:", "MediaWiki_talk:", "Talk_talk:")
BLOCK_EXACT = {"Main_Page", "Wikipedia", "Search"}

def log(msg):
    print(msg, flush=True)

def cache_path(key):
    return os.path.join(CACHE, key + ".json")

def fetch(url, cache_key=None, retries=4):
    key = cache_key or hashlib.sha1(url.encode("utf-8")).hexdigest()
    path = cache_path(key)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last_err = None
    for a in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                obj = json.loads(r.read().decode("utf-8"))
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f)
            time.sleep(0.06)
            return obj
        except urllib.error.HTTPError as e:
            if e.code == 404:
                obj = {"_error": 404}
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(obj, f)
                return obj
            last_err = "HTTP %d" % e.code
            time.sleep(2.0 + 2.0 * a if e.code == 429 else 1.0 + a)
        except Exception as e:
            last_err = str(e)
            time.sleep(1.0 + a)
    return {"_error": last_err}

def tmap(fn, items, workers=WORKERS, label=""):
    out = {}
    if not items:
        return out
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fn, it): it for it in items}
        done = 0
        for fu in as_completed(futs):
            it = futs[fu]
            try:
                out[it] = fu.result()
            except Exception as e:
                out[it] = {"_error": str(e)}
            done += 1
            if done % 100 == 0:
                log("  [%s] %d/%d" % (label, done, len(items)))
    return out

def canon(title):
    return title.replace(" ", "_")

def pv_url(title, d0, d1):
    t = urllib.parse.quote(canon(title), safe="")
    return ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
            "en.wikipedia/all-access/user/%s/daily/%s/%s"
            % (t, d0.strftime("%Y%m%d"), d1.strftime("%Y%m%d")))

def fetch_pv(title, d0, d1):
    key = "pv_" + hashlib.sha1((canon(title) + d0.isoformat() + d1.isoformat()).encode("utf-8")).hexdigest()
    obj = fetch(pv_url(title, d0, d1), cache_key=key)
    series = {}
    for it in obj.get("items", []):
        ts = it["timestamp"][:8]
        series["%s-%s-%s" % (ts[:4], ts[4:6], ts[6:8])] = it["views"]
    # zero-fill
    out = {}
    d = d0
    while d <= d1:
        out[d.isoformat()] = series.get(d.isoformat(), 0)
        d += dt.timedelta(days=1)
    out["_error"] = obj.get("_error")
    return out

# ---------------- stage 0: pageview availability ----------------
def detect_pv_end():
    d1 = dt.date(2026, 6, 13)
    d0 = dt.date(2026, 6, 1)
    obj = fetch(pv_url("Earth", d0, d1), cache_key="pv_avail_probe")
    items = obj.get("items", [])
    if not items:
        return None
    ts = items[-1]["timestamp"][:8]
    return dt.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))

# ---------------- stage 1: protection log ----------------
def get_prot_log():
    events, cont, page = [], None, 0
    while True:
        p = {"action": "query", "list": "logevents", "letype": "protect",
             "lelimit": "500", "lenamespace": "0",
             "leprop": "ids|title|type|user|timestamp|comment|details",
             "lestart": PROT_END.isoformat() + "T23:59:59Z",
             "leend": PROT_START.isoformat() + "T00:00:00Z",
             "format": "json", "formatversion": "2"}
        if cont:
            p["lecontinue"] = cont
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
        obj = fetch(url, cache_key="protlog_p%03d" % page)
        evs = obj.get("query", {}).get("logevents", [])
        events.extend(evs)
        cont = obj.get("continue", {}).get("lecontinue")
        page += 1
        log("  protlog page %d: +%d events (total %d)" % (page, len(evs), len(events)))
        if not cont or page > 60:
            break
    return events

TRIGGER_RULES = [
    ("vandalism",   ["vandal"]),
    ("edit_war",    ["edit war", "warring", "content dispute", "dispute"]),
    ("blp",         ["blp", "biographies of living", "living person"]),
    ("sock",        ["sock", "block evasion", "banned user"]),
    ("disruptive",  ["disrupt"]),
    ("arbitration", ["arbitration", "contentious topic", "arbcom", "ctop", "/ae", "ae action", "general sanction", "community sanction"]),
    ("high_visibility", ["high-risk", "high risk", "highly visible", "high traffic", "visible template"]),
]

def classify_trigger(comment):
    c = (comment or "").lower()
    hits = [name for name, kws in TRIGGER_RULES if any(k in c for k in kws)]
    return (hits[0] if hits else "other"), hits

def edit_level(details):
    levels = [d.get("level") for d in (details or []) if d.get("type") == "edit"]
    if not levels:
        return None
    rank = {"autoconfirmed": 1, "extendedconfirmed": 2, "sysop": 3}
    best = max(levels, key=lambda L: rank.get(L, 0))
    return {"autoconfirmed": "semi", "extendedconfirmed": "ec", "sysop": "full"}.get(best, best)

def parse_events(events):
    """Keep protect/modify with an edit restriction; earliest per title."""
    per_title = {}
    all_logged_titles = set()
    for ev in events:
        title = ev.get("title")
        if not title:
            continue
        all_logged_titles.add(canon(title))
        if ev.get("action") not in ("protect", "modify"):
            continue
        params = ev.get("params", {}) or {}
        details = params.get("details")
        lev = edit_level(details)
        if lev is None:
            desc = params.get("description", "") or ""
            if "[edit=" not in desc:
                continue
            for token, name in (("[edit=sysop]", "full"), ("[edit=extendedconfirmed]", "ec"),
                                ("[edit=autoconfirmed]", "semi")):
                if token in desc:
                    lev = name
                    break
            if lev is None:
                lev = "unknown"
        expiry = None
        for d in (details or []):
            if d.get("type") == "edit":
                expiry = d.get("expiry")
        indef = (expiry in ("infinite", "infinity", "never")) if expiry else None
        ts = ev["timestamp"]
        date = dt.date(int(ts[:4]), int(ts[5:7]), int(ts[8:10]))
        trigger, trigger_all = classify_trigger(ev.get("comment"))
        rec = {"title": title, "key": canon(title), "prot_ts": ts,
               "prot_date": date.isoformat(), "action": ev.get("action"),
               "level": lev, "expiry": expiry, "indef": indef,
               "comment": ev.get("comment"), "user": ev.get("user"),
               "trigger": trigger, "trigger_all": trigger_all}
        k = rec["key"]
        if k not in per_title or rec["prot_ts"] < per_title[k]["prot_ts"]:
            n_prev = per_title.get(k, {}).get("n_events_window", 0)
            rec["n_events_window"] = n_prev + 1
            per_title[k] = rec
        else:
            per_title[k]["n_events_window"] += 1
    return list(per_title.values()), all_logged_titles

# ---------------- storm detection (shared treated/control) ----------------
def detect_storm(series, anchor_date, kind):
    """series: iso-date -> views. anchor = protection date (treated) or top date (control).
    Returns dict with peak/baseline/qualifies/fail_reason."""
    dates = sorted([d for d in series if not d.startswith("_")])
    vals = {d: series[d] for d in dates}
    a = dt.date.fromisoformat(anchor_date)
    def day(off):
        return (a + dt.timedelta(days=off)).isoformat()
    if kind == "treated":
        ext = [day(o) for o in range(PEAK_EXT_LO, PEAK_EXT_HI + 1) if day(o) in vals]
        adm_lo, adm_hi = PEAK_LO, PEAK_HI
    else:
        ext = [day(o) for o in range(-10, 11) if day(o) in vals]
        adm_lo, adm_hi = -3, 3
    if not ext:
        return {"qualifies": False, "fail_reason": "no_data"}
    peak_date = max(ext, key=lambda d: vals[d])
    peak_views = vals[peak_date]
    off = (dt.date.fromisoformat(peak_date) - a).days
    if off < adm_lo:
        return {"qualifies": False, "fail_reason": "peak_too_early", "peak_date": peak_date, "peak_views": peak_views}
    if off > adm_hi:
        return {"qualifies": False, "fail_reason": "peak_too_late", "peak_date": peak_date, "peak_views": peak_views}
    p = dt.date.fromisoformat(peak_date)
    bl_days = [(p + dt.timedelta(days=o)).isoformat() for o in range(BASE_LO, BASE_HI + 1)]
    bl_vals = sorted(vals[d] for d in bl_days if d in vals)
    if len(bl_vals) < 20:
        return {"qualifies": False, "fail_reason": "baseline_short", "peak_date": peak_date, "peak_views": peak_views}
    baseline = bl_vals[len(bl_vals) // 2]
    excess = peak_views - baseline
    if peak_views < STORM_RATIO * max(baseline, 1):
        return {"qualifies": False, "fail_reason": "ratio", "peak_date": peak_date,
                "peak_views": peak_views, "baseline": baseline}
    if excess < STORM_EXCESS:
        return {"qualifies": False, "fail_reason": "excess", "peak_date": peak_date,
                "peak_views": peak_views, "baseline": baseline}
    # require enough post-peak coverage for k=1..14
    if (p + dt.timedelta(days=14)).isoformat() not in vals:
        return {"qualifies": False, "fail_reason": "post_window_short", "peak_date": peak_date,
                "peak_views": peak_views, "baseline": baseline}
    return {"qualifies": True, "fail_reason": None, "peak_date": peak_date,
            "peak_views": peak_views, "baseline": baseline, "peak_excess": excess,
            "peak_offset_vs_anchor": off}

# ---------------- main ----------------
def main():
    t0 = time.time()
    log("== P-L6 fetch stage ==")
    pv_end = detect_pv_end()
    log("pageview daily data available through: %s" % pv_end)
    if pv_end is None:
        log("FATAL: pageview availability probe failed"); sys.exit(1)
    global PROT_END
    need = PROT_END + dt.timedelta(days=PV_POST_D)
    if need > pv_end:
        PROT_END = pv_end - dt.timedelta(days=PV_POST_D)
        log("PROT_END shrunk to %s to keep +%dd windows complete" % (PROT_END, PV_POST_D))

    log("-- stage 1: protection log %s .. %s (ns=0, letype=protect)" % (PROT_START, PROT_END))
    events = get_prot_log()
    treated_events, all_logged = parse_events(events)
    log("raw log events: %d ; protect/modify-with-edit-restriction unique titles: %d ; all logged titles (exclusion set): %d"
        % (len(events), len(treated_events), len(all_logged)))

    log("-- stage 2: pageviews for %d treated candidates (threaded, cached)" % len(treated_events))
    def fetch_treated(i):
        ev = treated_events[i]
        d = dt.date.fromisoformat(ev["prot_date"])
        return fetch_pv(ev["title"], d - dt.timedelta(days=PV_PRE_D), d + dt.timedelta(days=PV_POST_D))
    pv_res = tmap(fetch_treated, list(range(len(treated_events))), label="treated pv")

    treated = []
    fail_counts = {}
    for i, ev in enumerate(treated_events):
        series = pv_res.get(i, {})
        det = detect_storm(series, ev["prot_date"], "treated")
        rec = dict(ev)
        rec.update(det)
        rec["series"] = {k: v for k, v in series.items() if not k.startswith("_")}
        treated.append(rec)
        fail_counts[det.get("fail_reason") or "QUALIFIES"] = fail_counts.get(det.get("fail_reason") or "QUALIFIES", 0) + 1
    qual = [t for t in treated if t["qualifies"]]
    log("storm-filter attrition: %s" % json.dumps(fail_counts))
    log("qualifying treated storms: %d" % len(qual))

    log("-- stage 3: top-1000 lists for unique treated peak dates")
    peak_dates = sorted({t["peak_date"] for t in qual})
    def fetch_top(dstr):
        d = dt.date.fromisoformat(dstr)
        url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/"
               "all-access/%04d/%02d/%02d" % (d.year, d.month, d.day))
        return fetch(url, cache_key="top_%s" % dstr)
    tops = tmap(fetch_top, peak_dates, label="tops")

    log("-- stage 4: control candidates")
    cand = {}   # key -> {"title":..., "anchors": {treated_key: top_date}}
    for t in qual:
        top = tops.get(t["peak_date"], {})
        arts = []
        for item in (top.get("items", [{}])[0].get("articles", []) if top.get("items") else []):
            a, v = item.get("article", ""), item.get("views", 0)
            if a in BLOCK_EXACT or any(a.startswith(p) for p in NS_PREFIXES):
                continue
            if a in all_logged:
                continue
            if not (CTRL_BAND[0] * t["peak_views"] <= v <= CTRL_BAND[1] * t["peak_views"]):
                continue
            arts.append((a, v))
        import math
        arts.sort(key=lambda av: abs(math.log10(max(av[1], 1)) - math.log10(max(t["peak_views"], 1))))
        for a, v in arts[:CTRL_CAND_PER_T]:
            cand.setdefault(a, {"title": a.replace("_", " "), "anchors": {}})
            cand[a]["anchors"][t["key"]] = t["peak_date"]
    log("unique control candidates: %d" % len(cand))

    def fetch_ctrl_pv(akey):
        anchors = sorted(cand[akey]["anchors"].values())
        d0 = dt.date.fromisoformat(anchors[0]) - dt.timedelta(days=PV_PRE_D)
        d1 = dt.date.fromisoformat(anchors[-1]) + dt.timedelta(days=PV_POST_D)
        return fetch_pv(cand[akey]["title"], d0, d1)
    ctrl_pv = tmap(fetch_ctrl_pv, list(cand.keys()), label="ctrl pv")

    log("-- stage 5: protection screening of control candidates")
    def fetch_ctrl_log(akey):
        p = {"action": "query", "list": "logevents", "letype": "protect",
             "letitle": cand[akey]["title"], "lelimit": "500",
             "leprop": "ids|title|type|timestamp|comment|details",
             "format": "json", "formatversion": "2"}
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
        return fetch(url, cache_key="ctlog_" + hashlib.sha1(akey.encode("utf-8")).hexdigest())
    ctrl_logs = tmap(fetch_ctrl_log, list(cand.keys()), label="ctrl logs")

    # current protection state, batch 50
    keys = list(cand.keys())
    cur_prot = {}
    for b in range(0, len(keys), 50):
        batch = keys[b:b + 50]
        p = {"action": "query", "prop": "info", "inprop": "protection",
             "titles": "|".join(cand[k]["title"] for k in batch),
             "format": "json", "formatversion": "2"}
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
        obj = fetch(url, cache_key="ctinfo_b%03d" % (b // 50))
        for pg in obj.get("query", {}).get("pages", []):
            prot = [pr for pr in pg.get("protection", []) if pr.get("type") == "edit"]
            cur_prot[canon(pg.get("title", ""))] = prot

    controls = []
    for akey, c in cand.items():
        series = ctrl_pv.get(akey, {})
        logobj = ctrl_logs.get(akey, {})
        levs = logobj.get("query", {}).get("logevents", [])
        # any protect/modify with an edit restriction near any anchor?
        bad, ever = False, False
        for ev in levs:
            if ev.get("action") not in ("protect", "modify"):
                continue
            det = (ev.get("params", {}) or {}).get("details")
            if edit_level(det) is None and "[edit=" not in ((ev.get("params", {}) or {}).get("description", "") or ""):
                continue
            ever = True
            ets = ev.get("timestamp", "")
            try:
                ed = dt.date(int(ets[:4]), int(ets[5:7]), int(ets[8:10]))
            except Exception:
                continue
            for D in c["anchors"].values():
                Dd = dt.date.fromisoformat(D)
                if Dd - dt.timedelta(days=365) <= ed <= Dd + dt.timedelta(days=40):
                    bad = True
        cur = cur_prot.get(akey, [])
        for D in sorted(set(c["anchors"].values())):
            det = detect_storm(series, D, "control")
            controls.append({"key": akey, "title": c["title"], "anchor_date": D,
                             "anchor_treated": [tk for tk, dd in c["anchors"].items() if dd == D],
                             "prot_event_near_window": bad,
                             "prot_event_ever": ever,
                             "currently_edit_protected": bool(cur),
                             "series": {k: v for k, v in series.items() if not k.startswith("_")},
                             **det})
    n_clean = sum(1 for c in controls if c["qualifies"] and not c["prot_event_near_window"] and not c["currently_edit_protected"])
    log("control storm records: %d ; qualifying+clean: %d" % (len(controls), n_clean))

    dataset = {
        "params": {"PROT_START": PROT_START.isoformat(), "PROT_END": PROT_END.isoformat(),
                   "PV_PRE_D": PV_PRE_D, "PV_POST_D": PV_POST_D,
                   "PEAK_WINDOW": [PEAK_LO, PEAK_HI], "BASE_WIN": [BASE_LO, BASE_HI],
                   "STORM_RATIO": STORM_RATIO, "STORM_EXCESS": STORM_EXCESS,
                   "CTRL_BAND": CTRL_BAND, "pv_end_detected": pv_end.isoformat(),
                   "endpoints": {
                       "protlog": "https://en.wikipedia.org/w/api.php?action=query&list=logevents&letype=protect",
                       "pageviews": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/daily/",
                       "top": "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"},
                   "ua": UA},
        "attrition": fail_counts,
        "treated": treated,
        "controls": controls,
    }
    out = os.path.join(DATA, "pl6_dataset.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(dataset, f)
    log("dataset written: %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
    log("done in %.1f s" % (time.time() - t0))

if __name__ == "__main__":
    main()
