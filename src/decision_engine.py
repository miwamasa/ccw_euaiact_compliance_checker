# decision_engine.py - Optimized Decision Engine for EU AI Act

from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Any, Tuple
from enum import Enum
from optimizer import State, Answer, Question, QuestionType, DecisionTreeOptimizer

class DecisionResult(Enum):
    OUT_OF_SCOPE = "out_of_scope"
    EXCLUDED = "excluded"
    PROHIBITED = "prohibited"
    COMPLIANCE_REQUIRED = "compliance_required"

@dataclass
class ComplianceResult:
    """Final compliance determination"""
    result: DecisionResult
    flags: Dict[str, bool]
    obligations: Set[str]
    questions_asked: int
    path_taken: List[str]
    explanation: str

class OptimizedDecisionEngine:
    """Optimized decision engine for EU AI Act compliance"""
    
    def __init__(self):
        self.optimizer = DecisionTreeOptimizer()
        self.questions = self._initialize_questions()
        self._initialize_inference_rules()
        self.current_state = State()
        self.path: List[str] = []
        
    def _initialize_questions(self) -> Dict[str, Question]:
        """Initialize optimized question set"""
        questions = {
            'Q1': Question(
                id='Q1',
                question_text='Does your AI system have ANY connection to the EU?',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'no_eu_connection', 'label': 'No - System not placed on EU market, not used in EU, I\'m not in EU', 'terminal': True},
                    {'value': 'has_eu_connection', 'label': 'Yes - At least one of: placed on EU market, used in EU, I\'m in EU'}
                ],
                priority=1,
                information_gain=0.85,
                terminal_probability=0.30
            ),
            
            'Q2': Question(
                id='Q2',
                question_text='What is your primary role with this AI system?',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'provider', 'label': 'Provider - I develop/place the system on market under my name'},
                    {'value': 'deployer', 'label': 'Deployer - I use/operate the system'},
                    {'value': 'distributor', 'label': 'Distributor - I make available on EU market'},
                    {'value': 'importer', 'label': 'Importer - I\'m in EU, placing system from outside EU'},
                    {'value': 'product_manufacturer', 'label': 'Product Manufacturer - AI integrated into my product'},
                    {'value': 'authorised_representative', 'label': 'Authorised Representative', 'terminal': True}
                ],
                priority=2,
                information_gain=0.92
            ),
            
            'Q3': Question(
                id='Q3',
                question_text='Does your system fall under ANY of these exclusion categories?',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'military_only', 'label': 'Exclusively for military purposes', 'terminal': True},
                    {'value': 'personal_non_professional', 'label': 'Personal, non-professional use only', 'terminal': True},
                    {'value': 'research_only', 'label': 'Scientific research & development only', 'terminal': True},
                    {'value': 'open_source_not_deployed', 'label': 'Open source, not yet placed on market', 'terminal': True},
                    {'value': 'third_country_law_enforcement', 'label': 'Third country authority', 'terminal': True},
                    {'value': 'none', 'label': 'None of these apply'}
                ],
                priority=3,
                information_gain=0.78,
                terminal_probability=0.15
            ),
            
            'Q4': Question(
                id='Q4',
                question_text='Does your system perform ANY of these PROHIBITED functions?',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'subliminal_manipulation', 'label': 'Subliminal manipulation', 'terminal': True},
                    {'value': 'exploit_vulnerabilities', 'label': 'Exploiting vulnerabilities', 'terminal': True},
                    {'value': 'social_scoring_public', 'label': 'Social scoring', 'terminal': True},
                    {'value': 'predictive_policing_individual', 'label': 'Predictive policing', 'terminal': True},
                    {'value': 'scraping_facial_recognition', 'label': 'Facial recognition scraping', 'terminal': True},
                    {'value': 'emotion_recognition_workplace', 'label': 'Emotion recognition in workplace', 'terminal': True},
                    {'value': 'biometric_categorization_sensitive', 'label': 'Biometric categorization', 'terminal': True},
                    {'value': 'realtime_remote_biometric_public', 'label': 'Real-time biometric ID', 'terminal': True},
                    {'value': 'none', 'label': 'None - my system does NOT do any of these'}
                ],
                priority=4,
                information_gain=0.95,
                terminal_probability=0.05
            ),
            
            'Q5': Question(
                id='Q5',
                question_text='Are you placing a General Purpose AI MODEL on the EU market?',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'yes_gpai', 'label': 'Yes - I\'m placing a GPAI model on market'},
                    {'value': 'no_gpai', 'label': 'No - I\'m working with AI systems/applications'}
                ],
                priority=5,
                information_gain=0.88
            ),
            
            'Q5A': Question(
                id='Q5A',
                question_text='Does your GPAI model have high-impact capabilities? (>10^25 FLOPs)',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'yes_systemic', 'label': 'Yes - >10^25 FLOPs or Commission-designated'},
                    {'value': 'no_systemic', 'label': 'No - Below threshold'}
                ],
                priority=5.1,
                information_gain=0.82,
                skip_conditions=['Q5_answer != yes_gpai']
            ),
            
            'Q6': Question(
                id='Q6',
                question_text='Does your AI system fall under ANY high-risk category?',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'annex_i_section_a', 'label': 'Annex I Safety Components (Machinery, Medical, etc.)'},
                    {'value': 'annex_i_section_b', 'label': 'Annex I Transport & Aviation'},
                    {'value': 'annex_iii_biometrics', 'label': 'Biometric identification/categorization'},
                    {'value': 'annex_iii_critical_infra', 'label': 'Critical infrastructure'},
                    {'value': 'annex_iii_education', 'label': 'Education & vocational training'},
                    {'value': 'annex_iii_employment', 'label': 'Employment & HR'},
                    {'value': 'annex_iii_essential_services', 'label': 'Access to essential services'},
                    {'value': 'annex_iii_law_enforcement', 'label': 'Law enforcement'},
                    {'value': 'annex_iii_migration', 'label': 'Migration, asylum, border control'},
                    {'value': 'annex_iii_justice', 'label': 'Justice & democracy'},
                    {'value': 'none', 'label': 'None of these categories apply'}
                ],
                priority=6,
                information_gain=0.91
            ),
            
            'Q6A': Question(
                id='Q6A',
                question_text='Is third-party conformity assessment required for your product?',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'yes_required', 'label': 'Yes - third-party conformity assessment required'},
                    {'value': 'no_or_opt_out', 'label': 'No, or I can opt-out per Article 43(3)'}
                ],
                priority=6.1,
                information_gain=0.87,
                skip_conditions=['Q6_answer not in [annex_i_section_a, annex_i_section_b]']
            ),
            
            'Q6B': Question(
                id='Q6B',
                question_text='Does your system pose significant risk to health, safety, or fundamental rights?',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'yes_significant', 'label': 'Yes - poses significant risk (or profiles persons)'},
                    {'value': 'no_significant', 'label': 'No - meets exception criteria'}
                ],
                priority=6.2,
                information_gain=0.84,
                skip_conditions=['Q6_answer == none']
            ),
            
            'Q7': Question(
                id='Q7',
                question_text='What functions does your AI system perform? (Select all that apply)',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'interact_with_people', 'label': 'Interacts directly with people'},
                    {'value': 'generate_synthetic_content', 'label': 'Generates synthetic audio/image/video/text'},
                    {'value': 'emotion_recognition', 'label': 'Emotion recognition or biometric categorization'},
                    {'value': 'deepfake', 'label': 'Generates deepfakes'},
                    {'value': 'text_manipulation_public', 'label': 'Text manipulation for public interest'},
                    {'value': 'none', 'label': 'None of these apply'}
                ],
                priority=7,
                information_gain=0.73
            ),
            
            'Q8': Question(
                id='Q8',
                question_text='Have you made substantial modifications to an existing AI system?',
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    {'value': 'different_trademark', 'label': 'Applied different name/trademark'},
                    {'value': 'changed_purpose', 'label': 'Changed the intended purpose'},
                    {'value': 'substantial_modification', 'label': 'Made substantial modification'},
                    {'value': 'none', 'label': 'No modifications'}
                ],
                priority=8,
                information_gain=0.45,
                skip_conditions=['flag_is_provider == True']
            ),
            
            'Q9': Question(
                id='Q9',
                question_text='Are you a public body or private entity providing public services?',
                question_type=QuestionType.SINGLE_CHOICE,
                options=[
                    {'value': 'yes_public', 'label': 'Yes'},
                    {'value': 'no_private', 'label': 'No'}
                ],
                priority=9,
                information_gain=0.35,
                skip_conditions=['flag_high_risk == False', 'flag_is_deployer == False']
            )
        }
        
        # Register questions with optimizer
        for q in questions.values():
            self.optimizer.add_question(q)
        
        return questions
    
    def _initialize_inference_rules(self):
        """Initialize inference rules for deriving flags and obligations"""
        
        # Rule: Provider → AI Literacy
        self.optimizer.add_inference_rule(
            'provider_ai_literacy',
            lambda s: 'provider' in str(s.get_answer('Q2')),
            {'flag_is_provider': True, 'obligation_ai_literacy': True}
        )
        
        # Rule: Deployer → AI Literacy
        self.optimizer.add_inference_rule(
            'deployer_ai_literacy',
            lambda s: 'deployer' in str(s.get_answer('Q2')),
            {'flag_is_deployer': True, 'obligation_ai_literacy': True}
        )
        
        # Rule: No EU connection → Out of scope
        self.optimizer.add_inference_rule(
            'out_of_scope',
            lambda s: s.get_answer('Q1') == 'no_eu_connection',
            {'flag_out_of_scope': True}
        )
        
        # Rule: Exclusions → Excluded
        self.optimizer.add_inference_rule(
            'excluded',
            lambda s: s.get_answer('Q3') and s.get_answer('Q3') != 'none',
            {'flag_excluded': True}
        )
        
        # Rule: Prohibited functions → Prohibited
        self.optimizer.add_inference_rule(
            'prohibited',
            lambda s: s.get_answer('Q4') and s.get_answer('Q4') != 'none',
            {'flag_prohibited': True}
        )
        
        # Rule: GPAI → GPAI obligations
        self.optimizer.add_inference_rule(
            'gpai_base',
            lambda s: s.get_answer('Q5') == 'yes_gpai',
            {'flag_gpai': True, 'obligation_gpai_base': True}
        )
        
        # Rule: GPAI systemic risk
        self.optimizer.add_inference_rule(
            'gpai_systemic',
            lambda s: s.get_answer('Q5A') == 'yes_systemic',
            {'flag_gpai_systemic_risk': True, 'obligation_gpai_systemic': True}
        )
        
        # Rule: High-risk determination
        self.optimizer.add_inference_rule(
            'high_risk_annex_i',
            lambda s: (s.get_answer('Q6A') == 'yes_required'),
            {'flag_high_risk': True}
        )
        
        self.optimizer.add_inference_rule(
            'high_risk_annex_iii',
            lambda s: (s.get_answer('Q6B') == 'yes_significant'),
            {'flag_high_risk': True}
        )
        
        # Rule: High-risk provider obligations
        self.optimizer.add_inference_rule(
            'provider_high_risk_obligations',
            lambda s: s.get_flag('flag_high_risk') and s.get_flag('flag_is_provider'),
            {'obligation_provider_high_risk': True}
        )
        
        # Rule: High-risk deployer obligations
        self.optimizer.add_inference_rule(
            'deployer_high_risk_obligations',
            lambda s: s.get_flag('flag_high_risk') and s.get_flag('flag_is_deployer'),
            {'obligation_deployer_high_risk': True}
        )
        
        # Rule: Modifications → Becomes provider
        self.optimizer.add_inference_rule(
            'becomes_provider',
            lambda s: s.get_answer('Q8') and s.get_answer('Q8') != 'none',
            {'flag_becomes_provider': True, 'flag_is_provider': True, 'obligation_handover': True}
        )
        
        # Rule: Public body + high-risk → Fundamental rights assessment
        self.optimizer.add_inference_rule(
            'fundamental_rights',
            lambda s: (s.get_answer('Q9') == 'yes_public' and 
                      s.get_flag('flag_high_risk') and 
                      s.get_flag('flag_is_deployer')),
            {'obligation_fundamental_rights_assessment': True}
        )
        
        # Rule: Transparency - Natural persons
        self.optimizer.add_inference_rule(
            'transparency_natural',
            lambda s: 'interact_with_people' in str(s.get_answer('Q7')),
            {'obligation_transparency_natural_persons': True}
        )
        
        # Rule: Transparency - Synthetic content
        self.optimizer.add_inference_rule(
            'transparency_synthetic',
            lambda s: 'generate_synthetic_content' in str(s.get_answer('Q7')),
            {'obligation_transparency_synthetic_content': True}
        )
        
        # Rule: Transparency - Emotion & biometric
        self.optimizer.add_inference_rule(
            'transparency_emotion',
            lambda s: 'emotion_recognition' in str(s.get_answer('Q7')),
            {'obligation_transparency_emotion_biometric': True}
        )
        
        # Rule: Transparency - Content resemblance
        self.optimizer.add_inference_rule(
            'transparency_deepfake',
            lambda s: ('deepfake' in str(s.get_answer('Q7')) or 
                      'text_manipulation_public' in str(s.get_answer('Q7'))),
            {'obligation_transparency_content_resemblance': True}
        )
    
    def get_next_question(self) -> Optional[Question]:
        """Get next question based on current state and optimization"""
        # Check for terminal states
        if self.current_state.get_flag('flag_out_of_scope'):
            return None
        if self.current_state.get_flag('flag_excluded'):
            return None
        if self.current_state.get_flag('flag_prohibited'):
            return None
        
        # Determine next question based on path
        question_order = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q5A', 'Q6', 'Q6A', 'Q6B', 'Q7', 'Q8', 'Q9']
        
        for q_id in question_order:
            # Skip if already answered
            if self.current_state.get_answer(q_id) is not None:
                continue
            
            question = self.questions[q_id]
            
            # Check skip conditions
            skippable, reason = question.is_skippable(self.current_state)
            if skippable:
                continue
            
            # Additional logic for conditional questions
            if q_id == 'Q5A' and self.current_state.get_answer('Q5') != 'yes_gpai':
                continue
            
            if q_id == 'Q6A':
                q6_answer = self.current_state.get_answer('Q6')
                if not q6_answer or 'annex_i' not in str(q6_answer):
                    continue
            
            if q_id == 'Q6B':
                q6_answer = self.current_state.get_answer('Q6')
                if not q6_answer or q6_answer == 'none':
                    continue
            
            if q_id == 'Q8' and self.current_state.get_flag('flag_is_provider'):
                continue
            
            if q_id == 'Q9':
                if not (self.current_state.get_flag('flag_high_risk') and 
                       self.current_state.get_flag('flag_is_deployer')):
                    continue
            
            return question
        
        return None
    
    def answer_question(self, question_id: str, answer_value: Any):
        """Process answer and update state"""
        answer = Answer(question_id, answer_value)
        self.current_state = self.current_state.with_answer(answer)
        self.path.append(question_id)
        
        # Apply inference rules
        self.current_state = self.optimizer.apply_inference_rules(self.current_state)
    
    def get_result(self) -> ComplianceResult:
        """Get final compliance result"""
        flags = self.current_state.get_flags_dict()
        obligations = self.current_state.get_obligations_set()
        
        # Determine result
        if flags.get('flag_out_of_scope'):
            result = DecisionResult.OUT_OF_SCOPE
            explanation = "System is outside the scope of the EU AI Act"
        elif flags.get('flag_excluded'):
            result = DecisionResult.EXCLUDED
            explanation = "System is excluded from EU AI Act requirements"
        elif flags.get('flag_prohibited'):
            result = DecisionResult.PROHIBITED
            explanation = "System performs prohibited functions and cannot be placed on EU market"
        else:
            result = DecisionResult.COMPLIANCE_REQUIRED
            explanation = f"System requires compliance with {len(obligations)} obligations"
        
        return ComplianceResult(
            result=result,
            flags=flags,
            obligations=obligations,
            questions_asked=len(self.path),
            path_taken=self.path,
            explanation=explanation
        )
    
    def reset(self):
        """Reset engine for new assessment"""
        self.current_state = State()
        self.path = []