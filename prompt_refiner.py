"""
PromptRefiner Module

This module analyzes main app prompts and generates enhanced, explicit specifications
by identifying ambiguities and adding missing details for comprehensive app development.
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedSpec:
    """Data structure for enhanced app specification"""
    original_prompt: str
    app_name: str
    app_type: str
    target_audience: str
    core_purpose: str
    user_roles: List[Dict[str, str]]
    features: List[Dict[str, Any]]
    technical_requirements: Dict[str, Any]
    business_constraints: Dict[str, Any]
    ui_requirements: Dict[str, Any]
    data_requirements: Dict[str, Any]
    integration_requirements: List[Dict[str, str]]
    security_requirements: List[str]
    performance_requirements: Dict[str, Any]
    deployment_requirements: Dict[str, Any]
    ambiguities_resolved: List[Dict[str, str]]
    enhancement_timestamp: str

class PromptRefiner:
    """
    Main class for analyzing and refining app prompts into comprehensive specifications
    """
    
    def __init__(self):
        """Initialize the PromptRefiner with predefined patterns and templates"""
        self.app_type_patterns = {
            'e-commerce': ['shop', 'store', 'buy', 'sell', 'product', 'cart', 'payment', 'checkout'],
            'social': ['social', 'chat', 'message', 'friend', 'follow', 'post', 'share', 'community'],
            'productivity': ['task', 'todo', 'project', 'manage', 'organize', 'schedule', 'calendar'],
            'content': ['blog', 'article', 'content', 'publish', 'cms', 'editor', 'media'],
            'analytics': ['dashboard', 'analytics', 'report', 'chart', 'data', 'metrics', 'insights'],
            'booking': ['book', 'appointment', 'reservation', 'schedule', 'availability', 'calendar'],
            'learning': ['course', 'learn', 'education', 'tutorial', 'quiz', 'lesson', 'training'],
            'finance': ['finance', 'money', 'budget', 'expense', 'invoice', 'payment', 'accounting']
        }
        
        self.common_features = {
            'authentication': ['login', 'register', 'auth', 'user', 'account', 'profile'],
            'search': ['search', 'find', 'filter', 'query', 'lookup'],
            'notifications': ['notify', 'alert', 'email', 'sms', 'push', 'reminder'],
            'file_upload': ['upload', 'file', 'image', 'document', 'attachment'],
            'real_time': ['real-time', 'live', 'instant', 'websocket', 'chat'],
            'mobile': ['mobile', 'responsive', 'app', 'ios', 'android'],
            'admin': ['admin', 'manage', 'control', 'moderate', 'dashboard']
        }

    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the original prompt to identify key components and potential ambiguities
        
        Args:
            prompt (str): The original app prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results including detected patterns and ambiguities
        """
        logger.info("Starting prompt analysis...")
        
        analysis = {
            'app_type': self._detect_app_type(prompt),
            'detected_features': self._detect_features(prompt),
            'user_roles': self._extract_user_roles(prompt),
            'ambiguities': self._identify_ambiguities(prompt),
            'technical_hints': self._extract_technical_hints(prompt),
            'business_context': self._extract_business_context(prompt)
        }
        
        logger.info(f"Detected app type: {analysis['app_type']}")
        logger.info(f"Found {len(analysis['detected_features'])} features")
        logger.info(f"Identified {len(analysis['ambiguities'])} ambiguities")
        
        return analysis

    def _detect_app_type(self, prompt: str) -> str:
        """Detect the primary app type based on keywords"""
        prompt_lower = prompt.lower()
        scores = {}
        
        for app_type, keywords in self.app_type_patterns.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                scores[app_type] = score
        
        return max(scores, key=scores.get) if scores else 'general'

    def _detect_features(self, prompt: str) -> List[str]:
        """Detect mentioned features in the prompt"""
        prompt_lower = prompt.lower()
        detected = []
        
        for feature, keywords in self.common_features.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected.append(feature)
        
        return detected

    def _extract_user_roles(self, prompt: str) -> List[str]:
        """Extract mentioned user roles from the prompt"""
        role_patterns = [
            r'\b(admin|administrator|manager|moderator)\b',
            r'\b(user|customer|client|member)\b',
            r'\b(seller|vendor|merchant|store owner)\b',
            r'\b(buyer|shopper|consumer)\b',
            r'\b(teacher|instructor|educator)\b',
            r'\b(student|learner)\b',
            r'\b(author|writer|creator|contributor)\b'
        ]
        
        roles = []
        prompt_lower = prompt.lower()
        
        for pattern in role_patterns:
            matches = re.findall(pattern, prompt_lower)
            roles.extend(matches)
        
        return list(set(roles))

    def _identify_ambiguities(self, prompt: str) -> List[Dict[str, str]]:
        """Identify potential ambiguities in the prompt"""
        ambiguities = []
        prompt_lower = prompt.lower()
        
        # Check for vague terms
        vague_terms = {
            'simple': 'What specific features define "simple"?',
            'easy': 'What makes it "easy" for users?',
            'modern': 'What specific modern design elements are needed?',
            'secure': 'What specific security measures are required?',
            'fast': 'What are the specific performance requirements?',
            'scalable': 'What are the expected user/data volume requirements?',
            'user-friendly': 'What specific usability features are needed?'
        }
        
        for term, question in vague_terms.items():
            if term in prompt_lower:
                ambiguities.append({
                    'type': 'vague_requirement',
                    'term': term,
                    'question': question
                })
        
        # Check for missing technical details
        if 'database' not in prompt_lower and 'data' in prompt_lower:
            ambiguities.append({
                'type': 'missing_technical',
                'term': 'database',
                'question': 'What type of database and data structure is needed?'
            })
        
        if 'payment' in prompt_lower and 'currency' not in prompt_lower:
            ambiguities.append({
                'type': 'missing_business',
                'term': 'currency',
                'question': 'What currencies should be supported?'
            })
        
        if 'notification' in prompt_lower:
            if 'email' not in prompt_lower and 'sms' not in prompt_lower:
                ambiguities.append({
                    'type': 'missing_feature',
                    'term': 'notification_channels',
                    'question': 'What notification channels are needed (email, SMS, push)?'
                })
        
        return ambiguities

    def _extract_technical_hints(self, prompt: str) -> Dict[str, Any]:
        """Extract technical requirements and hints from the prompt"""
        prompt_lower = prompt.lower()
        
        hints = {
            'platforms': [],
            'integrations': [],
            'technologies': [],
            'scalability': None
        }
        
        # Platform detection
        if any(term in prompt_lower for term in ['mobile', 'ios', 'android']):
            hints['platforms'].append('mobile')
        if any(term in prompt_lower for term in ['web', 'website', 'browser']):
            hints['platforms'].append('web')
        
        # Integration detection
        integration_patterns = {
            'stripe': 'payment processing',
            'paypal': 'payment processing',
            'google': 'authentication/maps/analytics',
            'facebook': 'social authentication',
            'twitter': 'social integration',
            'email': 'email service',
            'sms': 'SMS service'
        }
        
        for service, purpose in integration_patterns.items():
            if service in prompt_lower:
                hints['integrations'].append({'service': service, 'purpose': purpose})
        
        return hints

    def _extract_business_context(self, prompt: str) -> Dict[str, Any]:
        """Extract business context and constraints"""
        context = {
            'target_market': None,
            'business_model': None,
            'monetization': [],
            'compliance': []
        }
        
        prompt_lower = prompt.lower()
        
        # Business model detection
        if any(term in prompt_lower for term in ['subscription', 'monthly', 'plan']):
            context['business_model'] = 'subscription'
        elif any(term in prompt_lower for term in ['marketplace', 'commission', 'fee']):
            context['business_model'] = 'marketplace'
        elif any(term in prompt_lower for term in ['ads', 'advertising', 'sponsored']):
            context['business_model'] = 'advertising'
        
        # Monetization detection
        if 'payment' in prompt_lower or 'buy' in prompt_lower:
            context['monetization'].append('direct_payment')
        if 'subscription' in prompt_lower:
            context['monetization'].append('subscription')
        if 'ads' in prompt_lower:
            context['monetization'].append('advertising')
        
        return context

    def generate_enhanced_spec(self, prompt: str) -> EnhancedSpec:
        """
        Generate a comprehensive enhanced specification from the original prompt
        
        Args:
            prompt (str): The original app prompt
            
        Returns:
            EnhancedSpec: Enhanced specification with resolved ambiguities
        """
        logger.info("Generating enhanced specification...")
        
        analysis = self.analyze_prompt(prompt)
        
        # Generate app name if not explicitly mentioned
        app_name = self._generate_app_name(prompt, analysis['app_type'])
        
        # Define user roles with permissions
        user_roles = self._define_user_roles(analysis['user_roles'], analysis['app_type'])
        
        # Generate comprehensive features list
        features = self._generate_features(analysis['detected_features'], analysis['app_type'])
        
        # Define technical requirements
        technical_requirements = self._define_technical_requirements(analysis)
        
        # Define business constraints
        business_constraints = self._define_business_constraints(analysis['business_context'])
        
        # Generate UI requirements
        ui_requirements = self._generate_ui_requirements(analysis['app_type'])
        
        # Define data requirements
        data_requirements = self._define_data_requirements(analysis['app_type'], features)
        
        # Generate integration requirements
        integration_requirements = self._generate_integration_requirements(analysis)
        
        # Define security requirements
        security_requirements = self._define_security_requirements(analysis['app_type'])
        
        # Define performance requirements
        performance_requirements = self._define_performance_requirements()
        
        # Define deployment requirements
        deployment_requirements = self._define_deployment_requirements(analysis['technical_hints'])
        
        # Resolve ambiguities
        resolved_ambiguities = self._resolve_ambiguities(analysis['ambiguities'], analysis)
        
        enhanced_spec = EnhancedSpec(
            original_prompt=prompt,
            app_name=app_name,
            app_type=analysis['app_type'],
            target_audience=self._define_target_audience(analysis['app_type']),
            core_purpose=self._define_core_purpose(prompt, analysis['app_type']),
            user_roles=user_roles,
            features=features,
            technical_requirements=technical_requirements,
            business_constraints=business_constraints,
            ui_requirements=ui_requirements,
            data_requirements=data_requirements,
            integration_requirements=integration_requirements,
            security_requirements=security_requirements,
            performance_requirements=performance_requirements,
            deployment_requirements=deployment_requirements,
            ambiguities_resolved=resolved_ambiguities,
            enhancement_timestamp=datetime.now().isoformat()
        )
        
        logger.info("Enhanced specification generated successfully")
        return enhanced_spec

    def _generate_app_name(self, prompt: str, app_type: str) -> str:
        """Generate a suitable app name based on prompt and type"""
        # Try to extract name from prompt first
        name_patterns = [
            r'app called "([^"]+)"',
            r'application named "([^"]+)"',
            r'platform called "([^"]+)"',
            r'"([^"]+)" app'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Generate based on app type
        type_names = {
            'e-commerce': 'ShopHub',
            'social': 'ConnectApp',
            'productivity': 'TaskMaster',
            'content': 'ContentPro',
            'analytics': 'DataInsights',
            'booking': 'BookEasy',
            'learning': 'LearnHub',
            'finance': 'FinanceTracker'
        }
        
        return type_names.get(app_type, 'MyApp')

    def _define_user_roles(self, detected_roles: List[str], app_type: str) -> List[Dict[str, str]]:
        """Define comprehensive user roles with permissions"""
        roles = []
        
        # Always include basic user role
        roles.append({
            'name': 'user',
            'description': 'Standard application user',
            'permissions': ['read', 'create_own', 'update_own', 'delete_own']
        })
        
        # Add admin role for most app types
        if app_type in ['e-commerce', 'content', 'analytics', 'booking', 'learning']:
            roles.append({
                'name': 'admin',
                'description': 'System administrator with full access',
                'permissions': ['read', 'create', 'update', 'delete', 'manage_users', 'system_config']
            })
        
        # Add specific roles based on app type
        if app_type == 'e-commerce':
            roles.append({
                'name': 'seller',
                'description': 'Product seller/vendor',
                'permissions': ['read', 'create_products', 'update_products', 'manage_orders']
            })
        elif app_type == 'learning':
            roles.append({
                'name': 'instructor',
                'description': 'Course instructor/teacher',
                'permissions': ['read', 'create_courses', 'update_courses', 'grade_students']
            })
        
        return roles

    def _generate_features(self, detected_features: List[str], app_type: str) -> List[Dict[str, Any]]:
        """Generate comprehensive features list"""
        features = []
        
        # Core features based on app type
        core_features = {
            'e-commerce': [
                {'name': 'product_catalog', 'priority': 'high', 'description': 'Browse and search products'},
                {'name': 'shopping_cart', 'priority': 'high', 'description': 'Add/remove items from cart'},
                {'name': 'checkout', 'priority': 'high', 'description': 'Complete purchase process'},
                {'name': 'payment_processing', 'priority': 'high', 'description': 'Handle payments securely'},
                {'name': 'order_management', 'priority': 'high', 'description': 'Track and manage orders'}
            ],
            'social': [
                {'name': 'user_profiles', 'priority': 'high', 'description': 'User profile management'},
                {'name': 'messaging', 'priority': 'high', 'description': 'Direct messaging between users'},
                {'name': 'content_sharing', 'priority': 'high', 'description': 'Share posts and media'},
                {'name': 'social_connections', 'priority': 'medium', 'description': 'Follow/friend system'}
            ],
            'productivity': [
                {'name': 'task_management', 'priority': 'high', 'description': 'Create and manage tasks'},
                {'name': 'project_organization', 'priority': 'high', 'description': 'Organize tasks into projects'},
                {'name': 'collaboration', 'priority': 'medium', 'description': 'Team collaboration features'},
                {'name': 'reporting', 'priority': 'medium', 'description': 'Progress and productivity reports'}
            ]
        }
        
        features.extend(core_features.get(app_type, []))
        
        # Add detected features
        feature_definitions = {
            'authentication': {'name': 'user_authentication', 'priority': 'high', 'description': 'User login and registration'},
            'search': {'name': 'search_functionality', 'priority': 'medium', 'description': 'Search and filter content'},
            'notifications': {'name': 'notification_system', 'priority': 'medium', 'description': 'User notifications'},
            'file_upload': {'name': 'file_management', 'priority': 'medium', 'description': 'Upload and manage files'},
            'real_time': {'name': 'real_time_updates', 'priority': 'medium', 'description': 'Live updates and messaging'},
            'mobile': {'name': 'mobile_optimization', 'priority': 'high', 'description': 'Mobile-responsive design'},
            'admin': {'name': 'admin_panel', 'priority': 'medium', 'description': 'Administrative interface'}
        }
        
        for feature in detected_features:
            if feature in feature_definitions:
                features.append(feature_definitions[feature])
        
        return features

    def _define_technical_requirements(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define comprehensive technical requirements"""
        return {
            'frontend': {
                'framework': 'React',
                'styling': 'Tailwind CSS',
                'state_management': 'React Context/Redux',
                'routing': 'React Router'
            },
            'backend': {
                'runtime': 'Node.js',
                'framework': 'Express.js',
                'api_style': 'REST',
                'authentication': 'JWT'
            },
            'database': {
                'type': 'PostgreSQL',
                'orm': 'Prisma',
                'caching': 'Redis'
            },
            'hosting': {
                'frontend': 'Vercel/Netlify',
                'backend': 'Railway/Heroku',
                'database': 'Supabase/PlanetScale'
            },
            'development': {
                'version_control': 'Git',
                'package_manager': 'npm',
                'bundler': 'Vite',
                'testing': 'Jest + React Testing Library'
            }
        }

    def _define_business_constraints(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Define business constraints and requirements"""
        return {
            'budget': {
                'development': 'To be determined',
                'hosting': 'Cloud-based, scalable pricing',
                'third_party_services': 'Pay-per-use model preferred'
            },
            'timeline': {
                'mvp': '2-3 months',
                'full_release': '4-6 months',
                'iterations': 'Bi-weekly sprints'
            },
            'compliance': {
                'data_protection': 'GDPR compliant',
                'accessibility': 'WCAG 2.1 AA',
                'security': 'OWASP guidelines'
            },
            'localization': {
                'languages': ['English'],
                'currencies': ['USD'],
                'regions': ['North America']
            }
        }

    def _generate_ui_requirements(self, app_type: str) -> Dict[str, Any]:
        """Generate UI/UX requirements"""
        return {
            'design_system': {
                'style': 'Modern, clean, minimalist',
                'color_scheme': 'Professional with brand colors',
                'typography': 'Sans-serif, readable fonts',
                'spacing': 'Consistent grid system'
            },
            'responsive_design': {
                'mobile_first': True,
                'breakpoints': ['mobile', 'tablet', 'desktop'],
                'touch_friendly': True
            },
            'accessibility': {
                'screen_reader': 'Full support',
                'keyboard_navigation': 'Complete navigation',
                'color_contrast': 'WCAG AA compliant',
                'focus_indicators': 'Clear visual indicators'
            },
            'performance': {
                'load_time': '< 3 seconds',
                'interactive_time': '< 5 seconds',
                'image_optimization': 'WebP format, lazy loading'
            }
        }

    def _define_data_requirements(self, app_type: str, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Define data structure and requirements"""
        base_entities = {
            'users': {
                'fields': ['id', 'email', 'password_hash', 'profile_data', 'created_at', 'updated_at'],
                'relationships': ['has_many_sessions', 'has_one_profile']
            },
            'sessions': {
                'fields': ['id', 'user_id', 'token', 'expires_at', 'created_at'],
                'relationships': ['belongs_to_user']
            }
        }
        
        # Add app-specific entities
        if app_type == 'e-commerce':
            base_entities.update({
                'products': {
                    'fields': ['id', 'name', 'description', 'price', 'inventory', 'images', 'category_id'],
                    'relationships': ['belongs_to_category', 'has_many_order_items']
                },
                'orders': {
                    'fields': ['id', 'user_id', 'total', 'status', 'shipping_address', 'created_at'],
                    'relationships': ['belongs_to_user', 'has_many_order_items']
                }
            })
        
        return {
            'entities': base_entities,
            'data_volume': {
                'expected_users': '1K-10K initially',
                'data_growth': '20% monthly',
                'storage_needs': '< 100GB initially'
            },
            'backup_strategy': {
                'frequency': 'Daily automated backups',
                'retention': '30 days',
                'disaster_recovery': 'Cross-region replication'
            }
        }

    def _generate_integration_requirements(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate integration requirements"""
        integrations = []
        
        # Add detected integrations
        for integration in analysis['technical_hints']['integrations']:
            integrations.append(integration)
        
        # Add common integrations based on app type
        app_type = analysis['app_type']
        if app_type == 'e-commerce':
            integrations.extend([
                {'service': 'Stripe', 'purpose': 'Payment processing'},
                {'service': 'SendGrid', 'purpose': 'Email notifications'},
                {'service': 'Cloudinary', 'purpose': 'Image management'}
            ])
        elif app_type == 'social':
            integrations.extend([
                {'service': 'AWS S3', 'purpose': 'Media storage'},
                {'service': 'Pusher', 'purpose': 'Real-time messaging'},
                {'service': 'Google OAuth', 'purpose': 'Social authentication'}
            ])
        
        return integrations

    def _define_security_requirements(self, app_type: str) -> List[str]:
        """Define security requirements"""
        base_security = [
            'HTTPS encryption for all communications',
            'Password hashing with bcrypt',
            'JWT token authentication',
            'Input validation and sanitization',
            'SQL injection prevention',
            'XSS protection',
            'CSRF protection',
            'Rate limiting on API endpoints',
            'Secure session management',
            'Regular security audits'
        ]
        
        # Add app-specific security requirements
        if app_type == 'e-commerce':
            base_security.extend([
                'PCI DSS compliance for payment processing',
                'Secure payment token handling',
                'Order data encryption'
            ])
        elif app_type == 'social':
            base_security.extend([
                'Content moderation system',
                'Privacy controls for user data',
                'Secure file upload validation'
            ])
        
        return base_security

    def _define_performance_requirements(self) -> Dict[str, Any]:
        """Define performance requirements"""
        return {
            'response_time': {
                'api_endpoints': '< 200ms average',
                'page_load': '< 3 seconds',
                'database_queries': '< 100ms'
            },
            'throughput': {
                'concurrent_users': '1000+',
                'requests_per_second': '100+',
                'database_connections': '50+'
            },
            'scalability': {
                'horizontal_scaling': 'Auto-scaling enabled',
                'load_balancing': 'Multi-instance support',
                'caching_strategy': 'Redis + CDN'
            },
            'monitoring': {
                'uptime_target': '99.9%',
                'error_rate': '< 0.1%',
                'alerting': 'Real-time monitoring'
            }
        }

    def _define_deployment_requirements(self, technical_hints: Dict[str, Any]) -> Dict[str, Any]:
        """Define deployment requirements"""
        return {
            'environments': {
                'development': 'Local development setup',
                'staging': 'Pre-production testing',
                'production': 'Live application'
            },
            'ci_cd': {
                'pipeline': 'GitHub Actions',
                'testing': 'Automated test suite',
                'deployment': 'Automated deployment on merge'
            },
            'infrastructure': {
                'containerization': 'Docker containers',
                'orchestration': 'Kubernetes (if needed)',
                'monitoring': 'Application and infrastructure monitoring'
            },
            'domains': {
                'staging': 'staging.app-domain.com',
                'production': 'app-domain.com',
                'ssl': 'Automated SSL certificates'
            }
        }

    def _define_target_audience(self, app_type: str) -> str:
        """Define target audience based on app type"""
        audiences = {
            'e-commerce': 'Online shoppers and retail businesses',
            'social': 'Social media users and communities',
            'productivity': 'Professionals and teams seeking efficiency',
            'content': 'Content creators and publishers',
            'analytics': 'Business analysts and data-driven organizations',
            'booking': 'Service providers and customers needing appointments',
            'learning': 'Students, educators, and lifelong learners',
            'finance': 'Individuals and businesses managing finances'
        }
        return audiences.get(app_type, 'General users')

    def _define_core_purpose(self, prompt: str, app_type: str) -> str:
        """Extract or define the core purpose of the application"""
        # Try to extract purpose from prompt
        purpose_patterns = [
            r'to (help|enable|allow|provide) ([^.]+)',
            r'for ([^.]+)',
            r'that (helps|enables|allows|provides) ([^.]+)'
        ]
        
        for pattern in purpose_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Fallback to app type purpose
        purposes = {
            'e-commerce': 'Enable online buying and selling of products',
            'social': 'Connect people and facilitate social interactions',
            'productivity': 'Improve efficiency and task management',
            'content': 'Create, manage, and publish content',
            'analytics': 'Provide data insights and reporting',
            'booking': 'Facilitate appointment scheduling and booking',
            'learning': 'Deliver educational content and learning experiences',
            'finance': 'Manage financial transactions and budgeting'
        }
        
        return purposes.get(app_type, 'Provide value to users through digital solutions')

    def _resolve_ambiguities(self, ambiguities: List[Dict[str, str]], analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Resolve identified ambiguities with specific recommendations"""
        resolved = []
        
        for ambiguity in ambiguities:
            resolution = {
                'original_ambiguity': ambiguity['question'],
                'resolution': self._get_resolution_for_ambiguity(ambiguity, analysis),
                'rationale': self._get_rationale_for_resolution(ambiguity, analysis)
            }
            resolved.append(resolution)
        
        return resolved

    def _get_resolution_for_ambiguity(self, ambiguity: Dict[str, str], analysis: Dict[str, Any]) -> str:
        """Get specific resolution for an ambiguity"""
        term = ambiguity['term']
        app_type = analysis['app_type']
        
        resolutions = {
            'simple': f'Implement clean, intuitive UI with minimal clicks for core {app_type} functions',
            'secure': 'Implement HTTPS, JWT authentication, input validation, and regular security audits',
            'fast': 'Target <3s page load, <200ms API response, implement caching and CDN',
            'scalable': 'Design for 10K+ concurrent users with horizontal scaling and load balancing',
            'currency': 'Support USD initially, with multi-currency framework for future expansion',
            'notification_channels': 'Implement email notifications with SMS and push notification framework'
        }
        
        return resolutions.get(term, f'Define specific requirements for {term} based on user research')

    def _get_rationale_for_resolution(self, ambiguity: Dict[str, str], analysis: Dict[str, Any]) -> str:
        """Get rationale for the resolution"""
        return f"Based on {analysis['app_type']} app requirements and industry best practices"

    def save_enhanced_spec(self, enhanced_spec: EnhancedSpec, filename: Optional[str] = None) -> str:
        """
        Save the enhanced specification to a JSON file
        
        Args:
            enhanced_spec (EnhancedSpec): The enhanced specification to save
            filename (str, optional): Custom filename for the output file
            
        Returns:
            str: Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_spec_{timestamp}.json"
        
        logger.info(f"Saving enhanced specification to {filename}")
        
        # Convert dataclass to dictionary
        spec_dict = asdict(enhanced_spec)
        
        # Save to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(spec_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Enhanced specification saved successfully to {filename}")
        return filename

    def refine_prompt(self, prompt: str, output_file: Optional[str] = None) -> EnhancedSpec:
        """
        Main method to refine a prompt into an enhanced specification
        
        Args:
            prompt (str): The original app prompt to refine
            output_file (str, optional): Custom output filename
            
        Returns:
            EnhancedSpec: The enhanced specification
        """
        logger.info("=== Starting Prompt Refinement Process ===")
        logger.info(f"Original prompt: {prompt[:100]}...")
        
        try:
            # Generate enhanced specification
            enhanced_spec = self.generate_enhanced_spec(prompt)
            
            # Save to file
            saved_file = self.save_enhanced_spec(enhanced_spec, output_file)
            
            logger.info("=== Prompt Refinement Completed Successfully ===")
            logger.info(f"Enhanced specification saved to: {saved_file}")
            
            return enhanced_spec
            
        except Exception as e:
            logger.error(f"Error during prompt refinement: {str(e)}")
            raise


def main():
    """
    Example usage of the PromptRefiner module
    """
    # Example prompt
    sample_prompt = """
    Create a simple e-commerce app where users can buy and sell products. 
    It should be secure and fast, with a modern design. Users should be able to 
    create accounts, browse products, add items to cart, and checkout with payment.
    Admin users should be able to manage products and orders.
    """
    
    # Initialize refiner
    refiner = PromptRefiner()
    
    # Refine the prompt
    enhanced_spec = refiner.refine_prompt(sample_prompt)
    
    # Print summary
    print(f"\n=== ENHANCEMENT SUMMARY ===")
    print(f"App Name: {enhanced_spec.app_name}")
    print(f"App Type: {enhanced_spec.app_type}")
    print(f"Features: {len(enhanced_spec.features)} identified")
    print(f"User Roles: {len(enhanced_spec.user_roles)} defined")
    print(f"Ambiguities Resolved: {len(enhanced_spec.ambiguities_resolved)}")
    print(f"Integrations: {len(enhanced_spec.integration_requirements)} required")


if __name__ == "__main__":
    main()