import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

llm_name = "gpt-3.5-turbo"

model = ChatOpenAI(api_key=openai_key, model=llm_name)

df = pd.read_csv("datos/datos_jugadores_v4/jugadores_total.csv")

from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
    create_csv_agent,
)

agent = create_pandas_dataframe_agent(
    llm=model,
    df=df,
    verbose=True,
)

res = agent.invoke("how many rows are there in the dataframe?")

print(res)

