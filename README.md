# prompteng

This repo gives a scaffold for trying out different prompts for LLMs and measuring their performance.

## Get started

0. Make sure you have an Azure OpenAI deployment [set up](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-python) with a deployed gpt-35-turbo model.
1. Clone this repo
2. Install the requirements: `pip install -r requirements.txt`. You may want to do this in a virtual environment. To do this with conda, run `conda create -n prompteng python=3.9` and then `conda activate prompteng`.
3. Create an `.env` file in the root of this repo with the following contents:

```
OPENAI_API_BASE=<https://<Your Azure Resource Name>.openai.azure.com>
OPENAI_API_KEY=<your openai api key>
```

4. Make sure you are running Redis for Motion. You can do this by running the Redis docker container: `docker run -p 6379:6379 --name motion redis/redis-stack-server:latest`. If you don't have docker, you can install it [here](https://docs.docker.com/get-docker/).
5. Run `python travelagent.py` to run the sample code, which tests out different prompts for creating a travel itinerary on a set of example places.
6. See your results in the `results` folder.

## How it works

The `travelagent.py` script runs a series of prompts for creating a travel itinerary on a set of example places. The outputs of chat gpt are saved in the `results` folder.

The Motion component `TravelAgent` in `components/travelagent.py` simply runs the chatgpt model on the prompt and returns the output. The `TravelAgent` component is used in the `travelagent.py` script.

The only thing Motion is useful for here is caching results (24 hour expiry for now, but you can pass in a [`cache_ttl`](https://dm4ml.github.io/motion/api/component-instance/#motion.instance.ComponentInstance.run) parameter into your calls to `run` or `arun`). Results are cached in Redis, based on the prompt value and the input.
