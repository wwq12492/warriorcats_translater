'''
pyproject标记的入口点

主入口点的逻辑应该简单，只负责标记入口
'''
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())  # 只是转发调用
    '''
    为何使用sys.exit？
    接受cli.py的退出码，返回退出码
    例：a && b这样的脚本逻辑就由退出码决定执行逻辑（a exit 0 -> b/a exit 1 -> x）

    此处用例：
    cli.py/main: return 1 # 此处只是“码”数据
    __main__.py：sys.exit(1) # 真实退出码

    异常处理：
    不应该直接raise（出现异常python解释器会以 1 退出。程序也会，但是程序不会按照显式指定的退出码退出）
    
    所以：在cli.py的顶层（raise最终传播到的地方），使用以上正确方式打印异常，返回退出“码”
    '''