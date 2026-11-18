"""Record a real, reproducible local AI critique of the disclosed assisted journey."""
import json
from pathlib import Path
import httpx

root = Path(__file__).resolve().parent.parent
thinking = (root / 'THINKING.md').read_text(encoding='utf-8')
journey = thinking.split('## User journey\n', 1)[1].split('## AI challenge', 1)[0]
prompt = ('Act as a skeptical shop-floor supervisor and product manager. Critique this AI-assisted journey. '
          'This journey was developed with AI assistance. '
          'Give four concrete risks and four practical changes. Focus on mobile use, source trust, '
          'unclear questions, safety exceptions, revision control and failed connectivity. '
          'Keep your response under 350 words.\n\n' + journey)
response = httpx.post('http://127.0.0.1:11434/api/chat', json={
    'model': 'qwen3:4b', 'think': False, 'stream': False,
    'options': {'temperature': 0, 'num_ctx': 4096, 'num_predict': 1024},
    'messages': [{'role': 'user', 'content': prompt}],
}, timeout=240)
response.raise_for_status()
answer = response.json()['message']['content']
answer = answer.split('</think>')[-1].strip()
answer = answer.split('**Why this works on the floor**')[0].strip()
log_dir = root / 'backend/data/logs'
log_dir.mkdir(parents=True, exist_ok=True)
(log_dir / 'journey-critique.txt').write_text('Prompt:\n' + prompt + '\n\nResponse:\n' + answer + '\n', encoding='utf-8')
print(answer)
