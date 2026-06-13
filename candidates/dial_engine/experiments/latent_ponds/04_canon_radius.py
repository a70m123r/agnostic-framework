"""
Canon-radius analysis:
- identify windows where en-es / en-de co-move strongly (global-canon events)
- identify windows where en-ja / en-ar diverge (local-canon events)
- rolling 7-day Pearson r for all pairs
- simple peak detection: which daily dates had the highest cross-language correlation?
"""

import json
import numpy as np
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
START = "2026030100"
END   = "2026060123"
LANGUAGES = ["en", "ja", "de", "ar", "es"]

def load_hourly(lang):
    path = CACHE_DIR / f"hourly_{lang}_{START}_{END}.json"
    with open(path) as f:
        items = json.load(f)
    return [x["views"] for x in items], [x["timestamp"] for x in items]

def pearson_r(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    a0 = a - a.mean()
    b0 = b - b.mean()
    denom = np.sqrt(np.sum(a0**2)*np.sum(b0**2))
    if denom == 0: return float("nan")
    return float(np.dot(a0,b0)/denom)

# Load all hourly series
hourly = {}
timestamps = {}
for lang in LANGUAGES:
    v, t = load_hourly(lang)
    hourly[lang] = np.array(v, dtype=float)
    timestamps[lang] = t

# Aggregate to daily
n_hours = len(hourly["en"])
n_days = n_hours // 24
daily = {}
day_timestamps = []
for lang in LANGUAGES:
    x = hourly[lang]
    daily[lang] = np.array([x[i*24:(i+1)*24].sum() for i in range(n_days)])
for i in range(n_days):
    day_timestamps.append(timestamps["en"][i*24][:8])  # YYYYMMDD

# Rolling 7-day Pearson r for en vs each other language
window = 7
print("Rolling 7-day r: en vs {ja, de, ar, es}")
print(f"  {'date':>10s} {'en-ja':>8s} {'en-de':>8s} {'en-ar':>8s} {'en-es':>8s}  note")
others = ["ja", "de", "ar", "es"]

global_canon_days = []  # days where ALL pairs > 0.8
local_diverge_days = []  # days where en-ja or en-ar < 0.2

for i in range(n_days - window + 1):
    en_chunk = daily["en"][i:i+window]
    rs = {}
    for lang in others:
        rs[lang] = pearson_r(en_chunk, daily[lang][i:i+window])
    date = day_timestamps[i]
    note = ""
    # classify
    if all(rs[l] > 0.75 for l in others):
        note = "<-- ALL HIGH (global-canon)"
        global_canon_days.append((date, rs))
    elif rs.get("ja", 0) < 0.2 and rs.get("ar", 0) < 0.2:
        note = "<-- JA+AR LOW (local-canon diverge)"
        local_diverge_days.append((date, rs))
    elif rs.get("de", 0) > 0.9 and rs.get("es", 0) > 0.9:
        note = "<-- DE+ES VERY HIGH"
    print(f"  {date:>10s} {rs['ja']:>8.4f} {rs['de']:>8.4f} {rs['ar']:>8.4f} {rs['es']:>8.4f}  {note}")

print(f"\nSummary:")
print(f"  Global-canon windows (all pairs > 0.75): {len(global_canon_days)}")
print(f"  Local-canon diverge windows (ja+ar < 0.2): {len(local_diverge_days)}")

if global_canon_days:
    print(f"\n  Global-canon examples:")
    for date, rs in global_canon_days[:5]:
        print(f"    {date}: en-ja={rs['ja']:.3f} en-de={rs['de']:.3f} "
              f"en-ar={rs['ar']:.3f} en-es={rs['es']:.3f}")

if local_diverge_days:
    print(f"\n  Local-canon diverge examples:")
    for date, rs in local_diverge_days[:5]:
        print(f"    {date}: en-ja={rs['ja']:.3f} en-de={rs['de']:.3f} "
              f"en-ar={rs['ar']:.3f} en-es={rs['es']:.3f}")

# Find the top-5 days by average cross-lang r (most "global" canon events)
print()
print("Top-5 days by mean cross-language r (most globally shared attention):")
scores = []
for i in range(n_days - window + 1):
    en_chunk = daily["en"][i:i+window]
    rs_vals = []
    for lang in others:
        r = pearson_r(en_chunk, daily[lang][i:i+window])
        if not np.isnan(r):
            rs_vals.append(r)
    if rs_vals:
        scores.append((day_timestamps[i], np.mean(rs_vals)))
scores.sort(key=lambda x: x[1], reverse=True)
for date, score in scores[:5]:
    print(f"  start {date}: mean_r={score:.4f}")

print()
print("Bottom-5 days by mean cross-language r (most locally isolated attention):")
scores.sort(key=lambda x: x[1])
for date, score in scores[:5]:
    print(f"  start {date}: mean_r={score:.4f}")
