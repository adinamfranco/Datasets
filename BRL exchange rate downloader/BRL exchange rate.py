import pandas as pd                    # for handling datasets
import requests as rq                  # for handling the BACEN URL
import io                              # for loading the dataset buffered in memory
from datetime import datetime as dt    # for manipulating the date column


# Manipulating the BACEN URL (date format dd/mm/yyyy)
tdy = dt.today().strftime('%d/%m/%Y')    # bring the date to the current day if needed
url_bc = 'https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVFechamentoMoedaNoPeriodo&ChkMoeda='
ini_date = '01/10/2019'
final_date = '05/10/2019'
currency = '61'    # The BACEN has an indexed list off the available curenccies, consult the index for more info
url_cplt = url_bc + currency + '&DATAINI=' + ini_date + '&DATAFIM=' + final_date    # use tdy or final_date

# loading the buffered dataset from the url
with rq.Session() as s:
    download = s.get(url_cplt)
    downloaded = download.content.decode('utf8')
df1 = pd.read_csv(io.StringIO(downloaded), delimiter=';', thousands='.', header=None)

# showing the raw dataset
print(df1)
#         0    1  2    3       4       5       6       7
#0  1102019  220  A  USD  4,1734  4,1740  1,0000  1,0000
#1  2102019  220  A  USD  4,1540  4,1546  1,0000  1,0000
#2  3102019  220  A  USD  4,1006  4,1012  1,0000  1,0000
#3  4102019  220  A  USD  4,0604  4,0610  1,0000  1,0000


# manipulating the dataframe
name = ['Data', 'A', 'B', 'Currency', 'BRL/Compra', 'BRL/Venda', 'US$/Compra', 'US$/Venda']    # new column names
df1.columns = name    # renaming the columns
df1 = df1.drop(['A', 'B'], axis=1)    # these columns are not useful
df1 = df1.drop(['US$/Compra', 'US$/Venda'], axis=1)    # only drop these columns if you are dealing with US$

# bringing the date to the Brazilian pattern
df1['Data'] = df1['Data'].astype(str)
df1['Data'] = df1['Data'].str[-4:] + '/' + df1['Data'].str[-6:-4] + '/' + df1['Data'].str[:-6]
df1['Data'] = pd.to_datetime(df1['Data'])
df1['Data'] = df1['Data'].dt.strftime('%d/%m/%Y')

# showing the cleaned dataframe
print(df1)
#         Data Ccurrency BRL/Compra BRL/Venda
#0  01/10/2019       USD     4,1734    4,1740
#1  02/10/2019       USD     4,1540    4,1546
#2  03/10/2019       USD     4,1006    4,1012
#3  04/10/2019       USD     4,0604    4,0610

