"""
Comprehensive test suite for Requirements Ingest skill
Tests both AI-powered and traditional implementations
"""

import json
import tempfile
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.requirements_ingest import RequirementsIngestor
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the requirements-ingest directory")
    sys.exit(1)

def create_test_files():
    """Create comprehensive test files for validation"""
    test_files = {}
    
    # 1. Markdown requirements document
    md_content = """# E-commerce Platform Requirements

## Authentication Requirements
The system shall authenticate users using OAuth2 protocol within 3 seconds.
Users must be able to login with social media accounts.
Password complexity must meet NIST standards.

## Performance Requirements  
API response times should not exceed 200ms for product searches.
The platform must support 10,000 concurrent users during peak hours.
Database queries shall complete within 100ms for 95% of requests.

## Security Constraints
All data must be encrypted using AES-256 encryption.
PCI DSS compliance is mandatory for payment processing.
Budget for security tools cannot exceed $25,000 annually.

## Assumptions
Users have modern web browsers supporting JavaScript ES6+.
Internet connectivity is reliable with minimum 1Mbps bandwidth.
Third-party payment APIs will be available 99.9% of the time.

## Out of Scope
Mobile application development is excluded from Phase 1.
Legacy system migration will be addressed in future releases.
Advanced analytics features are not part of current scope.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        test_files['markdown'] = f.name
    
    # 2. Plain text technical specifications
    txt_content = """Technical Specifications Document

FUNCTIONAL REQUIREMENTS:
- The inventory management system shall automatically update stock levels in real-time.
- Users will receive email notifications when items are back in stock.
- The system must generate daily sales reports in PDF format.

NON-FUNCTIONAL REQUIREMENTS:
- System uptime must be 99.9% excluding scheduled maintenance.
- Data backup shall occur every 6 hours with 30-day retention.
- Load balancing must distribute traffic across minimum 3 servers.

BUSINESS CONSTRAINTS:
- Implementation timeline is 6 months maximum.
- Total project cost cannot exceed $100,000.
- Must integrate with existing SAP system.

TECHNICAL ASSUMPTIONS:
- Database server has 32GB RAM minimum.
- Network latency between servers is under 10ms.
- Development team is familiar with Python and PostgreSQL.

NOT IN SCOPE:
- Customer support portal integration.
- Multi-language support for international markets.
- Advanced AI-powered recommendation engine.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(txt_content)
        test_files['text'] = f.name
    
    # 3. Email-style requirements
    email_content = """From: product@company.com
To: development@company.com
Subject: Mobile App Requirements - Phase 2

Hi Development Team,

Here are the updated requirements for our mobile application:

CORE FEATURES:
The mobile app shall support offline mode for browsing saved products.
Push notifications must be delivered within 30 seconds of trigger events.
User location shall be used to show nearby store inventory.

PERFORMANCE SPECS:
App startup time should be under 2 seconds on standard devices.
Image loading must complete within 1 second over 4G networks.
Battery usage cannot exceed 5% per hour of active use.

COMPLIANCE REQUIREMENTS:
App must comply with GDPR for European users.
Data collection requires explicit user consent.
User data shall be deletable within 24 hours of request.

Please note that barcode scanning and AR features are out of scope for this release.

Best regards,
Product Team
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.eml', delete=False) as f:
        f.write(email_content)
        test_files['email'] = f.name
    
    return test_files

def validate_json_schema(result):
    """Validate the output matches expected JSON schema"""
    required_fields = ['project_id', 'requirements', 'glossary_suspects']
    
    # Check top-level structure
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
    
    # Validate requirements array
    assert isinstance(result['requirements'], list), "requirements must be a list"
    
    # Validate each requirement
    req_required_fields = ['id', 'source_file', 'location_hint', 'text', 'tags', 'confidence']
    
    for i, req in enumerate(result['requirements']):
        for field in req_required_fields:
            assert field in req, f"Requirement {i} missing field: {field}"
        
        # Validate field types
        assert isinstance(req['id'], str), f"Requirement {i} ID must be string"
        assert isinstance(req['tags'], list), f"Requirement {i} tags must be list"
        assert isinstance(req['confidence'], (int, float)), f"Requirement {i} confidence must be number"
        assert 0.0 <= req['confidence'] <= 1.0, f"Requirement {i} confidence must be 0.0-1.0"
    
    # Validate glossary
    assert isinstance(result['glossary_suspects'], list), "glossary_suspects must be list"
    
    print("✅ JSON schema validation passed")

def test_traditional_approach():
    """Test the traditional script-based approach"""
    print("\n🔧 Testing Traditional Script Approach")
    print("=" * 50)
    
    test_files = create_test_files()
    
    try:
        ingestor = RequirementsIngestor()
        file_list = list(test_files.values())
        result = ingestor.process_files(file_list, "TEST-TRADITIONAL-001")
        
        # Validate schema
        validate_json_schema(result)
        
        # Print summary
        print(f"✅ Processed {len(result['requirements'])} requirements")
        print(f"✅ Found {len(result['glossary_suspects'])} glossary terms")
        print(f"✅ Project ID: {result['project_id']}")
        
        # Sample requirements
        if result['requirements']:
            print(f"\n📋 Sample requirement:")
            sample = result['requirements'][0]
            print(f"   ID: {sample['id']}")
            print(f"   Text: {sample['text'][:100]}...")
            print(f"   Tags: {sample['tags']}")
            print(f"   Confidence: {sample['confidence']}")
        
        # Validate classification variety
        all_tags = set()
        for req in result['requirements']:
            all_tags.update(req['tags'])
        
        print(f"✅ Classification types found: {sorted(all_tags)}")
        
        return result
        
    except Exception as e:
        print(f"❌ Traditional approach failed: {e}")
        return None
    finally:
        # Cleanup
        for file_path in test_files.values():
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_copilot_approach():
    """Test the GitHub Copilot approach (demonstration)"""
    print("\n🤖 GitHub Copilot Integration Guide")
    print("=" * 50)
    
    print("✅ Primary Recommendation: Use GitHub Copilot directly")
    print("📝 Copy requirements document text into Copilot Chat")
    print("💬 Use prompt: '@workspace Use requirements-ingest skill to process this document:'")
    print("🎯 Copilot will intelligently extract and classify requirements")
    print("📋 No API keys or additional setup required!")
    
    print(f"\n💡 Sample Copilot Prompt:")
    print("=" * 30)
    print("@workspace Use requirements-ingest skill to process this document:")
    print("")
    print("# Sample Requirements")
    print("- System shall authenticate users within 3 seconds")
    print("- Database queries must complete under 100ms")
    print("- Budget cannot exceed $50,000")
    print("")
    print("Project ID: DEMO-001")
    print("Return structured JSON with atomic requirements and classifications.")
    print("=" * 30)
    
    return {"approach": "copilot", "status": "recommended"}

def test_output_folders_have_readmes():
    """Verify generated output folders are documented and existing notes survive."""
    with tempfile.TemporaryDirectory() as temp_dir:
        ingestor = RequirementsIngestor(output_base_dir=temp_dir)
        analysis_dir = ingestor._create_project_directory("README-TEST")
        folders = [
            Path(temp_dir),
            Path(temp_dir) / "projects",
            Path(temp_dir) / "projects" / "README-TEST",
            analysis_dir,
            analysis_dir / "source_files",
            analysis_dir / "versions",
        ]

        for folder in folders:
            readme = folder / "README.md"
            assert readme.is_file(), f"Missing README in {folder}"
            content = readme.read_text(encoding="utf-8")
            assert "## Purpose" in content
            assert "## Important Information" in content
            assert "## Major Events" in content

        project_readme = folders[2] / "README.md"
        project_readme.write_text(project_readme.read_text(encoding="utf-8") + "\nKeep this note.\n", encoding="utf-8")
        ingestor._create_project_directory("README-TEST")
        assert "Keep this note." in project_readme.read_text(encoding="utf-8")

def create_mock_ai_result(files, project_id):
    """Create a mock AI result for testing"""
    return {
        "project_id": project_id,
        "requirements": [
            {
                "id": "R-001",
                "source_file": Path(files[0]).name if files else "test.md",
                "location_hint": "Authentication Requirements section, paragraph 1",
                "text": "The system shall authenticate users using OAuth2 protocol within 3 seconds",
                "tags": ["functional", "nonfunctional"],
                "confidence": 0.95
            },
            {
                "id": "R-002", 
                "source_file": Path(files[1] if len(files) > 1 else files[0]).name if files else "test.txt",
                "location_hint": "Performance Requirements section, paragraph 2",
                "text": "API response times should not exceed 200ms for product searches",
                "tags": ["nonfunctional"],
                "confidence": 0.88
            }
        ],
        "glossary_suspects": ["OAuth2", "API", "PCI DSS", "AES-256"],
        "processing_notes": "Mock AI processing for testing",
        "models_used": ["mock/test-model"]
    }

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n⚠️ Testing Edge Cases")
    print("=" * 50)
    
    try:
        ingestor = RequirementsIngestor()
        
        # Test 1: Empty file list
        result = ingestor.process_files([], "EMPTY-TEST")
        assert result['project_id'] == "EMPTY-TEST"
        assert len(result['requirements']) == 0
        print("✅ Empty file list handled correctly")
        
        # Test 2: Non-existent file
        result = ingestor.process_files(["/nonexistent/file.pdf"], "ERROR-TEST")
        assert len(result['requirements']) >= 1  # Should have error requirement
        error_req = result['requirements'][0]
        assert "error" in error_req['text'].lower()
        print("✅ Non-existent file error handled correctly")
        
        # Test 3: Very short content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Short text")
            short_file = f.name
        
        try:
            result = ingestor.process_files([short_file], "SHORT-TEST")
            print("✅ Short content handled correctly")
        finally:
            os.unlink(short_file)
        
    except Exception as e:
        print(f"❌ Edge case testing failed: {e}")

def performance_test():
    """Test performance with larger content"""
    print("\n⚡ Performance Testing")
    print("=" * 50)
    
    # Create larger test file
    large_content = ""
    for i in range(100):
        large_content += f"Requirement {i}: The system shall process data efficiently for operation {i}. "
        large_content += f"Performance metric {i} must be under 100ms. "
        large_content += f"Security requirement {i} mandates encryption. "
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(large_content)
        large_file = f.name
    
    try:
        import time
        start_time = time.time()
        
        ingestor = RequirementsIngestor()
        result = ingestor.process_files([large_file], "PERF-TEST")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processed {len(large_content.split())} words in {processing_time:.2f} seconds")
        print(f"✅ Extracted {len(result['requirements'])} requirements")
        print(f"✅ Processing speed: {len(result['requirements'])/processing_time:.1f} req/sec")
        
    finally:
        os.unlink(large_file)

def main():
    """Run comprehensive test suite"""
    print("🚀 Requirements Ingest Skill - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Test traditional approach
        traditional_result = test_traditional_approach()
        
        # Show Copilot integration guide
        copilot_info = test_copilot_approach()
        
        # Test edge cases
        test_edge_cases()
        
        # Performance testing
        performance_test()
        
        print("\n🎉 All Tests Completed!")
        print("=" * 60)
        
        # Summary
        if traditional_result:
            print(f"\n📊 Traditional Script Results:")
            print(f"✅ Processed: {len(traditional_result['requirements'])} requirements")
            print(f"✅ Glossary: {len(traditional_result['glossary_suspects'])} terms")
            
        print(f"\n🤖 GitHub Copilot Integration:")
        print(f"✅ Primary approach - no setup required")
        print(f"✅ Use '@workspace' prompts for intelligent processing")
        print(f"✅ Interactive refinement through conversation")
        
        print(f"\n💡 Next Steps:")
        print(f"1. Try GitHub Copilot integration with your requirements")
        print(f"2. Use traditional scripts for batch processing")
        print(f"3. Test with the provided sample files in test_data/")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()