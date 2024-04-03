import traceback

import agenthub.monologue_agent.utils.json as json
import agenthub.monologue_agent.utils.prompts as prompts
from opendevin.llm.llm import LLM       # TODOO added just to support LLM type
from typing import Any

class Monologue:
    def __init__(self) -> None:
        self.thoughts: list[dict[str, Any]] = []        # TODOO can dict value be ANY? 'str' looks OK, but ANY? may be it can be another dict? they yes

    def add_event(self, t: dict[str, Any]) -> None:
        if not isinstance(t, dict):
            raise ValueError("Event must be a dictionary")
        self.thoughts.append(t)

    def get_thoughts(self) -> list[dict[str, Any]]:
        return self.thoughts

    def get_total_length(self) -> int:
        total_length = 0
        for t in self.thoughts:
            try:
                total_length += len(json.dumps(t))
            except TypeError as e:
                print(f"Error serializing thought: {e}")
        return total_length

    def condense(self, llm: LLM) -> None:       # TODOO LLM is not know here
        try:
            prompt = prompts.get_summarize_monologue_prompt(self.thoughts)
            messages = [{"content": prompt,"role": "user"}]
            resp = llm.completion(messages=messages)
            summary_resp = resp['choices'][0]['message']['content']
            self.thoughts = prompts.parse_summary_response(strip_markdown(summary_resp))
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Error condensing thoughts: {e}")

def strip_markdown(markdown_json: str) -> str:
    # remove markdown code block
    return markdown_json.replace('```json\n', '').replace('```', '').strip()