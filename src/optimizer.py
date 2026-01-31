# optimizer.py - Decision Tree Optimizer

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum
import math
from collections import defaultdict

class QuestionType(Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

@dataclass(frozen=True)
class Answer:
    """Immutable answer representation"""
    question_id: str
    value: Any
    
    def __hash__(self):
        if isinstance(self.value, list):
            return hash((self.question_id, tuple(sorted(self.value))))
        return hash((self.question_id, self.value))

@dataclass(frozen=True)
class State:
    """Immutable state representation"""
    answers: Tuple[Answer, ...] = field(default_factory=tuple)
    flags: Tuple[Tuple[str, bool], ...] = field(default_factory=tuple)
    obligations: Tuple[str, ...] = field(default_factory=tuple)
    
    def __hash__(self):
        return hash((self.answers, self.flags, self.obligations))
    
    def with_answer(self, answer: Answer) -> 'State':
        """Return new state with additional answer"""
        return State(
            answers=self.answers + (answer,),
            flags=self.flags,
            obligations=self.obligations
        )
    
    def with_flags(self, new_flags: Dict[str, bool]) -> 'State':
        """Return new state with updated flags"""
        flag_tuples = tuple(sorted(new_flags.items()))
        return State(
            answers=self.answers,
            flags=flag_tuples,
            obligations=self.obligations
        )
    
    def with_obligations(self, new_obligations: Set[str]) -> 'State':
        """Return new state with updated obligations"""
        return State(
            answers=self.answers,
            flags=self.flags,
            obligations=tuple(sorted(new_obligations))
        )
    
    def get_answer(self, question_id: str) -> Optional[Any]:
        """Get answer for specific question"""
        for answer in self.answers:
            if answer.question_id == question_id:
                return answer.value
        return None
    
    def get_flag(self, flag_name: str) -> bool:
        """Get flag value"""
        for name, value in self.flags:
            if name == flag_name:
                return value
        return False
    
    def get_flags_dict(self) -> Dict[str, bool]:
        """Convert flags to dictionary"""
        return dict(self.flags)
    
    def get_obligations_set(self) -> Set[str]:
        """Convert obligations to set"""
        return set(self.obligations)

@dataclass
class Question:
    """Question definition"""
    id: str
    question_text: str
    question_type: QuestionType
    options: List[Dict[str, Any]]
    priority: int = 0
    information_gain: float = 0.0
    skip_conditions: List[str] = field(default_factory=list)
    terminal_probability: float = 0.0
    
    def is_skippable(self, state: State) -> Tuple[bool, Optional[str]]:
        """Check if question should be skipped given current state"""
        for condition in self.skip_conditions:
            if self._evaluate_condition(condition, state):
                return True, condition
        return False, None
    
    def _evaluate_condition(self, condition: str, state: State) -> bool:
        """Evaluate skip condition"""
        # Simple condition evaluation
        # Format: "flag_name == True" or "flag_name == False"
        parts = condition.split("==")
        if len(parts) == 2:
            flag_name = parts[0].strip()
            expected = parts[1].strip() == "True"
            return state.get_flag(flag_name) == expected
        return False

class DecisionTreeOptimizer:
    """Optimizes decision tree for minimum expected path length"""
    
    def __init__(self):
        self.questions: Dict[str, Question] = {}
        self.inference_rules: List[Tuple[str, callable, Dict]] = []
        self.state_probabilities: Dict[State, float] = {}
        self.ig_cache: Dict[Tuple[str, int], float] = {}
        
    def add_question(self, question: Question):
        """Add question to optimizer"""
        self.questions[question.id] = question
    
    def add_inference_rule(self, name: str, condition: callable, 
                          effects: Dict[str, Any]):
        """Add inference rule for deriving flags/obligations"""
        self.inference_rules.append((name, condition, effects))
    
    def calculate_information_gain(self, question: Question, 
                                   state: State, 
                                   state_space: List[State]) -> float:
        """
        Calculate information gain for asking question in current state
        
        IG(Q, S) = H(S) - Σ p(v) × H(S|Q=v)
        """
        cache_key = (question.id, hash(state))
        if cache_key in self.ig_cache:
            return self.ig_cache[cache_key]
        
        # Calculate current entropy
        current_entropy = self._calculate_entropy(state_space)
        
        # Calculate conditional entropy for each possible answer
        conditional_entropy = 0.0
        answer_distributions = self._partition_by_answer(
            question, state, state_space
        )
        
        for answer_value, subset in answer_distributions.items():
            prob = len(subset) / len(state_space)
            subset_entropy = self._calculate_entropy(subset)
            conditional_entropy += prob * subset_entropy
        
        ig = current_entropy - conditional_entropy
        self.ig_cache[cache_key] = ig
        return ig
    
    def _calculate_entropy(self, state_space: List[State]) -> float:
        """
        Calculate Shannon entropy of state space
        H(S) = -Σ p(s) × log₂(p(s))
        """
        if not state_space:
            return 0.0
        
        # Count distinct terminal states
        terminal_counts = defaultdict(int)
        for state in state_space:
            # Hash by flags and obligations (terminal classification)
            key = (state.flags, state.obligations)
            terminal_counts[key] += 1
        
        total = len(state_space)
        entropy = 0.0
        for count in terminal_counts.values():
            if count > 0:
                prob = count / total
                entropy -= prob * math.log2(prob)
        
        return entropy
    
    def _partition_by_answer(self, question: Question, state: State,
                            state_space: List[State]) -> Dict[Any, List[State]]:
        """Partition state space by possible answers to question"""
        partitions = defaultdict(list)
        
        for s in state_space:
            # Simulate answering question in this state
            # For now, assume uniform distribution over options
            for option in question.options:
                answer_value = option['value']
                partitions[answer_value].append(s)
        
        return partitions
    
    def optimize_question_order(self, questions: List[Question],
                               initial_state: State) -> List[Question]:
        """
        Optimize question order using greedy information gain algorithm
        
        At each step, select question with maximum:
        score(q) = IG(q) × (1 + α × p_terminal(q))
        """
        ordered = []
        remaining = questions.copy()
        current_state = initial_state
        alpha = 0.5  # Weight for terminal probability
        
        while remaining:
            # Calculate scores for all remaining questions
            scores = []
            for q in remaining:
                # Skip if question has skip condition met
                skippable, _ = q.is_skippable(current_state)
                if skippable:
                    continue
                
                # Calculate score
                ig = q.information_gain  # Pre-calculated or use calculate_information_gain
                score = ig * (1 + alpha * q.terminal_probability)
                scores.append((score, q))
            
            if not scores:
                break
            
            # Select question with highest score
            scores.sort(reverse=True, key=lambda x: x[0])
            best_question = scores[0][1]
            ordered.append(best_question)
            remaining.remove(best_question)
            
            # Update state (simulate average answer)
            # In practice, this would need more sophisticated simulation
        
        return ordered
    
    def calculate_expected_path_length(self, root: Question,
                                      decision_tree: Dict) -> float:
        """
        Calculate expected path length for decision tree
        E[L] = Σᵢ p(pathᵢ) × |pathᵢ|
        """
        def traverse(node_id: str, probability: float, depth: int) -> float:
            if node_id == "TERMINAL":
                return probability * depth
            
            node = decision_tree.get(node_id)
            if not node:
                return probability * depth
            
            expected = 0.0
            for child, child_prob in node.get('children', {}).items():
                expected += traverse(child, probability * child_prob, depth + 1)
            
            return expected
        
        return traverse(root.id, 1.0, 0)
    
    def apply_inference_rules(self, state: State) -> State:
        """Apply all applicable inference rules to derive flags/obligations"""
        current_state = state
        changed = True
        
        # Fixed-point iteration
        max_iterations = 10
        iteration = 0
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            for rule_name, condition, effects in self.inference_rules:
                if condition(current_state):
                    # Apply effects
                    new_flags = current_state.get_flags_dict()
                    new_obligations = current_state.get_obligations_set()
                    
                    for key, value in effects.items():
                        if key.startswith('flag_'):
                            if new_flags.get(key) != value:
                                new_flags[key] = value
                                changed = True
                        elif key.startswith('obligation_'):
                            if value and key not in new_obligations:
                                new_obligations.add(key)
                                changed = True
                    
                    current_state = current_state.with_flags(new_flags)
                    current_state = current_state.with_obligations(new_obligations)
        
        return current_state
    
    def generate_optimization_report(self, original_tree: Dict,
                                    optimized_tree: Dict) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        report = {
            'metrics': {
                'original': self._analyze_tree(original_tree),
                'optimized': self._analyze_tree(optimized_tree)
            },
            'improvements': {},
            'savings': {}
        }
        
        # Calculate improvements
        orig = report['metrics']['original']
        opt = report['metrics']['optimized']
        
        report['improvements'] = {
            'avg_path_reduction': f"{((orig['avg_path'] - opt['avg_path']) / orig['avg_path'] * 100):.1f}%",
            'max_depth_reduction': f"{((orig['max_depth'] - opt['max_depth']) / orig['max_depth'] * 100):.1f}%",
            'questions_saved': orig['total_questions'] - opt['total_questions']
        }
        
        return report
    
    def _analyze_tree(self, tree: Dict) -> Dict[str, float]:
        """Analyze decision tree metrics"""
        return {
            'total_questions': len(tree.get('questions', [])),
            'max_depth': tree.get('max_depth', 0),
            'avg_path': tree.get('avg_path_length', 0),
            'branching_factor': tree.get('avg_branching_factor', 0)
        }


class InformationGainCalculator:
    """Utility class for information gain calculations"""
    
    @staticmethod
    def calculate_entropy(probabilities: List[float]) -> float:
        """Calculate Shannon entropy H = -Σ p × log₂(p)"""
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    @staticmethod
    def calculate_conditional_entropy(partitions: List[List[float]],
                                     partition_probs: List[float]) -> float:
        """Calculate H(Y|X) = Σ p(x) × H(Y|X=x)"""
        conditional = 0.0
        for partition, prob in zip(partitions, partition_probs):
            conditional += prob * InformationGainCalculator.calculate_entropy(partition)
        return conditional
    
    @staticmethod
    def mutual_information(joint_probs: Dict[Tuple, float]) -> float:
        """Calculate I(X;Y) = H(X) + H(Y) - H(X,Y)"""
        # Calculate marginal probabilities
        x_probs = defaultdict(float)
        y_probs = defaultdict(float)
        
        for (x, y), p in joint_probs.items():
            x_probs[x] += p
            y_probs[y] += p
        
        # Calculate entropies
        h_x = InformationGainCalculator.calculate_entropy(list(x_probs.values()))
        h_y = InformationGainCalculator.calculate_entropy(list(y_probs.values()))
        h_xy = InformationGainCalculator.calculate_entropy(list(joint_probs.values()))
        
        return h_x + h_y - h_xy