# test_cases.py - Comprehensive test cases

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestCase:
    """Test case definition"""
    name: str
    description: str
    answers: Dict[str, Any]
    expected_questions: int
    expected_flags: Dict[str, bool]
    expected_obligations: List[str]
    expected_result: str
    category: str

# Test case definitions
TEST_CASES = [
    # ===== EDGE CASES =====
    TestCase(
        name="edge_case_1_out_of_scope",
        description="Out of scope - fastest path (1 question)",
        answers={'Q1': 'no_eu_connection'},
        expected_questions=1,
        expected_flags={'flag_out_of_scope': True},
        expected_obligations=[],
        expected_result='OUT_OF_SCOPE',
        category='edge_cases'
    ),
    
    TestCase(
        name="edge_case_2_prohibited_social_scoring",
        description="Prohibited system - social scoring (4 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['social_scoring_public']
        },
        expected_questions=4,
        expected_flags={
            'flag_prohibited': True,
            'flag_is_provider': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='PROHIBITED',
        category='edge_cases'
    ),
    
    TestCase(
        name="edge_case_3_excluded_personal_use",
        description="Excluded - personal use (3 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['personal_non_professional']
        },
        expected_questions=3,
        expected_flags={
            'flag_excluded': True,
            'flag_is_deployer': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='EXCLUDED',
        category='edge_cases'
    ),
    
    TestCase(
        name="edge_case_4_excluded_research",
        description="Excluded - research only (3 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['research_only']
        },
        expected_questions=3,
        expected_flags={
            'flag_excluded': True,
            'flag_is_provider': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='EXCLUDED',
        category='edge_cases'
    ),
    
    TestCase(
        name="edge_case_5_excluded_open_source",
        description="Excluded - open source not deployed (3 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['open_source_not_deployed']
        },
        expected_questions=3,
        expected_flags={
            'flag_excluded': True,
            'flag_is_provider': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='EXCLUDED',
        category='edge_cases'
    ),
    
    # ===== COMMON CASES =====
    TestCase(
        name="common_case_1_provider_high_risk_employment",
        description="Provider of high-risk employment AI (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_iii_employment'],
            'Q6B': 'yes_significant',
            'Q7': ['interact_with_people']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_high_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_provider_high_risk',
            'obligation_transparency_natural_persons'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='common_cases'
    ),
    
    TestCase(
        name="common_case_2_deployer_non_high_risk_chatbot",
        description="Deployer of non-high-risk chatbot (6 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['none'],
            'Q7': ['interact_with_people']
        },
        expected_questions=6,
        expected_flags={
            'flag_is_deployer': True,
            'flag_high_risk': False
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_transparency_natural_persons'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='common_cases'
    ),
    
    TestCase(
        name="common_case_3_gpai_systemic_risk",
        description="GPAI model with systemic risk (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'yes_gpai',
            'Q5A': 'yes_systemic',
            'Q6': ['none'],
            'Q7': ['generate_synthetic_content']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_gpai': True,
            'flag_gpai_systemic_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_gpai_base',
            'obligation_gpai_systemic',
            'obligation_transparency_synthetic_content'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='common_cases'
    ),
    
    TestCase(
        name="common_case_4_gpai_no_systemic_risk",
        description="GPAI model without systemic risk (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'yes_gpai',
            'Q5A': 'no_systemic',
            'Q6': ['none'],
            'Q7': ['none']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_gpai': True,
            'flag_gpai_systemic_risk': False
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_gpai_base'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='common_cases'
    ),
    
    # ===== COMPLEX CASES =====
    TestCase(
        name="complex_case_1_product_manufacturer_medical",
        description="Product manufacturer with high-risk medical device (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['product_manufacturer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_i_section_a'],
            'Q6A': 'yes_required',
            'Q7': ['none']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_product_manufacturer': True,
            'flag_becomes_provider': True,
            'flag_is_provider': True,
            'flag_high_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_provider_high_risk'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='complex_cases'
    ),
    
    TestCase(
        name="complex_case_2_deployer_becomes_provider",
        description="Deployer modifies system → becomes provider (9 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_iii_biometrics'],
            'Q6B': 'yes_significant',
            'Q7': ['emotion_recognition'],
            'Q8': ['substantial_modification'],
            'Q9': 'yes_public'
        },
        expected_questions=9,
        expected_flags={
            'flag_is_deployer': True,
            'flag_becomes_provider': True,
            'flag_is_provider': True,
            'flag_high_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_handover',
            'obligation_deployer_high_risk',
            'obligation_provider_high_risk',
            'obligation_transparency_emotion_biometric',
            'obligation_fundamental_rights_assessment'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='complex_cases'
    ),
    
    TestCase(
        name="complex_case_3_high_risk_law_enforcement",
        description="High-risk law enforcement system (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_iii_law_enforcement'],
            'Q6B': 'yes_significant',
            'Q7': ['none']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_high_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_provider_high_risk'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='complex_cases'
    ),
    
    # ===== REGRESSION TESTS =====
    TestCase(
        name="regression_1_medical_no_third_party",
        description="Medical device NOT requiring 3rd party assessment (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_i_section_a'],
            'Q6A': 'no_or_opt_out',
            'Q6B': 'no_significant',
            'Q7': ['none']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_high_risk': False
        },
        expected_obligations=[
            'obligation_ai_literacy'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='regression_tests'
    ),
    
    TestCase(
        name="regression_2_multiple_transparency",
        description="System with multiple transparency obligations (6 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['none'],
            'Q7': ['interact_with_people', 'generate_synthetic_content']
        },
        expected_questions=6,
        expected_flags={
            'flag_is_provider': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_transparency_natural_persons',
            'obligation_transparency_synthetic_content'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='regression_tests'
    ),
    
    TestCase(
        name="regression_3_critical_infrastructure",
        description="High-risk critical infrastructure system (7 questions)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider', 'deployer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['annex_iii_critical_infra'],
            'Q6B': 'yes_significant',
            'Q7': ['none']
        },
        expected_questions=7,
        expected_flags={
            'flag_is_provider': True,
            'flag_is_deployer': True,
            'flag_high_risk': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_provider_high_risk',
            'obligation_deployer_high_risk'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='regression_tests'
    ),
    
    # ===== PROHIBITED FUNCTION TESTS =====
    TestCase(
        name="prohibited_1_subliminal_manipulation",
        description="Prohibited - subliminal manipulation",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['subliminal_manipulation']
        },
        expected_questions=4,
        expected_flags={
            'flag_prohibited': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='PROHIBITED',
        category='prohibited_tests'
    ),
    
    TestCase(
        name="prohibited_2_exploit_vulnerabilities",
        description="Prohibited - exploiting vulnerabilities",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['provider'],
            'Q3': ['none'],
            'Q4': ['exploit_vulnerabilities']
        },
        expected_questions=4,
        expected_flags={
            'flag_prohibited': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='PROHIBITED',
        category='prohibited_tests'
    ),
    
    TestCase(
        name="prohibited_3_realtime_biometric",
        description="Prohibited - real-time biometric ID",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['none'],
            'Q4': ['realtime_remote_biometric_public']
        },
        expected_questions=4,
        expected_flags={
            'flag_prohibited': True
        },
        expected_obligations=['obligation_ai_literacy'],
        expected_result='PROHIBITED',
        category='prohibited_tests'
    ),
    
    # ===== TRANSPARENCY OBLIGATION TESTS =====
    TestCase(
        name="transparency_1_deepfake",
        description="Transparency - deepfake content",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['none'],
            'Q7': ['deepfake']
        },
        expected_questions=6,
        expected_flags={
            'flag_is_deployer': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_transparency_content_resemblance'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='transparency_tests'
    ),
    
    TestCase(
        name="transparency_2_emotion_recognition",
        description="Transparency - emotion recognition (non-high-risk)",
        answers={
            'Q1': 'has_eu_connection',
            'Q2': ['deployer'],
            'Q3': ['none'],
            'Q4': ['none'],
            'Q5': 'no_gpai',
            'Q6': ['none'],
            'Q7': ['emotion_recognition']
        },
        expected_questions=6,
        expected_flags={
            'flag_is_deployer': True
        },
        expected_obligations=[
            'obligation_ai_literacy',
            'obligation_transparency_emotion_biometric'
        ],
        expected_result='COMPLIANCE_REQUIRED',
        category='transparency_tests'
    )
]

def get_test_cases_by_category(category: str) -> List[TestCase]:
    """Get test cases for specific category"""
    return [tc for tc in TEST_CASES if tc.category == category]

def get_all_categories() -> List[str]:
    """Get list of all test categories"""
    return list(set(tc.category for tc in TEST_CASES))