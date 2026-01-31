#!/usr/bin/env python3
"""
Convert use_case2 JSON to YAML format similar to use_case1
Includes routing logic from checkerlogic_20260130_with_routing.json
"""

import json
import yaml
from typing import Dict, Any, List

def load_json(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_yaml_structure(content_data: Dict, routing_data: Dict = None) -> Dict:
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

    # Get routing logic if available
    routing_logic = routing_data.get('questions_logic', {}) if routing_data else {}

    # Convert questions
    for qid, q_data in content_data['questions_content'].items():
        question_entry = {
            'id': qid,
            'question': q_data.get('secondary_title', q_data.get('main_title', '')),
            'info': q_data.get('info', ''),
            'type': 'single_choice' if len(q_data.get('answers', {})) <= 3 else 'multiple_choice',
            'sources': q_data.get('sources', ''),
            'options': []
        }

        # Get routing for this question
        q_routing = routing_logic.get(qid, {})

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

        # Add routing from routing JSON
        if q_routing and 'routing' in q_routing:
            question_entry['routing'] = q_routing['routing']

        # Add answer flags from routing JSON
        if q_routing and 'answers' in q_routing:
            for ans_key, ans_flags in q_routing['answers'].items():
                if 'set_flags' in ans_flags:
                    # Find matching option and add flags
                    for opt in question_entry['options']:
                        if opt['value'] == ans_key:
                            opt['set_flags'] = ans_flags['set_flags']
                            break

        yaml_data['questionnaire'][qid] = question_entry

    # Convert flags/results
    for flag_id, flag_content in content_data['flags_content'].items():
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

def analyze_routing(routing_data: Dict) -> Dict:
    """Analyze routing data for optimization summary"""
    questions_logic = routing_data.get('questions_logic', {})

    stats = {
        'total_questions': len(questions_logic),
        'end_points': 0,
        'qais_questions': 0,
        'qgpai_questions': 0,
        'condition_types': set()
    }

    for qid, q_data in questions_logic.items():
        if qid.startswith('QAIS'):
            stats['qais_questions'] += 1
        elif qid.startswith('QGPAI'):
            stats['qgpai_questions'] += 1

        for route in q_data.get('routing', []):
            if route.get('go_to') == 'END':
                stats['end_points'] += 1
            for cond in route.get('conditions', []):
                for key in cond.keys():
                    stats['condition_types'].add(key)

    stats['condition_types'] = list(stats['condition_types'])
    return stats

def main():
    # Load JSON files
    content_data = load_json('checkerlogic_20260130.json')
    routing_data = load_json('checkerlogic_20260130_with_routing.json')

    # Analyze routing
    stats = analyze_routing(routing_data)
    print("\n=== Routing Analysis ===")
    print(f"Total questions with routing: {stats['total_questions']}")
    print(f"QAIS questions: {stats['qais_questions']}")
    print(f"QGPAI questions: {stats['qgpai_questions']}")
    print(f"END terminal states: {stats['end_points']}")
    print(f"Condition types: {stats['condition_types']}")

    # Convert to YAML structure with routing
    yaml_data = convert_to_yaml_structure(content_data, routing_data)

    # Write original YAML (with routing)
    with open('original_checker_ec.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

    print(f"\nConverted {len(yaml_data['questionnaire'])} questions")
    print(f"Converted {len(yaml_data['results'])} result flags")
    print("Output: original_checker_ec.yaml")

    # Also show question flow summary
    print("\n=== Question Flow Summary ===")
    for qid in list(yaml_data['questionnaire'].keys())[:10]:
        q = yaml_data['questionnaire'][qid]
        has_routing = 'Yes' if 'routing' in q else 'No'
        print(f"{qid}: {q['question'][:40]}... ({len(q['options'])} options, routing: {has_routing})")

if __name__ == '__main__':
    main()
