# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:13:36 2021

@author: Administrator
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, shape

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False

def select_data(target_city, time_period):
    path_body = '交通态势\\处理后\\'
    path_head = 'E:\\1 - git\\traffic-status\\原始数据\\0 - 长三角\\'
    path_tail = '.xlsx'
    path = path_head + target_city[:-1] + path_body + time_period + path_tail
    try:
        df_traffic = pd.read_excel(path)
        # 获取交通态势
    except Exception as err:
        df_traffic = None
        print(err)
        print('数据暂缺')
    CN_city_shp = gpd.read_file(r'E:\1 - git\traffic-status\原始数据\市.shp').to_crs("EPSG:4326")
    #中国城市的行政边界
    ad_target_city = CN_city_shp[CN_city_shp['市'] == target_city]
    save_path = r'C:\Users\Administrator\Desktop' + '\\' + target_city + '_' + time_period + '.png'
    return df_traffic, ad_target_city, save_path

def draw_traffic_status(df_traffic, ad_target_city, save_path):
    fig, ax0 = plt.subplots(figsize = (12,12))
    ax1 = ad_target_city.plot(ax = ax0, color='#D9D9D9', linewidth=0.5, edgecolor='w')
    # 绘制相应市级的行政边界
    
    geometry = [Point(xy) for xy in zip(df_traffic.lon, df_traffic.lat)]
    traffic_pt_shp = gpd.GeoDataFrame(df_traffic, geometry = geometry, crs='EPSG:4326')
    # 从交通态势excel中生成点状shp
    df_traffic_ln = pd.DataFrame(df_traffic.groupby(['roadID'])['geometry'].apply(lambda x: LineString(x.tolist())))
    # 对点状shp按照roadID进行归类，并将同一roadID的点状xy坐标连成线
    df_speed = df_traffic.groupby(['roadID'])['speed']
    speed_list = []
    for i in range(len(df_traffic.groupby(['roadID'])['speed'].unique())):
        speed_list.append(df_traffic.groupby(['roadID'])['speed'].unique()[i][0])
    # 将各条路段平均车速speed的唯一值存储在speed_list中
    df_traffic_ln['speed'] = speed_list
    # 将各路段平均车速添加到要连成pl shp的dataframe中
    colors = ['#da9694','#fabf8f','#ffff99','#c4d79b','#95b3d7'][::-1]
    speed_threshold = [0,10,25,40,60,1000][::-1]
    widths = [4,3,2,1,0.5][::-1]
    for i in range(5):
        traffic_pl_name = 'traffic1_pl_shp' + str(i)
        locals()[traffic_pl_name] = gpd.GeoDataFrame(df_traffic_ln[(df_traffic_ln['speed']>speed_threshold[i+1])&(df_traffic_ln['speed']<=speed_threshold[i])], geometry = 'geometry')
        # 根据不同车速生成线状shp
        ax2 = locals()[traffic_pl_name].plot(ax = ax0, color = colors[i], linewidth = widths[i])
    plt.axis('off')  
    plt.savefig(save_path, dpi = 300)  
    plt.show()

if __name__ == '__main__':
    while True:
        print('\n' + '常州市，杭州市，嘉兴市，金华市，南京市，宁波市，上海市，绍兴市，苏州市，温州市，无锡市')
        target_city = input('请从以上城市中选择一个输入' + '\n')
        time_period = input('请从 "早" "中" "晚" 中选择一个输入' + '\n')
        df_traffic, ad_target_city, save_path = select_data(target_city, time_period)
        try:
            draw_traffic_status(df_traffic, ad_target_city, save_path)
        except Exception as err:
            print(err)
            print('数据暂缺')




