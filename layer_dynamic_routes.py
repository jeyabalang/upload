# -*- coding: utf-8 -*-
"""Layer-dynamic-routes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bbaA81WwtsgATS0qmUVOLqPspuAGkxcy

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aurelio-labs/semantic-router/blob/main/docs/02-dynamic-routes.ipynb) [![Open nbviewer](https://raw.githubusercontent.com/pinecone-io/examples/master/assets/nbviewer-shield.svg)](https://nbviewer.org/github/aurelio-labs/semantic-router/blob/main/docs/02-dynamic-routes.ipynb)

# Dynamic Routes

In semantic-router there are two types of routes that can be chosen. Both routes belong to the `Route` object, the only difference between them is that _static_ routes return a `Route.name` when chosen, whereas _dynamic_ routes use an LLM call to produce parameter input values.

For example, a _static_ route will tell us if a query is talking about mathematics by returning the route name (which could be `"math"` for example). A _dynamic_ route can generate additional values, so it may decide a query is talking about maths, but it can also generate Python code that we can later execute to answer the user's query, this output may look like `"math", "import math; output = math.sqrt(64)`.

***⚠️ Note: We have a fully local version of dynamic routes available at [docs/05-local-execution.ipynb](https://github.com/aurelio-labs/semantic-router/blob/main/docs/05-local-execution.ipynb). The local 05 version tends to outperform the OpenAI version we demo in this notebook, so we'd recommend trying [05](https://github.com/aurelio-labs/semantic-router/blob/main/docs/05-local-execution.ipynb)!***

## Installing the Library
"""

pip install -qU semantic-router==0.0.32
pip install unifyai

"""## Initializing Routes and RouteLayer

Dynamic routes are treated in the same way as static routes, let's begin by initializing a `RouteLayer` consisting of static routes.
"""

from semantic_router import Route

# Define routes for Math and Coding
math_route = Route(
    name="math",
    utterances=[
        "solve for x in the equation",
        "what is the integral of",
        "how to calculate the derivative",
        "mathematical proofs",
        "how do you find the percentage of this number"
    ],
)

coding_route = Route(
    name="coding",
    utterances=[
        "how to write a for loop in Python",
        "explain the use of classes in Java",
        "what is recursion in programming",
        "how do i optimise this problem using hash tables",
        "suggest a more efficient data structure for this problem"
    ],
)

# List of all routes
routes = [math_route, coding_route]

"""We initialize our `RouteLayer` with our `encoder` and `routes`. We can use popular encoder APIs like `CohereEncoder` and `OpenAIEncoder`, or local alternatives like `FastEmbedEncoder`."""

import os
from getpass import getpass
from semantic_router import RouteLayer
from semantic_router.encoders import CohereEncoder, OpenAIEncoder

# dashboard.cohere.ai
# os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY") or getpass(
#     "Enter Cohere API Key: "
# )
# platform.openai.com
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or getpass(
    "Enter OpenAI API Key: "
)

# encoder = CohereEncoder()
encoder = OpenAIEncoder()

rl = RouteLayer(encoder=encoder, routes=routes)

"""We run the solely static routes layer:"""

rl("Solve the equation 5-x=12 for x?")

from unify import Unify
# Environment setup for API keys
os.environ["UNIFY_KEY"] = os.getenv("UNIFY_KEY") or getpass("Enter Unify API Key: ")

#Unify process query
def process_query(query):
    route_choice = rl(query)
    print(f"Route chosen: {route_choice.name}")

    if route_choice.name == "math":
        # Initialize Unify with the endpoint for math queries
        unify = Unify(
            api_key=os.environ["UNIFY_KEY"],
            endpoint="gpt-4@anyscale"  # Use the correct endpoint for math queries
        )
        # Generate the response using Unify
        response = unify.generate(user_prompt=query)
        return response

    elif route_choice.name == "coding":
        # Initialize Unify with the endpoint for coding queries
        unify = Unify(
            api_key=os.environ["UNIFY_KEY"],
            endpoint="deepseek-coder-33b-instruct@anyscale"  # Use the correct endpoint for coding queries
        )
        # Generate the response using Unify
        response = unify.generate(user_prompt=query)
        return response

    else:
        return "This query does not fall under a supported category."

# Process query test
process_query("Solve the equation 5-x=12 for x?")

"""## Creating a Dynamic Route

As with static routes, we must create a dynamic route before adding it to our route layer. To make a route dynamic, we need to provide a `function_schema`. The function schema provides instructions on what a function is, so that an LLM can decide how to use it correctly.
"""

from datetime import datetime
from zoneinfo import ZoneInfo


def get_time(timezone: str) -> str:
    """Finds the current time in a specific timezone.

    :param timezone: The timezone to find the current time in, should
        be a valid timezone from the IANA Time Zone Database like
        "America/New_York" or "Europe/London". Do NOT put the place
        name itself like "rome", or "new york", you must provide
        the IANA format.
    :type timezone: str
    :return: The current time in the specified timezone."""
    now = datetime.now(ZoneInfo(timezone))
    return now.strftime("%H:%M")

get_time("America/New_York")

"""To get the function schema we can use the `get_schema` function from the `function_call` module."""

from semantic_router.utils.function_call import get_schema

schema = get_schema(get_time)
print(schema)

"""We use this to define our dynamic route:"""

time_route = Route(
    name="get_time",
    utterances=[
        "what is the time in new york city?",
        "what is the time in london?",
        "I live in Rome, what time is it?",
    ],
    function_schema=schema,
)

"""Add the new route to our `layer`:"""

rl.add(time_route)

"""Now we can ask our layer a time related question to trigger our new dynamic route."""

out = rl("what is the time in new york city?")
get_time(**out.function_call)

"""Our dynamic route provides both the route itself _and_ the input parameters required to use the route.

---
"""
