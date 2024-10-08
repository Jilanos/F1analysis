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
import math
current_directory = os.getcwd()
cache_directory = os.path.join(current_directory, '_cache')
plots_directory = os.path.join(current_directory, '_plots')
fastf1.Cache.enable_cache(cache_directory)

def path(path):
    if not os.path.isdir(path): # check if folder exists, otherwise create it
        os.mkdir(path)
        
def nanIsaccurate(session, num):
    act_lapp = session.laps.loc[session.laps["DriverNumber"]==num,"LapTime"]
    act_corr = session.laps.loc[session.laps["DriverNumber"]==num,"IsAccurate"]
    out = []
    for timelap, accur in zip(act_lapp,act_corr):
        if accur:
            out.append(pd.Timedelta.total_seconds(timelap))
        else:
            out.append(float("nan"))
    return out

def adefinir(session, drivers_num):
    val = {}
    for num in drivers_num :
        val[num] = []
    max_lap = int(np.max(session.laps["LapNumber"]))
    for n_laps in range(1,max_lap+1):
        act_lapp = session.laps.loc[session.laps["LapNumber"]==n_laps,["LapStartTime","DriverNumber"]]
        fastest = np.min(act_lapp["LapStartTime"])
        for sta_time, numb in zip(act_lapp['LapStartTime'], act_lapp['DriverNumber']):
            val[numb].append(sta_time-fastest)
    act_lapp = session.laps.loc[session.laps["LapNumber"]==n_laps,["LapTime", "LapStartTime", "DriverNumber"]]
    act_lapp["LapEndTime"] = act_lapp["LapStartTime"]+act_lapp["LapTime"]
    fastest = np.min(act_lapp["LapEndTime"])
    for sta_time, numb in zip(act_lapp['LapEndTime'], act_lapp['DriverNumber']):
        val[numb].append(sta_time-fastest)
    return val  


     
def min_pos(array):
    n=len(array)
    maxi,Imaxi = array[0],0
    for i in range(n):
        elt = array[i]
        if elt<maxi:
            maxi,Imaxi=elt,i
    return maxi,Imaxi 

for num_gp in range(5,17) : 

    try :
        session = fastf1.get_session(2024, num_gp, 'R')
        session.load()
        nom = session.event["EventName"]
        
        plots_directory_g = plots_directory+"\\"+nom+"\\"
        path(plots_directory_g)
        session.load()
        print(session.laps.columns)
        #print(session.laps.loc[session.laps["DriverNumber"]=="1",["DriverNumber","LapTime"]])
        print(session.laps.loc[session.laps["DriverNumber"]=="1","LapTime"])
        print(session.laps.loc[session.laps["DriverNumber"]=="1",["LapTime","LapStartTime", "LapNumber"]])
        
        #%%
        drivers_num = pd.unique(session.laps['DriverNumber'])
        drivers_name = pd.unique(session.laps['Driver'])
        list_fastest_laps = list()
        for drv in drivers_num:
            drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        team_colors = list()
        markers = list()
        line_style = list()
        team_reach = list()
        for index, lap in enumerate(list_fastest_laps):
            if type(lap["DriverNumber"]) == str :
                team_reach.append(lap['Team'])
                if team_reach.count(lap['Team'])==1:
                    markers.append('o')
                    line_style.append('-')
                else :
                    markers.append('^')
                    line_style.append('dotted')
                color = fastf1.plotting.team_color(lap['Team'])
                if color != "#ffffff":
                    team_colors.append(color)
                else : 
                    team_colors.append("#d9ca82")
        #%%
        plt.figure(figsize = (20,10))
        for ind, color, num ,name, marker in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers):
            plt.plot(nanIsaccurate(session,num),c = color, label = name,linestyle='--',marker=marker ,markersize=7, )
        
        plt.title("Driver laptime",fontsize=30, fontweight = 'bold')
        plt.xlabel("Laps",fontsize=20)
        plt.ylabel("Time (s)",fontsize=20)
        plt.grid(True)
        plt.legend()
        plt.savefig(plots_directory_g + "\\lap_time.png",bbox_inches='tight')
        plt.close("all")
        #%%
        look = ['PER', 'VER', 'ALO', 'HAM', 'GAS', 'STR']
        plt.figure(figsize = (20,10))
        for ind, color, num ,name, marker in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers):
            if name in look :
                plt.plot(nanIsaccurate(session,num),c = color, label = name,linestyle='--',marker=marker ,markersize=7, )
        
        plt.title("Driver laptime",fontsize=30, fontweight = 'bold')
        plt.xlabel("Laps",fontsize=20)
        plt.ylabel("Time (s)",fontsize=20)
        plt.grid(True)
        plt.legend()
        plt.savefig(plots_directory_g + "\\lap_time_few.png",bbox_inches='tight')
        plt.close("all")
        
        #%% plot position graph
        
        
        fig = plt.figure(figsize =(20,10))
          
        ax =plt.Subplot(fig, 111)
        fig.add_subplot(ax)
        val = adefinir(session, drivers_num)
        for ind, color, num ,name, marker, time in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers, val.values()):
            if name in look :    
                plt.plot([elt.total_seconds() for elt in time],c = color, label = name,linestyle='--',marker=marker ,markersize=7, )
        
        ax.invert_yaxis()
        plt.title("Time delta to the leader",fontsize=30, fontweight = 'bold')
        plt.xlabel("Laps",fontsize=20)
        plt.ylabel("Time (s)",fontsize=20)
        plt.grid(True)
        plt.legend()
        plt.savefig(plots_directory_g + "\\delta_leader_few.png",bbox_inches='tight')
        plt.close("all") 
        
        
        fig = plt.figure(figsize =(20,10))
          
        ax =plt.Subplot(fig, 111)
        fig.add_subplot(ax)
        for ind, color, num ,name, marker, time in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, markers, val.values()):
            plt.plot([elt.total_seconds() for elt in time],c = color, label = name,linestyle='--',marker=marker ,markersize=7, )
        ax.invert_yaxis()
        plt.title("Time delta to the leader",fontsize=30, fontweight = 'bold')
        plt.xlabel("Laps",fontsize=20)
        plt.ylabel("Time (s)",fontsize=20)
        plt.grid(True)
        plt.legend()
        plt.savefig(plots_directory_g + "\\delta_leader.png",bbox_inches='tight')
        plt.close("all") 
        
        #%% Grid Position movement
        max_lap = int(np.max(session.laps["LapNumber"]))
        timing = np.empty((20,max_lap))
        timing[:] = np.nan   
        for key, value in val.items():
            pos_driver = np.where(np.array(drivers_num) == key)
            for i, elt in enumerate(value[1:]):
                timing[pos_driver, i] = elt.total_seconds()
        
        
        position = np.empty((20,max_lap))
        position[:] = np.nan  
        abandon = 0
        new_ab= False
        for n_laps in range(max_lap):
            j = 0
            while j< 20-abandon :
                mini= np.nanmin(timing[:,n_laps])
                pos_min = np.where(timing[:,n_laps] == mini)
                if mini != 99999e30:
                    position[pos_min, n_laps] = j+1
                    timing[pos_min,n_laps] = 99999e30
                else :
                    abandon +=20-abandon-1-j
                    new_ab = True
                j+=1
            if new_ab:
                for i in range(19,-1,-1):
                    if np.isnan(timing[i,n_laps]):
                        position[i, n_laps:]=np.ones((1,max_lap-n_laps))*(20-abandon)
                        timing[i, n_laps:]=np.ones((1,max_lap-n_laps))*99999e30
                new_ab=False
        
                
                
        fig = plt.figure(figsize =(20,10))
        ax = plt.Subplot(fig, 111)
        for ind, color, num ,name, marker, time in zip(np.arange(len(drivers_num)), team_colors, drivers_num, drivers_name, line_style, val.values()):
            plt.plot(position[ind],c = color, label = name,linestyle = marker, linewidth=6 )
        plt.title("Driver position",fontsize=30, fontweight = 'bold')
        plt.xlabel("Laps",fontsize=20)
        plt.ylabel("Position",fontsize=20)
        plt.grid(True)
        plt.xlim([0,max_lap+4])
        plt.ylim([20.25, 0.75])
        plt.legend()
        plt.savefig(plots_directory_g + "\\position.png",bbox_inches='tight')
        plt.close("all")          
    except :
        print("\n\nGP : " + str(num_gp) + " failed\n\n")
        
            
        
        
        
        
