"""Copy the five saved additional evaluation responses into the project README."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8').split('\n## Five additional questions and actual app answers')[0]
results = json.loads((root / 'backend/evaluation-results.json').read_text(encoding='utf-8'))
parts = ['\n## Five additional questions and actual app answers\n',
         'Recorded outputs from 12 November 2026. Bracketed numbers identify source cards for that individual request.\n']
for number, result in enumerate(results[5:], 1):
    parts.append(f"### {number}. {result['question']}\n")
    if result['history']:
        parts.append('Mode: include superseded revisions for this comparison.\n')
    parts.append('**Actual app answer:** ' + result['answer'] + '\n')
    sources = ', '.join(dict.fromkeys(f"{s['file']}, page {s['page']}" for s in result['sources']))
    parts.append('Sources: ' + (sources or 'None; the requested specification is absent from the supplied documents.') + '\n')
suffix = readme.read_text(encoding='utf-8').split('## Use from a phone on the same Wi-Fi', 1)[1]
readme.write_text(text + '\n'.join(parts) + '## Use from a phone on the same Wi-Fi' + suffix, encoding='utf-8')
