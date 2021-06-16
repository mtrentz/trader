import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import time

if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()


first_start = datetime.today()
ativo = "LTCBTC"
ts = mt5.TIMEFRAME_M5
filename = "LTCBTC_M5"

df1 = pd.DataFrame(mt5.copy_rates_from(ativo, ts, first_start, 10000))
df1['time']=pd.to_datetime(df1['time'], unit='s')

dfs = []
dfs.append(df1.copy())

try:
    for i in range(50):
        # Pega a data mais antiga do dataframe, que vai ser a data de início do novo.
        new_start = df1.iloc[0]['time'].to_pydatetime()
        print(new_start)

        # Pega os dados a partir daquela data de início
        df2 = pd.DataFrame(mt5.copy_rates_from(ativo, ts, new_start, 10000))
        df2['time']=pd.to_datetime(df2['time'], unit='s')

        dfs.append(df2.copy())

        # Junta as duas dataframes, deixando a com dados mais antigos (df2) na frente
        # ou seja, linhas iniciais
        concat = pd.concat([df2, df1])
        
        # Passa essa dataframe junta para a df1 novamente
        df1 = concat.copy()

        # Espera um pouco para nao sobrecarregar o API (metatrader)
        time.sleep(.3)
        print(i+1)

except Exception as e:
    print("FODEO")
    print(e)
    mt5.shutdown()
    df1.to_csv(f'{filename}_ERROR.csv', index=False)


# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# Remove as linhas totalmente duplicadas (ele nao obedece bem o datetime q passei)
df1 = df1.drop_duplicates()

df1.to_csv(f'{filename}.csv', index=False)

