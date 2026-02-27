import requests
import datetime
import os

def fetch_trending_repos():
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://api.github.com/search/repositories?q=created:>{yesterday}&sort=stars&order=desc"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ 抓取失败！")
        return None
        
    data = response.json()
    
    content = "\n\n"
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
        
    # 🌟 我们的新路标：直接认你主页上这个肉眼可见的标题！
    delimiter = "### My Latest Trending Repos 👇"
    
    if delimiter in readme:
        # 以这个标题为界限，把文章劈成两半。保留上半部分（你的API圆环等），扔掉下半部分。
        top_part = readme.split(delimiter)[0]
        
        # 重新拼接：上半部分 + 标题 + 最新的热门数据
        updated_readme = top_part + delimiter + content
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("🎉 更新成功！使用了全新的标题定位法！")
    else:
        print(f"❌ 错误：找不到标题 '{delimiter}'，请确保 README 中有这行字！")

if __name__ == "__main__":
    trending_content = fetch_trending_repos()
    if trending_content:
        update_readme(trending_content)
