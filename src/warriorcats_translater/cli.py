'''
真正的能够的cli入口

分离__main__入口点和cli入口点优势：
1. 清晰的关注点分离
2. 便于作为正常包时被导入
3. 便于专注扩展cli相关功能（比如子命令）
4. 便于调试
'''
def main():
    pass

if __name__ == "__main__":
    main() # 允许直接运行 python -m warriorcats_translater.cli