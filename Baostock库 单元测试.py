import baostock as bs
import pandas as pd

# 登录baostock
lg = bs.login()

# 获取今天日期&20日之前的日期
today = pd.to_datetime('today').strftime('%Y-%m-%d')
start_date = (pd.to_datetime(today) - pd.Timedelta(days=28)).strftime('%Y-%m-%d')

# 获取市场所有股票的基本信息
stock_info = bs.query_stock_basic().get_data()

# 过滤出类型为股票（type == '1'）且上市状态（status == '1'）的记录
stock_info_code = stock_info[(stock_info['type'] == '1') & (stock_info['status'] == '1')]

# 初始化一个列表用于存储结果
result_list = []

# 遍历每一只股票
for index, row in stock_info_code.iterrows():
    code = row['code']

    # 获取该股票的历史日线数据（包括今日及过去28天）
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,close,turn,isST,trades",
                                      start_date=start_date, end_date=today,
                                      frequency="d", adjustflag="3")

    df = rs.get_data()
    if not df.empty:
        df['close'] = df['close'].astype(float)
        df['turn'] = df['turn'].astype(float)

        # 确保昨日的数据存在
        yesterday_df = df[df['date'] == today]
        if not yesterday_df.empty:
            yesterday_close = yesterday_df['close'].values[0]
            yesterday_turn = yesterday_df['turn'].values[0]
            yesterday_isST = yesterday_df['isST'].values[0] if 'isST' in yesterday_df.columns else None
            yesterday_trades = yesterday_df['trades'].values[0] if 'trades' in yesterday_df.columns else None

            # 计算20日简单移动平均线（SMA）作为布林线中轨
            ma_df = df.tail(20)  # 取最近20个交易日的数据
            ma = ma_df['close'].mean()  # 简单移动平均

            # 判断是否突破中轨且不是ST股
            if yesterday_close > ma and yesterday_isST != '1':
                result_list.append({
                    'code': code,
                    'date': today,
                    'close': yesterday_close,
                    'ma': ma,
                    'turn': yesterday_turn,
                    'isST': yesterday_isST,
                    'trades': yesterday_trades
                })

# 注销登录
bs.logout()

# 将结果转换为DataFrame并保存为csv文件
if result_list:
    result_df = pd.DataFrame(result_list)
    result_df.to_csv('bollinger_breakout_baostock.csv', index=False)
    print("数据已成功保存到'bollinger_breakout_baostock.csv'")
else:
    print("没有符合条件的数据")