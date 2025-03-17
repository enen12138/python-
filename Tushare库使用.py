
# tushare库使用，但是每小时最多访问该接口1次
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta

# 设置您的Tushare API Token
ts.set_token('e6a69ed904ba43e987d13c7642d09bc75009090782142c0660415fe8')
pro = ts.pro_api()
# 获取昨日时间
yesterday = datetime.now() - timedelta(days=1)

# 获取所用股票列表
stock_list = pro.stock_basic(exchanges=['sh', 'sz'], fields='ts_code', )

# 初始化空的DataFrame用于存储结果
result_df = pd.DataFrame()

# 遍历每一只股票
for index, row in stock_list.iterrows():
    ts_code = row['ts_code']

    # 获取该股票历史日线数据
    df = pro.daily(ts_code=ts_code, start_date=yesterday, end_date=yesterday)

    if not df.empty:
        df['ma'] = df['close'].rolling(window=20).mean()
        df['std'] = df['close'].rolling(window=20).std()
        df['upper'] = df['ma'] + 2 * df['std']
        df['lower'] = df['ma'] - 2 * df['std']

        if df.iloc[0]['close'] > df['close'].iloc[-1]:
            result_df = result_df.append(df)

print(result_df[['ts_code', 'trade_date', 'close', 'ma', 'std', 'upper', 'lower']])
#output_path = 'E:\python项目\Tushare_stock.xlsx'
#result_df.to_excel(output_path)





