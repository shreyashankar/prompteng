from components import TravelAgent, LLMRequest

import asyncio
import hashlib
import pandas as pd

from rich import print
from datetime import datetime

import time

EXAMPLES = [
    "Paris",
    "London",
    "New York",
    "Tokyo",
    "Sydney",
    "Berlin",
    "Moscow",
    "Rome",
    "Madrid",
    "Beijing",
    "Cairo",
    "Rio de Janeiro",
    "Buenos Aires",
    "Mexico City",
    "Lima",
    "Santiago",
    "Toronto",
    "Vancouver",
]

PROMPT_TEMPLATES = [
    "write an itinerary for {example}",
    "write an itinerary for a vacation in {example}",
    "write a detailed 3-day travel guide for {example}",
]


async def main():
    # Initialize the travel agents
    travel_agents = []
    for template in PROMPT_TEMPLATES:
        # Create name as a hash of the template
        # This is so, for successive runs, we can reuse the same
        # outputs if the template is the same
        h = hashlib.new("md5")
        h.update(template.encode("utf-8"))
        instance_name = h.hexdigest()

        travel_agents.append(
            TravelAgent(
                name=instance_name,
                init_state_params={"prompt_template": template},
            )
        )

    # Run the travel agents to get their performances
    print(
        f"Running {len(travel_agents)} travel agents on {len(EXAMPLES)} examples each..."
    )
    agent_tasks = []
    for travel_agent in travel_agents:
        agent_tasks += [
            travel_agent.arun(example=LLMRequest(place=example))
            for example in EXAMPLES
        ]

        # If you don't want to use the cache, you can include the
        # ignore_cache=True param
        # agent_tasks += [
        #     travel_agent.arun(example=LLMRequest(place=example, ignore_cache=True))
        #     for example in EXAMPLES
        # ]

    # Await the results
    results = await asyncio.gather(*agent_tasks)
    result_df = pd.DataFrame(results)
    out_file = f"results/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    result_df.to_csv(out_file, index=False)
    print(f"Results saved to {out_file}")

    total_cost = result_df["cost"].sum()
    print(
        f"Total cost: ${total_cost:.2f} (might be less if cached w/ 24 hour expiry)"
    )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Total time: {end - start:.2f} seconds")
