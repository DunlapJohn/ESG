import pandas as pd
import streamlit as st
import numpy as np

df1 = pd.read_csv('all_transactions.csv', error_bad_lines=False)
df2 = pd.read_csv('2021-house-scorecard-grid-export.csv', error_bad_lines=False)
housestatus=df2['Lifetime Score'].mean()

esg=df2[['Member of Congress','Lifetime Score']]

df1.columns = df1.columns.str.replace('district', 'District')


    
st.header('Climate Conconsciousness and Trading Activity in the House')


with st.expander('Why'):
    st.write(" The compliance enviromental commondities market will likely become a trillion dollar relatugated market within the next 50 years. \
        The relationship between climate focused Members and their portfolio could provide insights to their enviromental commitment. I beleived that US Representatives who voted consistently for\
             enviromental protection would have sustainable themed longterm portfolio holdings which were \
            grounded in ESG conviction. However, after combining the House's Envivromental Score-cards\
                and the Stock Watcher historical trading activity of representatives, data suggests \
             that the upper quintile of Climate/ESG rated Representatives traded in greater volume and \
            more frequently than the bottom quintile.  \
              While, much more could be research, it appears when their financial security is on the line, 'climate' Members do not rely on a long-term investment strategy."         
                )
with st.expander(' Methodology'):
    st.write(" The data from Stock Watchers aggergated trades excecuted on behlf of US Representatives. \
            The measurement of the total USD volume of trades was considered; however, the reporting criteria  \
                for trading activity requires equity positions must be reported within a speicifed USD range. \
                    In addition, many congressional members took positions on bothsides of in a particular \
                        equity market. Given that mambers only have to report within a broad range, their final position could range \
                        from a 400% increase to a complete exit, thus a total USD volume metric was deemed too noisy. Only \
                            total transactions were factored into analysis."
                )

df2['Black']= df2['Lifetime Score'] < 20
df2['Green'] = df2['Lifetime Score'] > 80
housestatus=housestatus.round(2)
st.subheader('Representative Lifetime ESG Score')
st.dataframe(esg) 

df = pd.merge(df2,df1,on='District')
df['sell'] = np.where(df['type']=='sale_full', 1, 0 )

black = df.loc[df['Black']==True]
green = df.loc[df['Green']==True]


green['disclosure_date'] = pd.to_datetime(green['disclosure_date']).dt.strftime('%m/%Y')
black['disclosure_date'] = pd.to_datetime(black['disclosure_date']).dt.strftime('%m/%Y')


green["date"] = pd.to_datetime(df["disclosure_date"])
black["date"] = pd.to_datetime(df["disclosure_date"])
green['Transaction'] = green['transaction_date']
black['Transaction'] = black['transaction_date']

# green=green[['date', 'amount', 'Transactions', 'Member of Congress']]
# black=black[['date', 'amount', 'Transactions', 'Member of Congress']]



g_count = green['Member of Congress'].nunique()
b_count = black['Member of Congress'].nunique()

black_sell = black.groupby(['date'])['sell'].sum()
black = black.groupby(['date'])['Transaction'].count()

green_sell = green.groupby(['date'])['sell'].sum()
green = green.groupby(['date'])['Transaction'].count()

black = pd.merge(black_sell, black, left_index=True, right_index=True)
black['buy'] = black['Transaction'] - black['sell']
black = black[['sell','buy']]
black['sell'] = black['sell'] * -1

green = pd.merge(green_sell, green, left_index=True, right_index=True)
green['buy'] = green['Transaction'] - green['sell']

green['sell'] = green['sell'] * -1


green= green[['sell','buy']]



st.subheader('Trading Activity within the Lowest ESG Quintile')
st.bar_chart(black)
black['total']=black['buy']+(black['sell']*-1)
black['total']=black['total'].cumsum()


b_avg=black['total'][-1]/b_count

col1, col2,col3 = st.columns(3)
col1.metric(label='Number of Members', value =b_count )
col2.metric(label='Total Number of Transactions', value=black['total'][-1] )
col3.metric(label='Average Number of Transactions', value =b_avg.round(2) )

black['buy']=black['buy'].cumsum()
black['sell']=black['sell'].cumsum()

col1, col2,col3 = st.columns(3)
col1.metric(label='Total Number of Buys', value =black['buy'][-1]  )
col2.metric(label='Total Number of Sells', value =(black['sell'][-1]*-1) )
col3.metric(label='Buy/Sell Ratio', value = (black['buy'][-1] / (black['sell'][-1]*-1 )).round(2) )





st.subheader('Trading Activity within the Highest ESG Quintile ')
st.bar_chart(green)
green['total']=green['buy']+(green['sell']*-1)
green['total']=green['total'].cumsum()


g_avg=green['total'][-1]/g_count
g_avg=g_avg.round(2)

col1, col2,col3 = st.columns(3)
col1.metric(label='Number of Members', value =g_count )
col2.metric(label='Total Number of Transactions', value =green['total'][-1] )
col3.metric(label='Average Number of Transactions', value =g_avg )
green['buy']=green['buy'].cumsum()
green['sell']=green['sell'].cumsum()

col1, col2,col3 = st.columns(3)
col1.metric(label='Total Number of Buys', value =green['buy'][-1]  )
col2.metric(label='Total Number of Sells', value =(green['sell'][-1]*-1) )
col3.metric(label='Buy/Sell Ratio', value = (green['buy'][-1] / (green['sell'][-1]*-1 )).round(2) )



with st.expander('Findings'):
    st.write(" Portfolio trading activity mirrors modern liberal and conservative tendencies. In addition, there was a distinct spike in trading activity at the begining of covid. \
            This uptick was most pronounced in the bottom Quintile, possibly indictating\
                conservatives serve as better signals for capital preservation oppertunities."
                )
with st.expander('Moving Forward'):
    st.write(" Further research should be done to investigate sector speific activity within these reported trades. \
            While many Members do not directly control their portfolio, they are still are still human. Cross-referencing these positions with committee hearings could provide unique insights.\
                "
                )
