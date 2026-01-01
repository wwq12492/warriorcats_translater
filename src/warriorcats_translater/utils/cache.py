'''
此模块用于读取、diff（删除多余和生成任务列表）translate_cache.json
'''
import json
import os

def load_cache() -> dict[str, dict[str, str]]: # 读取cache文件
    '''
    读取cache文件，返回{"hash":{"chapter":"content"}}格式的dict
    '''
    CWD: str = os.getcwd()
    try:
        with open(os.path.join(CWD, "translate_cache.json"),"r",encoding="utf-8") as f:
            cache_data: dict[str, dict[str, str]] = json.load(f)
            return cache_data
    except FileNotFoundError:
        print("[警告] cache文件未创建，已自动创建在当前目录下")
        with open(os.path.join(CWD, "translate_cache.json"),"w",encoding="utf-8") as f:
            json.dump({},f)
            return {}
    except json.JSONDecodeError as e:
        print(f"[错误] cache文件损坏，请检查修复cache文件/删除：{e}")
        raise

def diff_cache(books_metedata_all: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    '''
    比较缓存和用户翻译元数据（英文）差异
    传入所有书读取和生成的{"hash":{"chapter":"content"}}
    返回待翻译列表
    '''
    cahce_data: dict[str, dict[str, str]] = load_cache() # 缓存数据
    translate_data: dict[str, dict[str, str]] = json.loads(json.dumps(books_metedata_all)) # 最终待翻译数据
    '''
    translate_data: dict[str, dict[str, str]] = cahce_data
    这样写是错误的，这是一个dict的浅拷贝，内部结构仍然指向同一内存地址，并且发生了变化
    '''
    for key,value in books_metedata_all.items():
        if key in cahce_data:
            for chapter,content in cahce_data[key].items():
                if chapter in books_metedata_all[key]: # 删除已经存在翻译结果的章节
                    del translate_data[key][chapter]
            if translate_data[key] == {}:
                del translate_data[key] # 删除空的全书缓存
    return translate_data