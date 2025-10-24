import pandas as pd
from tabulate import tabulate
dfBigmarket = pd.read_csv(f"Bigmarket.csv")
print(dfBigmarket)

def pp(toprint):
    return print(tabulate(toprint))

pp(dfBigmarket.head())
pp(dfBigmarket.tail())
print(dfBigmarket.shape)

# iloc

print("¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬")

# filtering
print(dfBigmarket[dfBigmarket.Sales > 4000])
print(dfBigmarket[(dfBigmarket.Sales > 4000) & (dfBigmarket.Month == 'May')])

print("¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬")
# ordering
print(dfBigmarket.sort_values('Sales', ascending=False))


print("¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬")
dict1 = {
    "Month":["jun", "jun", "jun", "jun", "jun"],
    "Store":["A", "B", "C", "D", "E"],
    "Sales":[101,200,256,300,250]}
newdata = pd.DataFrame(dict1)

newdf = pd.concat([dfBigmarket, newdata], ignore_index=True)

# renaming columns
newdf = newdf.rename(columns={'Store':'newstore'})
print(newdf.head)

# drop rows
newdf = newdf.drop([1])
print(newdf.head)

