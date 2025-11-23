# sample_soilgrids.py
import requests, time, csv, os, sys
import pandas as pd

INPUT = "farms.csv"
OUTPUT = "farms_soilgrid.csv"
DELAY = 12  # seconds between calls to be polite (approx 5 calls/min)

def query_soilgrids(lat, lon):
    url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    params = {"lat": lat, "lon": lon}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    js = r.json()
    # safe extraction helper
    def extract_var(js, var, depth_label="0-5cm"):
        try:
            layers = js.get("properties", {}).get("layers", {})
            v = layers.get(var, {})
            depths = v.get("depths", [])
            # find matching depth by label or take first
            for d in depths:
                if depth_label in d.get("depth", ""):
                    return d.get("values", {}).get("mean")
            if depths:
                return depths[0].get("values", {}).get("mean")
        except Exception:
            return None
        return None

    return {
        "phh2o_0_5cm": extract_var(js, "phh2o", "0-5cm") or extract_var(js, "phh2o"),
        "ocd_0_5cm":  extract_var(js, "ocd",  "0-5cm") or extract_var(js, "ocd"),
        "sand_0_5cm": extract_var(js, "sand", "0-5cm") or extract_var(js, "sand"),
        "clay_0_5cm": extract_var(js, "clay", "0-5cm") or extract_var(js, "clay")
    }

def main():
    if not os.path.exists(INPUT):
        print(f"Create {INPUT} first (see example).")
        sys.exit(1)
    df = pd.read_csv(INPUT)
    results = []
    # load cache if exists
    cache = {}
    if os.path.exists(OUTPUT):
        cache_df = pd.read_csv(OUTPUT)
        for _, r in cache_df.iterrows():
            cache[(r.latitude, r.longitude)] = r.to_dict()

    for _, row in df.iterrows():
        lat = float(row.latitude)
        lon = float(row.longitude)
        key = (lat, lon)
        if key in cache:
            rec = cache[key]
            print(f"Using cached for {row.farm_id} {lat},{lon}")
        else:
            print(f"Querying SoilGrids for {row.farm_id} {lat},{lon} ...")
            try:
                rec_vals = query_soilgrids(lat, lon)
            except Exception as e:
                print("  ERROR:", e)
                rec_vals = {"phh2o_0_5cm": None, "ocd_0_5cm": None, "sand_0_5cm": None, "clay_0_5cm": None}
            rec = {
                "farm_id": row.farm_id,
                "latitude": lat,
                "longitude": lon,
                "district_id": row.get("district_id", ""),
                "district_name": row.get("district_name", "")
            }
            rec.update(rec_vals)
            # append to cache
            cache[key] = rec
            time.sleep(DELAY)
        results.append(cache[key])

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT, index=False)
    print("Saved:", OUTPUT)

if __name__ == "__main__":
    main()
