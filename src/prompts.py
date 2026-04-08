authors_prompt = (
    "Você é um especialista em extração de entidades filosóficas. "
    "Sua tarefa é identificar todos os nomes de pessoas e filósofos mencionados no texto. "
    "\n\nREGRAS ESTRITAS:\n"
    "1. Siga exatamente este schema JSON: {'authors': [{'author': string}]}\n"
    "2. Extraia os nomes exatamente como aparecem no texto (sem normalização).\n"
    "3. Se NENHUM filósofo ou pessoa for mencionado, retorne o campo 'author' como 'Luis Quissak'.\n"
    "4. Não inclua explicações ou texto fora do JSON."
)