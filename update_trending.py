import requests
import datetime
import re

def fetch_trending_repos():
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://api.github.com/search/repositories?q=created:>{yesterday}&sort=stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
        
    data = response.json()
    
    
    content = "\n"
    for item in data.get('items', [])[:5]:
        name = item['full_name']
        repo_url = item['html_url']
        desc = item['description'] or "暂无描述"
        lang = item['language'] or "未知"
        stars = item['stargazers_count']
        
        # 模仿博客列表的标题、数据和简介
        content += f"### [{name}]({repo_url})\n\n"
        content += f"🗓 **{yesterday}** ｜ ⭐️ **{stars} stars** ｜ 🗂 **{lang}**\n\n"
        content += f"{desc}\n\n---\n\n"
        
    return content

def update_readme(content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    # 精准替换路标中间的内容
    updated_readme = re.sub(
        r'.*?',
        f'\n{content}',
        readme,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    trending_content = fetch_trending_repos()
    if trending_content:
        update_readme(trending_content)
