"""
Requirements Ingest System
Normalizes requirements from multiple file formats into structured chunks.
"""

import json
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
import uuid

# File format handlers
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    PyPDF2 = None
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from email import message_from_string
    from email.policy import default
except ImportError:
    message_from_string = None

@dataclass
class RequirementChunk:
    """Single atomic requirement with metadata"""
    id: str
    source_file: str
    location_hint: str
    text: str
    tags: List[str]
    confidence: float

class RequirementsIngestor:
    """Main class for requirements ingestion and processing"""
    
    def __init__(self):
        self.classification_keywords = {
            'functional': [
                'shall', 'must', 'will', 'should', 'function', 'feature', 
                'user', 'system', 'process', 'calculate', 'display', 'store'
            ],
            'nonfunctional': [
                'performance', 'speed', 'response time', 'security', 'usability',
                'reliability', 'availability', 'scalability', 'throughput'
            ],
            'constraint': [
                'budget', 'timeline', 'technology', 'regulation', 'compliance',
                'limitation', 'restriction', 'cannot', 'prohibited'
            ],
            'assumption': [
                'assume', 'given', 'provided', 'available', 'expected',
                'prerequisite', 'dependency', 'relies on'
            ],
            'out-of-scope': [
                'out of scope', 'excluded', 'not included', 'future release',
                'phase 2', 'beyond', 'outside'
            ]
        }
    
    def process_files(self, files: List[str], project_id: str) -> Dict[str, Any]:
        """Main entry point for processing multiple files"""
        all_requirements = []
        all_glossary_terms = []
        
        for file_path in files:
            try:
                chunks = self._process_single_file(file_path)
                all_requirements.extend(chunks)
                
                # Extract glossary candidates
                text_content = ' '.join([chunk.text for chunk in chunks])
                glossary_terms = self._extract_glossary_suspects(text_content)
                all_glossary_terms.extend(glossary_terms)
                
            except Exception as e:
                # Add error chunk for problematic files
                error_chunk = RequirementChunk(
                    id=f"R-ERROR-{len(all_requirements) + 1:03d}",
                    source_file=file_path,
                    location_hint="file processing error",
                    text=f"Error processing file: {str(e)}",
                    tags=["assumption"],
                    confidence=0.1
                )
                all_requirements.append(error_chunk)
        
        # Remove duplicate glossary terms and filter
        unique_glossary = list(set(all_glossary_terms))
        
        return {
            "project_id": project_id,
            "requirements": [self._chunk_to_dict(chunk) for chunk in all_requirements],
            "glossary_suspects": unique_glossary
        }
    
    def _process_single_file(self, file_path: str) -> List[RequirementChunk]:
        """Process a single file and extract requirements"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._process_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._process_docx(file_path)
        elif file_ext in ['.md', '.markdown']:
            return self._process_markdown(file_path)
        elif file_ext in ['.eml', '.email', '.txt']:
            return self._process_email(file_path)
        else:
            # Fallback: treat as plain text
            return self._process_text(file_path)
    
    def _process_pdf(self, file_path: str) -> List[RequirementChunk]:
        """Extract requirements from PDF files"""
        chunks = []
        
        if not pdfplumber:
            raise ImportError("PDF processing requires pdfplumber: pip install pdfplumber")
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    page_chunks = self._split_into_chunks(
                        text, 
                        file_path, 
                        f"page {page_num}"
                    )
                    chunks.extend(page_chunks)
        
        return chunks
    
    def _process_docx(self, file_path: str) -> List[RequirementChunk]:
        """Extract requirements from DOCX files"""
        if not Document:
            raise ImportError("DOCX processing requires python-docx: pip install python-docx")
        
        doc = Document(file_path)
        chunks = []
        
        for para_num, paragraph in enumerate(doc.paragraphs, 1):
            if paragraph.text.strip():
                chunk_text = paragraph.text.strip()
                if self._is_requirement_candidate(chunk_text):
                    chunk = self._create_chunk(
                        chunk_text, 
                        file_path, 
                        f"paragraph {para_num}"
                    )
                    chunks.append(chunk)
        
        return chunks
    
    def _process_markdown(self, file_path: str) -> List[RequirementChunk]:
        """Extract requirements from Markdown files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by headers to get sections
        sections = re.split(r'^#{1,6}\s+', content, flags=re.MULTILINE)
        chunks = []
        
        for i, section in enumerate(sections):
            if section.strip():
                section_chunks = self._split_into_chunks(
                    section, 
                    file_path, 
                    f"section {i+1}"
                )
                chunks.extend(section_chunks)
        
        return chunks
    
    def _process_email(self, file_path: str) -> List[RequirementChunk]:
        """Extract requirements from email files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if message_from_string:
            try:
                email_msg = message_from_string(content, policy=default)
                body = email_msg.get_body(preferencelist=('plain', 'html'))
                if body:
                    content = str(body)
            except:
                pass  # Fallback to treating as plain text
        
        return self._split_into_chunks(content, file_path, "email body")
    
    def _process_text(self, file_path: str) -> List[RequirementChunk]:
        """Fallback processor for plain text files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self._split_into_chunks(content, file_path, "text file")
    
    def _split_into_chunks(self, text: str, source_file: str, location_hint: str) -> List[RequirementChunk]:
        """Split text into atomic requirement chunks"""
        chunks = []
        
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        
        current_chunk = ""
        sentence_count = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_count += 1
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            # Check if chunk is getting too long (≈200 tokens ≈ 150 words)
            word_count = len(test_chunk.split())
            
            if word_count > 150 and current_chunk:
                # Save current chunk and start new one
                if self._is_requirement_candidate(current_chunk):
                    chunk = self._create_chunk(
                        current_chunk,
                        source_file,
                        f"{location_hint}, sent {sentence_count - 1}"
                    )
                    chunks.append(chunk)
                current_chunk = sentence
            else:
                current_chunk = test_chunk
        
        # Handle the last chunk
        if current_chunk and self._is_requirement_candidate(current_chunk):
            chunk = self._create_chunk(
                current_chunk,
                source_file,
                f"{location_hint}, sent {sentence_count}"
            )
            chunks.append(chunk)
        
        return chunks
    
    def _is_requirement_candidate(self, text: str) -> bool:
        """Determine if text contains requirements"""
        text_lower = text.lower()
        
        # Skip very short texts
        if len(text.split()) < 3:
            return False
        
        # Look for requirement indicators
        requirement_indicators = [
            'shall', 'must', 'will', 'should', 'requires', 'needs',
            'system', 'user', 'application', 'feature', 'function'
        ]
        
        return any(indicator in text_lower for indicator in requirement_indicators)
    
    def _create_chunk(self, text: str, source_file: str, location_hint: str) -> RequirementChunk:
        """Create a RequirementChunk with classification"""
        # Generate unique ID
        chunk_id = f"R-{hash(text + source_file + location_hint) % 10000:04d}"
        
        # Classify the requirement
        tags = self._classify_requirement(text)
        
        # Calculate confidence based on text clarity
        confidence = self._calculate_confidence(text)
        
        return RequirementChunk(
            id=chunk_id,
            source_file=Path(source_file).name,
            location_hint=location_hint,
            text=text.strip(),
            tags=tags,
            confidence=confidence
        )
    
    def _classify_requirement(self, text: str) -> List[str]:
        """Classify requirement into tags"""
        text_lower = text.lower()
        tags = []
        
        for category, keywords in self.classification_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(category)
        
        # Default to functional if no other tags
        if not tags:
            tags = ['functional']
        
        return tags
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score based on text clarity"""
        score = 0.5  # Base score
        
        # Higher confidence for clear requirement language
        if any(word in text.lower() for word in ['shall', 'must', 'will']):
            score += 0.3
        
        # Higher confidence for specific measurements
        if re.search(r'\d+', text):
            score += 0.2
        
        # Lower confidence for vague language
        if any(word in text.lower() for word in ['maybe', 'probably', 'might', 'unclear']):
            score -= 0.3
        
        # Lower confidence for very long sentences
        if len(text.split()) > 50:
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _extract_glossary_suspects(self, text: str) -> List[str]:
        """Extract potential glossary terms from text"""
        # Find technical terms (capitalized words, acronyms)
        words = re.findall(r'\b[A-Z][A-Za-z]*\b|\b[A-Z]{2,}\b', text)
        
        # Count occurrences
        word_counts = {}
        for word in words:
            if len(word) > 2:  # Skip short words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Return words that appear 2+ times
        return [word for word, count in word_counts.items() if count >= 2]
    
    def _chunk_to_dict(self, chunk: RequirementChunk) -> Dict[str, Any]:
        """Convert RequirementChunk to dictionary"""
        return {
            "id": chunk.id,
            "source_file": chunk.source_file,
            "location_hint": chunk.location_hint,
            "text": chunk.text,
            "tags": chunk.tags,
            "confidence": round(chunk.confidence, 2)
        }


def main():
    """CLI interface for requirements ingestion"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python requirements_ingest.py <project_id> <file1> [file2] ...")
        sys.exit(1)
    
    project_id = sys.argv[1]
    files = sys.argv[2:]
    
    ingestor = RequirementsIngestor()
    result = ingestor.process_files(files, project_id)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()