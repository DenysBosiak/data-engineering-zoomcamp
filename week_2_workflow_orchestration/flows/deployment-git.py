from prefect_github import GitHubRepository
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

github_block = GitHub.load("githubrepo")

deployment = Deployment.build_from_flow(
    flow=github_block.load_existing("etl_web_to_gcs"),
    name="Github Example",
)

if __name__ == "__main__":
    deployment.apply()