import requests
import csv

# Paste your collected ids here
districts = {610: 'ariyalur', 730: 'chengalpattu', 568: 'chennai', 569: 'coimbatore', 570: 'cuddalore', 571: 'dharmapuri', 572: 'dindigul', 573: 'erode', 729: 'kallakurichi', 574: 'kanchipuram', 575: 'kanniyakumari', 576: 'karur', 577: 'krishnagiri', 578: 'madurai', 735: 'mayiladuthurai', 579: 'nagapattinam', 580: 'namakkal', 581: 'perambalur', 582: 'pudukottai', 583: 'ramanathapuram', 731: 'ranipet', 584: 'salem', 585: 'sivaganga', 733: 'tenkasi', 586: 'thanjavur', 588: 'theni', 587: 'the nilgiris', 589: 'thiruvallur', 590: 'thiruvarur', 591: 'tiruchirappalli', 592: 'tirunelveli', 732: 'tirupathur', 634: 'tiruppur', 593: 'tiruvannamalai', 594: 'tuticorin', 595: 'vellore', 596: 'villupuram', 597: 'virudhunagar'}


base_url = "https://tnagriculture.in/mannvalam/districsoils/{}"
data = []

for d_id, name in districts.items():
    url = base_url.format(d_id)
    resp = requests.get(url)
    
    if resp.status_code == 200:
        json_data = resp.json()
        if json_data:
            row = json_data[0]
            row["district_id"] = d_id
            row["district_name"] = name
            data.append(row)
    else:
        print(f"Failed to fetch {name} (ID {d_id})")

# Write to CSV
if data:
    with open("tn_soil_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

print("✅ Done! Data saved to tn_soil_data.csv")
