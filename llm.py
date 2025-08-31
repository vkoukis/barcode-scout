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

MODEL = "gemma3:4b"
PROMPT = \
    ("The following is a list of Google search results for a specific"
     " product. Each result is a tuple (URL, title, snippet), one tuple for"
     " each page. Based on these results, give your best guess for the product"
     " name. Follow these rules:\n\n"
     "* Make the product name as detailed as possible.\n"
     "* DO NOT INCLUDE any information on the actual packaging.\n"
     "* DO NOT INCLUDE any information on package weight, e.g., grams.\n"
     "* DO NOT INCLUDE any information on pack size.\n"
     "* DO NOT INCLUDE any information on bottle volume, e.g., ml.\n"
     "* DO include information on active ingredient content, or alcohol"
     " content."
     "* DO NOT make up product names if you don't have enough information."
     "* Respond with \"Unknown\" if you don't have enough information to"
     " deduce a product name."
     "* DO NOT give any other explanation, just a single string, on a single"
     " line, with the product name.\n\n"
     " Here is the list of results:\n\n")


def query_llm(prompt):
    """Query an LLM served by Ollama and return its response as a string."""
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(model=MODEL)

    chunks = []
    for chunk in llm.stream(prompt):
        chunks.append(chunk)
    return "".join(chunks)


def product_name(results):
    """Query an LLM with a specific prompt to retrieve a product name."""
    results_str = "\n".join(("* URL: %s\n"
                             "  Title: %s\n"
                             "  Description: %s\n") %
                            (res["url"], res["title"], res["desc"])
                            for res in results)

    prompt = PROMPT + results_str

    print(prompt)
    print("\n\n*********\n\n")

    return query_llm(prompt)


if __name__ == "__main__":
    q = input("Ask the LLM: ")
    print(query_llm(q))
