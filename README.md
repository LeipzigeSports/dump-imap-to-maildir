Python script for dumping all messages from all folders in an IMAP mailbox to a local [Maildir folder](https://en.wikipedia.org/wiki/Maildir).

# Installation

Clone this repository.
In the root directory, execute the following commands.

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

To exit the virtual environment, run `deactivate`.
To re-open the virtual environment and use the script, simply re-run `source .venv/bin/activate`.

# Usage

```
python main.py imap_user
```

There are additional options.
The default values connect to the Leipzig eSports e.V. IMAP host.

- `-H`, `--host`: IMAP host (default: mxe956.netcup.net)
- `-p`, `--password`: IMAP password
- `-m`, `--maildir`: path to Maildir folder (default: ./maildir)

Using `--password` to pass the IMAP password to the script is generally not recommended.
Instead, it should be passed using the `IMAP_PASSWORD` environment variable.
You can either set it manually or copy the [environment file](.env.example) to a new `.env` file and enter the 
desired password there.

`--maildir` must point to a path that doesn't exist yet.
If the path exists, the script will exit with an error.

## Archival

For archival purposes, it is recommended to compress the generated Maildir folder and encrypt it.

```
tar czvf user-at-leipzigesports-dot-de.tar.gz maildir
gpg -c user-at-leipzigesports-dot-de.tar.gz
```

The generated file can later be decrypted as follows.

```
gpg user-at-leipzigesports-dot-de.tar.gz.gpg
```

# License

MIT.s
