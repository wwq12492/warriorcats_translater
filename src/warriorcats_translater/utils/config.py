'''
此模块用于读写config和进行校验
'''
from pydantic import Field,ValidationError
from pydantic_settings import BaseSettings,SettingsConfigDict
import json
import os

class Config(BaseSettings):
    api_key: str = Field(description="用户的api密钥")

    model_config = SettingsConfigDict(strict=True,env_file="../../.env",env_file_encoding="utf-8") # 警告：使用了本文件到.env的相对路径

def load_config() -> dict:
    CWD: str = os.getcwd() # 获取用户运行工具的目录

    try:
        with open(os.path.join(CWD,"translate.json"),"r",encoding="utf-8") as f:
            metadata: dict = json.load(f) # 获取json配置文件数据
    except FileNotFoundError:
        print("未发现translate.json")
        raise
    except json.JSONDecodeError as e:
        print(f"[错误] translate.json文件json错误，请检查修复文件：{e}")
        raise

    try:
        config: dict = Config.model_validate(metadata).model_dump() # 校验之后的配置文件结果
    except ValidationError as e:
        print(f"配置文件选项错误:{e}")
        raise

    return config