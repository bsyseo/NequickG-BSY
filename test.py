import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from NequickG import NEQTime, Position, GalileoBroadcast
from NequickG_global import NequickG_global

# 1. 설정
month, utc = 3, 3
a0, a1, a2 = 236.832, -0.394, 0.0040
TX = NEQTime(month, utc)
BX = GalileoBroadcast(a0, a1, a2)

# 2. 격자 생성 (위도/경도)
lats = np.linspace(33, 39, 50)
lons = np.linspace(124, 131, 70)
LAT, LON = np.meshgrid(lats, lons)

vtec_map = np.zeros_like(LAT)

# 3. VTEC 계산
for i in range(LAT.shape[0]):
    for j in range(LAT.shape[1]):
        RX = Position(LAT[i, j], LON[i, j])
        model = NequickG_global(TX, BX)
        NEQ, _ = model.get_Nequick_local(RX)
        vtec_map[i, j] = NEQ.vTEC(100, 2000)

# 4. 지도 시각화
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([124, 131, 33, 39], crs=ccrs.PlateCarree())

# VTEC 맵
cp = ax.contourf(LON, LAT, vtec_map, 60, transform=ccrs.PlateCarree(), cmap='jet')
cbar = plt.colorbar(cp, orientation='vertical', pad=0.02, aspect=30)
cbar.set_label("TECU")

# 지도 요소 추가
ax.coastlines(resolution='10m', color='black', linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='white')

plt.title(f"Korea Ionospheric TEC Map (2025-{month:02d}-23 {utc:02d}:00 UTC)")
plt.grid(True)
plt.savefig("korea_tec_map_cartopy.png")
print("✅ 저장 완료: korea_tec_map_cartopy.png")
