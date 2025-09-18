from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 模拟的数据库或搜索引擎数据
# 在真实应用中，这些数据会来自数据库或真实的搜索引擎
mock_db = {
    "生财有术": [
        {
            "title": "生财有术项目精选_shengcaiyoushu - 飞书文档",
            "url": "https://docs.feishu.cn/article/wiki/SeldwZ...",
            "description": "专栏简介. 66个赚到钱的人, 分享他们已经跑通的项目。【重要】添加服务官鱼丸微信(yuwan831), 领取配套的10张项目步骤拆解图;.【阅读建议】先看拆解图, 定位自己擅长的..."
        },
        {
            "title": "生财有术·赚钱训练营指南 - 飞书文档",
            "url": "https://docs.feishu.cn/v/wiki/VEzMwxfsmik...",
            "description": "学霸学员·专属学霸学员毕业证书·价值69元《生财有术66个项目精选》·价值199元《生财365问:像赚钱高手一样行动和思考》·进入生财有术“重点培养人才库”·风向标..."
        }
    ],
    "tiktok": [
        {
            "title": "TikTok 运营全攻略 - 飞书文档",
            "url": "#",
            "description": "从入门到精通，全面解析 TikTok 的运营策略和变现模式。"
        }
    ],
    "blender": [
        {
            "title": "Blender 3D 建模入门教程 - 飞书文档",
            "url": "#",
            "description": "专为初学者设计的 Blender 教程，轻松掌握 3D 建模的核心技巧。"
        }
    ]
}


@app.route('/')
def index():
    """
    渲染主页面
    """
    return render_template('index.html')


@app.route('/search')
def search():
    """
    处理搜索请求的 API 接口
    """
    query = request.args.get('keyword', '')

    # 根据查询关键字在模拟数据库中查找结果
    # .get(query, []) 如果找不到关键字，返回一个空列表
    results = mock_db.get(query, [])

    # 以 JSON 格式返回数据
    return jsonify(results)


if __name__ == '__main__':
    # 启动 Flask 应用，开启调试模式
    app.run(debug=True)