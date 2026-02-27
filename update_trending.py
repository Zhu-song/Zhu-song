import requests
import datetime
import os

def fetch_trending_repos():
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://api.github.com/search/repositories?q=created:>{yesterday}&sort=stars&order=desc"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # 🌟 这里就是给机器人加的 VIP 通行证！
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ 抓取失败！被 GitHub 拦截了。状态码: {response.status_code}")
        print(response.text)
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
    
    start_idx = readme.find(start_marker)
    end_idx = readme.find(end_marker)
    
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        updated_readme = readme[:start_idx + len(start_marker)] + "\n" + content + readme[end_idx:]
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("🎉 更新成功！路标找到了，数据也写进去了！")
    else:
        print("❌ 错误：在 README.md 中找不到那两行隐形路标，或者排版乱了！")

if __name__ == "__main__":
    trending_content = fetch_trending_repos()
    if trending_content:
        update_readme(trending_content)
    else:
        print("❌ 没有获取到热门数据，放弃修改 README。")
