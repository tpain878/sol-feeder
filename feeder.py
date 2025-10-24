import os, time, json, requests
from typing import List, Dict

# CONFIG
API_URL = "https://memecoin-qv75.onrender.com"
FEED_KEY = "feed-tyler-001"
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")  # set in Render environment

# --- Real candidate discovery ---
def find_new_candidates() -> List[Dict]:
    """
    Fetch new Solana tokens from Helius (or another data source),
    and compute a basic score to decide whether to feed them.
    """
    url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
    headers = {"Content-Type": "application/json"}

    # Example: fetch recent token creation events
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": ["So11111111111111111111111111111111111111112", {"limit": 50}]
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()

    candidates = []
    for tx in data.get("result", []):
        mint = tx.get("signature")
        if mint:
            # Placeholder scoring logic – replace with your real model
            score = 85
            candidates.append({"mint": mint, "score": score})
    return candidates

# --- Push candidate to your API ---
def push_candidate(mint: str, score: int):
    r = requests.post(
        f"{API_URL}/feed",
        headers={"Content-Type": "application/json", "x-api-key": FEED_KEY},
        json={"mint": mint, "score": score}
    )
    r.raise_for_status()

# --- Main loop ---
def main():
    print("feeder: starting")
    while True:
        try:
            cands = find_new_candidates()
            for c in cands:
                if c["score"] >= 80:
                    push_candidate(c["mint"], c["score"])
                    print("pushed", c)
        except Exception as e:
            print("error:", e)
        time.sleep(30)

if __name__ == "__main__":
    main()
