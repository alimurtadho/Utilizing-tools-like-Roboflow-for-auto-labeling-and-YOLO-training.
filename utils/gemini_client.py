"""
Google Gemini API Client
For LLM-based analysis and insights
"""

import logging
import google.generativeai as genai
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiClient:
    """Google Gemini API wrapper"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            logger.info("✅ Gemini API initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise
    
    def analyze_results(self, results: dict) -> str:
        """
        Analyze detection results and generate insights
        
        Args:
            results: Detection results dictionary
            
        Returns:
            Analysis text from Gemini
        """
        try:
            prompt = f"""
            Analyze the following motorcycle helmet compliance detection results and provide insights:
            
            Total Motorcycles: {results.get('motorcycles_detected', 0)}
            Total Occupants: {results.get('total_occupants', 0)}
            Helmets Worn: {results.get('helmets_worn', 0)}
            Compliance Rate: {results.get('compliance_rate', 0)}%
            
            Please provide:
            1. Key findings about helmet compliance
            2. Risk assessment (high/medium/low)
            3. Recommendations for improvement
            4. Specific areas of concern
            
            Keep the response concise and actionable.
            """
            
            response = self.model.generate_content(prompt)
            
            logger.info("✅ Analysis generated from Gemini")
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return f"Error analyzing results: {str(e)}"
    
    def generate_report(self, results: dict) -> str:
        """Generate executive report from results"""
        try:
            summary = f"""
            HELMET COMPLIANCE REPORT
            
            Statistics:
            - Total Videos Processed: {len(results.get('videos', []))}
            - Motorcycles Detected: {results.get('total_motorcycles', 0)}
            - Average Compliance: {results.get('average_compliance_rate', 0):.1f}%
            
            Details:
            {results}
            """
            
            prompt = f"""
            Based on the following data, generate a professional compliance report:
            
            {summary}
            
            Include:
            1. Executive Summary
            2. Key Metrics
            3. Compliance Analysis
            4. Recommendations
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Report generation error: {e}")
            return f"Error generating report: {str(e)}"
    
    def identify_risks(self, results: dict) -> list:
        """Identify high-risk scenarios"""
        try:
            compliance_rate = results.get('compliance_rate', 0)
            
            risks = []
            
            if compliance_rate < 50:
                risks.append("CRITICAL: Compliance rate below 50%")
            elif compliance_rate < 70:
                risks.append("HIGH: Compliance rate below 70%")
            elif compliance_rate < 85:
                risks.append("MEDIUM: Compliance rate below 85%")
            
            if results.get('helmets_not_worn', 0) > results.get('helmets_worn', 0):
                risks.append("HIGH: Non-compliance exceeds compliance")
            
            total_occupants = results.get('total_occupants', 0)
            if total_occupants > 100 and compliance_rate < 60:
                risks.append("CRITICAL: High traffic volume with low compliance")
            
            return risks
            
        except Exception as e:
            logger.error(f"Risk identification error: {e}")
            return [f"Error: {str(e)}"]
