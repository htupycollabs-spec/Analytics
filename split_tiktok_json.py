"""
split_tiktok_json.py
Splits user_data_tiktok.json (20MB) into manageable files (<= 1MB each).
Output folder: tiktok_data_json/
"""

import json
import os
import math

# ── CONFIG ──────────────────────────────────────────────────────────────────
SRC = "user_data_tiktok.json"
OUT = "tiktok_data_json"
# Chunk sizes for large lists
POSTS_CHUNK    = 1000   # ~1.26 MB/chunk
BROWSING_CHUNK = 2500   # ~0.49 MB/chunk
LOGIN_CHUNK    = 3000   # ~0.44 MB/chunk
WATCH_CHUNK    = 5000   # ~0.49 MB/chunk

os.makedirs(OUT, exist_ok=True)

def write(name, obj):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    kb = os.path.getsize(path) / 1024
    print(f"  [{kb:6.0f} KB]  {name}")
    return kb

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

# ── LOAD ─────────────────────────────────────────────────────────────────────
print(f"Loading {SRC}…")
with open(SRC, "r", encoding="utf-8") as f:
    data = json.load(f)
print("Done. Splitting…\n")

# ── 01  COMMENTS ─────────────────────────────────────────────────────────────
write("01_comments.json", data["Comment"])

# ── 02  DIRECT MESSAGES ──────────────────────────────────────────────────────
write("02_direct_messages.json", data["Direct Message"])

# ── 03  WALLET ───────────────────────────────────────────────────────────────
write("03_wallet.json", data["Income+ Wallet"])

# ── 04  LIKES & FAVORITES ────────────────────────────────────────────────────
write("04_likes_favorites.json", data["Likes and Favorites"])

# ── 05  LOCATION REVIEWS ─────────────────────────────────────────────────────
write("05_location_reviews.json", data["Location Review"])

# ── 06  POSTS (split by chunk of 1000) ───────────────────────────────────────
video_list = data["Post"]["Posts"]["VideoList"]
total_posts = len(video_list)
n_chunks = math.ceil(total_posts / POSTS_CHUNK)
for i, chunk in enumerate(chunks(video_list, POSTS_CHUNK), 1):
    payload = {
        "Post": {
            "Posts": {
                "VideoList": chunk,
                "_meta": {
                    "part": i,
                    "of": n_chunks,
                    "items_in_part": len(chunk),
                    "total_items": total_posts,
                    "date_range": f"{chunk[-1]['Date'][:10]} – {chunk[0]['Date'][:10]}"
                }
            },
            "Recently Deleted Posts": data["Post"]["Recently Deleted Posts"],
            "Story": data["Post"]["Story"]
        }
    }
    fname = f"06_posts_p{i:02d}_of_{n_chunks:02d}.json"
    write(fname, payload)

# ── 07  PROFILE & SETTINGS ───────────────────────────────────────────────────
ps = data["Profile And Settings"]
profile_core = {k: v for k, v in ps.items()
                if k not in ("Follower", "Following")}
write("07_profile_settings.json", {"Profile And Settings": profile_core})

# ── 08  FOLLOWERS ────────────────────────────────────────────────────────────
write("08_followers.json", {
    "Follower": ps["Follower"],
    "_meta": {"total_followers": len(ps["Follower"]["FansList"])}
})

# ── 09  FOLLOWING ────────────────────────────────────────────────────────────
write("09_following.json", {
    "Following": ps["Following"],
    "_meta": {"total_following": len(ps["Following"]["Following"])}
})

# ── 10  TIKTOK LIVE ──────────────────────────────────────────────────────────
write("10_tiktok_live.json", data["TikTok Live"])

# ── 11  TIKTOK SHOP OVERVIEW (everything except product browsing) ─────────────
shop = data["TikTok Shop"]
shop_overview = {k: v for k, v in shop.items() if k != "Product Browsing History"}
write("11_shop_overview.json", {"TikTok Shop": shop_overview})

# ── 12  SHOP PRODUCT BROWSING (split by chunk of 2500) ───────────────────────
browsing_list = shop["Product Browsing History"]["ProductBrowsingHistories"]
total_browsing = len(browsing_list)
n_browsing = math.ceil(total_browsing / BROWSING_CHUNK)
for i, chunk in enumerate(chunks(browsing_list, BROWSING_CHUNK), 1):
    payload = {
        "Product Browsing History": {
            "ProductBrowsingHistories": chunk,
            "_meta": {
                "part": i,
                "of": n_browsing,
                "items_in_part": len(chunk),
                "total_items": total_browsing,
                "date_range": f"{chunk[-1]['browsing_date'][:10]} – {chunk[0]['browsing_date'][:10]}"
            }
        }
    }
    fname = f"12_shop_browsing_p{i:02d}_of_{n_browsing:02d}.json"
    write(fname, payload)

# ── 13  ACTIVITY – MISC (hashtags, searches, reposts, shares, status, ad interests) ──
act = data["Your Activity"]
misc_keys = ["Ad Interests", "Donation", "Fundraiser", "Hashtag",
             "Instant Form Ads Responses", "Off TikTok Activity",
             "Purchases", "Reposts", "Searches", "Share History", "Status", "Stickers"]
act_misc = {k: act[k] for k in misc_keys if k in act}
write("13_activity_misc.json", {"Your Activity": act_misc})

# ── 14  LOGIN HISTORY (split by chunk of 3000) ───────────────────────────────
login_list = act["Login History"]["LoginHistoryList"]
total_logins = len(login_list)
n_logins = math.ceil(total_logins / LOGIN_CHUNK)
for i, chunk in enumerate(chunks(login_list, LOGIN_CHUNK), 1):
    payload = {
        "Login History": {
            "LoginHistoryList": chunk,
            "_meta": {
                "part": i,
                "of": n_logins,
                "items_in_part": len(chunk),
                "total_items": total_logins,
                "date_range": f"{chunk[-1]['Date'][:10]} – {chunk[0]['Date'][:10]}"
            }
        }
    }
    fname = f"14_login_history_p{i:02d}_of_{n_logins:02d}.json"
    write(fname, payload)

# ── 15  WATCH HISTORY (split by chunk of 5000) ───────────────────────────────
watch_list = act["Watch History"]["VideoList"]
total_watches = len(watch_list)
n_watches = math.ceil(total_watches / WATCH_CHUNK)
for i, chunk in enumerate(chunks(watch_list, WATCH_CHUNK), 1):
    payload = {
        "Watch History": {
            "VideoList": chunk,
            "_meta": {
                "part": i,
                "of": n_watches,
                "items_in_part": len(chunk),
                "total_items": total_watches,
                "date_range": f"{chunk[-1]['Date'][:10]} – {chunk[0]['Date'][:10]}"
            }
        }
    }
    fname = f"15_watch_history_p{i:02d}_of_{n_watches:02d}.json"
    write(fname, payload)

# ── SUMMARY ──────────────────────────────────────────────────────────────────
all_files = sorted(os.listdir(OUT))
total_kb = sum(os.path.getsize(os.path.join(OUT, f)) / 1024 for f in all_files)
print(f"\n✓ {len(all_files)} files written to '{OUT}/'  ({total_kb/1024:.1f} MB total)")
