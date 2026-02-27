import requests
import datetime

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
        
        content += f"### [{name}]({repo_url})\n\n"
        content += f"🗓 **{yesterday}** ｜ ⭐️ **{stars} stars** ｜ 🗂 **{lang}**\n\n"
        content += f"{desc}\n\n---\n\n"
        
    return content

def update_readme(content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    start_marker = ""
    end_marker = ""
    
    # 找到这两个路标的精确位置
    start_idx = readme.find(start_marker)
    end_idx = readme.find(end_marker)
    
    # 只要找到了路标，直接暴力切掉中间的所有东西！
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        updated_readme = readme[:start_idx + len(start_marker)] + "\n" + content + readme[end_idx:]
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("更新成功！")
    else:
        print("错误：在 README.md 中找不到路标！")

if __name__ == "__main__":
    trending_content = fetch_trending_repos()
    if trending_content:
        update_readme(trending_content)
