import csv
import json


def convector(file_csv, file_json=None, model=None):

    with open(file_csv, encoding="utf-8") as file_c:
        result = []
        for row in csv.DictReader(file_c):
            del row["id"]

            if "location_id" in row:
                row["location"] = [int(row["location_id"])]
                del row["location_id"]

            if "is_published" in row:
                if row['is_published'] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False
            result.append({"model": model, "fields": row})

    with open(file_json, "w", encoding="utf-8") as file_j:
        file_j.write(json.dumps(result, ensure_ascii=False))


convector("ad.csv", "ad.json", "app.ad")
convector("category.csv", "category.json", "app.category")
convector("location.csv", "location.json", "users.location")
convector("user.csv", "user.json", "users.user")
