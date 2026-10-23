# Corex NOC MONITOR

### Intelligent Network Monitoring, AI-Assisted Troubleshooting & Performance Analytics

Corex NOC MONITOR is a Python-based network operations application that combines PRTG integration, independent background link-health monitoring, Groq-powered AI analysis, performance visualization, automated reporting, and cloud-based license validation.

The system is designed to help network engineers monitor multiple links, investigate connectivity issues, understand utilization trends, and generate operational reports through a centralized desktop interface.

**Its defining architectural feature is the separation of PRTG-dependent monitoring from an independent ping-based health monitoring engine.** This allows configured link reachability checks to continue when the PRTG server becomes unavailable.

> This repository documents the project and its capabilities. It does not contain the complete proprietary application source code or confidential operational configuration.

## 1. Key Features

- Real-time traffic utilization monitoring through PRTG integration
- Independent background ping monitoring
- Automatic link-status and outage detection
- Real-time latency and packet-loss visualization
- Historical performance analytics
- Daily, weekly, monthly, and custom-period traffic graphs
- Groq AI-powered link analysis and troubleshooting assistance
- Interactive geographic network map
- Automated Excel reports using OpenPyXL
- PDF graph and report generation using ReportLab
- Email delivery of generated reports
- Voice alerts and configurable repeated-alert controls
- Link and sensor management
- Protected administrative settings
- Cloud-based license validation

## 2. Dual Monitoring Architecture

### 2.1 PRTG-Integrated Traffic Monitoring

The PRTG integration retrieves supported sensor and utilization data from a configured PRTG server.

Features include:

- Live traffic utilization in Mbps
- Automatic peak-utilization tracking
- Utilization status monitoring
- Historical traffic graph generation
- Custom date and time-range selection
- Traffic statistics and reporting
- Graph export and email delivery

This component uses PRTG as its monitoring data source. PRTG-dependent features therefore require the server and relevant APIs to be accessible.

### 2.2 Independent Background Link-Health Monitoring

The independent monitoring engine continuously pings configured network endpoints in the background, recording reachability and performance information without depending on PRTG for those checks.

Features include:

- Continuous background pinging
- Automatic detection of unresponsive endpoints
- Latency measurement
- Packet-loss and timeout tracking
- Historical performance records
- Downtime-event tracking
- Availability and latency statistics
- Link-health alerts and visual status indicators

**Resilience advantage:** If PRTG becomes unavailable, the independent ping engine can continue checking configured endpoints as long as the monitoring workstation, monitoring process, and relevant network paths remain operational.

This provides an additional source of link-health information instead of making all monitoring dependent on a single server.

*Technical note: Ping confirms IP-level reachability, not the health of every application or service running behind an endpoint.*

## 3. AI Analysis and Troubleshooting — Groq AI

The application integrates a Groq-powered AI assistant into its dedicated AI Analysis interface.

Rather than requiring an engineer to interpret every monitoring value or diagnostic log manually, the feature uses relevant diagnostic information to generate plain-language analysis and troubleshooting suggestions.

### Capabilities

- Analyse available link-performance information and diagnostic logs
- Help investigate connectivity faults and network congestion
- Identify potential causes based on the supplied evidence
- Recommend practical diagnostic steps
- Provide troubleshooting guidance during network incidents
- Work alongside the monitoring, ping diagnostics, and graph modules

### AI-assisted workflow

1. The monitoring components collect available utilization, latency, packet-loss, and status information.
2. The engineer selects a link or issue to investigate.
3. Relevant diagnostic information is submitted to the configured Groq AI service.
4. The service returns an analysis and suggested troubleshooting actions.
5. The engineer evaluates the recommendations against actual network conditions.

The AI feature is intended to support technical decision-making, not replace engineering verification. Its availability depends on internet access and valid AI-service configuration.

## 4. Real-Time Alerts and Outage Detection

The alert system helps operators identify important monitoring events without continuously watching every screen.

Supported functionality includes:

- Automatic link-down detection
- Live status changes
- Voice notifications
- Repeated alerts at configured intervals
- Alert reset and suppression logic
- Dashboard indicators for critical faults
- Navigation to relevant monitoring information

These features help make network failures more visible and support quicker investigation.

## 5. Latency and Network Performance Analytics

The Ping Monitoring and Performance module provides a dedicated view of network responsiveness and recorded connectivity events.

### Real-time performance

- Continuously updated latency graph
- Automatically scrolling performance window
- Dynamic latency scaling
- Average and peak latency indicators
- Packet-loss visualization
- Timeout-event markers

### Historical performance

The application supports historical views covering selected periods, including 8 hours, 24 hours, and 7 days.

Available statistics include:

- Average latency
- Maximum latency
- Packet-loss percentage
- Recorded downtime events
- Availability percentage
- Number of collected samples

The statistics are calculated from stored monitoring records, allowing engineers to investigate performance beyond the current moment.

## 6. Advanced Traffic Graph Analytics

The Live Graph module retrieves supported traffic graphs directly from PRTG.

### Graph capabilities

- Daily, weekly, and monthly views
- Custom dates and time ranges
- Traffic statistics visualization
- Dedicated graph-viewer windows
- PDF export
- Email delivery of generated graphs

### Graph-generation workflow

1. Select a configured link.
2. Choose the graph type.
3. Select the required date and time range.
4. Calculate the corresponding time window.
5. Construct the appropriate authenticated PRTG request.
6. Retrieve the graph in SVG format where supported.
7. Convert the graph for desktop display.
8. Display it in the graph viewer.
9. Export or email the result where supported.

This workflow provides a practical way to review historical traffic and prepare performance evidence for operational reporting.

## 7. Geographic Network Visualization

The application includes a geographic map that displays configured network links using location coordinates.

Its purpose is to give engineers a visual overview of network distribution and provide an additional way to identify affected links.

Features include:

- Geographic coordinate mapping
- Configurable link-location records
- Dynamically rendered link paths
- Visual differentiation between healthy and down links
- Dashboard navigation to fault details

The map is designed to update link-state presentation using the application's monitoring status information.

*Public documentation and screenshots should use sanitized locations or demonstration data rather than exposing real network topology or customer locations.*

## 8. Automated Reporting

### Excel Reporting Engine

The Excel reporting module uses OpenPyXL to generate structured workbooks for monitoring analysis.

Supported reporting capabilities include:

- Peak utilization values
- Historical utilization records
- Daily and monthly reports
- Capacity tracking
- Formatted data and utilization highlighting

### PDF Reporting Engine

The PDF reporting module uses ReportLab to produce reports suitable for sharing and presentation.

Supported functionality includes:

- Automated PDF generation
- Embedded traffic graphs
- Utilization and device statistics
- Structured report formatting

### Email Delivery

SMTP integration allows supported reports and graph attachments to be delivered by email.

This reduces the manual effort involved in preparing and distributing monitoring information.

## 9. Technical Architecture

The application uses a modular, multi-threaded desktop architecture designed to keep background monitoring work separate from interface rendering.

| Layer | Technology and responsibility |
|---|---|
| Desktop interface | CustomTkinter and native Tkinter |
| Shared application state | Centralized state and calculation components |
| Network workers | Background threads and socket-based ping checks |
| PRTG integration | HTTP/API communication and sensor data retrieval |
| Historical storage | SQLite |
| Data visualization | SVG processing, CairoSVG and image rendering |
| Geographic visualization | TkinterMapView and canvas-based rendering |
| Excel reporting | OpenPyXL |
| PDF generation | ReportLab |
| AI analysis | Groq API integration |
| Configuration | JSON-based application settings |
| Email delivery | SMTP |
| Licensing | Separate Django-based cloud service |

The architecture separates interface updates, network polling, data processing, reporting, and external service communication to help keep the desktop interface responsive.

## 10. Data Storage and Configuration

The application uses SQLite to store historical ping and performance records.

Stored information may include:

- Device identifier
- Configured endpoint address
- Latency
- Reachability status
- Packet-loss information
- Sample timestamp

A configured retention policy removes older records to help control database growth. The current documented retention period is seven days.

Application configuration and supporting data files are managed separately from the core application logic. Required directories and configuration files can be initialized automatically.

## 11. Security and Access Control

The application distinguishes between normal operational access and administrative functions.

### Normal-user functions

- View monitoring information
- Review reports
- Generate graphs
- Monitor link status

### Administrative functions

- Manage configured links
- Modify application settings
- Maintain monitoring configuration
- Perform supported maintenance operations

Administrative settings are protected by password-based access controls.

Security-sensitive implementation details, administrative credentials, private API keys, and internal configuration structures are intentionally omitted from this public README.

**Deployment security considerations:**

- Protect PRTG credentials and AI API keys.
- Avoid committing private configuration files.
- Restrict access to administrative functions.
- Protect monitoring databases and generated reports.
- Validate licensing responses securely.
- Keep confidential network and customer information out of public repositories.

## 12. Cloud Licensing

FOCUS NOC MONITOR integrates with a separate Django-based licensing service hosted within the COREX infrastructure.

Licensing functionality includes:

- Installation identification
- Remote license requests
- Server-side license validation
- License-status checking
- Expiration and activation handling
- Access control based on licensing status

The desktop application communicates with the licensing service through an API. Subscription administration and activation review are currently handled manually.

The licensing service is separate from the PRTG monitoring system and is part of the application's deployment and access-control architecture.

## 13. Windows Deployment

The application can be packaged as a standalone Windows executable using PyInstaller.

The deployment workflow supports:

- Packaging the Python application into an executable
- Initializing required application data directories
- Creating required configuration and database files
- Supporting deployment without a separately installed Python runtime, subject to packaged dependencies
- Using a Windows application icon

The executable still requires appropriate runtime configuration and network access for features that depend on PRTG, Groq, email services, or the licensing server.

## 14. Technologies and Engineering Skills Demonstrated

- Python desktop application development
- Network monitoring and diagnostics
- Background processing and multithreading
- REST API integration
- PRTG integration
- AI service integration
- SQLite database design and historical data analysis
- Data visualization and graph processing
- Excel and PDF report generation
- SMTP automation
- Geographic network visualization
- Configuration and access-control design
- Django API and licensing integration
- Windows application packaging

## 15. Future Development

Potential areas for further development include:

- Expanded network-performance analytics
- More advanced AI-assisted diagnostics
- Additional monitoring and alert integrations
- Enhanced reporting and dashboard capabilities
- Further testing and resilience improvements
- Improved configuration protection and deployment workflows

## Project Summary

COREX NOC MONITOR combines network traffic monitoring, independent reachability checks, latency analysis, AI-assisted troubleshooting, geographic visualization, automated reporting, and remote license validation in one desktop application.

Its key architectural advantage is that **the independent ping-monitoring component can continue checking configured links during a PRTG server outage**, while the PRTG-dependent features remain subject to PRTG availability.

**Developer:** Hardy

**Focus areas:** Network Engineering · Python · Network Monitoring · Automation · AI Integration · Software Development

*FOCUS NOC MONITOR is an independently developed application that integrates with PRTG. It is not an official PRTG product.*

