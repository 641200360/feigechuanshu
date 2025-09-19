from flask import Flask, render_template, request, jsonify
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Or

app = Flask(__name__)
INDEX_DIR = "indexdir"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    """
    处理搜索请求的 API 接口 (使用 Whoosh)
    """
    query_str = request.args.get('keyword', '')
    if not query_str:
        return jsonify([])

    try:
        # 1. 打开索引目录
        ix = open_dir(INDEX_DIR)

        # 2. 创建一个查询解析器
        # 我们希望在 'title' 和 'description' 两个字段中都进行搜索
        parser = QueryParser("title", ix.schema)

        # 允许多个字段搜索
        # We'll build the query manually to search multiple fields
        title_parser = QueryParser("title", ix.schema)
        desc_parser = QueryParser("description", ix.schema)

        # 3. 解析用户的查询字符串
        # 允许用户输入多个关键词，用 OR 连接
        title_query = title_parser.parse(query_str)
        desc_query = desc_parser.parse(query_str)
        combined_query = Or([title_query, desc_query])

        # 4. 使用 with 语句打开搜索器 (searcher)
        with ix.searcher() as searcher:
            # 5. 执行搜索
            results = searcher.search(combined_query, limit=20)  # 最多返回20条结果

            # 6. 格式化搜索结果
            # results 对象包含了丰富的元数据，我们只需要提取存储的字段
            # a list of dictionaries.
            output_results = [dict(hit) for hit in results]

        return jsonify(output_results)

    except Exception as e:
        print(f"搜索时发生错误: {e}")
        # 如果索引不存在或发生其他错误，返回空列表
        return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)