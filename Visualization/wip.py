
# def confusion_matrix(): # compare two datasets at a time
#   df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '1' order by date")
#   # generate random values for truth
#   truth = pd.DataFrame(np.random.randint(0,3,size=(len(df)+4)), columns=['Truth'])
#   df['Truth'] = truth
#   buyVal = []
#   buy = df[['Choice', 'Truth']][df['Choice'] == '1']
#   sell = df[['Choice', 'Truth']][df['Choice'] == '2']
#   hold = df[['Choice', 'Truth']][df['Choice'] == '0']
#   # buy = buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count()
#   # sell = sell['Choice'][sell['Choice'].astype(int) == sell['Truth'].astype(int)].count()
#   # hold = hold['Choice'][hold['Choice'].astype(int) == hold['Truth'].astype(int)].count()

#   # fig = go.Figure(data=go.Heatmap(labels=dict(x="What Should have Happened", y="What Algo DId", color="Viridis"),
#   #                  z=[[int(buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count()), int(buy['Choice'][buy['Choice'].astype(int) == buy[buy['Truth'] == '2'].astype(int)].count()), int(buy['Choice'][buy['Choice'].astype(int) == buy[buy['Truth'] == '0'].astype(int)].count())],
#   #                     [sell['Choice'][sell['Choice'].astype(int) == sell[sell['Truth']=='1'].astype(int)].count(), sell['Choice'][sell['Choice'].astype(int) == sell['Truth'].astype(int)].count(), sell['Choice'][sell['Choice'].astype(int) == sell[sell['Truth']=='0'].astype(int)].count()],
#   #                     [hold['Choice'][hold['Choice'].astype(int) == hold[hold['Truth']=='1'].astype(int)].count(), hold['Choice'][hold['Choice'].astype(int) == hold[hold['Truth']=='2'].astype(int)].count(), hold['Choice'][hold['Choice'].astype(int) == hold['Truth'].astype(int)].count()]],
#   #                  x=['Buy', 'Sell', 'Hold'],
#   #                  y=['Buy', 'Sell', 'Hold'],
#   #                  hoverongaps = False))
#   # fig.show()
#   print(buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count().iloc[0])