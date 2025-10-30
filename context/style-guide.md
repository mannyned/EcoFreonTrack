# EcoFreonTrack Style Guide

## Brand Identity

**Product Name:** EcoFreonTrack
**Tagline:** EPA Section 608 Refrigerant Tracking & Compliance System
**Primary Use Case:** EPA compliance management, refrigerant tracking, service logging for HVAC businesses

## Color Palette

### Primary Brand Colors
```css
--primary-color: #00B4A0;         /* Teal Green - primary actions, headers, highlights */
--primary-hover: #008c7a;         /* Darker teal for hover states */
--primary-light: #E6F7F5;         /* Light teal for backgrounds */
```

### Semantic Colors
```css
--success-color: #28a745;         /* Green - success messages, active status */
--danger-color: #dc3545;          /* Red - errors, critical alerts, delete actions */
--warning-color: #ffc107;         /* Yellow - warnings, pending status */
--info-color: #17a2b8;            /* Blue - informational messages */
```

### Neutral Colors
```css
--background-light: #F9FAFB;      /* Light gray - page backgrounds */
--background-white: #ffffff;      /* White - cards, modals */
--text-primary: #111327;          /* Dark navy - primary text */
--text-secondary: #6B7280;        /* Medium gray - secondary text */
--border-color: #dee2e6;          /* Light gray - borders, dividers */
```

## Typography

### Font Family
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Type Scale
- **H1 (Page Titles)**: 2rem (32px), font-weight: 700
- **H2 (Section Headers)**: 1.5rem (24px), font-weight: 600
- **H3 (Subsection Headers)**: 1.25rem (20px), font-weight: 600
- **Body Text**: 1rem (16px), font-weight: 400, line-height: 1.6
- **Small Text**: 0.875rem (14px), font-weight: 400
- **Labels**: 0.9rem (14.4px), font-weight: 600

## Spacing System

**Base Unit:** 8px

### Spacing Scale
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

## Components

### Buttons

#### Primary Button
```css
background: #00B4A0;
color: white;
padding: 10px 20px;
border-radius: 5px;
font-weight: 600;
hover: background #008c7a;
```

#### Secondary Button
```css
background: #6c757d;
color: white;
padding: 10px 20px;
border-radius: 5px;
```

#### Danger Button
```css
background: #dc3545;
color: white;
padding: 10px 20px;
border-radius: 5px;
```

### Cards
```css
background: white;
padding: 1.5rem;
border-radius: 8px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
```

### Forms

#### Input Fields
```css
padding: 0.75rem;
border: 1px solid #dee2e6;
border-radius: 4px;
font-size: 1rem;
focus: border-color #00B4A0;
```

#### Labels
```css
font-weight: 600;
margin-bottom: 0.5rem;
color: #111327;
```

### Navigation

#### Top Bar (Compliance Manager/Admin)
```css
background: white;
border-bottom: 1px solid #dee2e6;
padding: 1rem 2rem;
display: flex;
justify-content: space-between;
```

#### Header
```css
background: linear-gradient(135deg, #00B4A0, #008c7a);
color: white;
padding: 1rem 0;
box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
```

#### Navigation Menu
```css
background: #111327;
color: white;
active-link: background #00B4A0;
hover: background rgba(0, 180, 160, 0.1);
```

### Status Badges

#### Active/Success
```css
background: #28a745;
color: white;
padding: 0.25rem 0.75rem;
border-radius: 12px;
```

#### Warning
```css
background: #ffc107;
color: #111327;
padding: 0.25rem 0.75rem;
border-radius: 12px;
```

#### Danger/Critical
```css
background: #dc3545;
color: white;
padding: 0.25rem 0.75rem;
border-radius: 12px;
```

#### Info
```css
background: #17a2b8;
color: white;
padding: 0.25rem 0.75rem;
border-radius: 12px;
```

### Tables
```css
border-collapse: collapse;
width: 100%;
th: background #F9FAFB, padding 12px, text-align left, font-weight 600;
td: padding 12px, border-bottom 1px solid #dee2e6;
tr:hover: background #F9FAFB;
```

### Alerts
```css
padding: 1rem;
border-radius: 4px;
margin-bottom: 1rem;

success: background #d4edda, border #c3e6cb, color #155724;
danger: background #f8d7da, border #f5c6cb, color #721c24;
warning: background #fff3cd, border #ffeeba, color #856404;
info: background #d1ecf1, border #bee5eb, color #0c5460;
```

## Layout Guidelines

### Dashboard Layout
- **Sidebar Width:** 250px
- **Content Max Width:** 1400px
- **Card Grid:** 3-column layout for metrics (desktop)
- **Responsive Breakpoints:**
  - Desktop: > 1024px
  - Tablet: 768px - 1024px
  - Mobile: < 768px

### Consistent Patterns
1. **Page Structure:**
   - Header with page title and action button (right-aligned)
   - Main content in white cards
   - Consistent padding: 1.5rem

2. **Form Layout:**
   - Use `.form-row` for horizontal field grouping
   - Use `.form-group` for individual fields
   - Labels above inputs
   - Helper text below inputs in gray (#6B7280)

3. **Action Buttons:**
   - Primary action: Teal button
   - Cancel/Secondary: Gray button
   - Destructive: Red button
   - Always pair "Save" with "Cancel"

## Accessibility Requirements

### Color Contrast
- All text must meet WCAG AA standards (4.5:1 minimum)
- Interactive elements must have clear focus states
- Links should be underlined or clearly distinguishable

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Visible focus indicators required
- Tab order should follow logical reading order

### Screen Readers
- All images must have alt text
- Form inputs must have associated labels
- ARIA labels for icon-only buttons

## Compliance-Specific Design Patterns

### Compliance Alerts
- Use appropriate severity colors (Critical=Red, Warning=Yellow)
- Include clear action items
- Display EPA regulation references when applicable

### Equipment Status
- Active: Green badge
- Retired: Gray badge
- Non-Compliant: Red badge with exclamation icon

### Service Logs
- Chronological display (newest first)
- Clear visual distinction between log types
- Refrigerant quantities in bold
- Link to equipment and technician

### Reports
- Professional, print-friendly layouts
- EPA-compliant formatting
- Clear data tables
- Export options (PDF, Excel, CSV)

## Brand Voice & Tone

**Professional but Approachable**
- Clear, concise language
- Avoid jargon unless EPA-specific
- Instructional and helpful
- Confidence-inspiring for compliance matters

## Icons
- Use consistent icon set throughout
- Prefer SVG icons
- Common icons:
  - 🏠 Home
  - 📊 Dashboard
  - 🔧 Equipment
  - 👤 Technicians
  - 📝 Logs
  - 🔔 Alerts
  - 📄 Documents
  - ⚙️ Settings
