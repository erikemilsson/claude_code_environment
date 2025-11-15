# Citation Management Standards

## Purpose

This guide establishes standards for managing citations, references, and bibliographies in research projects. It covers citation styles, reference organization, in-text citation conventions, and bibliography maintenance.

## Citation Style Selection

### Choose Your Citation Style

Select based on your field and publication requirements:

| Style | Fields | Key Features |
|-------|--------|--------------|
| **APA** | Psychology, Education, Social Sciences | Author-date in-text, detailed reference list |
| **MLA** | Humanities, Literature, Arts | Author-page in-text, works cited page |
| **Chicago** | History, Business, Fine Arts | Footnotes/endnotes or author-date |
| **IEEE** | Engineering, Computer Science | Numbered in-text [1], numbered reference list |
| **Harvard** | Sciences, Social Sciences | Author-date in-text, reference list |
| **Vancouver** | Medicine, Health Sciences | Numbered in-text, numbered reference list |
| **ACS** | Chemistry | Numbered superscript, numbered references |

**Project Citation Style**: [Specify your chosen style here]

---

## In-Text Citation Formats

### APA Style (7th Edition)

**Single Author**:
- (Smith, 2023)
- Smith (2023) found that...

**Two Authors**:
- (Smith & Jones, 2023)
- Smith and Jones (2023) demonstrated...

**Three or More Authors**:
- (Smith et al., 2023)
- Smith et al. (2023) showed...

**Multiple Sources**:
- (Jones, 2022; Smith, 2023)
- Arranged alphabetically, separated by semicolons

**Direct Quote**:
- (Smith, 2023, p. 42)
- Smith (2023) stated, "quote here" (p. 42)

**No Author**:
- (Title of Work, 2023)

**No Date**:
- (Smith, n.d.)

### MLA Style (9th Edition)

**Single Author**:
- (Smith 42)
- Smith argues that "quote" (42)

**Two Authors**:
- (Smith and Jones 42)

**Three or More Authors**:
- (Smith et al. 42)

**No Page Number**:
- (Smith)

**Multiple Works Same Author**:
- (Smith, "First Title" 42)
- (Smith, "Second Title" 15)

### IEEE Style

**Single Reference**:
- [1]
- "As shown in [1], the method..."

**Multiple References**:
- [1], [3], [5]
- [1-3] for consecutive references

**Repeated Reference**:
- Use same number as first occurrence

### Chicago Style (Author-Date)

**Basic Format**:
- (Smith 2023, 42)
- Smith (2023) argues...

**Multiple Authors**:
- (Smith and Jones 2023)
- (Smith et al. 2023) for 4+ authors

**Multiple Works**:
- (Smith 2023; Jones 2022)

---

## Reference List Formats

### APA Reference Format

**Journal Article**:
```
Author, A. A., & Author, B. B. (Year). Title of article. Title of Periodical, volume(issue), page-page. https://doi.org/xxxxx
```

**Book**:
```
Author, A. A. (Year). Title of work: Subtitle. Publisher.
```

**Edited Book**:
```
Author, A. A. (Year). Chapter title. In B. B. Editor (Ed.), Book title (pp. xx-xx). Publisher.
```

**Website**:
```
Author, A. A. (Year, Month Day). Title of page. Site Name. https://url
```

**No Author**:
```
Title of work. (Year). Publisher.
```

### MLA Reference Format

**Journal Article**:
```
Author Last, First. "Article Title." Journal Title, vol. X, no. Y, Year, pp. XX-XX. DOI or URL.
```

**Book**:
```
Author Last, First. Book Title. Publisher, Year.
```

**Edited Book Chapter**:
```
Author Last, First. "Chapter Title." Book Title, edited by First Last, Publisher, Year, pp. XX-XX.
```

**Website**:
```
Author Last, First. "Page Title." Website Name, Day Month Year, URL. Accessed Day Month Year.
```

### IEEE Reference Format

**Journal Article**:
```
[1] A. A. Author and B. B. Author, "Article title," Journal Title, vol. X, no. Y, pp. XX-XX, Mon. Year.
```

**Book**:
```
[2] A. A. Author, Book Title, Edition. City, State: Publisher, Year.
```

**Conference Paper**:
```
[3] A. A. Author, "Paper title," in Conf. Name, City, State, Year, pp. XX-XX.
```

**Website**:
```
[4] A. A. Author. "Page title." Website Name. URL (accessed Mon. Day, Year).
```

---

## Reference Organization

### File Structure

```
research/
└── references/
    ├── library.bib              # Master bibliography file
    ├── pdfs/                    # Full-text PDFs
    │   ├── Smith2023.pdf
    │   └── Jones2022.pdf
    ├── notes/                   # Reading notes
    │   ├── Smith2023_notes.md
    │   └── Jones2022_notes.md
    └── searches/                # Search results
        └── database_export_2024-01-15.ris
```

### Naming Conventions

**PDF Files**: `FirstAuthorLastNameYear.pdf`
- Examples: `Smith2023.pdf`, `JonesEtAl2022.pdf`

**Notes Files**: `FirstAuthorLastNameYear_notes.md`
- Examples: `Smith2023_notes.md`

**Export Files**: `source_date.format`
- Examples: `pubmed_2024-01-15.ris`, `webofscience_2024-01-20.bib`

### Folder Organization by Project

For multi-project management:

```
references/
├── project-a/
│   ├── library.bib
│   └── pdfs/
├── project-b/
│   ├── library.bib
│   └── pdfs/
└── shared/
    ├── library.bib
    └── pdfs/
```

---

## Reference Management Tools

### Recommended Tools

**Zotero** (Recommended for most researchers):
- Free and open-source
- Excellent browser integration
- Collaborative collections
- BibTeX export
- Word/LibreOffice plugins

**Setup**:
1. Install Zotero desktop app
2. Install browser connector
3. Create collections for different projects
4. Enable auto-sync

**Workflow**:
1. Browse to paper online
2. Click Zotero browser button
3. Metadata and PDF auto-imported
4. Add tags and notes
5. Cite in Word/LibreOffice via plugin

**Mendeley**:
- PDF annotation features
- Cloud sync
- Academic social network
- Good for collaborative teams

**EndNote**:
- Comprehensive features
- Commercial (paid)
- Deep integration with Web of Science
- Good for large libraries (1000+ references)

**JabRef**:
- Free BibTeX manager
- Best for LaTeX users
- Cross-platform

### BibTeX for LaTeX Users

**BibTeX File Structure**:

```bibtex
@article{Smith2023,
  author = {Smith, John A. and Jones, Mary B.},
  title = {A Novel Approach to Data Analysis},
  journal = {Journal of Data Science},
  year = {2023},
  volume = {15},
  number = {3},
  pages = {234--256},
  doi = {10.1234/jds.2023.567}
}

@book{Johnson2022,
  author = {Johnson, Robert C.},
  title = {Statistical Methods in Research},
  publisher = {Academic Press},
  year = {2022},
  edition = {3rd},
  address = {New York, NY}
}
```

**Using in LaTeX**:

```latex
\documentclass{article}
\usepackage{cite}

\begin{document}

According to Smith and Jones \cite{Smith2023}, the method...
Statistical approaches are well documented \cite{Johnson2022}.

\bibliographystyle{plain}
\bibliography{library}

\end{document}
```

---

## Citation Workflow

### 1. During Literature Search

**As you find relevant papers**:
1. Import to reference manager immediately
2. Download full-text PDF
3. Add brief note: "Why this is relevant"
4. Tag with topic/theme keywords
5. Assign to project collection

**Search Tracking**:
- Keep log of searches performed
- Export search results from databases
- Store exports in `references/searches/`
- Document: database, date, search string, results count

### 2. During Reading

**For each paper**:
1. Read abstract first
2. If relevant, read full text
3. Take notes in reference manager or separate file
4. Extract key quotes with page numbers
5. Summarize main findings
6. Note methodology used
7. Tag with themes

**Note Template**:
```markdown
# [Author Year] - [Title]

## Summary
[One-paragraph summary]

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Methodology
[Brief description of methods]

## Relevance to My Research
[How this relates to my work]

## Key Quotes
> "Quote here" (p. XX)

## Limitations
[Any weaknesses or limitations noted]

## Citations to Follow Up
- Reference that looks interesting
```

### 3. During Writing

**Best Practices**:
1. Cite as you write (don't leave for later)
2. Use reference manager plugin for Word/Google Docs
3. For LaTeX, use `\cite{key}` commands
4. Keep bibliography file updated
5. Double-check citations before submission

**Avoiding Plagiarism**:
- Paraphrase in your own words
- Use quotes for exact language (with page numbers)
- Cite ideas even if not direct quotes
- When in doubt, cite

### 4. Before Submission

**Final Checks**:
- [ ] All in-text citations have reference entries
- [ ] All reference entries are cited in text
- [ ] Citation style consistent throughout
- [ ] DOIs included where available
- [ ] URLs functional (for web sources)
- [ ] Accessed dates for web sources
- [ ] Alphabetical or numerical order correct
- [ ] Formatting matches style guide exactly
- [ ] Author names spelled correctly
- [ ] Year matches across citation and reference

---

## Common Citation Scenarios

### Citing Multiple Works

**Supporting General Statement**:
```
Many studies have demonstrated this effect (Jones, 2020; Smith, 2021; Williams, 2022).
```

**Contrasting Views**:
```
While some researchers argue X (Smith, 2021), others suggest Y (Jones, 2022).
```

**Building on Prior Work**:
```
Building on the framework developed by Smith (2020), Jones (2021) extended the model to...
```

### Citing Secondary Sources

**Preferred**: Always find and cite the original source

**When Necessary**:
```
APA: Original Work as cited in Later Work (Year)
Example: Freud's work (as cited in Smith, 2023)

Reference list: Smith, A. (2023). Title...
[Only cite the secondary source you read]
```

### Citing Different Work Types

**Preprints**:
```
Author, A. A. (Year). Title [Preprint]. Repository. DOI or URL
```

**Datasets**:
```
Author, A. A. (Year). Dataset title (Version X) [Data set]. Repository. DOI
```

**Software**:
```
Author, A. A. (Year). Software title (Version X) [Computer software]. URL
```

**Conference Presentations**:
```
Author, A. A. (Year, Month). Title [Conference presentation]. Conference Name, Location.
```

**Personal Communication**:
```
(J. Smith, personal communication, January 15, 2024)
[Not included in reference list]
```

---

## Managing Large Numbers of References

### Organization Strategies

**By Project/Topic**:
- Create separate collections or folders
- Use tags for cross-cutting themes
- Example tags: "methodology", "theory", "empirical", "review"

**By Status**:
- "To Read"
- "Reading"
- "Read"
- "Important"
- "Cited in My Work"

**By Source Type**:
- Journal Articles
- Books
- Book Chapters
- Conference Papers
- Grey Literature

### Smart Tags

Use consistent tagging:
- **Topic**: "climate_change", "agriculture", "policy"
- **Method**: "qualitative", "RCT", "survey", "meta_analysis"
- **Population**: "children", "elderly", "professionals"
- **Status**: "to_read", "key_paper", "cited_in_intro"
- **Quality**: "high_quality", "seminal_work", "methodological_issues"

### Regular Maintenance

**Weekly**:
- Import new papers found
- Tag and organize imports
- Clean up duplicate entries

**Monthly**:
- Review "To Read" pile
- Update notes on papers read
- Clean up tags

**Before Submission**:
- Verify all cited papers are in library
- Check for duplicate entries
- Validate all DOIs and URLs
- Export final bibliography

---

## Best Practices

### Do's

1. **Import Immediately**: Add references as soon as you find them
2. **Download PDFs**: Attach full-text to reference entry
3. **Add Notes**: Brief summary of why it's relevant
4. **Tag Consistently**: Use predefined tags
5. **Cite While Writing**: Don't leave citations for later
6. **Backup Regularly**: Export library periodically
7. **Keep PDFs Organized**: Use consistent naming
8. **Update Metadata**: Fix errors when you spot them
9. **Use DOIs**: Include DOI when available
10. **Document Sources**: Note where you found the reference

### Don'ts

1. **Don't Procrastinate**: Don't wait to organize references
2. **Don't Rely on Memory**: Always save references immediately
3. **Don't Ignore Style Rules**: Follow citation style exactly
4. **Don't Cite Unseen Works**: Only cite what you've actually read
5. **Don't Forget Page Numbers**: For quotes, always include page
6. **Don't Mix Styles**: Be consistent within a document
7. **Don't Lose PDFs**: Keep organized, backed up
8. **Don't Skip Proofreading**: Check all citations before submission
9. **Don't Plagiarize**: Always attribute ideas to sources
10. **Don't Over-Cite**: Cite appropriately, not excessively

---

## Integration with Research Workflow

### Literature Review Phase

```
Find Paper → Import to Zotero → Tag "To Read"
    ↓
Read Paper → Take Notes → Tag with themes
    ↓
Extract Data → Update reference notes
```

### Writing Phase

```
Draft Section → Cite sources (via plugin)
    ↓
Auto-generate bibliography
    ↓
Continue writing
```

### Revision Phase

```
Check all citations → Verify reference list
    ↓
Fix formatting → Ensure style consistency
    ↓
Final check → All citations matched
```

---

## Troubleshooting Common Issues

### Problem: Duplicate Entries

**Solution**:
- Use reference manager's duplicate detection
- Merge duplicates, keeping most complete version
- Check before importing large batches

### Problem: Missing Information

**Solution**:
- Search for paper on Google Scholar
- Use DOI to find complete metadata
- Check publisher's website
- Add manually if needed

### Problem: Incorrect Formatting

**Solution**:
- Use reference manager's style selector
- Update citation style in document
- Manually fix edge cases
- Consult official style guide

### Problem: Broken URLs

**Solution**:
- Update to current URL
- Use DOI instead of URL when possible
- Check Wayback Machine for archived version
- Note if source no longer available

---

## Project-Specific Configuration

**Citation Style**: [e.g., APA 7th edition]

**Reference Manager**: [e.g., Zotero]

**Collections/Folders**:
- Main project library
- Background/literature review
- Methods papers
- Theoretical frameworks

**Tags Used**:
- [List your standard tags]

**Bibliography File**: `research/references/library.bib`

**PDF Location**: `research/references/pdfs/`

**Notes Location**: `research/references/notes/`

---

## Resources

### Official Style Guides
- **APA**: https://apastyle.apa.org/
- **MLA**: https://style.mla.org/
- **Chicago**: https://www.chicagomanualofstyle.org/
- **IEEE**: https://journals.ieeeauthorcenter.ieee.org/
- **AMA**: https://www.amamanualofstyle.com/

### Citation Generators
- Zotero
- Mendeley
- Citation Machine
- BibMe

### Citation Style Databases
- Citation Style Language (CSL): https://citationstyles.org/
- Zotero Style Repository: https://www.zotero.org/styles

### Guides and Tutorials
- Purdue OWL: https://owl.purdue.edu/
- Library guides from your institution
- Style guide quick reference sheets
