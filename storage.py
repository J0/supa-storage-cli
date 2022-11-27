import click
from pathlib import Path
import os

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
@click.pass_context
def files():
    pass

@click.group()
def bucket():
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

@files.command()
@click.option('-s', '--source', help='path of local file you want to upload', required=True)
@click.option('-d', '--destination',  help='destination file path on supabase storage', required=True)
def upload(filename, destination):
    storage = init_supa_storage()
    try:
        res = storage.from_(filename)
        print(res)
    except Exception as e:
        raise("error occurred")

@files.command()
@click.option('-s', '--source', help='path of local file you want to upload', required=True)
@click.option('-d', '--destination',  help='destination file path on supabase storage', required=True)
def download(filename, destination):
    click.echo('test')

@files.command()
@click.option('-s', 'source', help='path of local file you want to upload', required=True)
@click.option('-d', '--destination',  help='destination file path on supabase storage', required=True)
def move(filename, destination):
    click.echo('move file')

@files.command()
@click.option('-f', '--filename', help='filename on supabase storage', required=True)
def create_public_url(filename):
    click.echo('test')

@click.command()
def login():
    storage = init_supa_storage()
    click.echo(f"done")


@click.command()
@click.pass_context
def generate_url(ctx):
    click.echo(f"current context is: {ctx.obj['ACCESS_KEY']}")

storage.add_command(files)
storage.add_command(login)
storage.add_command(generate_url)
storage.add_command(bucket)

if __name__ == '__main__':
    storage(obj={})
