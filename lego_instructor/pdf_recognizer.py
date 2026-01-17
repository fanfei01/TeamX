"""
PDF Recognition Module
Recognizes e-version of building instructions in PDF format with pictures and text.
"""

import io
import logging
from typing import List, Dict, Any, Optional
from PyPDF2 import PdfReader
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstructionStep:
    """Represents a single step in the building instructions."""
    
    def __init__(self, step_number: int, text: str, images: List[Image.Image] = None, page_number: int = 0):
        self.step_number = step_number
        self.text = text
        self.images = images or []
        self.page_number = page_number
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary representation."""
        return {
            "step_number": self.step_number,
            "text": self.text,
            "image_count": len(self.images),
            "page_number": self.page_number,
            "metadata": self.metadata
        }
    
    def __repr__(self):
        return f"InstructionStep(step={self.step_number}, text='{self.text[:50]}...', images={len(self.images)})"


class PDFRecognizer:
    """
    Recognizes and extracts building instructions from PDF files.
    Extracts both text and images from each page.
    """
    
    def __init__(self):
        self.steps: List[InstructionStep] = []
        self.metadata = {}
    
    def load_pdf(self, pdf_path: str) -> bool:
        """
        Load and parse a PDF file containing Lego building instructions.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            reader = PdfReader(pdf_path)
            self.metadata = {
                "num_pages": len(reader.pages),
                "pdf_path": pdf_path
            }
            
            # Extract metadata if available
            if reader.metadata:
                self.metadata["title"] = reader.metadata.get("/Title", "Unknown")
                self.metadata["author"] = reader.metadata.get("/Author", "Unknown")
            
            return True
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text content from each page of the PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page number and text content
        """
        pages_content = []
        
        try:
            reader = PdfReader(pdf_path)
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                pages_content.append({
                    "page_number": page_num,
                    "text": text.strip() if text else "",
                    "has_text": bool(text and text.strip())
                })
                
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
        
        return pages_content
    
    def extract_images_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract images from each page of the PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page number and images
        """
        images_by_page = []
        
        try:
            reader = PdfReader(pdf_path)
            
            for page_num, page in enumerate(reader.pages, 1):
                page_images = []
                
                if "/XObject" in page["/Resources"]:
                    xobjects = page["/Resources"]["/XObject"].get_object()
                    
                    for obj_name in xobjects:
                        obj = xobjects[obj_name]
                        
                        if obj["/Subtype"] == "/Image":
                            try:
                                # Extract image data
                                size = (obj["/Width"], obj["/Height"])
                                data = obj.get_data()
                                
                                # Try to create PIL Image
                                if obj["/ColorSpace"] == "/DeviceRGB":
                                    img = Image.frombytes("RGB", size, data)
                                    page_images.append(img)
                                elif obj["/ColorSpace"] == "/DeviceGray":
                                    img = Image.frombytes("L", size, data)
                                    page_images.append(img)
                            except Exception as img_error:
                                logger.warning(f"Error extracting image from page {page_num}: {img_error}")
                
                images_by_page.append({
                    "page_number": page_num,
                    "images": page_images,
                    "image_count": len(page_images)
                })
                
        except Exception as e:
            logger.error(f"Error extracting images: {e}")
        
        return images_by_page
    
    def recognize_instructions(self, pdf_path: str) -> List[InstructionStep]:
        """
        Recognize and extract building instructions from PDF.
        Combines text and images into structured instruction steps.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of InstructionStep objects
        """
        if not self.load_pdf(pdf_path):
            return []
        
        # Extract text and images
        text_content = self.extract_text_from_pdf(pdf_path)
        images_content = self.extract_images_from_pdf(pdf_path)
        
        # Combine into instruction steps
        self.steps = []
        step_counter = 1
        
        for page_idx in range(len(text_content)):
            page_text = text_content[page_idx]["text"]
            page_images = images_content[page_idx]["images"] if page_idx < len(images_content) else []
            page_num = text_content[page_idx]["page_number"]
            
            # Create a step for each page (simplified approach)
            # In a real implementation, you'd parse the text to identify individual steps
            if page_text or page_images:
                step = InstructionStep(
                    step_number=step_counter,
                    text=page_text,
                    images=page_images,
                    page_number=page_num
                )
                self.steps.append(step)
                step_counter += 1
        
        return self.steps
    
    def get_steps(self) -> List[InstructionStep]:
        """Get the list of recognized instruction steps."""
        return self.steps
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the PDF."""
        return self.metadata
