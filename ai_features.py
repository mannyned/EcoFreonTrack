"""
AI Features for EcoFreonTrack
Provides intelligent leak prediction, natural language processing, and compliance assistance
"""
import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import anthropic
from models import db, Equipment, LeakInspection, ServiceLog, Technician


class AIConfig:
    """Configuration for AI features"""

    # Set to True to enable AI features (requires ANTHROPIC_API_KEY)
    ENABLED = os.environ.get('AI_ENABLED', 'false').lower() == 'true'

    # Anthropic API key
    API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

    # Model to use (claude-3-haiku-20240307 is faster and more cost-effective)
    MODEL = 'claude-3-haiku-20240307'

    # Enable/disable individual features
    LEAK_PREDICTION_ENABLED = True
    NL_SERVICE_ENTRY_ENABLED = True
    COMPLIANCE_CHATBOT_ENABLED = True


class LeakPredictionAI:
    """
    Intelligent leak prediction using historical data and pattern analysis
    Predicts which equipment is likely to exceed EPA leak rate thresholds
    """

    @staticmethod
    def analyze_equipment_risk(equipment_id: int) -> Dict:
        """
        Analyze leak risk for specific equipment

        Args:
            equipment_id: Equipment database ID

        Returns:
            Dict with risk score, prediction, and recommendations
        """
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return {'error': 'Equipment not found'}

        # Get inspection history
        inspections = LeakInspection.query.filter_by(
            equipment_id=equipment_id
        ).order_by(LeakInspection.inspection_date.desc()).limit(10).all()

        if len(inspections) < 2:
            return {
                'risk_level': 'Unknown',
                'risk_score': 0,
                'confidence': 'Low',
                'message': 'Insufficient data for prediction (need at least 2 inspections)',
                'recommendation': 'Continue regular inspections to build data history'
            }

        # Calculate risk factors
        risk_score = 0
        risk_factors = []

        # Factor 1: Recent leak rate trend
        recent_rates = [i.annual_leak_rate for i in inspections[:3] if i.annual_leak_rate]
        if len(recent_rates) >= 2:
            if recent_rates[0] > recent_rates[-1]:
                risk_score += 30
                risk_factors.append(f"Increasing leak rate trend ({recent_rates[-1]:.1f}% → {recent_rates[0]:.1f}%)")

        # Factor 2: Proximity to threshold
        if inspections[0].annual_leak_rate:
            proximity = (inspections[0].annual_leak_rate / equipment.leak_rate_threshold) * 100
            if proximity > 80:
                risk_score += 40
                risk_factors.append(f"Current leak rate at {proximity:.0f}% of threshold")
            elif proximity > 60:
                risk_score += 25
                risk_factors.append(f"Current leak rate at {proximity:.0f}% of threshold")

        # Factor 3: Non-compliant history
        non_compliant = [i for i in inspections if not i.compliant]
        if len(non_compliant) > 0:
            risk_score += 20 * min(len(non_compliant), 3)
            risk_factors.append(f"Failed {len(non_compliant)} compliance checks in history")

        # Factor 4: Equipment age
        if equipment.install_date:
            age_years = (datetime.now().date() - equipment.install_date).days / 365
            if age_years > 15:
                risk_score += 15
                risk_factors.append(f"Equipment age: {age_years:.1f} years")
            elif age_years > 10:
                risk_score += 10
                risk_factors.append(f"Equipment age: {age_years:.1f} years")

        # Factor 5: Service frequency
        services = ServiceLog.query.filter_by(equipment_id=equipment_id).count()
        if services > 5:
            risk_score += 10
            risk_factors.append(f"High service frequency ({services} service logs)")

        # Determine risk level
        if risk_score >= 70:
            risk_level = 'Critical'
            color = 'danger'
            prediction = f"High probability ({risk_score}%) of exceeding leak threshold within 30 days"
            recommendation = "Immediate inspection recommended. Consider proactive repair or replacement."
        elif risk_score >= 40:
            risk_level = 'High'
            color = 'warning'
            prediction = f"Moderate probability ({risk_score}%) of exceeding leak threshold within 60 days"
            recommendation = "Schedule inspection within 2 weeks. Monitor closely."
        elif risk_score >= 20:
            risk_level = 'Medium'
            color = 'info'
            prediction = f"Low probability ({risk_score}%) of exceeding leak threshold in near term"
            recommendation = "Continue regular inspection schedule."
        else:
            risk_level = 'Low'
            color = 'success'
            prediction = "Equipment performing within normal parameters"
            recommendation = "Maintain current inspection frequency."

        return {
            'equipment_id': equipment.equipment_id,
            'equipment_name': equipment.name,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'confidence': 'High' if len(inspections) >= 5 else 'Medium',
            'prediction': prediction,
            'risk_factors': risk_factors,
            'recommendation': recommendation,
            'color': color,
            'current_leak_rate': inspections[0].annual_leak_rate if inspections[0].annual_leak_rate else 0,
            'threshold': equipment.leak_rate_threshold,
            'inspections_analyzed': len(inspections)
        }

    @staticmethod
    def get_all_equipment_risks() -> List[Dict]:
        """Get risk analysis for all active equipment, sorted by risk score"""
        equipment_list = Equipment.query.filter_by(status='Active').all()
        risks = []

        for equip in equipment_list:
            risk = LeakPredictionAI.analyze_equipment_risk(equip.id)
            if 'error' not in risk:
                risks.append(risk)

        # Sort by risk score descending
        risks.sort(key=lambda x: x['risk_score'], reverse=True)
        return risks


class NaturalLanguageServiceParser:
    """
    Parse natural language service descriptions into structured data
    Uses Claude AI to extract equipment, refrigerant amounts, and service details
    """

    def __init__(self):
        self.client = None
        if AIConfig.ENABLED and AIConfig.API_KEY:
            self.client = anthropic.Anthropic(api_key=AIConfig.API_KEY)

    def parse_service_description(self, description: str, available_equipment: List, available_technicians: List) -> Dict:
        """
        Parse natural language service description into structured data

        Args:
            description: Natural language service description
            available_equipment: List of equipment objects
            available_technicians: List of technician objects

        Returns:
            Dict with extracted service log data
        """
        if not self.client:
            return {'error': 'AI features not enabled. Set AI_ENABLED=true and ANTHROPIC_API_KEY'}

        # Build context for AI
        equipment_list = "\n".join([f"- {e.equipment_id}: {e.name} ({e.refrigerant_name})" for e in available_equipment])
        tech_list = "\n".join([f"- {t.name} (Cert: {t.certification_number})" for t in available_technicians])

        prompt = f"""You are an EPA Section 608 compliance assistant. Parse this service description into structured data.

Available Equipment:
{equipment_list}

Available Technicians:
{tech_list}

Service Description:
"{description}"

Extract the following information and return as JSON:
{{
    "equipment_id": "equipment ID or closest match",
    "technician_name": "technician name or closest match",
    "service_date": "YYYY-MM-DD format (default to today if not specified)",
    "service_type": "one of: Routine Maintenance, Repair, Leak Repair, Installation, Decommission, Inspection",
    "refrigerant_added": number in pounds (0 if not mentioned),
    "refrigerant_recovered": number in pounds (0 if not mentioned),
    "leak_found": true/false,
    "leak_repaired": true/false,
    "leak_location": "location description or empty string",
    "work_performed": "detailed description of work",
    "follow_up_required": true/false,
    "follow_up_notes": "notes or empty string",
    "confidence": "High/Medium/Low - your confidence in the extraction"
}}

Return ONLY valid JSON, no other text."""

        try:
            message = self.client.messages.create(
                model=AIConfig.MODEL,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = re.sub(r'^```json?\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)

            parsed_data = json.loads(response_text)

            # Validate and set defaults
            today = datetime.now().date().isoformat()
            parsed_data.setdefault('service_date', today)
            parsed_data.setdefault('refrigerant_added', 0)
            parsed_data.setdefault('refrigerant_recovered', 0)
            parsed_data.setdefault('leak_found', False)
            parsed_data.setdefault('leak_repaired', False)
            parsed_data.setdefault('leak_location', '')
            parsed_data.setdefault('follow_up_required', False)
            parsed_data.setdefault('follow_up_notes', '')

            return parsed_data

        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse AI response: {str(e)}', 'raw_response': response_text}
        except Exception as e:
            return {'error': f'AI parsing error: {str(e)}'}


class ComplianceChatbot:
    """
    EPA Section 608 compliance chatbot
    Answers questions about regulations, procedures, and best practices
    """

    def __init__(self):
        self.client = None
        if AIConfig.ENABLED and AIConfig.API_KEY:
            self.client = anthropic.Anthropic(api_key=AIConfig.API_KEY)

        # EPA 608 Knowledge Base (condensed)
        self.knowledge_base = """
EPA Section 608 (40 CFR Part 82) - Key Requirements:

LEAK RATE THRESHOLDS:
- Commercial refrigeration & industrial process: 10% annually
- Comfort cooling: 20% annually
- Appliances with charge < 50 lbs: 30% annually

LEAK REPAIR REQUIREMENTS (40 CFR 82.156):
- Repair required within 30 days of exceeding threshold
- Verification inspection required after repair
- If repair not feasible, develop retrofit/retirement plan

RECORD KEEPING (40 CFR 82.166):
Required records (keep for 3 years):
- Equipment inventory with refrigerant type and full charge
- Service records with date, technician cert, refrigerant added/recovered
- Leak inspection records with dates and findings
- Refrigerant purchase invoices
- Recovery/disposal documentation

TECHNICIAN CERTIFICATION (40 CFR 82.161):
- Type I: Small appliances (< 5 lbs or < 15,000 BTU/hr)
- Type II: High-pressure systems (comfort cooling, commercial refrigeration)
- Type III: Low-pressure systems (chillers)
- Universal: All of the above

REFRIGERANT RECOVERY:
- Required for all servicing and disposal
- Must use EPA-certified recovery equipment
- Cannot knowingly vent refrigerants (except small amounts)
- Proper evacuation levels must be met

PENALTIES:
- Civil: Up to $44,539 per day per violation
- Criminal: Up to $25,000 per day and/or imprisonment

INSPECTION FREQUENCY:
- Within 30 days after exceeding leak threshold
- Quarterly if using alternative refrigerant while repair pending
- Follow manufacturer recommendations for routine inspections
"""

    def ask(self, question: str, context: Optional[Dict] = None) -> Dict:
        """
        Ask the compliance chatbot a question

        Args:
            question: User's question about EPA 608 compliance
            context: Optional context (equipment data, recent alerts, etc.)

        Returns:
            Dict with answer, sources, and confidence
        """
        if not self.client:
            return {
                'answer': 'AI chatbot not enabled. To enable, set environment variables: AI_ENABLED=true and ANTHROPIC_API_KEY=your-key',
                'confidence': 'N/A',
                'sources': []
            }

        # Build context string
        context_str = ""
        if context:
            context_str = f"\n\nCurrent System Context:\n{json.dumps(context, indent=2)}"

        prompt = f"""You are an EPA Section 608 compliance expert helping businesses comply with refrigerant handling regulations (40 CFR Part 82).

{self.knowledge_base}
{context_str}

User Question: {question}

Provide a clear, accurate answer based on EPA Section 608 regulations. Include:
1. Direct answer to the question
2. Relevant CFR citations
3. Practical compliance steps if applicable
4. Any warnings about penalties or common mistakes

Be concise but thorough. If the question is outside EPA 608 scope, politely redirect to refrigerant compliance topics."""

        try:
            message = self.client.messages.create(
                model=AIConfig.MODEL,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = message.content[0].text.strip()

            # Extract CFR citations
            sources = re.findall(r'40 CFR [0-9.]+', answer)

            return {
                'answer': answer,
                'confidence': 'High',
                'sources': list(set(sources)),  # Unique citations
                'model': AIConfig.MODEL
            }

        except Exception as e:
            return {
                'answer': f'Error getting response from AI: {str(e)}',
                'confidence': 'Error',
                'sources': []
            }


# Convenience functions for easy access

def get_equipment_at_risk(top_n: int = 10) -> List[Dict]:
    """Get top N equipment at highest risk of leak threshold violation"""
    if not AIConfig.LEAK_PREDICTION_ENABLED:
        return []

    risks = LeakPredictionAI.get_all_equipment_risks()
    return risks[:top_n]


def parse_service_nl(description: str) -> Dict:
    """Parse natural language service description"""
    if not AIConfig.NL_SERVICE_ENTRY_ENABLED:
        return {'error': 'Natural language parsing not enabled'}

    equipment = Equipment.query.filter_by(status='Active').all()
    technicians = Technician.query.filter_by(status='Active').all()

    parser = NaturalLanguageServiceParser()
    return parser.parse_service_description(description, equipment, technicians)


def ask_compliance_question(question: str, context: Optional[Dict] = None) -> Dict:
    """Ask EPA compliance chatbot a question"""
    if not AIConfig.COMPLIANCE_CHATBOT_ENABLED:
        return {'answer': 'Compliance chatbot not enabled', 'confidence': 'N/A', 'sources': []}

    chatbot = ComplianceChatbot()
    return chatbot.ask(question, context)
