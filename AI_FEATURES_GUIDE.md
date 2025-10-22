# AI Features Guide - EcoFreonTrack

## Overview

EcoFreonTrack includes three powerful AI features powered by Claude (Anthropic):

1. **Intelligent Leak Prediction** - Predicts which equipment will exceed EPA leak thresholds
2. **Natural Language Service Entry** - Parse service descriptions into structured data
3. **EPA Compliance Chatbot** - Answer EPA Section 608 regulation questions

---

## Setup & Configuration

### Step 1: Install AI Dependencies

```bash
pip install anthropic
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Get Anthropic API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Create an API key
4. Copy your API key

### Step 3: Enable AI Features

Set environment variables:

**Windows:**
```batch
set AI_ENABLED=true
set ANTHROPIC_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export AI_ENABLED=true
export ANTHROPIC_API_KEY=your-api-key-here
```

**Or create a `.env` file:**
```ini
AI_ENABLED=true
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### Step 4: Restart the Application

```batch
python app.py
```

The AI features will now appear in the navigation menu!

---

## Feature 1: Intelligent Leak Prediction 🔮

### What It Does

Analyzes historical data to predict which equipment is likely to exceed EPA leak rate thresholds BEFORE violations occur.

### How It Works

The AI examines:
- **Leak rate trends** - Is the leak rate increasing over time?
- **Proximity to threshold** - How close is equipment to violation?
- **Compliance history** - Has equipment failed inspections before?
- **Equipment age** - Older equipment tends to leak more
- **Service frequency** - More repairs may indicate declining condition

### Risk Scoring

Each piece of equipment gets a risk score (0-100%):
- **70%+**: Critical risk - immediate action recommended
- **40-69%**: High risk - schedule inspection within 2 weeks
- **20-39%**: Medium risk - continue regular monitoring
- **0-19%**: Low risk - equipment performing normally

### How to Use

1. Navigate to **AI Features → Leak Prediction**
2. View the risk analysis table
3. Click risk factors to see detailed analysis
4. Follow recommendations for each piece of equipment

### Business Value

- **Prevent EPA violations** (up to $44,539/day per violation)
- **Proactive maintenance** instead of reactive repairs
- **Reduce refrigerant loss** and associated costs
- **Prioritize inspection resources** effectively

### Requirements

- At least **2 leak inspections** per equipment for predictions
- More inspection history = higher prediction confidence

---

## Feature 2: Natural Language Service Entry 🎤

### What It Does

Converts plain English service descriptions into structured database entries - no forms required!

### How It Works

1. Technician describes work in natural language
2. AI extracts structured data (equipment ID, refrigerant amounts, leak info, etc.)
3. User reviews and confirms the extracted data
4. Data can be saved to database

### Example Usage

**Input:**
```
Serviced AC-12 today, found leak at condenser coil, added 3.5 pounds of R-410A,
repaired leak with brazing, follow-up needed in 30 days
```

**AI Extracts:**
- Equipment: AC-12
- Service Type: Leak Repair
- Refrigerant Added: 3.5 lbs
- Leak Found: Yes
- Leak Location: Condenser coil
- Work Performed: Leak repair via brazing
- Follow-up Required: Yes
- Follow-up Notes: Check in 30 days

### Best Practices

**Include these details for best results:**
- Equipment ID or name
- Date (if not today)
- Technician name
- What work was performed
- Refrigerant amounts (added/recovered)
- Leak information (location, repaired?)
- Follow-up requirements

**Good Example:**
```
John Smith serviced refrigerator REF-5 on March 15th. Found leak at evaporator,
recovered 2 lbs of R-404A, brazed connection, needs verification inspection.
```

**Also Works:**
```
AC unit 12 routine maintenance, no leaks, added half pound R-410A
```

### How to Use

1. Navigate to **AI Features → Quick Entry**
2. Type or speak your service description
3. Click "Parse with AI"
4. Review the extracted data
5. Continue to manual form to save (with pre-filled data)

### Business Value

- **5x faster** data entry (5 minutes → 1 minute)
- **Fewer errors** - no manual form filling
- **Better adoption** - technicians prefer speaking to typing
- **Field-ready** - works on mobile devices

---

## Feature 3: EPA Compliance Chatbot 💬

### What It Does

Answers questions about EPA Section 608 regulations, compliance requirements, and best practices.

### Knowledge Base

The chatbot knows:
- **40 CFR Part 82** - Complete EPA Section 608 regulations
- **Leak rate thresholds** for different equipment types
- **Repair requirements** and timelines
- **Record-keeping** requirements
- **Technician certification** (Type I, II, III, Universal)
- **Recovery and disposal** procedures
- **Penalties** for non-compliance
- **Best practices** for compliance

### Example Questions

**Leak Rate Thresholds:**
```
Q: What is the leak rate threshold for comfort cooling equipment?
A: Comfort cooling equipment has a 20% annual leak rate threshold under 40 CFR 82.156...
```

**Repair Requirements:**
```
Q: How long do I have to repair equipment after exceeding the threshold?
A: You must repair within 30 days of exceeding the leak threshold, per 40 CFR 82.156(i)...
```

**Record Keeping:**
```
Q: What service records do I need to keep?
A: Under 40 CFR 82.166, you must maintain records for 3 years including...
```

**Technician Certification:**
```
Q: What's the difference between Type II and Universal certification?
A: Type II certification covers high-pressure refrigeration systems, while Universal...
```

### How to Use

1. Navigate to **AI Features → EPA Assistant**
2. Type your question in plain English
3. Click "Ask AI Assistant"
4. Read the detailed answer with CFR citations
5. Click example questions for quick reference

### Response Format

Each answer includes:
- **Detailed explanation** of the regulation
- **CFR citations** (e.g., 40 CFR 82.156)
- **Practical compliance steps**
- **Warnings** about penalties or common mistakes

### Important Disclaimer

⚠️ The chatbot provides **general guidance** only. It is NOT legal advice. Always:
- Consult EPA compliance experts for regulatory matters
- Refer to official CFR documentation
- Verify information for your specific situation

### Business Value

- **Instant answers** - no manual searches through regulations
- **Training tool** - helps new employees learn regulations
- **Audit preparation** - understand requirements quickly
- **Reduce compliance confusion** - clear explanations

---

## API Endpoints

For developers integrating AI features:

### Parse Service Description
```bash
POST /api/ai/parse-service
Content-Type: application/json

{
  "description": "Serviced AC-12, added 3 lbs R-410A"
}
```

### Get Equipment Risk
```bash
GET /api/ai/equipment-risk/<equipment_id>
```

### Ask Compliance Question
```bash
POST /api/ai/ask
Content-Type: application/json

{
  "question": "What is the leak rate threshold?",
  "context": {"total_equipment": 10}
}
```

---

## Cost Estimates

### Anthropic Claude Pricing (as of 2024)

**Model**: Claude 3.5 Sonnet
- Input: $3 per million tokens
- Output: $15 per million tokens

### Estimated Monthly Costs

**Small Business (10-20 equipment, 5 users):**
- Leak Prediction: ~$2/month (runs on-demand, uses historical data)
- Natural Language Entry: ~$10-20/month (50-100 entries)
- Chatbot: ~$5-15/month (100-300 questions)
- **Total: $17-37/month**

**Medium Business (50 equipment, 15 users):**
- Leak Prediction: ~$5/month
- Natural Language Entry: ~$30-50/month (200-300 entries)
- Chatbot: ~$15-30/month (500-1000 questions)
- **Total: $50-85/month**

**Enterprise (200+ equipment, 50+ users):**
- **Total: $150-300/month**

### Cost vs. Benefit

**Single EPA violation fine**: $44,539/day

**Prevented violations**: If AI prevents just ONE violation per year, ROI = **100,000%+**

**Time saved**:
- Natural language entry: 4 minutes per log x 100 logs/month = 400 minutes = $200 value
- Chatbot answers: 15 minutes per question x 50 questions = 750 minutes = $375 value

**Total monthly value**: $500-1000 vs. cost of $17-85 = **Excellent ROI**

---

## Privacy & Data Security

### Data Sent to Anthropic

**Leak Prediction**: ❌ NO data sent to API (uses local algorithms only)

**Natural Language Entry**: ✅ Service descriptions sent to Claude
- Equipment IDs
- Technician names
- Service descriptions

**Compliance Chatbot**: ✅ Questions sent to Claude
- User questions
- System context (equipment counts, alert counts)

### Privacy Best Practices

1. **Don't include sensitive info** in natural language descriptions
   - ❌ BAD: "Serviced unit at 123 Main St for John Doe SSN 123-45-6789"
   - ✅ GOOD: "Serviced AC-12, added 3 lbs R-410A"

2. **Equipment IDs instead of addresses**
   - Use internal equipment IDs (AC-12, REF-5)
   - Avoid customer names or addresses

3. **Review Anthropic's privacy policy**
   - Data retention: 30 days
   - No training on customer data (with API)
   - SOC 2 Type II certified

4. **For maximum privacy**: Use leak prediction only (no API calls)

---

## Troubleshooting

### AI Features Don't Appear in Navigation

**Solution**: Check that AI is enabled
```bash
# Windows
echo %AI_ENABLED%

# Should show: true
```

Set if not enabled:
```bash
set AI_ENABLED=true
set ANTHROPIC_API_KEY=your-key
```

### "AI features not enabled" Error

**Cause**: Missing API key or AI_ENABLED not set

**Solution**:
1. Verify environment variables are set
2. Restart the application
3. Check `.env` file if using one

### "Invalid API Key" Error

**Cause**: Incorrect or expired API key

**Solution**:
1. Verify API key at https://console.anthropic.com/
2. Ensure key starts with `sk-ant-api03-`
3. Check for extra spaces or quotes

### Leak Prediction Shows "Insufficient Data"

**Cause**: Equipment needs at least 2 leak inspections

**Solution**:
1. Add leak inspections via **Inspections → Add Inspection**
2. Need historical data for predictions
3. Import past inspection records if available

### Natural Language Parser Not Working

**Possible Causes**:
1. API key not set correctly
2. Network connectivity issues
3. Anthropic API service down

**Solution**:
1. Check API key configuration
2. Test network connectivity
3. Check Anthropic status: https://status.anthropic.com/

---

## Disabling AI Features

To disable AI features:

```bash
# Windows
set AI_ENABLED=false

# Linux/Mac
export AI_ENABLED=false
```

Or remove from `.env` file.

The AI menu items will disappear, and the app will work normally without AI.

---

## Future AI Features (Roadmap)

Potential additions:
- **Automatic report generation** - AI-written compliance reports
- **Anomaly detection** - Flag suspicious data entries
- **Predictive maintenance scheduling** - Optimal service timing
- **Refrigerant cost forecasting** - Predict inventory needs
- **Voice interface** - Speak service logs hands-free
- **Photo analysis** - Upload leak photos for AI diagnosis

---

## Support & Feedback

For AI feature questions:
1. Check this guide
2. Test with example data
3. Contact support with specific error messages

**Remember**: AI features are optional. EcoFreonTrack works perfectly without them!

---

**Last Updated**: October 2025
**Version**: 1.0.0
