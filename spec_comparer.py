#!/usr/bin/env python3
"""
SpecComparer Module

This module compares the Enhanced Specification (from PromptRefiner) with the 
Feature Map (from CodeAnalyzer) to identify missing features, deviations, 
and potential logical mismatches in AI-generated or no-code applications.

Author: AI Debug Assistant
Version: 1.0
"""

import json
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime


class SpecComparer:
    """
    Compares Enhanced Specification with actual codebase Feature Map
    to identify discrepancies and generate comprehensive comparison reports.
    """
    
    def __init__(self):
        """Initialize the SpecComparer with empty data structures."""
        self.enhanced_spec = {}
        self.feature_map = {}
        self.comparison_results = {
            'missing_features': [],
            'deviations': [],
            'logical_mismatches': [],
            'extra_features': [],
            'summary': {}
        }
    
    def load_enhanced_spec(self, spec_path: str) -> bool:
        """
        Load the Enhanced Specification JSON file.
        
        Args:
            spec_path (str): Path to the enhanced specification JSON file
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            with open(spec_path, 'r', encoding='utf-8') as file:
                self.enhanced_spec = json.load(file)
            print(f"✅ Enhanced Spec loaded from {spec_path}")
            return True
        except FileNotFoundError:
            print(f"❌ Enhanced Spec file not found: {spec_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in Enhanced Spec: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading Enhanced Spec: {e}")
            return False
    
    def load_feature_map(self, feature_map_path: str) -> bool:
        """
        Load the Feature Map JSON file from CodeAnalyzer.
        
        Args:
            feature_map_path (str): Path to the feature map JSON file
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            with open(feature_map_path, 'r', encoding='utf-8') as file:
                self.feature_map = json.load(file)
            print(f"✅ Feature Map loaded from {feature_map_path}")
            return True
        except FileNotFoundError:
            print(f"❌ Feature Map file not found: {feature_map_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in Feature Map: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading Feature Map: {e}")
            return False
    
    def identify_missing_features(self) -> List[Dict[str, Any]]:
        """
        Identify features specified in Enhanced Spec but missing in codebase.
        
        Returns:
            List[Dict]: List of missing features with details
        """
        missing_features = []
        
        # Check core features
        spec_features = self.enhanced_spec.get('core_features', [])
        implemented_features = self.feature_map.get('features', [])
        implemented_names = [f.get('name', '').lower() for f in implemented_features]
        
        for spec_feature in spec_features:
            feature_name = spec_feature.get('name', '').lower()
            if feature_name not in implemented_names:
                missing_features.append({
                    'type': 'core_feature',
                    'name': spec_feature.get('name'),
                    'description': spec_feature.get('description'),
                    'priority': spec_feature.get('priority', 'medium'),
                    'impact': 'high'
                })
        
        # Check UI components
        spec_ui = self.enhanced_spec.get('ui_components', [])
        implemented_ui = self.feature_map.get('ui_components', [])
        implemented_ui_names = [ui.get('name', '').lower() for ui in implemented_ui]
        
        for spec_component in spec_ui:
            component_name = spec_component.get('name', '').lower()
            if component_name not in implemented_ui_names:
                missing_features.append({
                    'type': 'ui_component',
                    'name': spec_component.get('name'),
                    'description': spec_component.get('description'),
                    'priority': 'medium',
                    'impact': 'medium'
                })
        
        # Check API endpoints
        spec_apis = self.enhanced_spec.get('api_endpoints', [])
        implemented_apis = self.feature_map.get('api_endpoints', [])
        implemented_api_paths = [api.get('path', '').lower() for api in implemented_apis]
        
        for spec_api in spec_apis:
            api_path = spec_api.get('path', '').lower()
            if api_path not in implemented_api_paths:
                missing_features.append({
                    'type': 'api_endpoint',
                    'name': spec_api.get('path'),
                    'method': spec_api.get('method'),
                    'description': spec_api.get('description'),
                    'priority': 'high',
                    'impact': 'high'
                })
        
        return missing_features
    
    def identify_deviations(self) -> List[Dict[str, Any]]:
        """
        Identify deviations between specification and implementation.
        
        Returns:
            List[Dict]: List of deviations with details
        """
        deviations = []
        
        # Check feature implementations for deviations
        spec_features = self.enhanced_spec.get('core_features', [])
        implemented_features = self.feature_map.get('features', [])
        
        for spec_feature in spec_features:
            spec_name = spec_feature.get('name', '').lower()
            
            # Find matching implemented feature
            matching_impl = None
            for impl_feature in implemented_features:
                if impl_feature.get('name', '').lower() == spec_name:
                    matching_impl = impl_feature
                    break
            
            if matching_impl:
                # Check for configuration vs hardcoded values
                spec_config = spec_feature.get('configurable', True)
                impl_config = matching_impl.get('configurable', False)
                
                if spec_config and not impl_config:
                    deviations.append({
                        'type': 'configuration_deviation',
                        'feature': spec_feature.get('name'),
                        'expected': 'configurable',
                        'actual': 'hardcoded',
                        'severity': 'medium',
                        'description': f"Feature should be configurable but is hardcoded"
                    })
                
                # Check implementation approach
                spec_approach = spec_feature.get('implementation_approach', '')
                impl_approach = matching_impl.get('implementation_type', '')
                
                if spec_approach and impl_approach and spec_approach.lower() != impl_approach.lower():
                    deviations.append({
                        'type': 'implementation_deviation',
                        'feature': spec_feature.get('name'),
                        'expected': spec_approach,
                        'actual': impl_approach,
                        'severity': 'low',
                        'description': f"Different implementation approach used"
                    })
        
        # Check UI component deviations
        spec_ui = self.enhanced_spec.get('ui_components', [])
        implemented_ui = self.feature_map.get('ui_components', [])
        
        for spec_component in spec_ui:
            spec_name = spec_component.get('name', '').lower()
            
            matching_ui = None
            for impl_ui in implemented_ui:
                if impl_ui.get('name', '').lower() == spec_name:
                    matching_ui = impl_ui
                    break
            
            if matching_ui:
                # Check styling approach
                spec_styling = spec_component.get('styling', '')
                impl_styling = matching_ui.get('styling', '')
                
                if spec_styling and impl_styling and spec_styling.lower() != impl_styling.lower():
                    deviations.append({
                        'type': 'styling_deviation',
                        'component': spec_component.get('name'),
                        'expected': spec_styling,
                        'actual': impl_styling,
                        'severity': 'low',
                        'description': f"Different styling approach used"
                    })
        
        return deviations
    
    def identify_logical_mismatches(self) -> List[Dict[str, Any]]:
        """
        Identify logical mismatches and inconsistencies.
        
        Returns:
            List[Dict]: List of logical mismatches with details
        """
        mismatches = []
        
        # Check data flow consistency
        spec_data_flow = self.enhanced_spec.get('data_flow', [])
        impl_data_flow = self.feature_map.get('data_flow', [])
        
        for spec_flow in spec_data_flow:
            flow_name = spec_flow.get('name', '').lower()
            
            matching_flow = None
            for impl_flow in impl_data_flow:
                if impl_flow.get('name', '').lower() == flow_name:
                    matching_flow = impl_flow
                    break
            
            if matching_flow:
                # Check flow direction
                spec_direction = spec_flow.get('direction', '')
                impl_direction = matching_flow.get('direction', '')
                
                if spec_direction != impl_direction:
                    mismatches.append({
                        'type': 'data_flow_mismatch',
                        'flow': spec_flow.get('name'),
                        'expected_direction': spec_direction,
                        'actual_direction': impl_direction,
                        'severity': 'high',
                        'description': f"Data flow direction mismatch"
                    })
        
        # Check business logic consistency
        spec_business_rules = self.enhanced_spec.get('business_rules', [])
        impl_business_logic = self.feature_map.get('business_logic', [])
        
        for spec_rule in spec_business_rules:
            rule_name = spec_rule.get('name', '').lower()
            
            matching_logic = None
            for impl_logic in impl_business_logic:
                if impl_logic.get('name', '').lower() == rule_name:
                    matching_logic = impl_logic
                    break
            
            if not matching_logic:
                mismatches.append({
                    'type': 'business_logic_missing',
                    'rule': spec_rule.get('name'),
                    'description': spec_rule.get('description'),
                    'severity': 'high',
                    'impact': 'Business rule not implemented'
                })
        
        # Check security requirements
        spec_security = self.enhanced_spec.get('security_requirements', [])
        impl_security = self.feature_map.get('security_features', [])
        
        for spec_sec in spec_security:
            sec_name = spec_sec.get('name', '').lower()
            
            matching_sec = None
            for impl_sec in impl_security:
                if impl_sec.get('name', '').lower() == sec_name:
                    matching_sec = impl_sec
                    break
            
            if not matching_sec:
                mismatches.append({
                    'type': 'security_requirement_missing',
                    'requirement': spec_sec.get('name'),
                    'description': spec_sec.get('description'),
                    'severity': 'critical',
                    'impact': 'Security vulnerability'
                })
        
        return mismatches
    
    def identify_extra_features(self) -> List[Dict[str, Any]]:
        """
        Identify features implemented but not specified.
        
        Returns:
            List[Dict]: List of extra features with details
        """
        extra_features = []
        
        # Check for extra implemented features
        spec_features = self.enhanced_spec.get('core_features', [])
        implemented_features = self.feature_map.get('features', [])
        spec_names = [f.get('name', '').lower() for f in spec_features]
        
        for impl_feature in implemented_features:
            impl_name = impl_feature.get('name', '').lower()
            if impl_name not in spec_names:
                extra_features.append({
                    'type': 'extra_feature',
                    'name': impl_feature.get('name'),
                    'description': impl_feature.get('description', 'No description'),
                    'impact': 'low',
                    'recommendation': 'Consider if this feature adds value or should be removed'
                })
        
        return extra_features
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the comparison results.
        
        Returns:
            Dict: Summary statistics and overall assessment
        """
        missing_count = len(self.comparison_results['missing_features'])
        deviations_count = len(self.comparison_results['deviations'])
        mismatches_count = len(self.comparison_results['logical_mismatches'])
        extra_count = len(self.comparison_results['extra_features'])
        
        # Calculate severity distribution
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        all_issues = (self.comparison_results['missing_features'] + 
                     self.comparison_results['deviations'] + 
                     self.comparison_results['logical_mismatches'])
        
        for issue in all_issues:
            severity = issue.get('severity', issue.get('impact', 'medium'))
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Overall health score (0-100)
        total_issues = missing_count + deviations_count + mismatches_count
        max_possible_issues = len(self.enhanced_spec.get('core_features', [])) * 3
        health_score = max(0, 100 - (total_issues / max(max_possible_issues, 1)) * 100)
        
        return {
            'total_issues': total_issues,
            'missing_features_count': missing_count,
            'deviations_count': deviations_count,
            'logical_mismatches_count': mismatches_count,
            'extra_features_count': extra_count,
            'severity_distribution': severity_counts,
            'health_score': round(health_score, 1),
            'overall_status': self._get_overall_status(health_score, severity_counts),
            'recommendations': self._generate_recommendations()
        }
    
    def _get_overall_status(self, health_score: float, severity_counts: Dict[str, int]) -> str:
        """Determine overall project status based on health score and severity."""
        if severity_counts['critical'] > 0:
            return 'Critical Issues Found'
        elif health_score >= 80:
            return 'Good'
        elif health_score >= 60:
            return 'Needs Attention'
        else:
            return 'Poor'
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on findings."""
        recommendations = []
        
        if self.comparison_results['missing_features']:
            recommendations.append("Implement missing core features to meet specification requirements")
        
        if self.comparison_results['logical_mismatches']:
            recommendations.append("Review and fix logical mismatches to ensure proper functionality")
        
        if self.comparison_results['deviations']:
            recommendations.append("Address implementation deviations to align with specification")
        
        if not recommendations:
            recommendations.append("Implementation closely matches specification - good work!")
        
        return recommendations
    
    def compare_specifications(self) -> Dict[str, Any]:
        """
        Perform complete comparison between Enhanced Spec and Feature Map.
        
        Returns:
            Dict: Complete comparison results
        """
        print("🔍 Starting specification comparison...")
        
        # Perform all comparisons
        self.comparison_results['missing_features'] = self.identify_missing_features()
        self.comparison_results['deviations'] = self.identify_deviations()
        self.comparison_results['logical_mismatches'] = self.identify_logical_mismatches()
        self.comparison_results['extra_features'] = self.identify_extra_features()
        self.comparison_results['summary'] = self.generate_summary()
        
        # Add metadata
        self.comparison_results['metadata'] = {
            'comparison_timestamp': datetime.now().isoformat(),
            'enhanced_spec_features': len(self.enhanced_spec.get('core_features', [])),
            'implemented_features': len(self.feature_map.get('features', [])),
            'comparison_version': '1.0'
        }
        
        print("✅ Specification comparison completed")
        return self.comparison_results
    
    def save_comparison_report(self, output_dir: str = '.') -> Tuple[str, str]:
        """
        Save comparison results as both JSON and Markdown files.
        
        Args:
            output_dir (str): Directory to save the reports
            
        Returns:
            Tuple[str, str]: Paths to JSON and Markdown files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON report
        json_path = os.path.join(output_dir, 'spec_comparison_report.json')
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(self.comparison_results, file, indent=2, ensure_ascii=False)
        
        # Generate and save Markdown report
        md_path = os.path.join(output_dir, 'spec_comparison_report.md')
        markdown_content = self._generate_markdown_report()
        with open(md_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        print(f"📄 Reports saved:")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {md_path}")
        
        return json_path, md_path
    
    def _generate_markdown_report(self) -> str:
        """Generate a comprehensive Markdown report."""
        summary = self.comparison_results['summary']
        
        md_content = f"""# Specification Comparison Report

**Generated:** {self.comparison_results['metadata']['comparison_timestamp']}
**Health Score:** {summary['health_score']}/100
**Overall Status:** {summary['overall_status']}

## Executive Summary

- **Total Issues Found:** {summary['total_issues']}
- **Missing Features:** {summary['missing_features_count']}
- **Implementation Deviations:** {summary['deviations_count']}
- **Logical Mismatches:** {summary['logical_mismatches_count']}
- **Extra Features:** {summary['extra_features_count']}

### Severity Distribution
- **Critical:** {summary['severity_distribution']['critical']}
- **High:** {summary['severity_distribution']['high']}
- **Medium:** {summary['severity_distribution']['medium']}
- **Low:** {summary['severity_distribution']['low']}

## Recommendations

"""
        
        for rec in summary['recommendations']:
            md_content += f"- {rec}\n"
        
        # Missing Features Section
        if self.comparison_results['missing_features']:
            md_content += "\n## Missing Features\n\n"
            for feature in self.comparison_results['missing_features']:
                md_content += f"### {feature['name']} ({feature['type']})\n"
                md_content += f"**Priority:** {feature['priority']} | **Impact:** {feature['impact']}\n\n"
                md_content += f"{feature.get('description', 'No description available')}\n\n"
        
        # Deviations Section
        if self.comparison_results['deviations']:
            md_content += "\n## Implementation Deviations\n\n"
            for deviation in self.comparison_results['deviations']:
                md_content += f"### {deviation.get('feature', deviation.get('component', 'Unknown'))}\n"
                md_content += f"**Type:** {deviation['type']} | **Severity:** {deviation['severity']}\n\n"
                md_content += f"**Expected:** {deviation['expected']}\n"
                md_content += f"**Actual:** {deviation['actual']}\n\n"
                md_content += f"{deviation['description']}\n\n"
        
        # Logical Mismatches Section
        if self.comparison_results['logical_mismatches']:
            md_content += "\n## Logical Mismatches\n\n"
            for mismatch in self.comparison_results['logical_mismatches']:
                md_content += f"### {mismatch.get('flow', mismatch.get('rule', mismatch.get('requirement', 'Unknown')))}\n"
                md_content += f"**Type:** {mismatch['type']} | **Severity:** {mismatch['severity']}\n\n"
                md_content += f"{mismatch.get('description', mismatch.get('impact', 'No description'))}\n\n"
        
        # Extra Features Section
        if self.comparison_results['extra_features']:
            md_content += "\n## Extra Features (Not in Specification)\n\n"
            for extra in self.comparison_results['extra_features']:
                md_content += f"### {extra['name']}\n"
                md_content += f"**Type:** {extra['type']} | **Impact:** {extra['impact']}\n\n"
                md_content += f"{extra['description']}\n\n"
                md_content += f"**Recommendation:** {extra['recommendation']}\n\n"
        
        md_content += "\n---\n*Report generated by AI Debug Assistant SpecComparer v1.0*"
        
        return md_content


def main():
    """Main function to demonstrate SpecComparer usage."""
    comparer = SpecComparer()
    
    # Load input files
    if not comparer.load_enhanced_spec('demo_enhanced_spec.json'):
        print("❌ Failed to load Enhanced Spec")
        return
    
    if not comparer.load_feature_map('current_project_feature_map.json'):
        print("❌ Failed to load Feature Map")
        return
    
    # Perform comparison
    results = comparer.compare_specifications()
    
    # Save reports
    json_path, md_path = comparer.save_comparison_report()
    
    # Print summary
    summary = results['summary']
    print(f"\n📊 Comparison Summary:")
    print(f"   Health Score: {summary['health_score']}/100")
    print(f"   Status: {summary['overall_status']}")
    print(f"   Total Issues: {summary['total_issues']}")


if __name__ == "__main__":
    main()