import pandas as pd

ground_truths = {
    "Who are the 5 defensive midfielders with the highest pass completion rate, taller than 180 cm, and worth under 2 million euros?": ["Julian Weigl", "Rodrigo Hernández Cascante", "José Vicente Gómez Umpiérrez", "Seydou Keita", "Joan Jordán Moreno"],
    "Which goalkeeper has the highest penalty save percentage?": ["Yassine Bounou", "Emiliano Martínez", "Alisson Becker"],
    "Show me the winger with the most progressive carries per 90": ["Vinícius Júnior", "Moussa Diaby", "Khvicha Kvaratskhelia"]
}

def evaluate_agent_answer(question, agent_answer):
    expected_players = ground_truths.get(question, [])
    expected_players = [p.lower() for p in expected_players]
    answer = agent_answer.lower()
    is_correct = any(player in answer for player in expected_players)
    return is_correct


# Evaluación basada en si menciona al menos un jugador correcto
def check_if_correct(row):
    answer = row["agent_answer"].lower()
    expected_players = [p.lower() for p in row["expected_players"]]
    return any(player in answer for player in expected_players)

# Lista para registrar interacciones
historial = []

# Tras cada respuesta:
historial.append({
    "question": user_question,
    "agent_answer": agent_answer,
    "is_correct": is_correct
})

# Puedes mostrar o exportar:
df_historial = pd.DataFrame(historial)
st.dataframe(df_historial)
