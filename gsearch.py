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

from googlesearch import search


def google_advanced_search(query, num_results=10, lang="en", region="us",
                           safe="active"):
    """
    Perform an advanced Google search and return a list of tuples:
    (url, title, description snippet).
    """
    results = search(
        query,
        num_results=num_results,
        lang=lang,
        region=region,
        safe=safe,
        advanced=True
    )

    output = []
    for res in results:
        url = res.url
        title = res.title or ""
        desc = res.description or ""
        output.append({"url": url, "title": title, "desc": desc})
    return output


if __name__ == "__main__":
    q = input("Enter search query: ")
    items = google_advanced_search(q, num_results=10, lang="en", region="us",
                                   safe=None)

    for item in items:
        print("Title: {title}\nURL: {url}\nSnippet: {desc}\n".format(**item))
