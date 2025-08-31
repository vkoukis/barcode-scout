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

import sys
import logging

import llm
import gsearch
import logutils

log = logging.getLogger(__name__)


if __name__ == "__main__":
    logutils.setup_logging(logging.DEBUG)

    if len(sys.argv) > 1:
        if len(sys.argv) != 2:
            msg = "Zero or one command-line arguments expected."
            raise RuntimeError(msg)
        q = sys.argv[1]
    else:
        q = input("Enter search term [e.g., a barcode]: ")

    # Search Google, retrieve a list of results
    items = gsearch.google_advanced_search(q, num_results=10,
                                           lang="en", region="us", safe=None)

    # Query the LLM to interpret them, and print the outcome
    product_name = llm.product_name(items)
    product_name_noqty = llm.product_name_noqty(product_name)
    print(product_name)
    print(product_name_noqty)
