import numpy as np
import pandas as pd
from numpy import dtype
import matplotlib.pyplot as plt
import random

position = 1
walk = [position]
steps = 1000

for i in range(steps):
    step = 1 if random.randint(0, 1) else 0
    position += step
    walk.append(position)

plt.plot(walk)
plt.show()

'''
# 获取当前日期以及10天前的日期
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=10)).strftime('%Y%m%d')  # 获取略多于10天的数据以确保数据完整性

# 获取所有A股列表
stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,market')

filtered_stocks = stock_list[(~stock_list['ts_code'].str.startswith('688')) & (stock_list['market'] != '北京证券交易所')]

print(filtered_stocks)

output_path = 'E:\python项目\stock.xlsx'
filtered_stocks.to_excel(output_path, index=False)

# 创建一个DataFrame来保存结果
results = pd.DataFrame(columns=['ts_code', 'name', 'ma5', 'ma10'])

for index, row in stock_list.iterrows():
    ts_code = row['ts_code']
    try:
        # 获取个股日线行情
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if not df.empty:
            # 计算5日和10日均线
            df['ma5'] = df['close'].rolling(window=5).mean()
            df['ma10'] = df['close'].rolling(window=10).mean()
            # 只保留最新一天的数据
            latest_data = df.iloc[-1]
            results = results.append({
                'ts_code': ts_code,
                'name': row['name'],
                'ma5': latest_data['ma5'],
                'ma10': latest_data['ma10']
            }, ignore_index=True)
    except Exception as e:
        print(f"处理 {ts_code} 时出错: {e}")
        continue

print(results)
'''







