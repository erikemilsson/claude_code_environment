# Publish Command

## Purpose

Automated publication and deployment workflow for documentation sites, blog posts, and other content. This command handles building, validating, and deploying content to production.

## Context Required

- Content file(s) to publish
- Publication target (staging/production)
- Documentation generator being used
- Hosting platform

## Pre-Publication Checklist

Before running this command, ensure:

- [ ] All reviews completed and approved
- [ ] Content task marked as "Finished"
- [ ] Code examples tested
- [ ] Links verified
- [ ] Images optimized and uploaded
- [ ] Metadata complete (title, description, tags, date)
- [ ] Spell check passed
- [ ] No "TODO" or placeholder text remains

## Publication Process

### Step 1: Pre-Publish Validation

Run automated checks to catch common issues:

```bash
# Spell check
npx markdown-spellcheck '**/*.md' --report

# Link checking
npx markdown-link-check '**/*.md'

# Linting
npx markdownlint '**/*.md'

# Check for TODOs
grep -r "TODO\|FIXME\|XXX" content/
```

**Acceptance Criteria**:
- [ ] No spelling errors
- [ ] No broken links
- [ ] No linting errors
- [ ] No placeholder text

**If Issues Found**: Fix and re-run validation

---

### Step 2: Build Documentation

Generate static site from Markdown source:

#### For MkDocs

```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Build site
mkdocs build --clean --strict

# Verify build
ls -la site/
```

#### For Docusaurus

```bash
# Install dependencies (if needed)
npm install

# Build site
npm run build

# Verify build
ls -la build/
```

#### For Sphinx

```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Build HTML
make html

# Verify build
ls -la _build/html/
```

#### For VuePress

```bash
# Install dependencies (if needed)
npm install

# Build site
npm run build

# Verify build
ls -la .vuepress/dist/
```

#### For Hugo

```bash
# Build site
hugo --minify

# Verify build
ls -la public/
```

**Acceptance Criteria**:
- [ ] Build completes without errors
- [ ] Build warnings reviewed and addressed
- [ ] Generated files exist in output directory

---

### Step 3: Local Preview

Preview the built site locally before deploying:

#### MkDocs
```bash
mkdocs serve
# Open http://localhost:8000
```

#### Docusaurus
```bash
npm run serve
# Open http://localhost:3000
```

#### Sphinx
```bash
python -m http.server 8000 --directory _build/html
# Open http://localhost:8000
```

#### Hugo
```bash
hugo server
# Open http://localhost:1313
```

**Manual Verification**:
- [ ] New content appears correctly
- [ ] Navigation works
- [ ] Search functions (if applicable)
- [ ] Code examples render properly
- [ ] Images display correctly
- [ ] Links work
- [ ] Responsive design (check mobile view)

---

### Step 4: Deploy to Staging (Recommended)

Deploy to staging environment for final review:

#### GitHub Pages (Staging Branch)

```bash
# Build
mkdocs build --clean

# Deploy to staging branch
git checkout staging
cp -r site/* .
git add .
git commit -m "Deploy to staging: [content description]"
git push origin staging
```

**Staging URL**: `https://username.github.io/repo-name/staging/`

#### Netlify (Branch Deploy)

```bash
# Netlify automatically deploys branches
git checkout -b preview/[feature-name]
git push origin preview/[feature-name]
```

**Staging URL**: Provided by Netlify in PR comments

#### Vercel (Branch Deploy)

```bash
# Vercel automatically deploys branches
git checkout -b preview/[feature-name]
git push origin preview/[feature-name]
```

**Staging URL**: Provided by Vercel in PR comments

**Staging Review**:
- [ ] Content displays correctly in staging environment
- [ ] SSL/HTTPS works
- [ ] Custom domain works (if configured)
- [ ] Analytics tracking works (if configured)
- [ ] Search indexing excluded (robots.txt configured)

**Timeline**: Allow stakeholders 24 hours to review staging

---

### Step 5: Deploy to Production

Deploy approved content to production:

#### GitHub Pages (Main)

```bash
# From main branch
mkdocs gh-deploy --clean

# Or manually
mkdocs build --clean
git checkout gh-pages
cp -r site/* .
git add .
git commit -m "Publish: [content description]"
git push origin gh-pages
```

#### Netlify (Automated)

```bash
# Merge to main (triggers automatic deploy)
git checkout main
git merge staging
git push origin main
```

**Monitor**: Check Netlify dashboard for deploy status

#### Vercel (Automated)

```bash
# Merge to main (triggers automatic deploy)
git checkout main
git merge staging
git push origin main
```

**Monitor**: Check Vercel dashboard for deploy status

#### AWS S3 + CloudFront

```bash
# Build
mkdocs build --clean

# Sync to S3
aws s3 sync site/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

#### Read the Docs

```bash
# Commit and push (triggers automatic build)
git add .
git commit -m "Publish: [content description]"
git push origin main
```

**Monitor**: Check Read the Docs dashboard

#### Custom Server (SSH/SFTP)

```bash
# Build
mkdocs build --clean

# Deploy via rsync
rsync -avz --delete site/ user@server:/var/www/docs/

# Or via SCP
scp -r site/* user@server:/var/www/docs/
```

**Acceptance Criteria**:
- [ ] Deploy completes without errors
- [ ] Production site updated
- [ ] New content visible

---

### Step 6: Post-Deployment Verification

Verify production deployment:

**Automated Checks**:
```bash
# Check site is accessible
curl -I https://your-docs-site.com

# Check specific new page
curl -I https://your-docs-site.com/new-page

# Check SSL certificate
curl -vI https://your-docs-site.com 2>&1 | grep -i ssl
```

**Manual Verification**:
- [ ] New content appears on production site
- [ ] URLs resolve correctly
- [ ] Images load
- [ ] Navigation works
- [ ] Search includes new content (may take time to index)
- [ ] Mobile view works
- [ ] Page speed acceptable

**Performance Check**:
- [ ] PageSpeed Insights score acceptable
- [ ] Time to First Byte (TTFB) < 600ms
- [ ] First Contentful Paint (FCP) < 1.8s
- [ ] Largest Contentful Paint (LCP) < 2.5s

---

### Step 7: Update Sitemap and Search

Ensure new content is discoverable:

#### Sitemap

```bash
# Most generators create sitemap.xml automatically
# Verify it exists and includes new content
curl https://your-docs-site.com/sitemap.xml
```

#### Submit to Search Engines

```bash
# Google Search Console
# Manually submit sitemap or request indexing for specific URLs

# Or programmatically
curl https://www.google.com/ping?sitemap=https://your-docs-site.com/sitemap.xml
```

#### Update Internal Search

If using custom search (Algolia, etc.):

```bash
# Algolia DocSearch
npm run algolia:update

# Or trigger crawler
# Visit Algolia dashboard and trigger reindex
```

**Acceptance Criteria**:
- [ ] Sitemap generated and accessible
- [ ] Search engines notified
- [ ] Internal search updated

---

### Step 8: Announcement and Promotion

Notify relevant parties about new content:

#### Internal Notification

- [ ] Post in team Slack/Teams channel
- [ ] Update internal changelog
- [ ] Email stakeholders if needed

#### External Promotion (If Applicable)

- [ ] Share on social media (Twitter, LinkedIn)
- [ ] Post in community forums/Discord/Slack
- [ ] Send newsletter update
- [ ] Update related documentation with links

**Example Messages**:

**Internal**:
```
📚 New docs published!

"Getting Started with Authentication"
https://docs.example.com/guides/authentication

This guide covers OAuth setup, token management, and common troubleshooting.

#documentation #engineering
```

**External** (Twitter/X):
```
🚀 New guide: Getting Started with Authentication

Learn how to implement OAuth, manage tokens, and handle common auth issues.

📖 Read now: https://docs.example.com/guides/authentication

#API #authentication #developers
```

---

### Step 9: Monitor and Track

Track content performance:

#### Analytics Setup

Ensure tracking is configured:
- Google Analytics
- Plausible Analytics
- Mixpanel
- Custom analytics

#### Monitor Metrics

**First 24 Hours**:
- Page views
- Bounce rate
- Time on page
- Traffic sources

**First Week**:
- Search queries leading to page
- External links to page
- User feedback/reactions
- Support tickets (did new docs reduce them?)

**Ongoing**:
- Content engagement over time
- A/B test results (if applicable)
- User satisfaction (feedback widgets)

#### Set Up Alerts

```bash
# Example: Monitor for 404 errors with new URLs
# Set up monitoring in hosting platform or use services like:
# - UptimeRobot
# - Pingdom
# - StatusCake
```

---

### Step 10: Update Task Management

Mark publication complete:

1. **Update Task Status**: Mark task as "Finished"
2. **Add Completion Notes**:
   ```json
   "notes": "Published 2024-01-15. URL: https://docs.example.com/new-guide. Initial 24h views: 247."
   ```
3. **Run sync-tasks**: Update task-overview.md

---

## Rollback Procedure

If critical issues found after deployment:

### Quick Rollback

#### GitHub Pages
```bash
# Revert to previous commit
git checkout gh-pages
git revert HEAD
git push origin gh-pages
```

#### Netlify/Vercel
```bash
# Use dashboard to rollback to previous deploy
# Or revert commit and push
git revert HEAD
git push origin main
```

#### AWS S3
```bash
# Restore from S3 versioning
aws s3 cp s3://your-bucket-name/index.html s3://your-bucket-name/index.html --version-id VERSION_ID

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id ID --paths "/*"
```

### Rollback Decision Criteria

**Rollback immediately if**:
- Critical technical errors
- Security vulnerabilities exposed
- Broken site navigation
- Major factual errors
- Legal/compliance issues

**Fix forward (don't rollback) if**:
- Minor typos
- Small style issues
- Non-critical broken links
- Minor formatting problems

---

## Automation

### CI/CD Pipeline Example (GitHub Actions)

```yaml
# .github/workflows/publish-docs.yml
name: Publish Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Validate content
        run: |
          npx markdown-link-check 'docs/**/*.md'
          npx markdownlint 'docs/**/*.md'

      - name: Build docs
        run: mkdocs build --clean --strict

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force

      - name: Notify team
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK_URL }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"📚 Docs published: ${{ github.event.head_commit.message }}"}'
```

### Manual Publication Checklist

If not using automation, follow this checklist:

- [ ] Pre-publish validation (Step 1)
- [ ] Build documentation (Step 2)
- [ ] Local preview (Step 3)
- [ ] Deploy to staging (Step 4)
- [ ] Staging review completed
- [ ] Deploy to production (Step 5)
- [ ] Post-deployment verification (Step 6)
- [ ] Sitemap updated (Step 7)
- [ ] Announcement made (Step 8)
- [ ] Analytics configured (Step 9)
- [ ] Task updated (Step 10)

---

## Common Issues

### Build Fails

**Check**:
- Dependencies installed
- Configuration file syntax
- Image paths correct
- No broken internal links

### Deploy Succeeds But Content Not Visible

**Check**:
- Cache cleared (browser and CDN)
- Correct branch deployed
- File permissions on server
- Robots.txt not blocking

### Broken Links After Deploy

**Check**:
- Relative vs absolute paths
- Base URL configuration
- Renamed files
- URL structure changes

### Search Not Updated

**Wait**: Search reindexing can take hours to days
**Force Update**: Trigger manual reindex if available

---

## Customization

Adapt this command for your project:

1. **Choose Your Tools**: Update build commands for your doc generator
2. **Configure Deployment**: Set up your hosting platform steps
3. **Add Validation**: Include project-specific checks
4. **Set Notifications**: Configure team communication
5. **Automate**: Set up CI/CD for automatic publishing

---

## Output Location

**Published Content**: Production documentation site
**Deployment Log**: CI/CD logs or terminal output
**Task Update**: Mark task "Finished" with publication date and URL
