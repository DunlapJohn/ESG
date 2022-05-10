import string
import numpy as np
import pandas as pd
import datetime as dt
import streamlit as st
import pandas_datareader as web



df1 = pd.read_csv('all_transactions.csv', error_bad_lines=False)
df2 = pd.read_csv('2021-house-scorecard-grid-export.csv', error_bad_lines=False)
housestatus=df2['Lifetime Score'].mean()

esg=df2[['Member of Congress','Lifetime Score']]

df1.columns = df1.columns.str.replace('district', 'District')


    
st.header('The Relationship between Climate Conconsciousness and Trading Activity within the House')


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

black = df.loc[df['Black']==True]
green = df.loc[df['Green']==True]


green['disclosure_date'] = pd.to_datetime(green['disclosure_date']).dt.strftime('%m/%Y')
black['disclosure_date'] = pd.to_datetime(black['disclosure_date']).dt.strftime('%m/%Y')


green["date"] = pd.to_datetime(df["disclosure_date"])
black["date"] = pd.to_datetime(df["disclosure_date"])
green['Transactions'] = green['transaction_date']
black['Transactions'] = black['transaction_date']

green=green[['date', 'amount', 'Transactions', 'Member of Congress']]
black=black[['date', 'amount', 'Transactions', 'Member of Congress']]



g_count = green['Member of Congress'].nunique()
b_count = black['Member of Congress'].nunique()


black = black.groupby(['date'])['Transactions'].count()
green = green.groupby(['date'])['Transactions'].count()



st.subheader('Number of Trades within the Lowest ESG Quintile')
st.bar_chart(black)
black=black.cumsum().max()
b_avg=black/b_count

col1, col2,col3 = st.columns(3)
col1.metric(label='Number of Members', value =b_count )
col2.metric(label='Total Number of Trades', value =black )
col3.metric(label='Average Number of Trades', value =b_avg )





st.subheader('Number of Trades within the Highest ESG Quintile ')
st.bar_chart(green)
green=green.cumsum().max()

g_avg=green/g_count
g_avg=g_avg.round(2)

col1, col2,col3 = st.columns(3)
col1.metric(label='Number of Members', value =g_count )
col2.metric(label='Total Number of Trades', value =green )
col3.metric(label='Average Number of Trades', value =g_avg )




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
