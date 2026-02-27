import requests
import datetime
import re

def fetch_trending_repos():
    # 获取昨天的日期
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # 构建 GitHub 搜索 API URL (搜索昨天创建的高星项目)
    url = f"https://api.github.com/search/repositories?q=created:>{yesterday}&sort=stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
        
    data = response.json()
    
    # 构建 Markdown 表格内容
    content = "### 🌟 每日 GitHub 热门项目推荐 (自动更新)\n\n"
    content += "| 仓库名称 | 描述 | 主要语言 | ⭐️ 星标 |\n| --- | --- | --- | --- |\n"
    
    # 获取前 5 个项目
    for item in data.get('items', [])[:5]:
        name = item['full_name']
        repo_url = item['html_url']
        desc = item['description'] or "暂无描述"
        # 截断过长的描述
        if len(desc) > 50:
            desc = desc[:47] + "..."
        lang = item['language'] or "未知"
        stars = item['stargazers_count']
        
        content += f"| [{name}]({repo_url}) | {desc} | {lang} | {stars} |\n"
        
    return content

def update_readme(content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    # 使用正则替换占位符之间的内容
    updated_readme = re.sub(
        r'.*?',
        f'\n{content}\n',
        readme,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    trending_content = fetch_trending_repos()
    if trending_content:
        update_readme(trending_content)
        print("README 更新成功！")
    else:
        print("获取数据失败。")
