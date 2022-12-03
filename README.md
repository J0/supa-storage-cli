# Supa-Storage-Cli

This is a naive implementation of a Supabase Storage client and is meant to help with dogfooding `storage-py` because it is not on the critical path for day to day life at the moment


## Getting Started 

1. Create a virtualenv by doing `virtualenv .env` and the activate it `source .env/bin/activate`
2. Install dependencies `pip3 install supabase pyperclip click`
3. Use the application - run `python3 storage.py` to see available options - not everything there is implemented.

## To figure out
- How to make use of the context in click so we can store the bucket name for all `bucket` related commands
- How to come up with an interface for the `permissions` command so we allow user to set Row level Security policies in a sensible fashion
- How to skirt the timeout limit that comes with uploading large files via `httpx`. Possible options are to use `.stream()` or to allow a configurable timeout
- How to properly handle errors and give sensible error messages.

