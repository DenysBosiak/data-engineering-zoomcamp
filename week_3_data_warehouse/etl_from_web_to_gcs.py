from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url, low_memory=False, encoding='latin1')
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropOff_datetime"] = pd.to_datetime(df["dropOff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_file}.csv")
    df.to_csv(path, compression="gzip", encoding='utf-8')
    return path


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
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path, dataset_file)


@flow
def etl_parent(months: list[int], year: int):
    """The parent ETL function"""
    for month in months:
        etl_web_to_gcs(year, month)


if __name__ == "__main__":
    year = 2019
    months = list(range(1,12+1))
    etl_parent(months, year)