# ORCA AI-Service

AI intelligence layer for the ORCA Marine Intelligence platform.

The AI-Service is responsible for collaborative marine reasoning using Python, LangGraph, domain agents, structured validation, and explicit uncertainty handling.

---

## 1. Responsibilities

The AI-Service owns:

- Weather Agent
- Ocean Agent
- Ecosystem Agent
- Risk Agent
- Decision Agent
- LangGraph workflow
- Chat reasoning and context handling
- Structured input/output validation
- Multi-zone analysis
- Evidence and provenance handling
- Confidence and data-quality assessment
- Prompt definitions
- Service adapters for external environmental providers

The AI-Service does not directly serve the frontend.

The expected communication flow is:

```text
Frontend
   |
   v
Backend
   |
   v
AI-Service
   |
   +---- Weather Service
   |
   +---- Ocean Service
   |
   +---- Ecosystem Service
   |
   +---- GIS Service