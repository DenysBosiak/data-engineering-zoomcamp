from prefect import flow
from prefect_github import GitHubCredentials
from prefect_github.repository import query_repository
from prefect_github.mutations import add_star_starrable

@flow
def github_start_flow():
    gc = GitHubCredentials.load("github-credential")
    repository_id = query_repository(
        "DenisBosiak",
        "data-engineering-zoomcamp",
        github_credentials=gc,
        return_fields="id"
    )["id"]
    starrable = add_star_starrable(
        repository_id,
        gc
    )
    return starrable

github_start_flow()