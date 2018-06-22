from Core import CacheContorl
from Design import MapHandle,GameTime
from Flow import InScene

# 主角移动
def playerMove(targetScene):
    playerPosition = CacheContorl.playObject['object']['0']['Position']
    mapId = MapHandle.getMapIdForScene(playerPosition)
    nowSceneId = MapHandle.getMapSceneIdForSceneId(mapId, playerPosition)
    if nowSceneId == targetScene:
        InScene.getInScene_func()
    else:
        pathData = MapHandle.getPathfinding(mapId,nowSceneId,targetScene)
        if pathData == 'End':
            InScene.getInScene_func()
        else:
            timeList = pathData['Time']
            pathList = pathData['Path']
            nowTargetScenePosition = MapHandle.getSceneIdForMapSceneId(mapId, pathList[1])
            MapHandle.playerMoveScene(playerPosition, nowTargetScenePosition, '0')
            GameTime.setSubMinute(timeList[1])
            playerMove(targetScene)