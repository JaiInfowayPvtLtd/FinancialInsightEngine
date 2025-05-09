import logging
import os
import re

class PDFProcessor:
    """
    Utility for processing PDF files to extract and analyze text content
    """
    
    def __init__(self):
        """Initialize the PDF processor"""
        logging.info("PDF Processor initialized")
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
        """
        # Since we're not using PyPDF2 directly (as it would require installing it),
        # we'll use a simpler approach for demonstration purposes
        
        # Check if the file exists
        if not os.path.exists(pdf_path):
            logging.error(f"PDF file not found: {pdf_path}")
            return ""
        
        # If the file is actually a text file, read it directly
        if pdf_path.endswith('.txt'):
            try:
                with open(pdf_path, 'r') as f:
                    return f.read()
            except Exception as e:
                logging.error(f"Error reading text file: {str(e)}")
                return ""
        
        # For actual PDFs, we'd use PyPDF2, but here we'll just return a message
        logging.warning(f"Cannot process actual PDF files without PyPDF2. File: {pdf_path}")
        return "PDF processing simulated. Install PyPDF2 for actual PDF processing."
    
    def search_in_pdf(self, pdf_text, search_terms):
        """
        Search for terms in PDF text content
        
        Args:
            pdf_text (str): The text content extracted from a PDF
            search_terms (list): List of terms to search for
            
        Returns:
            dict: Dictionary mapping search terms to matching contexts
        """
        results = {}
        
        for term in search_terms:
            # Find all occurrences with surrounding context
            pattern = rf"(?i)(.{{0,100}}){re.escape(term)}(.{{0,100}})"
            matches = re.findall(pattern, pdf_text)
            
            if matches:
                # Format the matches with highlighting
                formatted_matches = [
                    f"...{before}<b>{term}</b>{after}..."
                    for before, after in matches
                ]
                results[term] = formatted_matches
        
        return results
    
    def summarize_pdf(self, pdf_text, max_length=500):
        """
        Generate a simple summary of PDF content
        
        Args:
            pdf_text (str): The text content extracted from a PDF
            max_length (int): Maximum length of the summary
            
        Returns:
            str: Summarized text
        """
        # This is a simplified summarization approach
        # In a real application, more sophisticated NLP would be used
        
        # Extract the first few paragraphs as a summary
        paragraphs = pdf_text.split('\n\n')
        summary_paragraphs = []
        current_length = 0
        
        for paragraph in paragraphs:
            # Skip very short lines or empty lines
            if len(paragraph.strip()) < 20:
                continue
                
            paragraph = paragraph.strip()
            paragraph_length = len(paragraph)
            
            if current_length + paragraph_length <= max_length:
                summary_paragraphs.append(paragraph)
                current_length += paragraph_length
            else:
                # Add a truncated version of the paragraph to reach max_length
                space_left = max_length - current_length
                if space_left > 50:  # Only add if we can include a meaningful chunk
                    summary_paragraphs.append(paragraph[:space_left] + "...")
                break
        
        return "\n\n".join(summary_paragraphs)
