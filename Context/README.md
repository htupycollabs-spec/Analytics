# TikTok Affiliate Brain — Context Repository

This repo stores all machine-readable context for the TikTok affiliate Claude assistant.

## How It Works

The assistant reads and writes these files to maintain full context across sessions. Notion holds human-readable, actionable content. GitHub holds everything else.

## File Map

| File | Purpose | Update frequency |
|---|---|---|
| `context/SESSION_LOG.md` | Current session state (DONE/SOON/LATER) | Every session |
| `context/PRODUCTS.md` | All affiliate products with commission, stats, status | When products change |
| `context/POSTING_SCHEDULE.md` | Video log + weekly posting plan | When posts are planned or logged |
| `context/PERFORMANCE_BASELINE.md` | 65-day historical data + ongoing performance | When new data is captured |
| `context/LIVE_CONTEXT.md` | Full project context, strategy, goals | On major decisions/shifts |
| `context/CONTENT_IDEAS.md` | Approved content idea backlog | When ideas are generated |
| `context/PROTOCOL.md` | Operating rules for the assistant | Rarely |

## Notion Counterpart

The assistant also maintains these Notion databases:
- **Post Schedule** — weekly posting checklist
- **Product Showcase** — browsable active products list
- **Commission Summary** — monthly earnings totals
- **Ideas Inbox** — quick idea capture
- **Affiliate Notes** — brand relationship notes

## First Session Setup Checklist

- [ ] Update `[NAME]` and `[GITHUB_RAW_URL]` placeholders in the system prompt
- [ ] Import 65-day performance data summary into `PERFORMANCE_BASELINE.md`
- [ ] Add current active products to `PRODUCTS.md`
- [ ] Set up Notion databases and add URLs to `LIVE_CONTEXT.md`
- [ ] Run "Plan this week" to generate first Notion Post Schedule
