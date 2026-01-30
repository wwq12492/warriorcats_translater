from dataclasses import dataclass

@dataclass
class Ebook:
    '''
    存储书籍解析数据
    '''
    name: str # 书籍名称
    chapter_contents: dict[str, str] # 书籍章节数据 {"chapter": "content"}

@dataclass
class Config:
    '''
    配置属性数据类
    '''
    pass