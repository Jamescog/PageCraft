import pandas as pd
import os
from data_access_layer.db import DataBaseManager as DB

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, "assets/csv/cleaned-data.csv")

db = DB()

df = pd.read_csv(file_path)

df = df.dropna()

# count = 0
# for index, row in df.iterrows():
#     try:
#         db.insert_one(
#             {
#                 "title": row["title"],
#                 "description": row["description"],
#                 "category": row["category"],
#                 "author": row["author"],
#                 "rating": row["rating"],
#                 "genre": row["top_genra"],
#                 "book_cover": row["book_cover"],
#                 "book_url": row["book_url"],
#             }
#         )
#         count += 1
#         print(count)
#     except Exception as e:
#         print(e)
#         break

print(db.get_one_by_id("656257fd4628b24f889210bc"))
