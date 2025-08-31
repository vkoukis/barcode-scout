
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


import logging

log = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    """Setup basic loggging."""
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def test_logging():
    """Log basic messages at different log levels."""
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.debug("This is a debug message.")


if __name__ == "__main__":
    setup_logging(logging.DEBUG)
    test_logging()
