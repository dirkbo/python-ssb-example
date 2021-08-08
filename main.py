import json
import sys

from ssb.database import SsbDatabase
from ssb.identity import SsbIdentity
from ssb.message import SSbMessage


def run_example():
    # Older versions of Python don't respect dictionary insertion order.
    is_recent_python = sys.version_info >= (3, 6)
    assert is_recent_python, "Please upgrade to Python 3.6 or greater"

    ssb_id = SsbIdentity()
    ssb_db = SsbDatabase()

    hello = SSbMessage(ssb_id, ssb_db, {'type': 'post', 'text': 'hello'})
    world = SSbMessage(ssb_id, ssb_db, {'type': 'post', 'text': 'world'})

    print(json.dumps([hello.as_dict, world.as_dict]))


if __name__ == "__main__":
    run_example()
