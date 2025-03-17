import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
# %matplotlib inline

# 无视warning
import warnings
warnings.filterwarnings("ignore")

# 正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False


# 配置 tushare token
my_token = 'e6a69ed904ba43e987d13c7642d09bc75009090782142c0660415fe8'
pro = ts.pro_api(my_token)

def get_data(code, start_date, end_date):
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df.index = pd.to_datetime(df.trade_date)
    return df.close

# 以上证综指、贵州茅台、工商银行、中国平安为例
stocks={
    '600519.SH':'贵州茅台',
    '601398.SH':'工商银行',
    '601318.SH':'中国平安'
}

df = pd.DataFrame()
for code,name in stocks.items():
    df[name] = get_data(code, '20180101', '20221231')

# 按照日期正序
df = df.sort_index()
'''
# 本地读入沪深300合并
df_base = pd.read_csv('000300.XSHG_2018_2022.csv')
df_base.index = pd.to_datetime(df_base.trade_date)
df['沪深300'] = df_base['close']

'''
# 以第一交易日2018年1月1日收盘价为基点，计算净值并绘制净值曲线
df_worth = df / df.iloc[0]
df_worth.plot(figsize=(15,6))
plt.title('股价净值走势', fontsize=10)
plt.xticks(pd.date_range('20180101','20221231',freq='Y'),fontsize=10)
plt.show()


# 区间累计收益率(绝对收益率)
total_return = df_worth.iloc[-1]-1
total_return = pd.DataFrame(total_return.values,columns=['累计收益率'],index=total_return.index)
print(total_return)


# 年化收益率
annual_return = pd.DataFrame((1 + total_return.values) ** (252 / 1826) - 1,columns=['年化收益率'],index=total_return.index)
print(annual_return)

import numpy as np
import matplotlib.pyplot as plt

# 创建角度数据
angles = np.linspace(0, 2 * np.pi, 360)
# 计算正弦值
sine_values = np.sin(angles)

# 绘制四个部分的正弦图像
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
for i, ax in enumerate(axs.flatten()):
    start_idx = i * 90
    end_idx = (i + 1) * 90
    ax.plot(angles[start_idx:end_idx], sine_values[start_idx:end_idx])
    ax.set_title(f'Section {i+1}')
plt.show()