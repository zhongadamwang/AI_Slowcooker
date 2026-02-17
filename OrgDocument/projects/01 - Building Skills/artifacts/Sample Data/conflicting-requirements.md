# Customer Portal System - Conflicting Requirements Sample

**Document Type**: Requirements Specification  
**Domain**: Customer Service  
**Complexity**: Medium  
**Format**: Mixed  
**Validation Target**: Conflict resolution, error handling, assumption identification

## Project Background

Our company needs a new customer portal to improve customer experience and reduce support costs. The project involves stakeholders from customer service, IT security, marketing, and executive leadership.

## Customer Service Department Requirements

The customer service team requires the portal to display all customer information immediately upon login without additional navigation. Customers should see their complete account history, service tickets, billing information, and product warranties on a single dashboard page.

Customer service representatives want customers to have the ability to escalate any issue directly to live chat support without restrictions. The portal must provide instant case creation capabilities for any customer concern.

Response times for loading customer data should be under 1 second to reduce customer frustration during support calls.

## IT Security Requirements  

All customer data access must be strictly controlled using role-based permissions. Sensitive financial information should only be visible after additional authentication steps including multi-factor verification.

Customer session timeouts must occur after 5 minutes of inactivity to prevent unauthorized access. All data transmissions must use end-to-end encryption with certificate pinning.

Third-party integrations are prohibited for security compliance. The system must be entirely self-contained with no external API calls.

## Marketing Department Requirements

The portal must integrate with our CRM system (Salesforce) to track customer engagement and provide personalized product recommendations. Marketing wants to display targeted promotional content based on customer purchase history and browsing patterns.

Customer data should be shared with our marketing automation platform (HubSpot) for campaign personalization. The portal should collect additional customer preferences and behavioral data for marketing analysis.

Social media integration is essential for modern customer engagement, allowing customers to share their experiences and connect their social profiles.

## Executive Requirements

The project budget is capped at $150,000 with a 6-month delivery timeline. The portal must reduce support call volume by 40% within the first quarter after launch.

Performance is critical - the portal must support 5,000 concurrent users with response times under 2 seconds for all operations.

The solution should leverage our existing cloud infrastructure investment in Microsoft Azure while also taking advantage of the cost savings available through Amazon AWS services.

## User Experience Requirements

From customer feedback sessions, users want a simple, intuitive interface that requires no training. The portal should work identically across all devices and browsers.

However, our user research also shows that customers prefer feature-rich interfaces that provide comprehensive functionality in a single location, even if this makes the interface more complex.

Customers want the ability to customize their dashboard layout and choose which information is displayed prominently. At the same time, they want a standardized interface that looks the same for all users to reduce confusion.

## Technical Constraints

The portal must integrate with our legacy customer database using SOAP web services. However, our data architecture team has mandated that all new integrations use RESTful APIs exclusively.

The system should be built using our standard Java enterprise stack. The development team has also requested approval to use modern JavaScript frameworks like React for improved user experience.

Database requirements specify that all customer data must be stored in our on-premises SQL Server environment. Cloud storage is prohibited due to data locality requirements. However, our disaster recovery plan requires all systems to have cloud-based backup solutions.

## Compliance and Regulatory Requirements

The portal must comply with GDPR requirements for European customers, including data portability and deletion rights. However, our audit requirements mandate that all customer data be retained for 10 years minimum without modification.

PCI DSS compliance is required for handling payment information. Customer payment data should be tokenized and stored securely. Marketing has requested direct access to payment patterns for customer segmentation analysis.

---

## Expected Validation Results

### Identified Conflicts

#### Performance vs Security Conflicts
- **Conflict 1**: Customer service wants <1s response times vs Security requires additional MFA steps for sensitive data
- **Conflict 2**: Executive requirement for 5,000 concurrent users vs 5-minute session timeouts

#### Integration Conflicts  
- **Conflict 3**: Security prohibits third-party integrations vs Marketing requires CRM/marketing automation integration
- **Conflict 4**: Legacy SOAP services vs mandate for RESTful APIs only

#### Infrastructure Conflicts
- **Conflict 5**: Executive wants Azure infrastructure + AWS cost savings (incompatible)
- **Conflict 6**: On-premises database requirement vs cloud backup requirement

#### Data Access Conflicts
- **Conflict 7**: Display all data immediately vs role-based restrictions with additional auth
- **Conflict 8**: GDPR data deletion rights vs 10-year retention mandate
- **Conflict 9**: PCI DSS data protection vs Marketing direct access to payment patterns

#### User Experience Conflicts
- **Conflict 10**: Simple interface requiring no training vs feature-rich comprehensive interface
- **Conflict 11**: Customizable dashboard layouts vs standardized interface for all users

### Domain Analysis Challenges
- **Inconsistent Stakeholder Priorities**: Security vs Marketing vs Customer Service have opposing requirements
- **Technology Stack Conflicts**: Java enterprise vs modern JavaScript, SOAP vs REST, on-premises vs cloud
- **Regulatory Contradictions**: Data retention vs deletion, security isolation vs integration

### Goals Extraction Complications
- **Competing Success Metrics**: Support cost reduction vs comprehensive feature delivery
- **Timeline vs Quality Trade-offs**: 6-month delivery with complex, conflicting requirements
- **Budget vs Infrastructure Conflicts**: $150K budget with dual cloud infrastructure

### Expected Change Management Needs
- **Stakeholder Alignment Sessions**: Required to resolve fundamental conflicts before development
- **Requirements Prioritization**: Must establish hierarchy of conflicting requirements
- **Compliance Review**: Legal review needed for GDPR vs retention conflicts
- **Architecture Decision Records**: Document resolution of technology stack conflicts

### Recommended Validation Behaviors
- **Conflict Detection**: System should identify and flag incompatible requirements
- **Stakeholder Mapping**: Identify requirement ownership for conflict resolution
- **Assumption Surfacing**: Highlight implicit assumptions underlying conflicts
- **Resolution Tracking**: Track how conflicts are resolved in change management system
- **Risk Assessment**: Flag high-risk conflicts that could derail project success