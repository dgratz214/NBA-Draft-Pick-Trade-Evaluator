import csv
import scipy
import pandas
import numpy
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
# You may or may not want to use this package, or others like it
# this is just a starting point for you

# Read the player database into an array of dictionaries
players = []
with open('playerDB.csv', mode='r') as player_csv:
    player_reader = csv.DictReader(player_csv)
    line_count = 0
    for row in player_reader:
        players.append(dict(row))

# Read the draft database into an array of dictionaries
draftPicks = []
with open('draftDB.csv', mode='r') as draft_csv:
    draft_reader = csv.DictReader(draft_csv)
    line_count = 0
    for row in draft_reader:
        draftPicks.append(dict(row))
        
print(draftPicks[100][5])

# Get the draft picks to give/receive from the user
# You can assume that this input will be entered as expected
# DO NOT CHANGE THESE PROMPTS
print("\nSelect the picks to be traded away and the picks to be received in return.")
print("For each entry, provide 1 or more pick numbers from 1-60 as a comma-separated list.")
print("As an example, to trade the 1st, 3rd, and 25th pick you would enter: 1, 3, 25.\n")
give_str = input("Picks to give away: ")
receive_str = input("Picks to receive: ")

# Convert user input to an array of ints
give_picks = list(map(int, give_str.split(',')))
receive_picks = list(map(int, receive_str.split(',')))

# Success indicator that you will need to update based on your trade analysis
success = True



# YOUR SOLUTION GOES HERE
x = []
y = []

for i in range(len(draftPicks)):
    if int(draftPicks[i]['yearDraft']) >= 1979 and int(draftPicks[i]['yearDraft']) < 2018:
        pick_num = int(draftPicks[i]['numberPickOverall'])
        if pick_num > 0 and pick_num < 61 :
            player_url = draftPicks[i]['basketball_reference_url']
            if player_url != '':
                player_tag = player_url.split('/')[3][0:-5]
                total_WOR = 0
                plr_seasons = 0
                found = False
                for j in range(len(players)):
                    if player_tag == players[j]['urlID'] and plr_seasons < 4:
                        found = True
                        total_WOR += float(players[j]['VORP']) * 2.70
                        plr_seasons += 1
                if (found):
                    x.append(pick_num)
                    y.append(total_WOR)

# for i in range(len(x)):
#     print(str(x[i]) + ": " + str(y[i]))
x = numpy.array(x).reshape((-1, 1))
x = sm.add_constant(x)
y = numpy.array(y).reshape((-1,1))
scaler = MinMaxScaler(feature_range=(0, 1))
rescaledy = scaler.fit_transform(y)
print("max: " + str(max(rescaledy)))
print("min: " + str(min(rescaledy)))
# model = LinearRegression().fit(x, rescaledy)
model = sm.OLS(rescaledy, x)
results = model.fit()
print(results.summary())

# 
# intercept = model.intercept_
# slope = model.coef_[0]
# 
# print(model.score(x, rescaledy))
# print(intercept)
# print(slope)
# give_picks_val = 0
# for i in range(len(give_picks)):
#     give_picks_val += intercept + slope * give_picks[i]
# 
# receive_picks_val = 0    
# for i in range(len(receive_picks)):
#     receive_picks_val += intercept + slope * receive_picks[i]
# 
# print("give: " + str(give_picks_val))
# print("receive: " + str(receive_picks_val))
# if receive_picks_val <= give_picks_val:
#     success = False
# 
# 
# 
# # Print feeback on trade
# # DO NOT CHANGE THESE OUTPUT MESSAGES
# if success:
#     print("\nTrade result: Success! This trade receives more value than it gives away.\n")
#     # Print additional metrics/reasoning here
# else:
#     print("\nTrade result: Don't do it! This trade gives away more value than it receives.\n")
#     # Print additional metrics/reasoning here
