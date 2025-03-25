"""
Time and Solar activity fully defines a global Nequick model.
From the global model, Nequick processing parameters are computed at each geographical location.
This task visualises the spatial variation in each Nequick processing parameter.
Useful for understanding the physical meaning behind each processing parameter and as a debugging tool
"""
"""
전리층 모델 파라미터 시각화 (disturbance_flag 포함)
"""

import matplotlib.pyplot as plt
import numpy as np
from NequickG import NEQTime, Position, GalileoBroadcast
from NequickG_global import NequickG_global
from mpl_toolkits.basemap import Basemap
import os

def plotparameters(TX, BX, path):
    attrs = [
        'foF1', 'foF2', 'foE', 'M3000F2', 'NmF2', 'NmF1', 'NmE',
        'hmE', 'hmF1', 'hmF2', 'modip', 'Az', 'Azr',
        'solarsine', 'solarcosine', 'chi', 'chi_eff',
        'H0', 'B1bot', 'B1top', 'B2bot', 'BEtop', 'BEbot',
        'A1', 'A2', 'A3', 'k', 'vTEC', 'seasp',
        'disturbance_flag'  # 🔥 전리층 교란 표시 항목 추가
    ]

    NEQ_global = NequickG_global(TX, BX)

    # 전지구 맵 생성 (격자 해상도: 150x150)
    latlat, lonlon, outs = NEQ_global.map_parameters(attrs, -70, -180, 70, 180, resolution=150)

    for i in range(len(outs)):
        plt.figure(figsize=(12, 6))
        mapp = Basemap(projection='cyl', llcrnrlat=-90., urcrnrlat=90.,
                       llcrnrlon=-180., urcrnrlon=180., resolution='c')

        mapp.drawcoastlines()
        mapp.drawcountries()
        mapp.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 0], fontsize=10)
        mapp.drawmeridians(np.arange(-180., 181., 30.), labels=[0, 0, 0, 1], fontsize=10)

        xx, yy = mapp(lonlon, latlat)
        cs = mapp.contourf(xx, yy, outs[i], cmap='viridis')
        mapp.colorbar(cs)

        plt.title(attrs[i])

        os.makedirs(path, exist_ok=True)
        plt.savefig(os.path.join(path, f"{attrs[i]}.png"))
        plt.close()

# === 실행 예시 ===

solar = 'High'  # Low / Medium / High

if solar == 'Low':
    BX = GalileoBroadcast(2.580271, 0.127628236, 0.0252748384)
elif solar == 'Medium':
    BX = GalileoBroadcast(121.129893, 0.351254133, 0.0134635348)
elif solar == 'High':
    BX = GalileoBroadcast(236.831641, -0.39362878, 0.00402826613)
else:
    raise ValueError("solar 값은 Low, Medium 또는 High 중 하나여야 합니다.")

for time in [0, 4, 8, 12, 16, 20]:
    TX = NEQTime(4, time)
    output_path = os.path.join("maps", solar, str(time))
    plotparameters(TX, BX, output_path)
