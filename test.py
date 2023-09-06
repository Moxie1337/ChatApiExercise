from pathlib import Path
import json

import openai

openai_conf_ = json.loads(Path("config/openai.json").read_text())
openai.api_base = openai_conf_.get("api_base")
openai.api_key = openai_conf_.get("api_key")


completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
         {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": "Hello!"}
      ]
   )

print(completion.get("choices")[0].message.content)