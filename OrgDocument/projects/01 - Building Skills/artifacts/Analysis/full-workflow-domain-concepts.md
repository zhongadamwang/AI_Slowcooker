# Domain Concepts Analysis

**Project**: full-workflow-test  
**Generated**: 2026-02-21T11:15:00Z  
**Source**: full-workflow-requirements.json, full-workflow-goals.json  
**Total Entities**: 6 | **Total Concepts**: 5 | **Total Relationships**: 5

## Domain Areas

### Transaction Processing
**Key Entities**: Transaction, Account  
**Core Concepts**: Transaction Authorization, High Availability  
**Primary Processes**: Authorization, Settlement, Balance Validation  
**Performance Requirements**: 150ms domestic authorization, 300ms international authorization, 50K TPS capacity

### Risk Management  
**Key Entities**: FraudDetectionEngine  
**Core Concepts**: Fraud Detection  
**Primary Processes**: Risk Scoring, Fraud Assessment, Model Training  
**Performance Requirements**: 50ms risk scoring, >99% accuracy, <0.1% false positives

### Payment Processing
**Key Entities**: PaymentNetwork  
**Core Concepts**: Transaction Authorization  
**Primary Processes**: Network Integration, Authorization Messaging, Settlement Processing  
**Performance Requirements**: 99.99% network uptime, PCI DSS Level 1 compliance

### Security Infrastructure
**Key Entities**: HSM  
**Core Concepts**: Regulatory Compliance, Event Sourcing  
**Primary Processes**: Key Generation, Key Rotation, Encryption Management  
**Performance Requirements**: FIPS 140-2 Level 3 compliance, Zero-downtime key rotation

### Currency Management
**Key Entities**: CurrencyExchange  
**Core Concepts**: Transaction Authorization  
**Primary Processes**: Rate Updates, Currency Conversion, Rate Validation  
**Performance Requirements**: 30-second rate updates, 0.01% rate accuracy, 47 currency support

### Compliance Management
**Key Entities**: (External Systems)  
**Core Concepts**: Regulatory Compliance  
**Primary Processes**: OFAC Screening, AML Monitoring, Audit Trail Maintenance  
**Performance Requirements**: 100ms OFAC screening, Real-time compliance monitoring, 7-year audit retention

## Entities

### Transaction *(ENT-001)*
**Domain Area**: Transaction Processing  
**Description**: Financial transaction processed by the NTPE system

**Attributes**:
- `transaction_id` (identifier): Unique transaction identifier [public]
- `amount` (decimal): Transaction monetary amount [public]
- `currency_code` (string): ISO 4217 currency code [public]
- `authorization_code` (string): Payment network authorization code [private]
- `status` (enumeration): Transaction processing status [pending, authorized, declined, settled, reversed] [public]
- `timestamp` (datetime): Transaction initiation timestamp [public]
- `risk_score` (decimal): ML-generated fraud risk score [private]

**Operations**:
- `authorize(account_id, amount, merchant_id)` → AuthorizationResult: Perform authorization check with 150ms/300ms response time [public]
- `calculateRisk(transaction_data, behavior_patterns)` → RiskScore: Generate fraud risk score within 50ms [private]
- `settle(authorization_code)` → SettlementResult: Process settlement and update account balances [public]

**Source References**: [R-008:Functional], [R-011:Functional], [R-022:Performance]

### Account *(ENT-002)*
**Domain Area**: Account Management  
**Description**: Bank account involved in transaction processing

**Attributes**:
- `account_number` (identifier): Unique account identifier [public]
- `balance` (decimal): Available account balance [private]
- `account_type` (enumeration): Type of account [checking, savings, credit, business] [public]
- `status` (enumeration): Account operational status [active, frozen, closed, restricted] [public]

**Operations**:
- `validateBalance(amount)` → boolean: Check sufficient funds for transaction [public]
- `updateBalance(amount, transaction_type)` → void: Apply debit/credit to account balance [private]

**Source References**: [R-008:Functional], [R-013:Integration]

### FraudDetectionEngine *(ENT-003)*
**Domain Area**: Risk Management  
**Description**: Machine learning system for real-time fraud detection

**Attributes**:
- `model_version` (string): Active ML model version identifier [public]
- `accuracy_threshold` (decimal): Minimum required accuracy (>99%) [private]
- `false_positive_rate` (decimal): Current false positive rate (<0.1%) [private]

**Operations**:
- `evaluateTransaction(transaction_data, customer_profile, behavioral_patterns)` → FraudAssessment: Analyze transaction for fraud risk within 50ms [public]
- `updateModel(model_data)` → void: Deploy updated ML model with continuous learning [private]

**Source References**: [R-011:Functional], [R-012:Functional]

### PaymentNetwork *(ENT-004)*
**Domain Area**: Payment Processing  
**Description**: External payment processing network (Visa, Mastercard, FedWire)

**Attributes**:
- `network_id` (identifier): Payment network identifier [public]
- `network_type` (enumeration): Type of payment network [visa, mastercard, fedwire, ach] [public]
- `certification_level` (string): Required certification (PCI DSS Level 1) [public]
- `uptime_sla` (decimal): Required uptime percentage (99.99%) [public]

**Operations**:
- `processAuthorization(iso8583_message)` → AuthorizationResponse: Send authorization request to payment network [public]
- `processSettlement(settlement_batch)` → SettlementConfirmation: Submit settlement batch to network [public]

**Source References**: [R-015:Integration], [R-016:Integration]

### HSM *(ENT-005)*
**Domain Area**: Security Infrastructure  
**Description**: Hardware Security Module for cryptographic key management

**Attributes**:
- `hsm_id` (identifier): Hardware security module identifier [public]
- `fips_level` (string): FIPS 140-2 certification level (Level 3) [public]
- `key_rotation_schedule` (string): Automatic monthly key rotation schedule [private]

**Operations**:
- `generateKey(key_type, key_length)` → CryptographicKey: Generate cryptographic keys with FIPS compliance [private]
- `rotateKeys(rotation_policy)` → void: Perform automatic monthly key rotation with zero downtime [private]

**Source References**: [R-018:Security], [R-019:Security]

### CurrencyExchange *(ENT-006)*
**Domain Area**: Currency Management  
**Description**: Multi-currency transaction processing and rate management

**Attributes**:
- `currency_pair` (string): Source/target currency pair (e.g., USD/EUR) [public]
- `exchange_rate` (decimal): Current exchange rate with 0.01% accuracy [public]
- `rate_timestamp` (datetime): Rate update timestamp (30-second intervals) [public]
- `rate_source` (enumeration): Exchange rate data source [federal_reserve, ecb, bank_of_england] [public]

**Operations**:
- `convertCurrency(amount, source_currency, target_currency)` → ConvertedAmount: Convert transaction amount using real-time rates [public]
- `updateRates(rate_feed_data)` → void: Refresh exchange rates every 30 seconds during market hours [private]

**Source References**: [R-009:Functional], [R-010:Functional]

## Business Concepts

### Transaction Authorization *(CON-001)*
**Domain Area**: Payment Processing  
**Definition**: Real-time process to approve or decline financial transactions within 150ms/300ms  
**Synonyms**: transaction approval, payment authorization, transaction validation  
**Source References**: [R-008:Functional]

### Fraud Detection *(CON-002)*
**Domain Area**: Risk Management  
**Definition**: Machine learning-based real-time evaluation of transaction risk with >99% accuracy  
**Synonyms**: risk assessment, fraud prevention, transaction screening  
**Source References**: [R-011:Functional], [R-012:Functional]

### Regulatory Compliance *(CON-003)*
**Domain Area**: Compliance Management  
**Definition**: Adherence to banking regulations including BSA/AML, OFAC, PCI DSS, and data protection laws  
**Synonyms**: compliance monitoring, regulatory adherence, audit compliance  
**Source References**: [R-024:Compliance], [R-025:Compliance]

### High Availability *(CON-004)*
**Domain Area**: System Reliability  
**Definition**: System uptime of 99.99% with maximum 15-minute recovery time and 30-second data loss tolerance  
**Synonyms**: system availability, uptime management, disaster recovery  
**Source References**: [R-023:Performance]

### Event Sourcing *(CON-005)*
**Domain Area**: System Architecture  
**Definition**: Architecture pattern maintaining complete audit trails of all transaction state changes  
**Synonyms**: event logging, audit trail, transaction history  
**Source References**: [R-004:Architecture]

## Terminology Glossary

| Term | Definition | Domain Area | Context |
|------|------------|-------------|---------|
| NTPE | NextGen Transaction Processing Engine - the core banking transaction system | System Architecture | System name for the new transaction processing platform |
| ISO 8583 | International standard for financial transaction messaging | Technical Standards | Message format for core banking system integration |
| TPS | Transactions Per Second - measure of system throughput | Performance Measurement | Performance metric for transaction processing capacity |
| OFAC | Office of Foreign Assets Control - US Treasury sanctions authority | Regulatory Compliance | Real-time sanctions screening requirement |
| HSM | Hardware Security Module - dedicated cryptographic hardware | Security Infrastructure | FIPS 140-2 Level 3 compliant encryption key management |
| Saga Pattern | Distributed transaction pattern using compensating transactions | System Architecture | ACID compliance implementation without two-phase commit |
| PCI DSS | Payment Card Industry Data Security Standard | Security Compliance | Level 1 certification requirement for payment network integration |
| RTO | Recovery Time Objective - maximum acceptable downtime | Disaster Recovery | 15-minute maximum recovery time requirement |
| RPO | Recovery Point Objective - maximum acceptable data loss | Disaster Recovery | 30-second maximum data loss tolerance |

## Entity Relationships

### FraudDetectionEngine → Transaction *(REL-001)*
**Type**: Processes (one-to-many)  
**Description**: Fraud detection engine evaluates every transaction for risk scoring  
**Source**: [R-011:Functional]

### PaymentNetwork → Transaction *(REL-002)*
**Type**: Authorizes (one-to-many)  
**Description**: Payment networks provide authorization responses for transactions  
**Source**: [R-015:Integration]

### HSM → Transaction *(REL-003)*
**Type**: Secures (one-to-many)  
**Description**: HSM provides cryptographic protection for transaction data  
**Source**: [R-018:Security]

### Transaction → Account *(REL-004)*
**Type**: Debits/Credits (many-to-one)  
**Description**: Transactions modify account balances through debit/credit operations  
**Source**: [R-008:Functional]

### CurrencyExchange → Transaction *(REL-005)*
**Type**: Converts (one-to-many)  
**Description**: Currency exchange service converts international transaction amounts  
**Source**: [R-009:Functional]

## Domain Complexity Analysis

### High Complexity Areas
- **Transaction Processing**: Real-time authorization with sub-second response times
- **Risk Management**: Machine learning fraud detection with accuracy requirements
- **Security Infrastructure**: FIPS 140-2 Level 3 cryptographic key management

### Medium Complexity Areas  
- **Payment Processing**: Multiple payment network integration and certification
- **Currency Management**: Real-time exchange rate processing for 47 currencies
- **Compliance Management**: Automated regulatory reporting and monitoring

### Integration Points
- **Core Banking Integration**: ISO 8583 messaging with FIS Profile system
- **External API Integration**: OFAC, credit bureaus, KYC/AML data providers
- **Network Integration**: Visa VisaNet, Mastercard Mastercom, FedWire, ACH

---

**Traceability**: Extracted from requirements R-001 through R-025  
**Confidence Score**: 0.92/1.0 (Excellent)  
**Generated**: 2026-02-21T11:15:00Z  
**Domain Coverage**: 6 functional areas with complete entity mapping