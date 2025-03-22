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


# 初始化一个列表用于存储结果
result_list = []
code_list = []

# 遍历情况
for index, row in stock_info_filtered.iterrows():
    code = row['code']

    # 排除以688开头的股票
    if code.startswith('688'):
        continue  # 跳过以688开头的股票

    rs = bs.query_history_k_data_plus(code, "code,close,open", start_date=s_date, end_date=e_date, frequency="d",
                                      adjustflag="3")
    df = rs.get_data()

    # 判断DataFrame是不是空的，并且没有空值
    if not df.empty and not df.isna().any().any():
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)

        # 计算20日简单移动平均线（SMA）作为布林线中轨
        df['ma'] = df['close'].rolling(window=20).mean().round(2)
        df['std'] = df['close'].rolling(window=20).std()
        df['upper_band'] = df['ma'] + 2 * df['std']
        df['lower_band'] = df['ma'] - 2 * df['std']

        # 获取最后一天的数据
        last_day_data = df.iloc[-1]

        # 获取最后一天的详细信息
        day_date = bs.query_history_k_data_plus(code, "open,close,high,low", start_date=e_date, end_date=e_date,
                                                frequency="d", adjustflag="3").get_data()

        if not day_date.empty:
            day_low = float(day_date['low'].values[0])
            day_high = float(day_date['high'].values[0])
            day_open = float(day_date['open'].values[0])
            day_close = float(day_date['close'].values[0])

            # 判断是否突破中轨
            if day_low < last_day_data['ma'] < day_high and day_open < last_day_data['ma'] < day_close:
                code_list.append(code)
        else:
            print(f"无法获取 {code} 在 {e_date} 的详细数据")
    else:
        print(f"{code} 数据为空或包含空值")

# 进一步筛选非ST股
for code in code_list:
    ds = bs.query_history_k_data_plus(code, "code,volume,amount,turn,pbMRQ,isST", start_date=e_date, end_date=e_date,
                                      frequency="d", adjustflag="3").get_data()

    if not ds.empty:
        ds['isST'] = ds['isST'].astype(str)  # 确保isST是字符串类型
        ds['turn'] = ds['turn'].astype(str)
        if ds['isST'].values[0] != '1' and ds['turn'].values[0] > '0.1':
            result_list.append({
                'code': ds['code'].values[0],
                'volume': float(ds['volume'].values[0]),
                'amount': float(ds['amount'].values[0]),
                'turn': float(ds['turn'].values[0]),
                'pbMRQ': float(ds['pbMRQ'].values[0]),
                'isST': ds['isST'].values[0]
            })

# 注销登录
bs.logout()

# 将结果转换为DataFrame并保存为csv文件
if result_list:
    result_df = pd.DataFrame(result_list)
    formatted_date = e_date.replace('-', '')
    filename = 'stock_' + formatted_date + '.csv'
    result_df.to_csv(filename, index=False)
    print("数据已成功保存到'bollinger_breakout_baostock.csv'")
else:
    print("没有符合条件的数据")