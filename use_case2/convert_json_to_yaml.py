#!/usr/bin/env python3
"""
Convert use_case2 JSON to YAML format similar to use_case1
"""

import json
import yaml
from typing import Dict, Any, List

def load_json(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_yaml_structure(data: Dict) -> Dict:
    """Convert JSON structure to YAML format similar to use_case1"""

    yaml_data = {
        'metadata': {
            'title': "EU AI Act Compliance Checker (EC Service Desk)",
            'version': "1.0",
            'source': "https://ai-act-service-desk.ec.europa.eu/en/eu-ai-act-compliance-checker",
            'updated': "2026-01-30",
            'purpose': "Determine obligations under the EU AI Act for AI systems and models"
        },
        'questionnaire': {},
        'results': {},
        'obligations': {}
    }

    # Convert questions
    for qid, q_data in data['questions_content'].items():
        question_entry = {
            'id': qid,
            'question': q_data.get('secondary_title', q_data.get('main_title', '')),
            'info': q_data.get('info', ''),
            'type': 'single_choice' if len(q_data.get('answers', {})) <= 3 else 'multiple_choice',
            'sources': q_data.get('sources', ''),
            'options': []
        }

        # Convert answers
        for ans_key, ans_data in q_data.get('answers', {}).items():
            option = {
                'value': ans_key,
                'label': ans_data.get('label', ''),
                'help': ans_data.get('help', '')
            }

            # Add next question if specified
            if 'next_question' in ans_data:
                option['next'] = ans_data['next_question']

            # Add flags if specified
            if 'flags' in ans_data:
                option['flags'] = ans_data['flags']

            question_entry['options'].append(option)

        yaml_data['questionnaire'][qid] = question_entry

    # Convert flags/results
    for flag_id, flag_content in data['flags_content'].items():
        if isinstance(flag_content, str):
            yaml_data['results'][flag_id] = {
                'id': flag_id,
                'description': flag_content
            }
        elif isinstance(flag_content, dict):
            yaml_data['results'][flag_id] = {
                'id': flag_id,
                'title': flag_content.get('title', ''),
                'description': flag_content.get('description', flag_content.get('content', ''))
            }

    return yaml_data

def main():
    # Load JSON
    json_data = load_json('checkerlogic_20260130.json')

    # Convert to YAML structure
    yaml_data = convert_to_yaml_structure(json_data)

    # Write YAML
    with open('original_checker_ec.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

    print(f"Converted {len(yaml_data['questionnaire'])} questions")
    print(f"Converted {len(yaml_data['results'])} result flags")
    print("Output: original_checker_ec.yaml")

    # Also show question flow summary
    print("\n=== Question Flow Summary ===")
    for qid in list(yaml_data['questionnaire'].keys())[:10]:
        q = yaml_data['questionnaire'][qid]
        print(f"{qid}: {q['question'][:50]}... ({len(q['options'])} options)")

if __name__ == '__main__':
    main()
