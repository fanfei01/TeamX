# LEGO Instruction Personalizer

Hackathon Project 2026 - TeamX

A personalized building instruction experience for Lego sets that recognizes, decomposes, and personalizes PDF building instructions to match individual user preferences and skill levels.

## Features

### 1. 📄 PDF Recognition
- Recognizes e-version of building instructions in PDF format
- Extracts both pictures and text from PDF documents
- Handles multi-page instruction manuals
- Preserves step-by-step structure

### 2. 🔧 Instruction Decomposition
- Decomposes building instruction sequences into minimal units
- Applies customizable decomposition rules
- Classifies units by type (basic, intermediate, complex, technique)
- Estimates difficulty and time for each unit

### 3. 👤 Personalization
- Re-selects and re-arranges instruction units based on:
  - User skill level (beginner, intermediate, advanced, expert)
  - User interests (vehicles, buildings, characters, techniques, etc.)
  - Pacing preferences (slow, normal, fast)
- Filters content appropriately for skill level
- Maintains logical prerequisites

### 4. 💬 Interactive Engagement
- Inserts interactions between instruction units:
  - ❓ Questions to check progress
  - 💡 Suggestions for better building
  - 💬 Comments about techniques
  - ⭐ Encouragement messages
  - 🔍 Pro tips and tricks
- Configurable interaction frequency (low, medium, high)

## Installation

```bash
# Clone the repository
git clone https://github.com/fanfei01/TeamX.git
cd TeamX

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## Usage

### Quick Start (Demo Mode)

Run with sample data (no PDF required):

```bash
python cli.py --demo --display
```

### Command Line Interface

```bash
# Basic usage with PDF
python cli.py --pdf instructions.pdf --display

# Customize for skill level
python cli.py --demo --skill-level advanced --display

# Add interests
python cli.py --demo --skill-level intermediate \
  --interests techniques detailed_build --display

# Adjust interaction frequency
python cli.py --demo --interaction-frequency high --display

# Export to JSON
python cli.py --demo --output personalized_instructions.json
```

### Python API

```python
from lego_instructor import (
    PDFRecognizer,
    InstructionDecomposer,
    InstructionPersonalizer,
    InteractionManager,
)
from lego_instructor.personalizer import UserProfile, SkillLevel, InterestCategory

# 1. Recognize PDF instructions
recognizer = PDFRecognizer()
steps = recognizer.recognize_instructions("lego_set_12345.pdf")

# 2. Decompose into minimal units
decomposer = InstructionDecomposer()
units = decomposer.decompose(steps)

# 3. Create user profile and personalize
profile = UserProfile(skill_level=SkillLevel.INTERMEDIATE)
profile.add_interest(InterestCategory.TECHNIQUES)

personalizer = InstructionPersonalizer(profile)
personalized_units = personalizer.personalize(units)

# 4. Add interactions
interaction_mgr = InteractionManager(frequency="medium")
interactions = interaction_mgr.generate_interactions(personalized_units)
final_sequence = interaction_mgr.insert_interactions(personalized_units, interactions)

# Use the personalized sequence
for item in final_sequence:
    print(item)
```

## Architecture

The system consists of four main modules:

### 1. `pdf_recognizer.py`
- **PDFRecognizer**: Extracts text and images from PDF files
- **InstructionStep**: Represents a single instruction step

### 2. `instruction_decomposer.py`
- **InstructionDecomposer**: Breaks down instructions into minimal units
- **InstructionUnit**: Represents a minimal instruction unit
- **DecompositionRule**: Defines rules for decomposition
- **UnitType**: Enum for unit types (basic, intermediate, complex, technique)

### 3. `personalizer.py`
- **InstructionPersonalizer**: Personalizes instruction sequences
- **UserProfile**: Stores user preferences and skill level
- **SkillLevel**: Enum for skill levels
- **InterestCategory**: Enum for user interests

### 4. `interaction_manager.py`
- **InteractionManager**: Generates and inserts interactions
- **Interaction**: Represents an interactive element
- **InteractionType**: Enum for interaction types

## Examples

### Example Output

```
============================================================
   PERSONALIZED BUILDING INSTRUCTIONS
============================================================

💬 COMMENT: Welcome! Let's build something amazing together!

[Unit 1] ⭐ (basic)
  Welcome to your LEGO building experience! Gather all pieces from the box.
  Tags: assembly

❓ QUESTION: Have you found all the pieces for this step?

[Unit 2] ⭐⭐ (intermediate)
  Step 1: Find 4 red 2x4 bricks. Connect them in a square formation.
  Tags: assembly, connection

💡 SUGGESTION: Try organizing your pieces by color before starting.

[Unit 3] ⭐⭐⭐⭐ (complex)
  Step 3: Attach the special technique piece - the turntable base. This allows rotation.
  Tags: technique

⭐ ENCOURAGEMENT: Congratulations! You've completed your build! 🎉
```

## Requirements

- Python 3.7+
- PyPDF2 >= 3.0.0
- pdf2image >= 1.16.0
- Pillow >= 10.0.0

## Project Structure

```
TeamX/
├── lego_instructor/
│   ├── __init__.py
│   ├── pdf_recognizer.py
│   ├── instruction_decomposer.py
│   ├── personalizer.py
│   └── interaction_manager.py
├── cli.py
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

## License

See LICENSE file for details.

## Contributing

This is a hackathon project. Contributions and feedback are welcome!

## Future Enhancements

- Support for more PDF formats and layouts
- Image recognition for piece identification
- Multi-language support
- Web interface
- Mobile app integration
- AR visualization of steps
- Community sharing of personalized sequences
