import os

from github import Github
from github import Auth

# Function to extract reference from an issue
def extract_ref_from_issue(issue):
    text = issue.body
    ref = text[text.find("```") + len("```"):text.rfind("```")]
    return ref.strip() if ref else None

if __name__ == "__main__":
    auth = Auth.Token(os.getenv("GITHUB_API_TOKEN"))
    g = Github(auth=auth)
    repo = g.get_repo("linukc/SUN3D_DATASETS")

    # Iterate through all issues and extract refs
    all_issue_refs = []
    counter = 0
    for issue in repo.get_issues(state="all"):
        counter += 1
        try:
            ref_text = extract_ref_from_issue(issue)
            if not ref_text:
                print(f"Warning: can't parse reference from issue #{issue.number}")
            else:
                all_issue_refs.append(ref_text)
        except Exception as e:
            print(f"Error: can't extract reference from issue #{issue.number}: {e}")

    root_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_path, "..", "ref.bib")
    with open(os.path.abspath(file_path), "w", encoding="utf-8") as f:
       for text in all_issue_refs:
           f.write(text + "\n\n")
    print("---")
    print(f"Saving {len(all_issue_refs)}/{counter}")
