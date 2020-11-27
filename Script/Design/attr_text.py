import random
import bisect
from typing import List
from Script.Core import (
    cache_contorl,
    constant,
    game_type,
)
from Script.Design import (
    handle_premise,
    map_handle
)
from Script.Config import game_config

cache:game_type.Cache = cache_contorl.cache
""" 游戏缓存数据 """

def get_random_name_for_sex(sex_grade: str) -> str:
    """
    按性别随机生成姓名
    Keyword arguments:
    sex_grade -- 性别
    """
    while 1:
        family_random = random.randint(1, cache.family_region_int_list[-1])
        family_region_index = bisect.bisect_left(cache.family_region_int_list, family_random)
        family_region = cache.family_region_int_list[family_region_index]
        family_name = cache.family_region_list[family_region]
        if sex_grade == "Man":
            sex_judge = 1
        elif sex_grade == "Woman":
            sex_judge = 0
        else:
            sex_judge = random.randint(0, 1)
        if sex_judge == 0:
            name_random = random.randint(1, cache.girls_region_int_list[-1])
            name_region_index = bisect.bisect_left(cache.girls_region_int_list, name_random)
            name_region = cache.girls_region_int_list[name_region_index]
            name = cache.girls_region_list[name_region]
        else:
            name_random = random.randint(1, cache.boys_region_int_list[-2])
            name_region_index = bisect.bisect_left(cache.boys_region_int_list, name_random)
            name_region = cache.boys_region_int_list[name_region_index]
            name = cache.boys_region_list[name_region]
        now_name = f"{family_name}{name}"
        if now_name not in cache.npc_name_data:
            cache.npc_name_data.add(now_name)
            return family_name + name


def get_stature_text(character_id: int) -> str:
    """
    按角色Id获取身材描述信息
    Keyword arguments:
    character_id -- 角色Id
    Return arguments:
    str -- 身材描述文本
    """
    descript_data = {}
    for descript in game_config.config_stature_description_text:
        descript_tem = game_config.config_stature_description_text[descript]
        now_weight = 0
        if descript in game_config.config_stature_description_premise_data:
            for premise in game_config.config_stature_description_premise_data[descript]:
                now_add_weight = handle_premise.handle_premise(premise, character_id)
                if now_add_weight:
                    now_weight += now_add_weight
                else:
                    now_weight = 0
                    break
        else:
            now_weight = 1
        if now_weight:
            descript_data.setdefault(now_weight, set())
            descript_data[now_weight].add(descript_tem.text)
    if len(descript_data):
        max_weight = max(descript_data.keys())
        return random.choice(list(descript_data[max_weight]))
    return ""

def get_scene_path_text(scene_path:List[str]) -> str:
    """
    从场景路径获取场景地址描述文本
    例:主教学楼-1F-101室
    Keyword arguments:
    scene_path -- 场景路径
    Return arguments:
    str -- 场景地址描述文本
    """
    map_list = map_handle.get_map_hierarchy_list_for_scene_path(scene_path,[])
    map_list.reverse()
    scene_path_str = map_handle.get_map_system_path_str_for_list(scene_path)
    scene_path_text = ""
    for now_map in map_list:
            now_map_map_system_str = map_handle.get_map_system_path_str_for_list(now_map)
            map_name = cache.map_data[now_map_map_system_str].map_name
            scene_path_text += map_name + "-"
    return scene_path_text + cache.scene_data[scene_path_str].scene_name
