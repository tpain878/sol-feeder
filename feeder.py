import os, time, json, random, requests

# CONFIG
API_URL = "https://memecoin-qv75.onrender.com"   # your API base
FEED_KEY = "feed-tyler-001"                       # your feed key
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")      # set on Render later

# ---- Replace this function later with real Helius logic ----
# For now: demo "candidate" mints (fake mints shaped like pump.fun style).
def find_new_candidates():
    # Simulate discovery of 1-3 new tokens per loop
    out = []
    for _ in range(random.randint(1,3)):
        mint = f"DUMMY{random.randint(1000000,9999999)}"
        # quick toy score; swap with real scoring later
        score = random.randint(80, 98)
        out.append({"mint": mint, "score": score})
    return out
# ------------------------------------------------------------

def push_candidate(mint: str, score: int):
    r = requests.post(
        f"{API_URL}/feed",
        headers={"Content-Type":"application/json", "x-api-key": FEED_KEY},
        json={"mint": mint, "score": score}
    )
    r.raise_for_status()

def main():
    print("feeder: starting")
    while True:
        try:
            cands = find_new_candidates()
            for c in cands:
                if c["score"] >= 85:       # threshold
                    push_candidate(c["mint"], c["score"])
                    print("pushed", c)
        except Exception as e:
            print("error:", e)
        time.sleep(10)

if __name__ == "__main__":
    main()
