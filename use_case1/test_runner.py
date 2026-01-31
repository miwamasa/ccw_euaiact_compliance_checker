# test_runner.py - Test execution and reporting

import sys
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from decision_engine import OptimizedDecisionEngine, DecisionResult
from test_cases import TEST_CASES, get_test_cases_by_category, get_all_categories, TestCase

@dataclass
class TestResult:
    """Individual test result"""
    test_case: TestCase
    passed: bool
    actual_questions: int
    actual_flags: Dict[str, bool]
    actual_obligations: List[str]
    actual_result: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0

@dataclass
class TestReport:
    """Complete test execution report"""
    timestamp: datetime
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    results_by_category: Dict[str, List[TestResult]]
    optimization_metrics: Dict[str, Any]
    errors_summary: List[str]

class TestRunner:
    """Execute and report on test cases"""
    
    def __init__(self):
        self.engine = OptimizedDecisionEngine()
        self.results: List[TestResult] = []
    
    def run_test_case(self, test_case: TestCase) -> TestResult:
        """Execute single test case"""
        import time
        start_time = time.time()
        
        # Reset engine
        self.engine.reset()
        
        errors = []
        warnings = []
        
        # Execute questionnaire
        try:
            for question_id in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q5A', 'Q6', 'Q6A', 'Q6B', 'Q7', 'Q8', 'Q9']:
                if question_id in test_case.answers:
                    self.engine.answer_question(question_id, test_case.answers[question_id])
                else:
                    # Check if question should be asked
                    next_q = self.engine.get_next_question()
                    if next_q and next_q.id == question_id:
                        # Question expected but not answered in test case
                        errors.append(f"Expected answer for {question_id} but none provided")
                        break
                
                # Check for early termination
                result = self.engine.get_result()
                if result.result in [DecisionResult.OUT_OF_SCOPE, DecisionResult.EXCLUDED, DecisionResult.PROHIBITED]:
                    break
        
        except Exception as e:
            errors.append(f"Exception during execution: {str(e)}")
        
        # Get final result
        result = self.engine.get_result()
        
        # Collect actual values
        actual_questions = result.questions_asked
        actual_flags = result.flags
        actual_obligations = sorted(result.obligations)
        actual_result = result.result.value.upper()
        
        # Validate results
        passed = True
        
        # Check question count
        if actual_questions != test_case.expected_questions:
            errors.append(
                f"Question count mismatch: expected {test_case.expected_questions}, got {actual_questions}"
            )
            passed = False
        
        # Check flags
        for flag_name, expected_value in test_case.expected_flags.items():
            actual_value = actual_flags.get(flag_name, False)
            if actual_value != expected_value:
                errors.append(
                    f"Flag mismatch for {flag_name}: expected {expected_value}, got {actual_value}"
                )
                passed = False
        
        # Check obligations
        expected_obligations = sorted(test_case.expected_obligations)
        if actual_obligations != expected_obligations:
            missing = set(expected_obligations) - set(actual_obligations)
            extra = set(actual_obligations) - set(expected_obligations)
            if missing:
                errors.append(f"Missing obligations: {missing}")
            if extra:
                errors.append(f"Extra obligations: {extra}")
            passed = False
        
        # Check result
        if actual_result != test_case.expected_result:
            errors.append(
                f"Result mismatch: expected {test_case.expected_result}, got {actual_result}"
            )
            passed = False
        
        execution_time_ms = (time.time() - start_time) * 1000
        
        return TestResult(
            test_case=test_case,
            passed=passed,
            actual_questions=actual_questions,
            actual_flags=actual_flags,
            actual_obligations=actual_obligations,
            actual_result=actual_result,
            errors=errors,
            warnings=warnings,
            execution_time_ms=execution_time_ms
        )
    
    def run_all_tests(self) -> TestReport:
        """Run all test cases"""
        print("="*80)
        print("EU AI ACT COMPLIANCE CHECKER - OPTIMIZATION TEST SUITE")
        print("="*80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Total test cases: {len(TEST_CASES)}")
        print()
        
        results_by_category = {}
        all_results = []
        
        categories = get_all_categories()
        for category in sorted(categories):
            print(f"\n{'='*80}")
            print(f"Category: {category.upper()}")
            print(f"{'='*80}")
            
            test_cases = get_test_cases_by_category(category)
            category_results = []
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n[{i}/{len(test_cases)}] {test_case.name}")
                print(f"    {test_case.description}")
                
                result = self.run_test_case(test_case)
                category_results.append(result)
                all_results.append(result)
                
                # Print result
                status = "✓ PASS" if result.passed else "✗ FAIL"
                print(f"    {status} - {result.actual_questions} questions, {result.execution_time_ms:.2f}ms")
                
                if not result.passed:
                    for error in result.errors:
                        print(f"      ERROR: {error}")
                
                if result.warnings:
                    for warning in result.warnings:
                        print(f"      WARNING: {warning}")
            
            results_by_category[category] = category_results
            
            # Category summary
            passed = sum(1 for r in category_results if r.passed)
            print(f"\n    Category Summary: {passed}/{len(category_results)} passed")
        
        # Generate overall report
        passed_count = sum(1 for r in all_results if r.passed)
        failed_count = len(all_results) - passed_count
        pass_rate = (passed_count / len(all_results) * 100) if all_results else 0
        
        # Calculate optimization metrics
        optimization_metrics = self._calculate_optimization_metrics(all_results)
        
        # Collect error summary
        errors_summary = []
        for result in all_results:
            if not result.passed:
                errors_summary.append(f"{result.test_case.name}: {', '.join(result.errors)}")
        
        report = TestReport(
            timestamp=datetime.now(),
            total_tests=len(all_results),
            passed=passed_count,
            failed=failed_count,
            pass_rate=pass_rate,
            results_by_category=results_by_category,
            optimization_metrics=optimization_metrics,
            errors_summary=errors_summary
        )
        
        self._print_final_report(report)
        return report
    
    def _calculate_optimization_metrics(self, results: List[TestResult]) -> Dict[str, Any]:
        """Calculate optimization metrics from test results"""
        if not results:
            return {}
        
        question_counts = [r.actual_questions for r in results]
        avg_questions = sum(question_counts) / len(question_counts)
        min_questions = min(question_counts)
        max_questions = max(question_counts)
        
        # Calculate path distribution
        path_distribution = {}
        for r in results:
            key = r.actual_questions
            path_distribution[key] = path_distribution.get(key, 0) + 1
        
        # Calculate estimated time savings (assuming 1 question = 30 seconds)
        original_avg = 10.2  # From theory
        time_per_question = 30  # seconds
        original_time = original_avg * time_per_question
        optimized_time = avg_questions * time_per_question
        time_saved = original_time - optimized_time
        time_saved_pct = (time_saved / original_time * 100) if original_time > 0 else 0
        
        return {
            'average_questions': round(avg_questions, 2),
            'min_questions': min_questions,
            'max_questions': max_questions,
            'median_questions': sorted(question_counts)[len(question_counts)//2],
            'path_distribution': path_distribution,
            'original_avg_questions': original_avg,
            'questions_saved': round(original_avg - avg_questions, 2),
            'improvement_percentage': round((original_avg - avg_questions) / original_avg * 100, 1),
            'estimated_time_saved_seconds': round(time_saved, 1),
            'estimated_time_saved_percentage': round(time_saved_pct, 1),
            'avg_execution_time_ms': round(sum(r.execution_time_ms for r in results) / len(results), 2)
        }
    
    def _print_final_report(self, report: TestReport):
        """Print final test report"""
        print("\n" + "="*80)
        print("FINAL TEST REPORT")
        print("="*80)
        print(f"Timestamp: {report.timestamp.isoformat()}")
        print(f"Total Tests: {report.total_tests}")
        print(f"Passed: {report.passed}")
        print(f"Failed: {report.failed}")
        print(f"Pass Rate: {report.pass_rate:.1f}%")
        
        print("\n" + "-"*80)
        print("OPTIMIZATION METRICS")
        print("-"*80)
        metrics = report.optimization_metrics
        print(f"Average Questions (Original): {metrics['original_avg_questions']}")
        print(f"Average Questions (Optimized): {metrics['average_questions']}")
        print(f"Questions Saved: {metrics['questions_saved']}")
        print(f"Improvement: {metrics['improvement_percentage']}%")
        print(f"Min Questions: {metrics['min_questions']}")
        print(f"Max Questions: {metrics['max_questions']}")
        print(f"Median Questions: {metrics['median_questions']}")
        
        print("\nPath Distribution:")
        for questions, count in sorted(metrics['path_distribution'].items()):
            pct = (count / report.total_tests * 100)
            bar = "█" * int(pct / 2)
            print(f"  {questions} questions: {count:2d} tests ({pct:5.1f}%) {bar}")
        
        print(f"\nEstimated Time Saved: {metrics['estimated_time_saved_seconds']}s per assessment")
        print(f"Time Improvement: {metrics['estimated_time_saved_percentage']}%")
        print(f"Average Execution Time: {metrics['avg_execution_time_ms']:.2f}ms")
        
        if report.errors_summary:
            print("\n" + "-"*80)
            print("ERRORS SUMMARY")
            print("-"*80)
            for error in report.errors_summary[:10]:  # Show first 10
                print(f"  • {error}")
            if len(report.errors_summary) > 10:
                print(f"  ... and {len(report.errors_summary) - 10} more errors")
        
        print("\n" + "="*80)
        if report.failed == 0:
            print("✓ ALL TESTS PASSED!")
        else:
            print(f"✗ {report.failed} TEST(S) FAILED")
        print("="*80)
    
    def export_report_markdown(self, report: TestReport, filename: str = "TEST_REPORT.md"):
        """Export test report as markdown"""
        with open(filename, 'w') as f:
            f.write("# EU AI Act Compliance Checker - Test Report\n\n")
            f.write(f"**Generated:** {report.timestamp.isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Tests:** {report.total_tests}\n")
            f.write(f"- **Passed:** {report.passed} ✓\n")
            f.write(f"- **Failed:** {report.failed} ✗\n")
            f.write(f"- **Pass Rate:** {report.pass_rate:.1f}%\n\n")
            
            f.write("## Optimization Metrics\n\n")
            metrics = report.optimization_metrics
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Original Avg Questions | {metrics['original_avg_questions']} |\n")
            f.write(f"| Optimized Avg Questions | {metrics['average_questions']} |\n")
            f.write(f"| Questions Saved | {metrics['questions_saved']} |\n")
            f.write(f"| Improvement | {metrics['improvement_percentage']}% |\n")
            f.write(f"| Min Questions | {metrics['min_questions']} |\n")
            f.write(f"| Max Questions | {metrics['max_questions']} |\n")
            f.write(f"| Median Questions | {metrics['median_questions']} |\n")
            f.write(f"| Avg Execution Time | {metrics['avg_execution_time_ms']:.2f}ms |\n\n")
            
            f.write("### Path Distribution\n\n")
            f.write("```\n")
            for questions, count in sorted(metrics['path_distribution'].items()):
                pct = (count / report.total_tests * 100)
                bar = "█" * int(pct / 2)
                f.write(f"{questions} questions: {count:2d} tests ({pct:5.1f}%) {bar}\n")
            f.write("```\n\n")
            
            f.write("## Results by Category\n\n")
            for category, results in sorted(report.results_by_category.items()):
                passed = sum(1 for r in results if r.passed)
                f.write(f"### {category.replace('_', ' ').title()}\n\n")
                f.write(f"**Status:** {passed}/{len(results)} passed\n\n")
                
                for result in results:
                    status = "✓" if result.passed else "✗"
                    f.write(f"- {status} **{result.test_case.name}**\n")
                    f.write(f"  - {result.test_case.description}\n")
                    f.write(f"  - Questions: {result.actual_questions}\n")
                    f.write(f"  - Execution time: {result.execution_time_ms:.2f}ms\n")
                    if result.errors:
                        f.write(f"  - Errors: {', '.join(result.errors)}\n")
                    f.write("\n")
            
            if report.errors_summary:
                f.write("## Errors\n\n")
                for error in report.errors_summary:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write(f"*Report generated on {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\nReport exported to {filename}")

def main():
    """Main test execution"""
    runner = TestRunner()
    report = runner.run_all_tests()
    runner.export_report_markdown(report)
    
    # Exit with appropriate code
    sys.exit(0 if report.failed == 0 else 1)

if __name__ == "__main__":
    main()