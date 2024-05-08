from flask import Flask, render_template, request

import os
import anthropic

# Set your Anthropic API key
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

def query_claude(prompt):
    # Construct the full prompt
    message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0.0,
    system="A patient just suffered brain injury and his details are below, respond with a diagnosis. Do not include a disclaimer, as a Glasgow Coma scale test has already been done.",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    
    return message.content

app = Flask(__name__, static_url_path='', static_folder="static")

name = "CogniTest"

@app.route('/')
def index():
  return render_template('index.html', name = name)

@app.route('/prelim', methods=['GET'])
def prelim():
    return render_template('prelim.html', name = name)

@app.route('/detailed', methods=['GET'])
def detailed():
    return render_template('detailed.html', name = name)

@app.route('/ai_diagnosis', methods=['GET'])
def ai_diagnosis():
   reaction_time = request.args.get("reaction")
   memory = request.args.get("memory")

  #  client = claude_client.ClaudeClient(api_key)

  #  organizations = client.get_organizations()
  #  # You can omit passing in the organization uuid and the wrapper will assume
  #  # you will use the first organization instead.
  #  claude_obj = claude_wrapper.ClaudeWrapper(client, organization_uuid=organizations[0]['uuid'])
   
  #  new_conversation_data = claude_obj.start_new_conversation("New Conversation", f"patient just suffered brain injury, respond with diagnosis. reaction time: {reaction_time}ms memory game: {memory}/5 numbers remembered (3 second gap)")
  #  conversation_uuid = new_conversation_data['uuid']
  #  # You can get the response from the initial message you sent with:
  #  initial_response = new_conversation_data['response']
   ai_diagnosis = query_claude(f"reaction time: {reaction_time}ms memory game: {memory}/5 numbers remembered (3 second gap)")
   print(ai_diagnosis)
   ai_diagnosis = f"{ai_diagnosis[0]}"[16:-15]
   ai_diagnosis = bytes(ai_diagnosis, "utf-8").decode("unicode_escape")



   return render_template("ai_diagnosis.html", name = name, ai_diagnosis = ai_diagnosis)



if __name__ == '__main__':
  app.run(debug=True)
