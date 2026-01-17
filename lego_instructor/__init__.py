"""
Lego Instruction Personalizer
A system for recognizing, decomposing, and personalizing Lego building instructions.
"""

__version__ = "1.0.0"

from .pdf_recognizer import PDFRecognizer
from .instruction_decomposer import InstructionDecomposer
from .personalizer import InstructionPersonalizer
from .interaction_manager import InteractionManager

__all__ = [
    "PDFRecognizer",
    "InstructionDecomposer",
    "InstructionPersonalizer",
    "InteractionManager",
]
