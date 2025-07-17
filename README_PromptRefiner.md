# PromptRefiner Module

An intelligent Python module that analyzes app prompts and generates comprehensive, enhanced specifications by identifying ambiguities and adding missing technical details.

## 🎯 Purpose

The PromptRefiner module transforms vague app ideas into detailed, actionable specifications that can guide development teams. It:

- **Analyzes** original prompts for app type, features, and user roles
- **Identifies** ambiguities and missing requirements  
- **Generates** comprehensive technical specifications
- **Resolves** unclear requirements with industry best practices
- **Outputs** structured JSON specifications for development use

## 🚀 Features

### Core Functionality
- **App Type Detection**: Automatically categorizes apps (e-commerce, social, productivity, etc.)
- **Feature Extraction**: Identifies mentioned and implied features
- **User Role Definition**: Defines user roles with specific permissions
- **Ambiguity Resolution**: Finds and resolves vague requirements
- **Technical Specification**: Generates complete tech stack recommendations

### Enhanced Specifications Include
- **User Roles & Permissions**: Detailed role definitions with access levels
- **Feature Specifications**: Prioritized feature list with descriptions
- **Technical Requirements**: Frontend, backend, database, and hosting specs
- **Business Constraints**: Budget, timeline, compliance requirements
- **UI/UX Requirements**: Design system, accessibility, performance targets
- **Data Architecture**: Entity relationships and storage requirements
- **Integration Needs**: Third-party services and APIs
- **Security Requirements**: Comprehensive security measures
- **Performance Targets**: Response times, scalability, monitoring
- **Deployment Strategy**: CI/CD, environments, infrastructure

## 📦 Installation

No external dependencies required! Uses only Python standard library.

```bash
# Clone or download the module files
# No pip install needed - uses built-in Python libraries
```

## 🔧 Usage

### Basic Usage

```python
from prompt_refiner import PromptRefiner

# Initialize the refiner
refiner = PromptRefiner()

# Your app prompt
prompt = """
Create a simple e-commerce app where users can buy and sell products. 
It should be secure and fast, with a modern design.
"""

# Generate enhanced specification
enhanced_spec = refiner.refine_prompt(prompt)

# Access the results
print(f"App Name: {enhanced_spec.app_name}")
print(f"App Type: {enhanced_spec.app_type}")
print(f"Features: {len(enhanced_spec.features)}")
```

### Advanced Usage

```python
from prompt_refiner import PromptRefiner

refiner = PromptRefiner()

# Analyze prompt first
analysis = refiner.analyze_prompt(prompt)
print(f"Detected app type: {analysis['app_type']}")
print(f"Found features: {analysis['detected_features']}")
print(f"Ambiguities: {len(analysis['ambiguities'])}")

# Generate full specification
enhanced_spec = refiner.generate_enhanced_spec(prompt)

# Save to custom file
refiner.save_enhanced_spec(enhanced_spec, "my_app_spec.json")
```

### Running Tests

```bash
python test_prompt_refiner.py
```

This will test the module with various prompt types and generate example specification files.

## 📋 Output Structure

The enhanced specification includes:

```json
{
  "original_prompt": "...",
  "app_name": "ShopHub",
  "app_type": "e-commerce",
  "target_audience": "Online shoppers and retail businesses",
  "core_purpose": "Enable online buying and selling of products",
  "user_roles": [
    {
      "name": "user",
      "description": "Standard application user",
      "permissions": ["read", "create_own", "update_own", "delete_own"]
    }
  ],
  "features": [
    {
      "name": "product_catalog",
      "priority": "high",
      "description": "Browse and search products"
    }
  ],
  "technical_requirements": {
    "frontend": {
      "framework": "React",
      "styling": "Tailwind CSS"
    },
    "backend": {
      "runtime": "Node.js",
      "framework": "Express.js"
    }
  },
  "ambiguities_resolved": [
    {
      "original_ambiguity": "What specific features define 'simple'?",
      "resolution": "Implement clean, intuitive UI with minimal clicks",
      "rationale": "Based on e-commerce app requirements and best practices"
    }
  ]
}
```

## 🎨 Supported App Types

The module automatically detects and optimizes for:

- **E-commerce**: Online stores, marketplaces, product catalogs
- **Social**: Social networks, messaging apps, communities  
- **Productivity**: Task management, project tools, collaboration
- **Content**: Blogs, CMS, publishing platforms
- **Analytics**: Dashboards, reporting, data visualization
- **Booking**: Appointment scheduling, reservations
- **Learning**: Educational platforms, courses, tutorials
- **Finance**: Budgeting, expense tracking, invoicing

## 🔍 Ambiguity Detection

The module identifies and resolves common ambiguities:

### Vague Terms
- "Simple" → Specific UI/UX requirements
- "Secure" → Detailed security measures
- "Fast" → Performance benchmarks
- "Modern" → Design system specifications

### Missing Technical Details
- Database requirements
- Authentication methods
- Payment processing
- Notification channels
- Hosting requirements

### Business Constraints
- Currency support
- Compliance requirements
- Scalability targets
- Integration needs

## 📊 Logging & Transparency

The module provides detailed console logging:

```
2024-01-15 10:30:00 - INFO - Starting prompt analysis...
2024-01-15 10:30:01 - INFO - Detected app type: e-commerce
2024-01-15 10:30:01 - INFO - Found 5 features
2024-01-15 10:30:01 - INFO - Identified 3 ambiguities
2024-01-15 10:30:02 - INFO - Generating enhanced specification...
2024-01-15 10:30:03 - INFO - Enhanced specification generated successfully
2024-01-15 10:30:03 - INFO - Saving enhanced specification to enhanced_spec_20240115_103003.json
```

## 🛠️ Customization

### Adding New App Types

```python
# Extend app type patterns
refiner.app_type_patterns['new_type'] = ['keyword1', 'keyword2']
```

### Custom Feature Detection

```python
# Add new feature patterns
refiner.common_features['new_feature'] = ['feature_keyword']
```

### Custom Ambiguity Rules

```python
# Override ambiguity resolution
def custom_resolution(ambiguity, analysis):
    return "Custom resolution logic"
```

## 📁 File Structure

```
├── prompt_refiner.py          # Main module
├── test_prompt_refiner.py     # Test suite
├── requirements.txt           # Dependencies (none needed)
├── README_PromptRefiner.md    # This documentation
└── generated_specs/           # Output directory (created automatically)
    ├── ecommerce_spec.json
    ├── social_spec.json
    └── productivity_spec.json
```

## 🔄 Integration with Development Workflow

1. **Requirements Gathering**: Use PromptRefiner to analyze initial app ideas
2. **Specification Review**: Review generated specs with stakeholders
3. **Development Planning**: Use technical requirements for architecture decisions
4. **Feature Prioritization**: Use feature priorities for sprint planning
5. **Quality Assurance**: Use security and performance requirements for testing

## 🎯 Example Use Cases

### Startup MVP Planning
```python
prompt = "Build a food delivery app for local restaurants"
spec = refiner.refine_prompt(prompt)
# Get comprehensive MVP requirements with technical stack
```

### Client Project Scoping
```python
prompt = "Create a booking system for hair salons"
spec = refiner.refine_prompt(prompt)
# Generate detailed project scope and timeline estimates
```

### Technical Architecture Planning
```python
prompt = "Design a real-time collaboration tool"
spec = refiner.refine_prompt(prompt)
# Get specific technical requirements and integration needs
```

## 🚀 Next Steps

After generating an enhanced specification:

1. **Review** the generated spec with your team
2. **Customize** any requirements specific to your needs
3. **Use** the technical requirements for architecture decisions
4. **Reference** the feature list for development planning
5. **Implement** security and performance requirements
6. **Integrate** with your project management tools

## 🤝 Contributing

To extend the module:

1. Add new app type patterns
2. Enhance feature detection logic
3. Improve ambiguity resolution rules
4. Add new technical requirement templates
5. Extend integration recommendations

## 📄 License

This module is part of the AI-Powered Debugging Assistant project and follows the same licensing terms.

---

**Ready to transform vague app ideas into actionable specifications!** 🎉