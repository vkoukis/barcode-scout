# Copyright © 2025 Vangelis Koukis <vkoukis@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import pickle
import hashlib
import logging
import functools
from pathlib import Path

log = logging.getLogger(__name__)


def lru_cache_to_file(cache_dir, max_size=4096):
    """A decorator that implements an LRU cache using files.

    Results of function calls are pickled and stored in a specified directory.
    The filename is a hash of the function's arguments. If the cache
    grows beyond max_size, the least recently used files are removed.

    Args:
        cache_dir (str): The path to the directory to hold cache files.
        max_size (int): The maximum number of cache files to store.

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Ensure the cache directory exists
            Path(cache_dir).mkdir(parents=True, exist_ok=True)

            # 2. Create a stable, hashable representation of the arguments
            # Sort the kwargs to ensure that the order doesn't affect the hash
            arg_tuple = (args, sorted(kwargs.items()))

            # 3. Hash the input arguments to determine the filename
            try:
                arg_pickle = pickle.dumps(arg_tuple)
                arg_hash = hashlib.sha256(arg_pickle).hexdigest()
                cache_file = os.path.join(cache_dir, f"{arg_hash}.pkl")
            except (pickle.PicklingError, TypeError):
                msg = ("Failed to pickle arguments for caching. Calling"
                       " function directly.")
                log.warning(msg, exc_info=True)
                return func(*args, **kwargs)

            # 4. If the file already exists, retrieve and return its contents
            if os.path.exists(cache_file):
                log.debug(f"Cache hit! Loading result from {cache_file}")
                try:
                    # Update the access time for LRU logic
                    os.utime(cache_file, None)
                    with open(cache_file, "rb") as f:
                        return pickle.load(f)
                except (pickle.UnpicklingError, EOFError, OSError):
                    msg = (f"Failed to load cached values from {cache_file}."
                           f" Removing {cache_file} and recalculating.")
                    log.error(msg, exc_info=True)
                    # Attempt to remove the file altogether.
                    try:
                        os.remove(cache_file)
                    except OSError:
                        msg = f"Failed to remove {cache_file}. Ignoring."
                        log.warning(msg, exc_info=True)

            # 5. Otherwise, call the wrapped function
            log.debug("Cache miss. Calling wrapped function...")
            result = func(*args, **kwargs)

            # 6. Store the new result into a file
            # FIXME: Use a temporary file to create the file atomically.
            #        See comment on exclusive access to lock directory above.
            try:
                with open(cache_file, "wb") as f:
                    pickle.dump(result, f)
                log.debug(f"Result stored in cache: {cache_file}")
            except (OSError, pickle.PicklingError):
                msg = f"Failed to write to cache file {cache_file}"
                log.warning(msg, exc_info=True)

            # 7. Trim the cache (LRU eviction)
            # FIXME: This assumes we have exclusive control of the cache,
            #        but we should probably lock the directory here.
            while True:
                try:
                    files = [os.path.join(cache_dir, f)
                             for f in os.listdir(cache_dir)]
                    files_cnt = len(files)
                except OSError:
                    msg = f"Failed to list files under {cache_dir}. Ignoring."
                    log.warning(msg, exc_info=True)
                    files = []
                    files_cnt = 0

                if files_cnt > max_size:
                    # Find the least recently accessed file
                    lru_file = min(files, key=os.path.getatime)
                    log.debug(f"Cache full. Removing least recently used file:"
                              f" {lru_file}")
                    os.remove(lru_file)
                else:
                    break

            return result
        return wrapper
    return decorator


#
# Example
#


# Define a directory for the cache
CACHE_DIR = "lru_cache_dir"


@lru_cache_to_file(cache_dir=CACHE_DIR, max_size=5)
def slow_req(user_id, endpoint):
    """
    A sample function that simulates a slow operation.
    """
    log.info(f"Performing slow operation for user '{user_id}' at"
             f" '{endpoint}'...")
    time.sleep(2)  # Simulate network latency
    return {"user_id": user_id, "data": f"some data from {endpoint}",
            "timestamp": time.time()}


if __name__ == "__main__":
    import logutils
    logutils.setup_logging(logging.DEBUG)

    print("--- First Run ---")
    # These calls will be slow and create cache files
    print("Result 1:", slow_req(100, "profile"))
    print("Result 2:", slow_req(200, "feed"))
    print("Result 3:", slow_req(100, "settings"))

    print("\n--- Second Run (should be fast) ---")
    # These calls should hit the cache and be instantaneous
    print("Result 1 (cached):", slow_req(100, "profile"))
    print("Result 2 (cached):", slow_req(200, "feed"))

    print("\n--- Testing Cache Eviction ---")
    print("Result 4:", slow_req(300, "a"))
    print("Result 5:", slow_req(400, "b"))
    # This should evict the third call (101, endpoint="settings")
    print("Result 6:", slow_req(500, "c"))

    print(f"\nCache directory '{CACHE_DIR}' now contains"
          f" {len(os.listdir(CACHE_DIR))} files.")
