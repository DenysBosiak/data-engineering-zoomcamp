from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task()
def write_gcs(path: Path, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("prefect-gsp")
    bucket_path = f"data/{dataset_file}.csv"
    gcs_block.upload_from_path(from_path=path, to_path=bucket_path)
    return


@flow()
def etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}"

    path = Path(f"data/{dataset_file}.csv")
    write_gcs(path, dataset_file)


@flow
def etl_parent(months: list[int], year: int):
    """The parent ETL function"""
    for month in months:
        etl_web_to_gcs(year, month)


if __name__ == "__main__":
    year = 2019
    months = [1]
    etl_parent(months, year)