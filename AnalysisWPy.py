import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)
    
    stock_data_specific = stock_data[stock_data['Date'] <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data['Date'] <= '2021-04-30']
    
    cleaned_revenue = revenue_data_specific['Revenue'].replace('[$,]', '', regex=True)
    revenue_data_specific['Revenue'] = pd.to_numeric(cleaned_revenue, errors='coerce')
    revenue_data_specific.dropna(subset=['Revenue'], inplace=True)
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific['Date']), y=stock_data_specific['Close'].astype(float), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific['Date']), y=revenue_data_specific['Revenue'], name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )
    
    fig.show()

tsla = yf.Ticker("TSLA")
historical_data = tsla.history(period="max")
print(historical_data)
tsla_data = pd.DataFrame(historical_data)
tsla_data.reset_index(inplace=True)
print(tsla_data.head())

tsla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
data = requests.get(tsla_url).text
soup = BeautifulSoup(data, 'xml')

tsla_dict = {}
tsla_dict["Date"]=[]
tsla_dict["Revenue"]=[]

table = soup.select("table")[1]
rows = table.select("tbody > tr")
for row in rows:
    col = row.find_all("td")
    if len(col) >= 2:
        tsla_date = col[0].text
        tsla_revenue_ = col[1].text
        tsla_dict["Date"].append(tsla_date)
        tsla_dict["Revenue"].append(tsla_revenue_)
tsla_revenue = pd.DataFrame(tsla_dict)
print(tsla_revenue.head())
tsla_revenue["Revenue"] = tsla_revenue['Revenue'].str.replace(',|\$',"")
tsla_revenue.dropna(inplace=True)

tsla_revenue = tsla_revenue[tsla_revenue['Revenue'] != ""]
print(tsla_revenue.head())

gamestop = yf.Ticker("GME")
historical_data_g = gamestop.history(period="max")

print(historical_data)
gme_data = pd.DataFrame(historical_data)
gme_data.reset_index(inplace=True)
print(gme_data.head())

gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
data_1 = requests.get(gme_url).text
soup_1 = BeautifulSoup(data_1, "html.parser")

gme_dict = {}
gme_dict["Date"] = []
gme_dict["Revenue"] = []

table_1 = soup_1.select("table")[1]
rows_1 = table_1.select("tbody > tr")

for row_1 in rows_1:
    col_1 = row_1.find_all("td")
    gme_date = col_1[0].text
    gme_revenue_ = col_1[1].text
    gme_dict["Date"].append(gme_date)
    gme_dict["Revenue"].append(gme_revenue_)

print(gme_dict)
gme_revenue = pd.DataFrame(gme_dict)
print(gme_revenue.head())
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(gme_revenue.head())

make_graph(tsla_data, tsla_revenue, 'Tesla Stock Data Graph')
make_graph(gme_data, gme_revenue, 'GameStop Stock Data Graph')