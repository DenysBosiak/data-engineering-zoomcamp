from prefect.filesystems import GitHub

gh = GitHub(repository="https://github.com/DenisBosiak/data-engineering-zoomcamp.git")
gh.save("githubrepo") 