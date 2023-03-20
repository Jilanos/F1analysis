# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 09:07:24 2023

@author: PM263553
"""

import matplotlib.pyplot as plt
import random
import numpy as np 
import pandas as pd
import datetime
import os
import time
import sys
import fastf1
import fastf1.plotting
current_directory = os.getcwd()
cache_directory = os.path.join(current_directory, '_cache')
plots_directory = os.path.join(current_directory, '_plots')
fastf1.Cache.enable_cache(cache_directory)

def nanIsaccurate(laps, num):
    act_lapp = session.laps.loc[session.laps["DriverNumber"]==num,"LapTime"]
    act_corr = session.laps.loc[session.laps["DriverNumber"]==num,"IsAccurate"]
    out = []
    for timelap, accur in zip(act_lapp,act_corr):
        if accur:
            out.append(pd.Timedelta.total_seconds(timelap))
        else:
            out.append(float("nan"))
    return out

session = fastf1.get_session(2023, 2, 'R')
session.load()


print(session.laps.columns)
#print(session.laps.loc[session.laps["DriverNumber"]=="1",["DriverNumber","LapTime"]])
print(session.laps.loc[session.laps["DriverNumber"]=="1","LapTime"])
print(session.laps.loc[session.laps["DriverNumber"]=="1",["LapTime","IsAccurate", "TyreLife"]])

#%%
ver_lapp = session.laps.loc[session.laps["DriverNumber"]=="1","LapTime"]
ver_lapp_2 = ver_lapp[session.laps["IsAccurate"]]
print(ver_lapp_2)
plt.plot(np.arange(len(ver_lapp_2)),ver_lapp_2)


#%%
drivers_num = pd.unique(session.laps['DriverNumber'])
drivers_name = pd.unique(session.laps['Driver'])
list_fastest_laps = list()
for drv in drivers_num:
    drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
    list_fastest_laps.append(drvs_fastest_lap)
team_colors = list()
markers = list()
team_reach = list()
for index, lap in enumerate(list_fastest_laps):
    team_reach.append(lap['Team'])
    if team_reach.count(lap['Team'])==1:
        markers.append('o')
    else :
        markers.append('^')
    color = fastf1.plotting.team_color(lap['Team'])
    if color != "#ffffff":
        team_colors.append(color)
    else : 
        team_colors.append("#d9ca82")
print(team_reach)
#%%
plt.figure(figsize = (20,10))
for ind, color, num ,name, marker in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers):
    plt.plot(nanIsaccurate(session.laps,num),c = color, label = name,linestyle='--',marker=marker ,markersize=7, )

plt.title("Driver laptime",fontsize=30, fontweight = 'bold')
plt.xlabel("Laps",fontsize=20)
plt.ylabel("Time (s)",fontsize=20)
plt.grid(True)
plt.legend()
plt.savefig(plots_directory + "\\lap_time.png",bbox_inches='tight')
plt.close("all")
#%%
look = ['PER', 'VER', 'ALO', 'HAM', 'LEC']
plt.figure(figsize = (20,10))
for ind, color, num ,name, marker in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers):
    if name in look :
        plt.plot(nanIsaccurate(session.laps,num),c = color, label = name,linestyle='--',marker=marker ,markersize=7, )

plt.title("Driver laptime",fontsize=30, fontweight = 'bold')
plt.xlabel("Laps",fontsize=20)
plt.ylabel("Time (s)",fontsize=20)
plt.grid(True)
plt.legend()
plt.savefig(plots_directory + "\\lap_time_few.png",bbox_inches='tight')
plt.close("all")

    