# app/services/crawler.py
import httpx
import json
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    content
    difficulty
    similarQuestions
    topicTags {
      name
    }
    codeSnippets {
      lang
      langSlug
      code
    }
  }
}
"""
SEARCH_QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    data {
      frontendQuestionId: questionFrontendId
      titleSlug
    }
  }
}
"""

USER_RECENT_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissions(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

class LeetCodeCrawler:
    async def get_problem_detail(self, title_slug: str) -> Dict[str, Any]:
        
        title_slug = title_slug.replace(" ", "-") # remove space char
        
        payload = {
            "query": QUESTION_QUERY,
            "variables": {"titleSlug": title_slug}
        }

        async with httpx.AsyncClient() as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                "Referer": f"https://leetcode.com/problems/{title_slug}/"
            }
            
            try:
                response = await client.post(LEETCODE_GRAPHQL_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                question_data = data.get("data", {}).get("question")
                if not question_data:
                    return {"error": "Problem not found"}

                clean_content = self._clean_html(question_data["content"])

                raw_similar = question_data.get("similarQuestions", "[]")
                
                try:
                    similar_questions_list = json.loads(raw_similar)
                except json.JSONDecodeError:
                    similar_questions_list = []

                
                return {
                    "id": question_data["questionId"],
                    "title": question_data["title"],
                    "difficulty": question_data["difficulty"],
                    "tags": [tag["name"] for tag in question_data["topicTags"]],
                    "similar_questions": similar_questions_list,
                    "content_html": question_data["content"],
                    "content_text": clean_content,
                    "code_snippets": question_data["codeSnippets"] 
                }

            except Exception as e:
                print(f"Crawler Error: {e}")
                return {"error": str(e)}

    def _clean_html(self, html_content: str) -> str:
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator="\n").strip()
    
    async def get_slug_by_id(self, frontend_id: str) -> Optional[str]:
        """
        ID -> problem title
        """
        payload = {
            "query": SEARCH_QUERY,
            "variables": {
                "categorySlug": "",
                "skip": 0,
                "limit": 100,
                "filters": {
                    "searchKeywords": frontend_id
                }
            }
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(LEETCODE_GRAPHQL_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                
                questions = data.get("data", {}).get("problemsetQuestionList", {}).get("data", [])
                
                for q in questions:
                    if q["frontendQuestionId"] == frontend_id:
                        return q["titleSlug"]
                
                return None
                
            except Exception as e:
                print(f"Slug Search Error: {e}")
                return None
    
    async def get_problem_by_id(self, frontend_id: str) -> Dict[str, Any]:
        slug = await self.get_slug_by_id(frontend_id)
        if not slug:
            return {"error": f"Problem ID {frontend_id} not found"}
        return await self.get_problem_detail(slug)

    async def get_user_recent_submissions(self, username: str, limit: int = 20) -> list[Dict[str, Any]]:
        payload = {
            "query": USER_RECENT_QUERY,
            "variables": {
                "username": username,
                "limit": limit
            }
        }

        async with httpx.AsyncClient() as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                "Content-Type": "application/json",
                "Referer": f"https://leetcode.com/{username}/"
            }
            
            try:
                response = await client.post(LEETCODE_GRAPHQL_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                if "errors" in data:
                    print(f"GraphQL Error: {data['errors']}")
                    return []
                
                return data.get("data", {}).get("recentAcSubmissions", [])

            except Exception as e:
                print(f"Crawler Error (Recent Submissions): {e}")
                return []

leetcode_crawler = LeetCodeCrawler()