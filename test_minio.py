import duckdb
from minio import Minio
from minio.error import S3Error

# Create a Minio client
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Create the bucket if it doesn't exist
bucket_name = "my-bucket"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)


# List all buckets
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket.name)

# Upload a file to a bucket
try:
    result = client.fput_object(
        "my-bucket", "my-object", "my_database.duckdb"
    )
    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )
except S3Error as exc:
    print("error occurred.", exc)

# Remove my_database.duckdb from local dir
import os
os.remove('my_database.duckdb')


# Download the DuckDB file from the MinIO bucket
try:
    client.fget_object("my-bucket", "my-object", "my_database_restored.duckdb")
except S3Error as exc:
    print("error occurred.", exc)

# Connect to the downloaded DuckDB file
con = duckdb.connect('my_database_restored.duckdb')

# List all tables
tables = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

# Print the tables
for table in tables:
    print(table[0])

# Execute a query to verify that the database was restored
result = con.execute("SELECT * FROM my_table").fetchall()

# Print the result
for row in result:
    print(row)