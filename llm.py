from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
def generate_implementation_plan(jira_data, repo_context):
    prompt = f"""
You are a Senior Backend Engineer.

Based on the Jira requirement and actual codebase context,
generate a detailed implementation plan.
Adding unit test is mandatory

==============================
JIRA REQUIREMENT
==============================
Summary:
{jira_data['summary']}

Description:
{jira_data['description']}

==============================
REPOSITORY CONTEXT
==============================
{repo_context}

Your output must include:

1. Functional Understanding
2. Exact Files To Modify (from context)
3. Specific Code-Level Changes
4. Architectural Considerations
5. Performance Implications
6. Edge Cases
7. Risks
8. Suggested Test Cases

Do not invent files.
Use only files present in context.
Be specific.
"""


    response = llm.invoke(prompt)
    return response.content

def review_pr(diff, context,jira_data=None,jira_key=None):
    jira_summary = ""
    jira_description = ""

    if jira_data:
        jira_summary = jira_data.get("summary", "")
        jira_description = jira_data.get("description", "")

    # Limit context size to prevent overshadowing Jira
    if context and len(context) > 6000:
        context = context[:6000]

    prompt = f"""
    You are a Principal Software Architect performing an enterprise-grade Pull Request review.

    ==============================
    PULL REQUEST DIFF
    ==============================
    {diff}

    ==============================
    REPOSITORY CONTEXT (RAG)
    ==============================
    {context}

    ==============================
    JIRA REQUIREMENTS (MANDATORY)
    ==============================
    Issue Key: {jira_key}
    Summary: {jira_summary}
    Description:
    {jira_description}

    ================================================================
    PART 1 — REQUIREMENT VALIDATION (HIGHEST PRIORITY)
    ================================================================

    You MUST validate whether the implementation satisfies the Jira requirements.

    1. Derive clear functional requirements from the Jira description.
    2. For each requirement:
       - Requirement
       - Evidence in PR (quote relevant diff lines)
       - Compliance Status (Compliant / Partially Compliant / Not Compliant)
    3. If a requirement is missing, explicitly state it.
    4. If PR introduces behavior not mentioned in Jira, flag it.

    If you do NOT explicitly validate Jira requirements,
    your response is considered invalid.

    ----------------------------------------------------------------

    PART 2 — ARCHITECTURAL & TECHNICAL REVIEW

    You must analyze the Pull Request using the following review dimensions:

    1. Architecture & Layering
       - Is business logic placed in the correct layer?
       - Separation of concerns?
       - Should this logic exist in Controller, Service, or Repository?

    2. Performance & Scalability
       - Unnecessary in-memory operations?
       - Should filtering/sorting be pushed to DB?
       - Behavior with 1M+ records?
       - Is pagination required?

    3. API Contract & Backward Compatibility
       - Does change alter existing behavior?
       - Could this silently break consumers?

    4. Correctness & Edge Cases
       - Null safety?
       - Data type correctness (BigDecimal vs primitive)?
       - Concurrency issues?

    5. Security
       - Data exposure?
       - Input validation?
       - Injection risks?

    6. Maintainability
       - Magic numbers?
       - Hardcoded values?
       - Configurability?

    7. Production Readiness
       - Logging?
       - Error handling?
       - Monitoring implications?

    IMPORTANT RULES:
    - Do NOT give generic advice.
    - Be specific to the code shown.
    - Assume high-scale production.
    - If something is acceptable for small data but risky at scale, explain why.
    - Provide severity level (Low / Medium / High / Critical) for each issue.

    ----------------------------------------------------------------

    PART 3 — SUMMARY

    Provide:

    1. Requirement Compliance Verdict:
       - Fully Compliant
       - Partially Compliant
       - Not Compliant
       - Over-Implemented

    2. Architectural Risk Assessment

    3. Recommended Refactor (if necessary)

    4. Overall PR Risk Score (1–10)
       - 1 = Safe
       - 10 = Severe Production Risk

    Be structured, analytical, and explicit.
    """

    response = llm.invoke(prompt)
    return response.content