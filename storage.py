import click
from pathlib import Path
import os
import pyperclip

from supabase import create_client, Client

def init_supa_storage():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    storage = supabase.storage()
    return storage

@click.group()
def storage():
    pass

@click.group()
def files():
    pass

@click.group()
def bucket():
    pass

@click.group()
def permissions():
    pass

@bucket.command()
@click.option('-n', '--name', help='name of bucket', required=True)
def create(name):
    try:
        storage_client = init_supa_storage()
        res = storage_client.create_bucket(name)
    except:
        raise("Failed to create bucket")

@bucket.command()
@click.option('-n', '--name', help='name of bucket', required=True)
def delete(name):
    try:
        storage_client = init_supa_storage()
        res = storage_client.delete_bucket(name)
    except:
        raise("Failed to delete bucket")

@bucket.command()
@click.option('-n', '--name', help='name of bucket', required=True)
def list(name):
    try:
        storage_client = init_supa_storage()
        res = storage_client.get_bucket(name)
        click.echo(f"{res}")
    except:
        raise("Failed to delete bucket")

@bucket.command()
@click.option('-n', '--name', help='name of bucket', required=True)
def empty(name):
    try:
        storage_client = init_supa_storage()
        res = storage_client.empty_bucket(name)
        click.echo(f"{res}")
    except:
        raise("Failed to empty bucket")


@files.command()
@click.option('-b', '--bucket', help='bucket to upload to', required=True)
@click.option('-s', '--source', help='path of local file you want to upload', required=True)
@click.option('-d', '--destination',  help='destination file path on supabase storage', required=True)
def upload(bucket, source, destination):
    storage = init_supa_storage()
    try:
        with open(source, 'rb+') as f:
            res = storage.from_(bucket).upload(destination, os.path.abspath(source))
    except Exception as e:
        raise("error occurred")

@files.command()
@click.option('-b', '--bucket-name', help='name of bucket', required=True)
@click.option('-s', '--source',  help='filepath on supastorage', required=True)
@click.option('-d', '--destination', help='output path to save the file to', required=True)
def download(bucket_name, source, destination):
    storage = init_supa_storage()
    try:
        with open(destination, 'wb+') as f:
            res = storage.from_(bucket_name).download(source)
            f.write(res)
    except Exception as e:
        raise("Download failed")

@files.command()
@click.option('-s', '--source', help='path of local file you want to upload', required=True)
@click.option('-d', '--destination',  help='destination file path on supabase storage', required=True)
def move(filename, destination):
    raise NotImplementedError("todo")

@files.command()
@click.option('-b', '--bucket-name', help='bucket name', required=True)
@click.option('-f', '--filepath', help='filepath', required=True)
@click.option('-e', '--expiry-duration', help='expiry duration for the link', default=3600)
def create_signed_url(bucket_name, filepath, expiry_duration):
    storage = init_supa_storage()
    try:
        res = storage.from_(bucket_name).create_signed_url(filepath, expiry_duration)
        pyperclip.copy(res['signedURL'])
        click.echo(f"{res['signedURL']}")
    except Exception as e:
        raise("failed to generate signed url")

@click.command()
def login():
    raise NotImplementedError("todo")

@permissions.command()
def allow():
    raise NotImplementedError("figure out which how to interface with rls policies here")


storage.add_command(files)
storage.add_command(login)
storage.add_command(bucket)
storage.add_command(permissions)

if __name__ == '__main__':
    storage(obj={})
