import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def extract_text_from_adf(adf):
    """
    Recursively extract text from Jira ADF format.
    Handles nested structures safely.
    """

    if not adf:
        return ""

    text_parts = []

    def recurse(node):
        if isinstance(node, dict):
            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))
            for value in node.values():
                recurse(value)
        elif isinstance(node, list):
            for item in node:
                recurse(item)

    recurse(adf)

    return " ".join(text_parts).strip()

def extract_jira_key(text: str):
    """
    Extracts Jira issue key from PR title or branch name.
    Example: CUDI-1234
    """
    match = re.search(r"[A-Z]+-\d+", text)
    return match.group(0) if match else None

def add_jira_comment(issue_key, comment_text):
    """
    Add comment to Jira issue.
    Jira Cloud requires ADF format for comments.
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }


    response = requests.post(
        url,
        json=payload,
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    if response.status_code != 201:
        print("❌ Failed to add Jira comment:", response.text)
        return False

    print("✅ Jira comment added successfully.")
    return True

def get_jira_issue(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        return None

    data = response.json()
    summary = data["fields"].get("summary", "")
    description_raw = data["fields"].get("description")

    # 👇 THIS IS WHERE YOU CALL IT
    description_text = extract_text_from_adf(description_raw)

    return {
        "key": issue_key,
        "summary": summary,
        "description": description_text
    }