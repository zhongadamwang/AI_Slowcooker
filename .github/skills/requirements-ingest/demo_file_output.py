#!/usr/bin/env python3
"""
Quick Demo: Requirements Ingest with File Output
Demonstrates the structured folder output functionality
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from requirements_ingest import RequirementsIngestor

def create_sample_requirements():
    """Create a sample requirements file for testing"""
    sample_content = """# Sample E-commerce Requirements

## Authentication
- The system shall authenticate users within 3 seconds using OAuth2
- Multi-factor authentication must be required for admin accounts  
- Session timeout shall occur after 30 minutes of inactivity

## Performance  
- Product search results must load within 200ms
- The platform shall support 10,000 concurrent users
- Database queries must complete within 100ms for 95th percentile

## Security Constraints
- All payment data must comply with PCI DSS Level 1
- Customer data shall be encrypted using AES-256 encryption
- Budget for security infrastructure cannot exceed $50,000

## Assumptions
- Users have modern browsers supporting ES6+ JavaScript
- Third-party payment gateway availability is 99.9%
- Development team is experienced with React and Node.js

## Out of Scope
- Mobile application development
- Multi-language support for Phase 1
"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_content)
        return f.name

def demo_file_output():
    """Demonstrate the new file output functionality"""
    print("🚀 Requirements Ingest - File Output Demo")
    print("=" * 50)
    
    # Create sample requirements file
    sample_file = create_sample_requirements()
    
    try:
        # Initialize ingestor with custom output directory for demo
        demo_output_dir = "./demo_outputs"
        ingestor = RequirementsIngestor(output_base_dir=demo_output_dir)
        
        print(f"\n📁 Output directory: {demo_output_dir}")
        print(f"📝 Sample file created: {sample_file}")
        
        # Process the file
        project_id = "DEMO-FILE-OUTPUT-001"
        print(f"\n🔄 Processing with project ID: {project_id}")
        
        result = ingestor.process_files([sample_file], project_id, save_to_file=True)
        
        # Show what was created
        project_dir = Path(demo_output_dir) / "projects" / project_id
        
        print(f"\n✅ Files created:")
        for file_path in project_dir.rglob("*.json"):
            file_size = file_path.stat().st_size
            print(f"   📄 {file_path.relative_to(demo_output_dir)} ({file_size} bytes)")
        
        # Show sample of main output
        requirements_file = project_dir / "requirements.json"
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                data = json.load(f)
            
            print(f"\n📊 Processing Summary:")
            print(f"   • Total requirements: {data['total_requirements']}")
            print(f"   • Glossary terms: {len(data['glossary_suspects'])}")
            print(f"   • Processing time: {data['processing_summary']['processing_time_seconds']}s")
            print(f"   • Average confidence: {data['processing_summary']['avg_confidence']}")
            
            if data['requirements']:
                print(f"\n📋 Sample requirement:")
                sample_req = data['requirements'][0]
                print(f"   ID: {sample_req['id']}")
                print(f"   Text: {sample_req['text'][:80]}...")
                print(f"   Tags: {sample_req['tags']}")
                print(f"   Confidence: {sample_req['confidence']}")
            
            print(f"\n📚 Glossary terms: {', '.join(data['glossary_suspects'][:5])}")
        
        # Show folder structure
        print(f"\n📂 Created folder structure:")
        for root, dirs, files in os.walk(project_dir):
            level = root.replace(str(project_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root) if level > 0 else project_id
            print(f"{indent}{folder_name}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
        print(f"\n🎯 **For Downstream Skills:**")
        print(f"   Load requirements from: {requirements_file}")
        print(f"   Standard access pattern:")
        print(f"   ```python")
        print(f"   with open('{requirements_file}') as f:")
        print(f"       requirements = json.load(f)")
        print(f"   ```")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup sample file
        if os.path.exists(sample_file):
            os.unlink(sample_file)

def main():
    """Run the file output demonstration"""
    success = demo_file_output()
    
    if success:
        print(f"\n🎉 Demo completed successfully!")
        print(f"\n💡 Next Steps:")
        print(f"   1. Check the created files in demo_outputs/")
        print(f"   2. Use 'requirements.json' with downstream skills")
        print(f"   3. Review 'processing_log.json' for audit trail")
        print(f"   4. Use 'glossary.json' for domain modeling")
    else:
        print(f"\n❌ Demo failed - check error messages above")

if __name__ == "__main__":
    main()