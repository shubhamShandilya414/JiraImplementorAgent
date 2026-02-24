import requests




def get_pr_diff(owner, repo, pr_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    return response.text


def get_changed_files(owner, repo, pr_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    files_data = response.json()

    return [file["filename"] for file in files_data]


def post_review(owner, repo, pr_number, token, review_text):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"body": review_text}
    requests.post(url, headers=headers, json=data)