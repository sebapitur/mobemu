import pandas as pd

df = pd.read_csv('C:\\Users\\seba_\\mobemu\\traces\\upb2011\\upb2011.dat', delim_whitespace=True)
df.to_csv('C:\\Users\\seba_\\mobemu\\traces\\upb2011\\upb2011.csv')