from datasets import load_dataset
import google.generativeai as genai

# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

"""
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
"""

# Given some function(s), create an unrelated prompt and explain why it's unrelated.
def generate_relevance_detection(functions):
	prompt_template = """
	"You are exceptionally skilled at analyzing code. I want you to read the following random function(s) and create a short prompt that is not related to the function(s). Present your output in two distinct sections: [Prompt] and [Output].

	Random function(s):
	{code}

	Guidelines for each section:
	1. [Prompt]: This should be some kind of short prompt that is not related to the provided function(s), but would still require some kind of function/API use.
	2. [Output]: Provide a brief one sentence explanation why the [Prompt] you provided is unrelated to the given function(s).
	"""
	prompt = prompt_template.format(code=functions)
	response = model.generate_content(prompt)
	return response.text

def main():

    dataset = load_dataset('json', data_files='t.json', split="train")
    for example in dataset:
        functions = str(example['Functions'])
        #print(functions)
        g = generate_relevance_detection(functions)
        #print(g)

if __name__ == "__main__":
    main()