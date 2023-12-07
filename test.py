from llm_helper import model

llm=model()
llm.cut_data_fit_input_limit(0,30)

# Initial Prompt for system, assitant, user
system_prompt = "You are a child development doctor. Your goal is to give a score from 1 to 5 by user's sentence"
ai_prompt = 'Describe a situation in which you and the child focus on a common activity or object.'

# Avoid user no input
user_prompt = 'I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable.'

#"I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable."

# Using model
_, score = llm.model_for_score(system_prompt, ai_prompt, user_prompt)
score = int(str(score).split(' ')[-1][:-1])

print(score)
