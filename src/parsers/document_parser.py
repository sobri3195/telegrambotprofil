"""
Document parser for handling PDF and text file inputs.
"""
import io
from typing import Optional
from PyPDF2 import PdfReader


class DocumentParser:
    """Parse various document formats to extract text content."""
    
    @staticmethod
    def parse_pdf(file_content: bytes) -> str:
        """
        Parse PDF file and extract text.
        
        Args:
            file_content: Raw PDF file bytes
            
        Returns:
            Extracted text content
        """
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return '\n'.join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def parse_text(file_content: bytes) -> str:
        """
        Parse text file.
        
        Args:
            file_content: Raw text file bytes
            
        Returns:
            Decoded text content
        """
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1')
            except Exception as e:
                raise ValueError(f"Failed to decode text: {str(e)}")
    
    @classmethod
    def parse_document(cls, file_content: bytes, file_extension: str) -> str:
        """
        Parse document based on file extension.
        
        Args:
            file_content: Raw file bytes
            file_extension: File extension (pdf, txt)
            
        Returns:
            Extracted text content
        """
        file_extension = file_extension.lower().strip('.')
        
        if file_extension == 'pdf':
            return cls.parse_pdf(file_content)
        elif file_extension == 'txt':
            return cls.parse_text(file_content)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
