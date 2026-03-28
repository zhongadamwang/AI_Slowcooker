# Test Validation Framework

**Purpose**: Systematic validation framework for AI Agent Skills using diverse requirement samples  
**Created**: 2026-02-17  
**Framework Version**: 1.0  

## Quick Start Guide

### Immediate Testing Steps
1. **Open VS Code** with the AI_Slowcooker workspace
2. **Ensure Copilot is active** and skills are loaded
3. **Start with simple validation**:
   ```
   @workspace Use the requirements-ingest skill to process the simple todo app requirements from /artifacts/Sample Data/simple-todo-app.md
   ```
4. **Verify output quality** against expected results documented in the sample
5. **Progress to complex samples** like healthcare-emr.md or banking-transactions.md

### First Test Execution
Try this complete workflow to validate the skill chain:
```
@workspace I want to test our skills end-to-end. Please process /artifacts/Sample Data/healthcare-emr.md through our complete analysis workflow: requirements ingestion → domain analysis → goals extraction → W5H analysis. Show me the output quality and any issues you identify.
```

## Overview

This framework provides structured testing procedures to validate AI skills against diverse requirement samples. Each test case includes expected outcomes, validation criteria, and success metrics to ensure skills perform accurately across varying complexity levels and domains.

## Test Sample Matrix

| Sample Name | Domain | Complexity | Format | Primary Validation Target |
|-------------|--------|------------|--------|---------------------------|
| healthcare-emr | Healthcare | Medium | Narrative | Domain extraction, regulatory compliance |
| ecommerce-marketplace | E-commerce | Complex | Mixed | Multi-stakeholder analysis, scope minimization |
| simple-todo-app | Productivity | Simple | Narrative | Basic skill validation, clean requirements |
| conflicting-requirements | Customer Service | Medium | Mixed | Conflict resolution, error handling |
| banking-transactions | Financial | Complex | Technical Specs | Technical analysis, integration planning |
| incomplete-requirements | Inventory | Medium | Narrative | Gap analysis, assumption identification |

## Skill Testing Procedures

### 1. Requirements Ingestion Skill Testing

**Test Objective**: Validate parsing and normalization of diverse requirement formats

**Test Procedure**:
1. Process each sample through requirements ingestion skill
2. Compare extracted requirements against expected outcomes documented in each sample  
3. Verify traceability links are created correctly
4. Validate metadata extraction (document type, complexity, domain)

**Success Criteria**:
- 100% requirement extraction completeness for structured samples
- 95% accuracy for narrative format parsing
- Correct classification of requirement types (functional, non-functional, constraint)
- Preservation of source document structure and formatting

**Expected Challenges**:
- Mixed format documents (ecommerce-marketplace)
- Technical specification parsing (banking-transactions)
- Incomplete information handling (incomplete-requirements)

### 2. Domain Concepts Extraction Testing

**Test Objective**: Validate identification and categorization of domain entities and relationships

**Test Procedure**:
1. Apply domain extraction skill to each sample
2. Compare identified concepts against expected domain analysis in each sample
3. Verify relationship mapping accuracy
4. Validate concept categorization and hierarchy

**Success Criteria**:
- Core entity identification: >95% accuracy
- Relationship mapping: >90% accuracy for explicit relationships
- Domain categorization: Correct primary domain classification
- Terminology consistency: Consistent use of domain vocabulary

**Sample-Specific Expectations**:
- **Healthcare EMR**: Identify patient, provider, appointment, medical record entities
- **E-commerce**: Recognize complex multi-tier relationships (manufacturer-reseller-customer)  
- **Banking**: Extract financial entities and regulatory concepts
- **Simple Todo**: Validate handling of simple domain with basic entities

### 3. Goals Extraction Testing

**Test Objective**: Validate identification of business goals, success criteria, and constraints

**Test Procedure**:
1. Run goals extraction on each sample
2. Compare extracted goals against expected outcomes
3. Verify success criteria identification and measurement validity
4. Check constraint recognition and categorization

**Success Criteria**:
- Primary goal identification: 100% accuracy
- Success criteria extraction: >90% completeness
- Constraint recognition: All explicit constraints captured
- KPI identification: Measurable metrics correctly identified

**Complexity Validation**:
- **Simple samples**: Should identify basic, clear goals
- **Complex samples**: Should handle multiple competing goals and complex success criteria
- **Conflicting samples**: Should identify goal conflicts and inconsistencies

### 4. W5H Analysis Testing

**Test Objective**: Validate comprehensive requirements analysis from multiple perspectives

**Test Procedure**:
1. Apply W5H analysis framework to each sample
2. Compare analysis results against expected W5H breakdowns
3. Verify completeness of perspective coverage
4. Validate insight quality and relevance

**Success Criteria**:
- Complete W5H coverage: All six dimensions analyzed
- Stakeholder identification: >95% accuracy for explicit stakeholders
- Context analysis: Relevant business and technical context captured
- Gap identification: Missing information flagged appropriately

**Analysis Depth Expectations**:
- **Healthcare/Banking**: Should identify complex stakeholder ecosystems and regulatory context
- **E-commerce**: Should recognize multi-party business model complexity
- **Simple Todo**: Should provide proportionate analysis depth

### 5. Change Management Testing

**Test Objective**: Validate traceability and change impact assessment capabilities

**Test Procedure**:
1. Process requirements through change management skill
2. Simulate requirement modifications using change templates
3. Verify traceability maintenance through changes
4. Test impact analysis accuracy

**Success Criteria**:
- Traceability links: 100% maintenance through processing
- Change documentation: Complete audit trail generation
- Impact assessment: Accurate identification of affected components
- Version control: Proper change sequencing and attribution

**Change Scenarios**:
- **Simple changes**: Single requirement modifications
- **Complex changes**: Multi-requirement impacts and dependencies
- **Conflicting changes**: Change conflict identification and resolution

### 6. Scope Minimization Testing

**Test Objective**: Validate MVP identification and prioritization logic

**Test Procedure**:
1. Apply scope minimization to complex samples (healthcare, e-commerce, banking)
2. Compare scope recommendations against expected analysis
3. Verify business value assessment accuracy
4. Validate dependency analysis and phasing recommendations

**Success Criteria**:
- Core feature identification: 100% accuracy for explicitly defined core features
- Prioritization logic: Consistent application of business value + complexity + dependency criteria
- Phase planning: Logical MVP and enhancement phase boundaries
- Risk assessment: Accurate identification of scope reduction risks

**Complexity Targeting**:
- Should defer complex features appropriately
- Should maintain functional integrity in MVP scope
- Should provide clear rationale for inclusion/exclusion decisions

## Integration Testing Procedures

### End-to-End Workflow Testing

**Test Objective**: Validate complete skill workflow integration using sample documents

**Test Procedure**:
1. Select one sample from each complexity level (simple, medium, complex)
2. Execute complete skill chain: ingestion → domain analysis → goals → W5H → scope → change management
3. Verify data flow and handoffs between skills
4. Validate cumulative output quality and consistency

**Success Criteria**:
- Workflow completion: 100% success rate for well-formed requirements
- Data consistency: No information loss or corruption between skill stages
- Output coherence: Final artifacts should tell coherent, complete story
- Performance: Complete workflow execution within reasonable time bounds

### Cross-Sample Consistency Testing

**Test Objective**: Validate consistent skill behavior across different samples

**Test Procedure**:
1. Compare skill outputs across samples within same domain/complexity
2. Verify consistent application of analysis frameworks
3. Check for bias or inconsistency in processing approach
4. Validate proportional analysis depth based on sample complexity

**Consistency Criteria**:
- Analysis framework application: Consistent methodology across samples
- Output format: Standardized structure and metadata
- Quality scaling: Analysis depth should scale with sample complexity
- Domain handling: Consistent accuracy across different business domains

## Error Handling and Edge Case Testing

### Conflict Resolution Testing

**Test Objective**: Validate handling of contradictory or ambiguous requirements

**Test Sample**: conflicting-requirements.md

**Expected Behaviors**:
- Conflict identification: All major conflicts should be detected and flagged
- Resolution guidance: Provide structured approach to conflict resolution
- Stakeholder mapping: Identify conflict ownership for resolution
- Risk assessment: Flag high-risk conflicts that could derail project

### Incomplete Information Handling

**Test Objective**: Validate graceful handling of missing or incomplete requirements

**Test Sample**: incomplete-requirements.md

**Expected Behaviors**:
- Gap identification: Missing information categories should be flagged
- Assumption surfacing: Implicit assumptions should be made explicit
- Question generation: Specific questions should be suggested to gather missing information
- Risk flagging: Risks from incomplete information should be highlighted

## Performance and Scalability Testing

### Processing Time Validation

**Test Objective**: Ensure skills perform within acceptable time bounds

**Test Procedure**:
1. Measure processing time for each skill on each sample
2. Compare performance across sample complexity levels
3. Identify performance bottlenecks or outliers
4. Validate scalability to larger requirement documents

**Performance Targets**:
- Simple samples: <30 seconds per skill
- Medium samples: <2 minutes per skill  
- Complex samples: <5 minutes per skill
- Memory usage: Reasonable resource consumption

### Load Testing

**Test Objective**: Validate skill performance under concurrent usage

**Test Procedure**:
1. Execute multiple skill operations simultaneously
2. Monitor system resource usage and response times
3. Verify output quality under load conditions
4. Test recovery from resource constraints

## Test Execution Instructions

### Prerequisites

Before executing tests, ensure:
1. AI Agent Skills system is properly installed and configured
2. VS Code is running with Copilot extension active
3. All skill files are accessible in the `.github/skills/` directory
4. Test sample files are available in the `Sample Data` directory

### Manual Test Execution

#### Step 1: Individual Skill Testing

**For each skill, test against appropriate samples:**

1. **Requirements Ingestion Skill**
   ```
   @workspace Use the requirements-ingest skill to process /artifacts/Sample Data/healthcare-emr.md
   ```
   - Expected: Structured requirements output with traceability links
   - Validation: Compare against expected outcomes in healthcare-emr.md

2. **Domain Concepts Extraction**
   ```
   @workspace Use the domain-extractconcepts skill on the healthcare EMR requirements
   ```
   - Expected: Healthcare entities (Patient, Provider, EMR, etc.)
   - Validation: Check against expected domain analysis section

3. **Goals Extraction**
   ```
   @workspace Apply the goals-extract skill to analyze business goals in the e-commerce marketplace requirements
   ```
   - Expected: Goal hierarchy with success criteria and constraints
   - Validation: Verify against expected goals section

#### Step 2: End-to-End Workflow Testing

Execute complete skill chain using Copilot commands:

```
@workspace I need to analyze project requirements end-to-end. Please:
1. Apply requirements-ingest to /Sample Data/banking-transactions.md
2. Extract domain concepts from the ingested requirements  
3. Identify business goals and success criteria
4. Perform W5H analysis
5. Generate scope minimization recommendations
6. Set up change management tracking

Please execute these skills in sequence and maintain traceability between outputs.
```

#### Step 3: Error Condition Testing

**Test conflict resolution:**
```
@workspace Use the requirements-ingest skill on /Sample Data/conflicting-requirements.md and identify all requirement conflicts
```

**Test gap analysis:**
```
@workspace Analyze /Sample Data/incomplete-requirements.md and identify what information is missing
```

### Copilot Skill Invocation Patterns

#### Basic Skill Invocation
```
@workspace Use the [skill-name] skill to [specific task] on [sample file]
```

#### Skill Chaining
```
@workspace Execute the following skills in sequence:
1. [skill-1] on [sample]
2. [skill-2] using output from step 1
3. [skill-3] to analyze results from step 2
```

#### Comparative Analysis
```
@workspace Compare the output of [skill-name] when applied to both [sample-1] and [sample-2]
```

### Automated Test Execution

#### Batch Processing Script
Create a PowerShell script for systematic testing:

```powershell
# Test all samples with requirements ingestion
$samples = @(
    "healthcare-emr.md",
    "ecommerce-marketplace.md", 
    "simple-todo-app.md",
    "conflicting-requirements.md",
    "banking-transactions.md",
    "incomplete-requirements.md"
)

foreach ($sample in $samples) {
    Write-Host "Testing $sample with requirements-ingest skill..."
    # Execute Copilot command programmatically
    # Store results for validation
}
```

#### Validation Checklist Generator
```python
# Generate validation checklist for each test run
def create_validation_checklist(sample_name, skill_name):
    checklist = {
        'sample': sample_name,
        'skill': skill_name,
        'timestamp': datetime.now(),
        'validation_points': [],
        'success_criteria': [],
        'actual_results': [],
        'pass_fail': None
    }
    return checklist
```

### Performance Measurement

#### Timing Test Commands
```
@workspace Time how long it takes to execute the domain-extractconcepts skill on the banking-transactions.md sample
```

#### Memory Usage Monitoring
```
@workspace Monitor system resources while executing the complete skill workflow on the e-commerce marketplace sample
```

### Test Result Validation

#### Output Comparison
1. **Capture Skill Output**: Save all skill outputs to timestamped files
2. **Compare Against Expected**: Use diff tools to compare with expected results
3. **Score Accuracy**: Calculate percentage match for structured outputs
4. **Document Deviations**: Record any unexpected behaviors or outputs

#### Quality Assessment Prompts
```
@workspace Evaluate the quality of domain concepts extracted from healthcare-emr.md:
- Are all major entities identified?
- Are relationships correctly mapped?
- Is terminology consistent with healthcare domain?
- Are regulatory concepts properly categorized?
```

### Test Reports Generation

#### Individual Test Report
```
@workspace Generate a test report for the goals-extract skill testing that includes:
- Test samples used
- Expected vs actual outcomes  
- Accuracy metrics
- Performance measurements
- Identified issues or gaps
```

#### Comprehensive Test Summary
```
@workspace Create a comprehensive test validation summary covering:
- All skills tested
- Overall accuracy rates
- Performance benchmarks
- Error handling effectiveness
- Recommendations for improvement
```

### Continuous Testing Integration

#### Regression Test Automation
Set up automated triggers for skill changes:
```
# When skills are modified, automatically run regression tests
@workspace After any skill modification, execute the core validation test suite against all sample files
```

#### Performance Baseline Tracking
```
@workspace Establish performance baselines by running the complete test suite and recording:
- Processing time per skill per sample
- Memory usage patterns
- Output quality scores
- Error rates
```

## Test Execution and Reporting

### Automated Test Framework

**Implementation Requirements**:
- Copilot command automation for systematic test execution
- Result comparison against expected outcomes documented in samples
- Performance measurement and benchmarking capabilities
- Error condition simulation and graceful failure validation
- Traceability maintenance throughout test execution

### Test Reports

**Required Reports**:
- **Skill Validation Report**: Individual skill accuracy and performance metrics with sample-by-sample breakdown
- **Integration Test Report**: End-to-end workflow validation results showing data flow integrity
- **Regression Test Report**: Comparison against baseline performance with trend analysis
- **Error Handling Report**: Edge case and error condition handling assessment with recovery validation

### Continuous Validation

**Ongoing Testing**:
- Regression testing after skill modifications
- New sample integration as skills evolve
- Performance monitoring and optimization
- User acceptance validation with real-world usage

## Success Metrics and KPIs

### Accuracy Metrics
- Requirements extraction completeness: >95%
- Domain concept identification accuracy: >95%
- Goals and success criteria capture: >90%
- Conflict and gap detection accuracy: >90%

### Performance Metrics
- Processing time within target bounds: 100%
- Memory usage within reasonable limits: <2GB per skill execution
- Concurrent execution capability: Support 5 simultaneous skill invocations
- Error recovery: 100% graceful handling of malformed inputs

### Quality Metrics
- Output consistency across samples: >95% framework adherence
- Traceability maintenance: 100% link preservation
- User satisfaction: Validation by domain experts
- Business value: Measurable improvement in requirements analysis efficiency

---

**Usage Instructions**: Execute test framework after any skill modifications or new skill additions to ensure system integrity and performance standards are maintained.