def min_sec(str_min, quarter):
    if len(str_min.split(':')) > 1:
        str_sec = float(str_min.split(':')[0]) * 60 + int(str_min.split(':')[1])
    else:
        str_sec = float(str_min)
    final_sec = quarter * 720 - str_sec
    return final_sec


from requests_html import HTMLSession
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
session = HTMLSession()
# # ==================nba官方網站================
# response = session.get('https://www.nbastuffer.com/2017-2018-nba-player-stats/')

# elements = response.html.find('.row-hover row-5 column-2')
# element_name = response.html.find('.column-2')
# element_team = response.html.find('.column-3')
# element_age = response.html.find('.column-5')
# element_MPG = response.html.find('.column-7')
# element_score = response.html.find('.column-19')
# element_assist = response.html.find('.column-23')

# name = []
# age = []
# MPG = []
# score = []
# ass = []
# for i in range( 0, 210):
#     if element_name[i].text != 'FULL NAME':
#         # print( i, element_name[i].text, element_team[i].text, float(element_score[i].text), sep='\t')
#         name.append ( element_name[i].text )
#         age.append ( int(element_age[i].text ))
#         MPG.append ( float(element_MPG[i].text ))
#         score.append ( float(element_score[i].text ))
#         ass.append ( float(element_assist[i].text ))

#==================espn官方網站================
'''
======================SETTING============================
'''
team = 'gs/'
seasontype = 'seasontype/'
year = 'year/2018/'
response_game_id = session.get('http://www.espn.com/nba/team/schedule/_/name/'+ team + year + seasontype)
element_game_id = response_game_id.html.find('.score a')
game_id = ['401034613']
# for element_id in element_game_id:
#     gameid = element_id.attrs['href'].split('/')
#     game_id.append(gameid[len(gameid)-1])

for g_id in game_id:
    print(g_id)
    response_espn = session.get('http://www.espn.com/nba/playbyplay?gameId='+g_id)

    element_espn_team_away_palyer = response_espn.html.find('select [data-homeaway = away]')
    element_espn_team_home_palyer = response_espn.html.find('select [data-homeaway = home]')
    element_espn_combined_score = response_espn.html.find('.combined-score')
    # element_espn_gamedetails = response_espn.html.find('#gp-quarter-2 .game-details')
    element_espn_gamedetails = response_espn.html.find('.game-details')
    element_espn_time = response_espn.html.find('.time-stamp')
    element_espn_logo = response_espn.html.find('.team-logo')

    # box_cle = {'Kevin Love', [pt, 2pthit, 2pttry, 3pthit, 3pttry, freehit, freetry]}
    box_away = {}
    box_home = {}
    # =======================make box==================================
    for player in element_espn_team_away_palyer:
        box_away[player.text] = [0, 0, 0, 0, 0, 0, 0]
        play = str(player.text)
        if play.split()[0].isupper():
            box_away[play.split()[0][0]+'.'+play.split()[0][1]+'. '+play.split()[1]] = [0, 0, 0, 0, 0, 0, 0]
    for player in element_espn_team_home_palyer:
        box_home[player.text] = [0, 0, 0, 0, 0, 0, 0]
        play = str(player.text)
        if play.split()[0].isupper():
            box_home[play.split()[0][0]+'.'+play.split()[0][1]+'. '+play.split()[1]] = [0, 0, 0, 0, 0, 0, 0]
    # ===================drawing parameters==============================
    time_sec_away = [0]
    time_sec_home = [0]
    points_away = [0]
    points_home = [0]
    quarter = 1
    three_point_time = []
    three_point_score = []
    # ===================start to calculate==============================
    for i in range(0, len(element_espn_gamedetails)-3):
        detail = element_espn_gamedetails[i].text.split()
        # if 'Bogut' in detail and 'makes' in detail:
        # print(element_espn_time[i].text, element_espn_gamedetails[i+1].text, sep = '\t')
        #   control quarter's number
        if 'End' in detail:
            quarter = quarter + 1
            # print(quarter)
        
        #   judge the player's name
        if 'make' in detail or 'makes' in detail or 'made' in detail:
            if detail[1] == 'makes' or detail[1] == 'make' or detail[1] == 'made':
                player_name = detail[0]
            elif detail[2] == 'makes' or detail[2] == 'make' or detail[2] == 'made':
                player_name = detail[0] + ' ' + detail[1]
            elif detail[3] == 'makes' or detail[3] == 'make' or detail[3] == 'made':
                player_name = detail[0] + ' ' + detail[1] + ' ' + detail[2]
            #   judge which team the player belong to 
            if player_name in box_away :
                box = box_away
                points = points_away
                time = time_sec_away
            elif player_name in box_home:
                box = box_home
                points = points_home
                time = time_sec_home

            #   remind box
            if player_name not in box :
                # print('he is not here')
                box[player_name] = [0, 0, 0, 0, 0, 0, 0]
            #   judge which team the player belong to 
            if player_name in box_away :
                box = box_away
                points = points_away
                time = time_sec_away
            elif player_name in box_home:
                box = box_home
                points = points_home
                time = time_sec_home
            # start to calculate points
            box[player_name][0] += 2
            box[player_name][1] += 1                    
            box[player_name][2] += 1
            box['All Players'][0] += 2
            box['All Players'][1] += 1                    
            box['All Players'][2] += 1
            points.append(points[len(points)-1]+2)
            #   import time
            time.append(min_sec(element_espn_time[i].text, quarter))
            if 'three' in detail or 'Three' in detail:
                box[player_name][0] += 1
                box[player_name][1] -= 1                    
                box[player_name][2] -= 1
                box[player_name][3] += 1                    
                box[player_name][4] += 1
                box['All Players'][0] += 1
                box['All Players'][1] -= 1                    
                box['All Players'][2] -= 1
                box['All Players'][3] += 1                    
                box['All Players'][4] += 1
                points[len(points)-1] = points[len(points)-1] + 1
                three_point_score.append(points[len(points)-1] + 1)
                three_point_time.append(min_sec(element_espn_time[i].text, quarter))
            elif 'throw' in detail or 'Throw' in detail:
                box[player_name][0] -= 1
                box[player_name][1] -= 1                    
                box[player_name][2] -= 1
                box[player_name][5] += 1                    
                box[player_name][6] += 1
                box['All Players'][0] -= 1
                box['All Players'][1] -= 1                    
                box['All Players'][2] -= 1
                box['All Players'][5] += 1                    
                box['All Players'][6] += 1
                points[len(points)-1] = points[len(points)-1] - 1
        elif 'miss' in detail or 'misses' in detail or 'missed' in detail:
            if detail[1] == 'miss' or detail[1] == 'misses' or detail[1] == 'missed':
                player_name = detail[0]
            elif detail[2] == 'miss' or detail[2] == 'misses' or detail[2] == 'missed':
                player_name = detail[0] + ' ' + detail[1]
            elif detail[1] == 'miss' or detail[1] == 'misses' or detail[1] == 'missed':
                player_name = detail[0] + ' ' + detail[1] + ' ' + detail[2]

            #   judge which team the player belong to 
            if player_name in box_away :
                box = box_away
            elif player_name in box_home:
                box = box_home
            #   remind box
            if player_name not in box :
                # print('he is not here')
                box[player_name] = [0, 0, 0, 0, 0, 0, 0]
            # start to calculate points                 
            box[player_name][2] += 1                 
            box['All Players'][2] += 1
            if 'three' in detail or 'Three' in detail:             
                box[player_name][2] -= 1                  
                box[player_name][4] += 1                   
                box['All Players'][2] -= 1                 
                box['All Players'][4] += 1
            elif 'throw' in detail or 'Throw' in detail:                 
                box[player_name][2] -= 1                 
                box[player_name][6] += 1                 
                box['All Players'][2] -= 1               
                box['All Players'][6] += 1


    # pprint.pprint(box_away)
    # pprint.pprint(box_home)
    # print(quarter)
    # print(time_sec_away)
    # print(time_sec_home)
    # print(points_away)
    # print(points_home)


plt.style.use('seaborn-darkgrid')
plt.figure(figsize=(10, 6))
plt.plot(time_sec_home, points_home, color='gold', linewidth=2.0, linestyle=':')
plt.plot(time_sec_away, points_away, color='firebrick', linewidth=2.0)
plt.scatter(three_point_time, three_point_score, s=5, c='navy', marker='o')
plt.xlabel('Time (sec)')
plt.ylabel('Scores (points)')
plt.legend(["Golden State Warriors", "Cleveland Cavaliers"], loc=2)
plt.title('Game 1')
plt.show()
