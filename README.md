# warriorcats_translater
## 现代化学习目标
- 现代化特性
    - pyproject.toml
    - 项目结构（模块化）
    - .env
    - pytest测试（虚拟文件目录）
- 技术栈
    - asyncio、aiohttp、aiofiles
    - pydantic
    - 面向对象编程

## 构建方式
打包为python“可执行”包并用python运行（入口文件为`__main__.py`）

## 用户工作流
### 用户目录
```markdown
translale_proj_dir: <!-- 用户翻译工作目录 -->
- translate.json <!-- 配置文件和翻译列表 -->
- translate_cache.json <!-- 翻译缓存（"哈希:分章节内容"数据） -->
- glossary.csv <!-- 专有名词列表 -->
- ...
```

#### 文件示例
- `translate.json`:
```json
{
    "booklist":[
        "~/a.epub",
        ...
    ],
    "translate": {
        "max_connections": 4,
        "prompt": "prompt for ai",
        ...
    },
    "output_directory": "~/outputs"
}
```
> 完整示例请见`./src/warriorcats_translater/config/schema.py`

- `translate_cache.json`:
```json
{
    "9f86d081884c7d659a2feaa0c55ad0...":{
        "Prologue": "xxxxxx",
        "Chapter 1": "xxxxxx",
        ...
    },
    ...
}
```
### ai翻译
1. 用户通过`warriorcats_translater`运行工具
2. 工具获取用户运行它的目录，查找`translate.json`（以及`traslate_cache.json`和`glossary.csv`）
3. 根据`translate_cache.json`缺失的内容发起翻译请求（根据`glossary.csv`标记过已知专有名词进行保护避免ai误翻译），响应翻译结果之后存入缓存
4. 完成全部书的翻译，退出程序

### 专有名词替换
1. 检查待翻译内容是否都出现在缓存中
2. 如果是，检查`glossary.csv`，根据ai标记的`{}`匹配需要手动声明的专有名词列表，退出程序
3. 用户编辑`glossary.csv`，声明对应的专有名词的替换方案，运行程序
4. 输出中文epub到指定目录