import sys
from jira_utils import get_jira_issue, add_jira_comment
from llm import review_pr, generate_implementation_plan
from rag import retrieve_context, retrieve_planning_context


def run_review_mode(issue_key, diff, context):
    jira_data = get_jira_issue(issue_key)
    review = review_pr(diff, context, jira_data, issue_key)
    print(review)


def run_plan_mode(issue_key):
    jira_data = get_jira_issue(issue_key)

    if not jira_data:
        print("Failed to fetch Jira.")
        return


    # Retrieve relevant repo context using Jira description
    repo_context = retrieve_planning_context(jira_data["description"])

    plan = generate_implementation_plan(jira_data, repo_context)

    add_jira_comment(issue_key, plan)

    print("Implementation plan posted to Jira.")


if __name__ == "__main__":

        issue_key = input("Enter Jira Issue Key: ").strip()
        run_plan_mode(issue_key)
