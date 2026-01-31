from dataclasses import dataclass

# 数据模型

@dataclass
class Ebook:
    '''
    存储书籍解析数据
    '''
    name: str # 书籍名称
    chapter_contents: dict[str, str] # 书籍章节数据 {"chapter": "content"}

# config类和相关的配置类

@dataclass
class APIConfig:
    '''
    单个api的配置类
    '''
    url: str # api路由
    api_key: str
    max_connections: int # 最大连接数
    qpm: int # 每分钟最大访问量

@dataclass
class EbookConfig:
    '''
    单本电子书配置类
    '''
    path: str # 电子书路径

@dataclass
class Config:
    '''
    主配置类，负责顶层配置（尤其是和全局和批量化相关）
    '''
    apis: list[APIConfig]
    books: list[EbookConfig]
    parser_processes: int = 8 # 并行解析进程池进程数
    max_concurrent_books: int = 4 # 创建的读取queue的任务的数量
    max_queue_size: int = 10 # 翻译队列大小