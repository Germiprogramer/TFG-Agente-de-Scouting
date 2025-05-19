import streamlit as st
import pandas as pd
import os
from langchain.llms import HuggingFaceHub
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools.python.tool import PythonREPLTool  # ✅ actualizado
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # Asegúrate de tener configurada esta variable de entorno o pasarla directamente
    huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not huggingface_api_key:
        st.error("No se ha encontrado la clave de HuggingFace. Añádela al archivo .env como HUGGINGFACEHUB_API_TOKEN")
        return

    st.set_page_config(page_title="Agente CSV gratuito")
    st.header("Agente CSV 🧠 (Gratis con Hugging Face)")

    csv_file = st.file_uploader("Sube un archivo CSV", type="csv")

    if csv_file is not None:
        df = pd.read_csv(csv_file)
        st.dataframe(df.head())

        # Crear LLM gratuito de Hugging Face (FLAN-T5 base)
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            model_kwargs={"temperature": 0, "max_length": 512}
        )

        # Crear agente sobre el DataFrame con herramientas pandas
        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

        pregunta = st.text_input("Hazle una pregunta a tu CSV:")

        if pregunta:
            with st.spinner("Pensando..."):
                try:
                    respuesta = agent.run(pregunta)
                    st.success(respuesta)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
