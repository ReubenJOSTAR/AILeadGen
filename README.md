# LeadQualify

An embeddable AI chat widget that replaces static lead capture forms. Visitors have a natural conversation with an AI agent that qualifies them by collecting name, company, email, phone, budget, campaign type, timeline, and call preference — then saves a structured lead and full transcript to a dashboard for review.

## Folder structure

```
leadqualify/
├── backend/      # Python FastAPI — chat API, lead storage, email
├── widget/       # React + Vite IIFE — embeddable chat widget
├── dashboard/    # React + Vite — internal lead management UI
└── supabase/     # Database migrations
```

## Run locally

**Backend**
```bash
cd backend && uvicorn main:app --reload
```

**Widget**
```bash
cd widget && npm run dev
```

**Dashboard**
```bash
cd dashboard && npm run dev
```
