'''
真正的cli入口

分离__main__入口点和cli入口点优势：
1. 清晰的关注点分离
2. 便于作为正常包时被导入
3. 便于专注扩展cli相关功能（比如子命令）
4. 便于调试

职能范围：参数解析（比如应该在这里的main直接CURRENT_DIR: str = os.getcwd() # 获得当前运行目录）
'''
import typer # 用实例对象（main运行）+装饰器函数定义参数和逻辑
from typing import Annotated

app = typer.Typer() # 创建typer实例
'''
全局实例：在模块导入时确定，用于“不可变”的命令参数注册
警告：条件注册可能使其发生变化，需要改动
'''

@app.command()
def main(clear_cache_force: Annotated[bool, typer.Option(help="强制清理所有翻译缓存（重新开始所有翻译）")] = False):
    print(f"clear cache?:{clear_cache_force}")

def cli_wrapper() -> int:
    """错误码返回处理"""
    try:
        app()
        return 0
    except typer.Exit as e:
        return e.exit_code
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        return 1

if __name__ == "__main__":
    cli_wrapper() # 允许直接运行 python -m warriorcats_translater.cli