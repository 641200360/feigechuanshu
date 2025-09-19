import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import RegexAnalyzer


def create_index():
    """
    创建搜索引擎索引
    """
    # 1. 定义索引结构 (Schema)
    # analyzer=RegexAnalyzer(r'\w+') 让 Whoosh 能更好地处理中文分词
    schema = Schema(
        title=TEXT(stored=True, analyzer=RegexAnalyzer(r'\w+')),
        url=ID(stored=True),
        description=TEXT(stored=True, analyzer=RegexAnalyzer(r'\w+'))
    )

    # 2. 检查索引目录是否存在，不存在则创建
    index_dir = "indexdir"
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    # 3. 创建索引文件
    ix = create_in(index_dir, schema)

    # 4. 获取一个写入器 (writer) 来添加文档
    writer = ix.writer()

    # 5. 准备要添加到索引的数据
    # 在真实应用中，这些数据会来自数据库或网络爬虫抓取的结果
    docs_to_add = [
        {
            "title": "生财有术项目精选_shengcaiyoushu - 飞书文档",
            "url": "https://docs.feishu.cn/article/wiki/SeldwZ...",
            "description": "专栏简介. 66个赚到钱的人, 分享他们已经跑通的项目。【重要】添加服务官鱼丸微信(yuwan831), 领取配套的10张项目步骤拆解图;.【阅读建议】先看拆解图, 定位自己擅长的..."
        },
        {
            "title": "生财有术·赚钱训练营指南 - 飞书文档",
            "url": "https://docs.feishu.cn/v/wiki/VEzMwxfsmik...",
            "description": "学霸学员·专属学霸学员毕业证书·价值69元《生财有术66个项目精选》·价值199元《生财365问:像赚钱高手一样行动和思考》·进入生财有术“重点培养人才库”·风向标..."
        },
        {
            "title": "TikTok 运营全攻略 - 飞书文档",
            "url": "#",
            "description": "从入门到精通，全面解析 TikTok 的运营策略和变现模式。"
        },
        {
            "title": "Blender 3D 建模入门教程 - 飞书文档",
            "url": "#",
            "description": "专为初学者设计的 Blender 教程，轻松掌握 3D 建模的核心技巧。"
        }
    ]

    # 6. 遍历数据并添加到写入器
    print("正在建立索引...")
    for doc in docs_to_add:
        writer.add_document(
            title=doc["title"],
            url=doc["url"],
            description=doc["description"]
        )

    # 7. 提交写入器的更改，完成索引创建
    writer.commit()
    print("索引建立完成！")


if __name__ == '__main__':
    create_index()