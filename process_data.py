import pandas as pd
from pathlib import Path

#path to data folder
data_path = Path("data")

#Read all csv files in the folder
dfs=[]
for file in data_path.glob("*.csv"):
    df=pd.read_csv(file)
    dfs.append(df)

#combine all files into one dataframe
combined_df=pd.concat(dfs, ignore_index=True)
combined_df.shape

#Keep only pink morsels
pink_df=combined_df[combined_df["product"]=="pink morsel"]
print(pink_df.dtypes)
#convert price: str -> float
pink_df["price"]=pink_df["price"].str.replace("$","",regex=False)
pink_df["price"]=pink_df["price"].astype(float)
print(pink_df.dtypes)

#Create sales column
pink_df["sales"]=pink_df["quantity"] * pink_df["price"]

#select required fields
final_df=pink_df[["sales","date","region"]]

#save output
final_df.to_csv(data_path/"formatted_output.csv", index=False)

print("formatted_output.csv created successfully...")