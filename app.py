import os
from flask import Flask, render_template, request, jsonify
from whoosh.index import open_dir, EmptyIndexError
from whoosh.qparser import MultifieldParser

# 1. 初始化 Flask 应用
app = Flask(__name__)

# 2. 定义存放 Whoosh 索引的目录常量
INDEX_DIR = "indexdir"


@app.route('/')
def index():
    """
    渲染主页面 index.html
    """
    return render_template('index.html')


@app.route('/search')
def search():
    """
    处理搜索请求的 API 接口 (带有内部诊断功能)
    """
    # 从 URL 参数中获取用户输入的查询关键词
    query_str = request.args.get('keyword', '')

    # --- 诊断点 1: 打印收到的关键词 ---
    # 使用 f-string 格式化字符串，确保每次请求都会打印
    print(f"\n[DEBUG] 1. 收到的搜索关键词: '{query_str}'")

    if not query_str:
        return jsonify([])

    # 检查索引目录是否存在
    if not os.path.exists(INDEX_DIR):
        print(f"[ERROR] 索引目录 '{INDEX_DIR}' 不存在。请先运行 indexer.py。")
        return jsonify([])

    try:
        # 打开已创建的索引目录
        ix = open_dir(INDEX_DIR)

        # 使用 with 语句确保 searcher 能被正确关闭
        with ix.searcher() as searcher:
            # --- 诊断点 2: 确认索引中的文档总数 ---
            doc_count = searcher.doc_count()
            print(f"[DEBUG] 2. 当前打开的索引中共有 {doc_count} 篇文档。")

            # 创建一个多字段查询解析器
            parser = MultifieldParser(["title", "description"], schema=ix.schema)

            # 解析用户的查询字符串
            query = parser.parse(query_str)

            # --- 诊断点 3: 打印生成的 Whoosh 查询对象 ---
            print(f"[DEBUG] 3. 生成的 Whoosh 查询对象: {query}")

            # 执行搜索
            results = searcher.search(query, limit=20)

            # --- 诊断点 4: 打印原始搜索结果的数量 (最关键) ---
            results_list = list(results)  # 将结果立即转换为列表以获取其长度
            print(f"[DEBUG] 4. Whoosh 找到的原始结果数量: {len(results_list)}")

            # 将结果格式化为字典列表
            output_results = [hit.fields() for hit in results_list]

        # 将结果列表以 JSON 格式返回给前端
        return jsonify(output_results)

    except EmptyIndexError:
        print(f"[ERROR] 索引 '{INDEX_DIR}' 是空的。请运行 indexer.py 并确保 data.json 中有数据。")
        return jsonify([])
    except Exception as e:
        # 捕获其他所有可能的错误
        print(f"[ERROR] 搜索时发生严重错误: {e}")
        return jsonify([])


# 4. 程序主入口
if __name__ == '__main__':
    # 启动 Flask 应用，并开启调试模式
    app.run(debug=True)