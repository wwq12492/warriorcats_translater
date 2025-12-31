'''
标记基本的包数据

常用需求：
1. __version__,__author__,__description__元数据
2. 导入c其他的包和方法（比如自己得内部结构）
3. __all__ = [ ... ]标记from package import *的默认行为（建立在你在这里导入了自己内部结构中的这些被用在__all__里的包）
4. 定义初始化逻辑
'''
__version__ = "0.0.0"
__author__ = "DiegoW"
__description__ = "A translater (en->zh) for Warrior Cats novel series"