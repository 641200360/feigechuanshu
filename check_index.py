import os
from whoosh.index import open_dir, EmptyIndexError

INDEX_DIR = "indexdir"

if not os.path.exists(INDEX_DIR):
    print(f"诊断失败：索引目录 '{INDEX_DIR}' 不存在！")
    print("请先运行 python indexer.py 来创建索引。")
else:
    try:
        ix = open_dir(INDEX_DIR)
        with ix.searcher() as searcher:
            doc_count = searcher.doc_count()
            print("--- 索引诊断报告 ---")
            print(f"索引目录 '{INDEX_DIR}' 存在。")
            print(f"索引中包含的文档总数: {doc_count}")
            if doc_count > 0:
                print("诊断成功：索引中确实包含数据。")
            else:
                print("诊断警告：索引是空的！请检查 indexer.py 和 data.json。")
    except EmptyIndexError:
        print(f"诊断错误：索引目录 '{INDEX_DIR}' 是空的或已损坏。")