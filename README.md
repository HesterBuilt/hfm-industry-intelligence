# HFM Industry Intelligence

A free, custom-branded, static HTML news dashboard designed for embedding in Notion.

## Publish to GitHub Pages

1. Create a **public** GitHub repository named `hfm-industry-intelligence`. Do not upload private business information.
2. Upload `index.html`, `update_feeds.py`, `requirements.txt`, and the entire `.github/workflows/update-news.yml` folder structure. GitHub's **Add file > Upload files** may not preserve hidden folders reliably; the easiest option is to upload using GitHub Desktop or Git. Alternatively, create `.github/workflows/update-news.yml` in GitHub's web editor.
3. In repository **Settings > Actions > General**, set **Workflow permissions** to **Read and write permissions** if available (the workflow needs permission to commit `news.json`).
4. In **Actions > Update HFM news**, click **Run workflow** to populate `news.json`. Check the run succeeds.
5. In **Settings > Pages**, choose **Deploy from a branch**, branch `main`, folder `/(root)`, then save.
6. Wait for GitHub Pages to publish. Your URL will normally be `https://YOUR-GITHUB-USERNAME.github.io/hfm-industry-intelligence/`.
7. In Notion, type `/embed`, paste the published GitHub Pages URL, and choose **Embed link**. Make the embed wide enough to read.

## Operation

- GitHub Actions updates the feed about every six hours. Scheduled workflows may be delayed or disabled for inactive public repositories.
- `update_feeds.py` uses Google News RSS **searches**, which aggregate publishers rather than subscribing directly to every publisher named in earlier discussions. Source coverage and headlines are not guaranteed.
- The dashboard uses the generated `news.json`, so visitors don't need to fetch cross-origin RSS feeds.
- The site and generated news data are public. No API key or paid RSS.app subscription is required.
- To change the topics, edit the `QUERIES` dictionary in `update_feeds.py` and run the workflow again.
- If Google News blocks requests or changes its feed format, updates may fail. Existing news.json remains until the next successful update.
