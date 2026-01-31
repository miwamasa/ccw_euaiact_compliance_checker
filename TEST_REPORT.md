# EU AI Act Compliance Checker - Test Report

**Generated:** 2026-01-31T01:47:03.855759

## Summary

- **Total Tests:** 20
- **Passed:** 20 ✓
- **Failed:** 0 ✗
- **Pass Rate:** 100.0%

## Optimization Metrics

| Metric | Value |
|--------|-------|
| Original Avg Questions | 10.2 |
| Optimized Avg Questions | 6.3 |
| Questions Saved | 3.9 |
| Improvement | 38.2% |
| Min Questions | 1 |
| Max Questions | 10 |
| Median Questions | 8 |
| Avg Execution Time | 0.18ms |

### Path Distribution

```
1 questions:  1 tests (  5.0%) ██
3 questions:  3 tests ( 15.0%) ███████
4 questions:  4 tests ( 20.0%) ██████████
7 questions:  1 tests (  5.0%) ██
8 questions:  7 tests ( 35.0%) █████████████████
9 questions:  3 tests ( 15.0%) ███████
10 questions:  1 tests (  5.0%) ██
```

## Results by Category

### Common Cases

**Status:** 4/4 passed

- ✓ **common_case_1_provider_high_risk_employment**
  - Provider of high-risk employment AI (8 questions)
  - Questions: 8
  - Execution time: 0.30ms

- ✓ **common_case_2_deployer_non_high_risk_chatbot**
  - Deployer of non-high-risk chatbot (8 questions)
  - Questions: 8
  - Execution time: 0.97ms

- ✓ **common_case_3_gpai_systemic_risk**
  - GPAI model with systemic risk (8 questions)
  - Questions: 8
  - Execution time: 0.19ms

- ✓ **common_case_4_gpai_no_systemic_risk**
  - GPAI model without systemic risk (8 questions)
  - Questions: 8
  - Execution time: 0.14ms

### Complex Cases

**Status:** 3/3 passed

- ✓ **complex_case_1_product_manufacturer_medical**
  - Product manufacturer with high-risk medical device (9 questions)
  - Questions: 9
  - Execution time: 0.22ms

- ✓ **complex_case_2_deployer_becomes_provider**
  - Deployer modifies system → becomes provider (10 questions)
  - Questions: 10
  - Execution time: 0.28ms

- ✓ **complex_case_3_high_risk_law_enforcement**
  - High-risk law enforcement system (8 questions)
  - Questions: 8
  - Execution time: 0.14ms

### Edge Cases

**Status:** 5/5 passed

- ✓ **edge_case_1_out_of_scope**
  - Out of scope - fastest path (1 question)
  - Questions: 1
  - Execution time: 0.02ms

- ✓ **edge_case_2_prohibited_social_scoring**
  - Prohibited system - social scoring (4 questions)
  - Questions: 4
  - Execution time: 0.07ms

- ✓ **edge_case_3_excluded_personal_use**
  - Excluded - personal use (3 questions)
  - Questions: 3
  - Execution time: 0.07ms

- ✓ **edge_case_4_excluded_research**
  - Excluded - research only (3 questions)
  - Questions: 3
  - Execution time: 0.05ms

- ✓ **edge_case_5_excluded_open_source**
  - Excluded - open source not deployed (3 questions)
  - Questions: 3
  - Execution time: 0.06ms

### Prohibited Tests

**Status:** 3/3 passed

- ✓ **prohibited_1_subliminal_manipulation**
  - Prohibited - subliminal manipulation
  - Questions: 4
  - Execution time: 0.07ms

- ✓ **prohibited_2_exploit_vulnerabilities**
  - Prohibited - exploiting vulnerabilities
  - Questions: 4
  - Execution time: 0.06ms

- ✓ **prohibited_3_realtime_biometric**
  - Prohibited - real-time biometric ID
  - Questions: 4
  - Execution time: 0.06ms

### Regression Tests

**Status:** 3/3 passed

- ✓ **regression_1_medical_no_third_party**
  - Medical device NOT requiring 3rd party assessment (9 questions)
  - Questions: 9
  - Execution time: 0.12ms

- ✓ **regression_2_multiple_transparency**
  - System with multiple transparency obligations (7 questions)
  - Questions: 7
  - Execution time: 0.20ms

- ✓ **regression_3_critical_infrastructure**
  - High-risk critical infrastructure system (9 questions)
  - Questions: 9
  - Execution time: 0.23ms

### Transparency Tests

**Status:** 2/2 passed

- ✓ **transparency_1_deepfake**
  - Transparency - deepfake content (8 questions)
  - Questions: 8
  - Execution time: 0.13ms

- ✓ **transparency_2_emotion_recognition**
  - Transparency - emotion recognition (non-high-risk) (8 questions)
  - Questions: 8
  - Execution time: 0.14ms

---

*Report generated on 2026-01-31 01:47:03*
