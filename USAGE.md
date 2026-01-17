# Usage Guide - Lego Instruction Personalizer

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Run Demo

```bash
# Basic demo with default settings
python cli.py --demo --display

# Advanced user with custom preferences
python cli.py --demo --skill-level advanced --interests techniques detailed_build --display

# Expert user with fast pacing
python cli.py --demo --skill-level expert --interaction-frequency low --display
```

### 3. Run Examples

```bash
python examples.py
```

### 4. Verify Implementation

```bash
python verify_requirements.py
```

## Command Line Options

### --demo
Run with sample instruction data (no PDF required)

### --pdf PATH
Path to PDF instruction file

### --skill-level LEVEL
User skill level: `beginner`, `intermediate`, `advanced`, `expert`

### --interests CATEGORIES
One or more interest categories:
- `vehicles` - Car, plane, boat builds
- `buildings` - House, castle, structure builds  
- `characters` - Minifigures and character builds
- `techniques` - Special building techniques
- `speed_build` - Quick, efficient building
- `detailed_build` - Detailed, complex building

### --interaction-frequency FREQ
How often to insert interactions: `low`, `medium`, `high`

### --output PATH
Export personalized instructions to JSON file

### --display
Display instructions in terminal

## Use Cases

### Beginner Builder
```bash
python cli.py --demo --skill-level beginner \
  --interaction-frequency high --display
```
- Shows all instruction steps
- High interaction frequency for guidance
- Includes basic tips and encouragement

### Expert Builder
```bash
python cli.py --demo --skill-level expert \
  --interests techniques --interaction-frequency low --display
```
- Filters to advanced techniques only
- Minimal interactions
- Fast-paced experience

### Teaching Children
```bash
python cli.py --demo --skill-level beginner \
  --interests characters speed_build \
  --interaction-frequency high --display
```
- Kid-friendly pacing
- Lots of encouragement
- Focus on fun character builds

### Speed Building
```bash
python cli.py --demo --skill-level advanced \
  --interests speed_build --interaction-frequency low --display
```
- Streamlined instructions
- Skips unnecessary details
- Minimal distractions

## Python API

### Basic Usage

```python
from lego_instructor import (
    PDFRecognizer,
    InstructionDecomposer,
    InstructionPersonalizer,
    InteractionManager,
)
from lego_instructor.personalizer import UserProfile, SkillLevel

# Load and recognize PDF
recognizer = PDFRecognizer()
steps = recognizer.recognize_instructions("instructions.pdf")

# Decompose into units
decomposer = InstructionDecomposer()
units = decomposer.decompose(steps)

# Create user profile
profile = UserProfile(skill_level=SkillLevel.INTERMEDIATE)

# Personalize
personalizer = InstructionPersonalizer(profile)
personalized = personalizer.personalize(units)

# Add interactions
interaction_mgr = InteractionManager(frequency="medium")
interactions = interaction_mgr.generate_interactions(personalized)
final = interaction_mgr.insert_interactions(personalized, interactions)
```

### Advanced: Custom Decomposition Rules

```python
from lego_instructor.instruction_decomposer import DecompositionRule

# Define custom rule
def has_keyword(step):
    return "special" in step.text.lower()

def split_special(step):
    # Custom splitting logic
    return [...]

rule = DecompositionRule("split_special", has_keyword, split_special)
decomposer.add_rule(rule)
```

### Advanced: Custom User Preferences

```python
profile = UserProfile(skill_level=SkillLevel.ADVANCED)
profile.add_interest(InterestCategory.TECHNIQUES)
profile.set_preference("skip_basics", True)
profile.set_preference("pacing", "fast")
profile.set_preference("show_techniques", True)
```

## Output Formats

### Terminal Display
Pretty-printed with icons and formatting
```bash
python cli.py --demo --display
```

### JSON Export
Structured data for integration
```bash
python cli.py --demo --output instructions.json
```

JSON structure:
```json
[
  {
    "type": "comment",
    "content": "Welcome!",
    "position": 0
  },
  {
    "unit_id": 1,
    "content": "Step 1...",
    "unit_type": "basic",
    "difficulty": 1,
    "tags": ["assembly"]
  }
]
```

## Tips

1. **For PDF Processing**: Ensure PDF has extractable text (not scanned images)
2. **Performance**: Large PDFs may take time to process
3. **Customization**: Create custom decomposition rules for specific instruction formats
4. **Testing**: Use `--demo` mode for quick testing without PDF files

## Troubleshooting

### No PDF file
Use `--demo` flag to run with sample data

### Missing dependencies
```bash
pip install -r requirements.txt
```

### PDF not recognized
- Check PDF has extractable text
- Verify file path is correct
- Try with demo mode first

## Examples Directory

See `examples.py` for comprehensive API usage examples:
- Basic workflow
- Advanced user profiles
- Custom interaction patterns
- Unit filtering and analysis
