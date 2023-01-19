import yfinance as yf
import matplotlib.pyplot as plt

def main():
    res_sp500 = yf.Ticker("^GSPC")
    res_jpy_usd = yf.Ticker("JPY=X")
    df_sp500 = res_sp500.history(period="max", interval="1mo", start="1997-1-1")
    df_jpy_usd = res_jpy_usd.history(period="max", interval="1mo", start="1997-1-1")
    print(df_sp500.head(10))

    # 日付情報/平均価格を付ける
    df_jpy_usd["Day"] = list(map(lambda x: f"{x.year}-{x.month}-{x.day}", df_jpy_usd.index))
    df_jpy_usd["Mean"] = (df_jpy_usd.High - df_jpy_usd.Low) / 2 + df_jpy_usd.Low

    # 日付の平均価格辞書を作成
    dollar_jpy = dict(zip(df_jpy_usd["Day"], df_jpy_usd["Mean"]))

    # S&P500を毎月定額買える金額だけ購入する
    yen_yosan = 50000
    accum_piece = 0
    accum_yosan_jpy = 0
    eval_value = []
    eval_yosan = []
    for idr, row in df_sp500.iterrows():
        value = row.Low + (row.Low - row.High) / 2
        day_str = f"{idr.year}-{idr.month}-{idr.day}"
        day_dollar = dollar_jpy[day_str]
        dollar_yosan = yen_yosan / day_dollar
        piece = dollar_yosan / value
        accum_piece += piece
        accum_yosan_jpy += yen_yosan
        eval_value.append(accum_piece * value * day_dollar)
        eval_yosan.append(accum_yosan_jpy)
        print(day_str)
        print(" ", value, piece, accum_piece, accum_yosan_jpy)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()
    ax.plot(df_sp500.index, df_sp500.High, marker="o", c="#e9002dff")
    plt.tight_layout()
    plt.savefig("sp500.png")
    plt.close()
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()
    ax.plot(df_sp500.index, eval_yosan, marker="o", c="#e9002dff", label="JPY")
    ax.plot(df_sp500.index, eval_value, marker="+", c="#ffaa00ff", label="SP500")
    plt.tight_layout()
    plt.legend()
    plt.savefig("sp500-jpy.png")
    plt.close()
    

if __name__ == '__main__':
    main()