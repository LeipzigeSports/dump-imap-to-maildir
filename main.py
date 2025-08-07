import logging
import mailbox
import optparse
import os.path

from dotenv import load_dotenv
from imap_tools import MailBox

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def dump_imap_to_maildir(imap_user: str, imap_password: str, imap_host: str, maildir_path: str):
    if os.path.isdir(maildir_path):
        raise OSError(f"path at {maildir_path} is not empty")

    maildir = mailbox.Maildir(maildir_path, factory=None)

    logger.info(f"logging in as {imap_user} at {imap_host}")

    with MailBox(imap_host).login(imap_user, imap_password) as m:
        logger.info("login successful")

        for imap_dir in m.folder.list():
            logger.info(f"entering {imap_dir.name}")

            m.folder.set(imap_dir.name, readonly=True)
            maildir_folder = maildir.add_folder(imap_dir.name)

            # get messsage count
            msg_count = m.folder.status()["MESSAGES"]
            cur_msg = 0

            # fetch all, do not mark as read
            for msg in m.fetch(criteria="ALL", mark_seen=False):
                cur_msg += 1
                logger.info(f'  [{cur_msg}/{msg_count}] <{msg.from_}> "{msg.subject}" {msg.date} ({msg.size} bytes)')

                # add mail to maildir
                maildir_folder.add(msg.obj)


def main():
    load_dotenv()

    usage = "usage: %prog [options] imap_user"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-H", "--host", dest="imap_host", help="imap host", default="mxe956.netcup.net")
    parser.add_option("-m", "--maildir", dest="maildir_path", help="maildir path", default="./maildir")
    parser.add_option("-p", "--password", dest="imap_password", help="imap password")

    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("must provide imap user")

    imap_password = opts.imap_password or os.getenv("IMAP_PASSWORD")

    if imap_password is None:
        parser.error("if not using -p option, password must be provided with IMAP_PASSWORD environment variable")

    try:
        dump_imap_to_maildir(args[0], imap_password, opts.imap_host, opts.maildir_path)
    except (ValueError, OSError):
        logger.exception("error during execution")
        exit(1)


if __name__ == "__main__":
    main()
