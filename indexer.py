import os
import json
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
# 导入 Jieba 分析器
from jieba.analyse import ChineseAnalyzer

# 使用 Jieba 的中文分析器
analyzer = ChineseAnalyzer()


def create_index():
    # 1. 定义 Schema，确保 TEXT 字段使用我们的中文分析器
    schema = Schema(
        title=TEXT(stored=True, analyzer=analyzer),
        url=ID(stored=True),
        description=TEXT(stored=True, analyzer=analyzer)
    )

    index_dir = "indexdir"
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    # 2. 创建索引
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            docs_to_add = json.load(f)
    except Exception as e:
        print(f"错误: 读取 data.json 文件失败: {e}")
        return

    print(f"正在从 data.json 为 {len(docs_to_add)} 条文档建立索引 (使用 Jieba 分词)...")
    for doc in docs_to_add:
        if "title" in doc and "url" in doc and "description" in doc:
            writer.add_document(
                title=doc["title"],
                url=doc["url"],
                description=doc["description"]
            )
    writer.commit()
    print("索引建立完成！")


if __name__ == '__main__':
    create_index()