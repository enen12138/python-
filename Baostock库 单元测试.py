import baostock as bs
import pandas as pd


# 登录baostock
lg = bs.login()

# 获取日期
e_date = (pd.to_datetime('today') - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
s_date = (pd.to_datetime('today') - pd.Timedelta(days=28)).strftime('%Y-%m-%d')
# 获取市场符合条件股票的名称代码
stock_info = bs.query_stock_basic().get_data()
stock_info_filtered = stock_info[(stock_info['type'] == '1') & (stock_info['status'] == '1')]
print(stock_info_filtered)

# 初始化一个列表用于存储结果
result_list = []
result_fined = []
code_list = []

# 遍历情况
## iterrows() 主要用于需要逐行处理DataFrame的情况
for index,row in stock_info_filtered.iterrows():
    code = row['code']
    rs = bs.query_history_k_data_plus(code,"code,close,open",start_date=s_date,end_date=e_date,frequency="d",adjustflag="3")
    df = rs.get_data()
    # 判断DataFrame是不是空的,但是无法判断是否存在空值，可使用isna()
    if not df.isna().any().any():
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        # 计算20日简单移动平均线（SMA）作为布林线中轨
        ma_df = df['close'].rolling(window=20).mean()
        ma_std = df['close'].rolling(window=20).std()
        ma_up = ma_df + 2 * ma_std
        day_date = bs.query_history_k_data_plus(code,"open,close,high,low",start_date=e_date,end_date=e_date,frequency="d",adjustflag="3")
        if day_date['low'] < ma_df < day_date['high']:
            code_list.append(code)
    else:
        result_fined.append(code)
for code in code_list:
    ds = bs.query_history_k_data_plus(code,"code,volume,amount,turn,pbMRQ,isST").get_data()
    if ds["isST"] == 1:
        result_list.append({'code':ds["code"],'volume':ds["volume"],'amount':ds["amount"],'turn':ds["turn"],'pbMRQ':ds["turn"],'isST':ds["isST"]})

# 注销登录
bs.logout()

# 将结果转换为DataFrame并保存为csv文件
if result_list:
    result_df = pd.DataFrame(result_list)
    result_df.to_csv('bollinger_breakout_baostock.csv', index=False)
    print("数据已成功保存到'bollinger_breakout_baostock.csv'")
else:
    print("没有符合条件的数据")
