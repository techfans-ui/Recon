Deployment instructions
=======================

This repo supports two deployment targets for the frontend:

- GitHub Pages (automatic on push to `main`) — uses static `next export` output.
- Vercel (manual dispatch via GitHub Actions) — recommended for SSR and incremental builds.

GitHub Pages
-----------
1. The workflow `.github/workflows/deploy_pages.yml` builds the frontend and exports static files into `frontend/out`, then publishes them to GitHub Pages.
2. To enable Pages: go to the repository Settings → Pages and ensure the `gh-pages` deployment source is set (the action will populate it).

Vercel
------
1. Create a Vercel project and connect it to this GitHub repo, or add the project via the Vercel dashboard.
2. Add the following repository secrets in GitHub Settings → Secrets:
   - `VERCEL_TOKEN` — your personal Vercel token
   - `VERCEL_ORG_ID` — your Vercel organization ID
   - `VERCEL_PROJECT_ID` — your Vercel project ID
3. Trigger the `Deploy Frontend to Vercel (manual)` workflow from Actions → Deploy Frontend to Vercel → Run workflow.

Notes
-----
- The GitHub Pages workflow relies on `npm run export`. Pages will serve the static `out` folder.
- Vercel deployment can be used instead for better Next.js support (SSR, edge functions).
