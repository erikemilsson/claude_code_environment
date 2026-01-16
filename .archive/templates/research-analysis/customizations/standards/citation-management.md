# Citation Management Standards

## Overview

This document defines standards for tracking, formatting, and managing citations throughout the research process. Proper citation management ensures academic integrity, gives credit to original authors, and enables readers to locate source materials.

## Citation Formats

### Major Citation Styles

#### APA (American Psychological Association)

**Common in**: Psychology, Education, Social Sciences

**Book**:
```
Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.
```
Example: Kahneman, D. (2011). Thinking, fast and slow. Farrar, Straus and Giroux.

**Journal Article**:
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Title of Periodical, volume(issue), pages. https://doi.org/xx.xxx/yyyy
```
Example: Smith, J. A., & Johnson, M. B. (2020). Effects of mindfulness on anxiety. Journal of Clinical Psychology, 76(4), 543-558. https://doi.org/10.1002/jclp.22901

**In-Text Citation**:
- Narrative: Smith and Johnson (2020) found that...
- Parenthetical: ...has been demonstrated (Smith & Johnson, 2020).
- Multiple authors (3+): (Smith et al., 2020)

#### MLA (Modern Language Association)

**Common in**: Humanities, Literature, Arts

**Book**:
```
Author Last Name, First Name. Title of Book. Publisher, Year.
```
Example: Woolf, Virginia. Mrs. Dalloway. Harcourt Brace, 1925.

**Journal Article**:
```
Author Last Name, First Name. "Title of Article." Title of Journal, vol. number, no. number, Year, pages.
```
Example: Peterson, Nancy J. "Against Negro Folklore: Morrison and the Voices of Toni Morrison's Fiction." American Literature, vol. 82, no. 2, 2010, pp. 289-314.

**In-Text Citation**:
- (Author Page): (Woolf 23)
- Multiple authors: (Smith and Jones 45)

#### Chicago/Turabian

**Common in**: History, Some Social Sciences

**Two Systems**:
1. **Notes-Bibliography** (humanities): Footnotes/endnotes + bibliography
2. **Author-Date** (sciences): In-text citations + reference list

**Book (Notes-Bibliography)**:
```
Footnote: First Name Last Name, Title of Book (Place: Publisher, Year), page.
Bibliography: Last Name, First Name. Title of Book. Place: Publisher, Year.
```

**Book (Author-Date)**:
```
Last Name, First Name. Year. Title of Book. Place: Publisher.
```

#### IEEE

**Common in**: Engineering, Computer Science

**In-Text**: [1], [2], [3] (numbered in order of appearance)

**Reference**:
```
[1] A. A. Author, "Title of article," Abbrev. Title of Periodical, vol. x, no. x, pp. xxx-xxx, Abbrev. Month, Year.
```
Example: [1] J. Smith and M. Jones, "Machine learning approaches to data analysis," IEEE Trans. Pattern Anal. Mach. Intell., vol. 42, no. 3, pp. 512-528, Mar. 2020.

#### Vancouver

**Common in**: Medical and Biological Sciences

**In-Text**: (1), (2), (3) or superscript¹,²,³

**Reference**:
```
1. Author AA, Author BB. Title of article. Abbreviated Journal Title. Year;volume(issue):pages.
```
Example: 1. Smith J, Johnson M. Effects of intervention on outcomes. J Clin Med. 2020;15(3):234-245.

### Choosing a Citation Style

**Factors**:
- Discipline conventions
- Journal/publisher requirements
- Institutional guidelines
- Advisor/committee preferences

**Consistency**: Use one style throughout a document.

## Reference Managers

### Zotero

**Pros**:
- Free and open-source
- Excellent browser integration
- Group libraries for collaboration
- Active development community

**Setup**:
1. Download from zotero.org
2. Install browser connector
3. Create account for syncing
4. Install word processor plugin

**Workflow**:
- Click browser icon to save citation
- Organize into collections
- Add notes and tags
- Cite while writing using plugin
- Generate bibliography

**Tips**:
- Use meaningful collection names
- Tag papers by theme, methodology, or status
- Sync across devices
- Back up regularly (export library)

### Mendeley

**Pros**:
- Free (Elsevier-owned)
- PDF annotation tools
- Social features (discover related papers)
- Mobile app

**Limitations**:
- Storage limits on free tier
- Privacy concerns (owned by publisher)
- Less flexible than Zotero

### EndNote

**Pros**:
- Professional features
- Excellent for large libraries
- Strong institutional support

**Cons**:
- Expensive (unless institutional license)
- Steeper learning curve

### BibTeX

**For**: LaTeX users

**Workflow**:
1. Create `.bib` file with entries
2. Cite in LaTeX: `\cite{key}`
3. Compile with bibliography style

**Example Entry**:
```bibtex
@article{smith2020effects,
  title={Effects of mindfulness on anxiety},
  author={Smith, John A and Johnson, Mary B},
  journal={Journal of Clinical Psychology},
  volume={76},
  number={4},
  pages={543--558},
  year={2020},
  publisher={Wiley}
}
```

## Organization Strategies

### Folder/Collection Structure

**By Project**:
```
Research Library
├── Dissertation
│   ├── Chapter 1: Introduction
│   ├── Chapter 2: Literature Review
│   ├── Chapter 3: Methods
│   └── Chapter 4: Results
├── Side Project A
└── Course Papers
```

**By Topic**:
```
Research Library
├── Cognitive Psychology
│   ├── Attention
│   ├── Memory
│   └── Decision Making
├── Research Methods
│   ├── Experimental Design
│   └── Statistical Analysis
└── To Read
```

**By Status**:
```
Research Library
├── Reading Queue
├── Currently Reading
├── Read - Key Papers
├── Read - Background
└── Cited in My Work
```

### Tagging Systems

**Methodological Tags**:
- `#RCT`, `#meta-analysis`, `#qualitative`, `#longitudinal`

**Content Tags**:
- `#theory`, `#empirical`, `#review`, `#methods-paper`

**Quality Tags**:
- `#high-quality`, `#seminal-paper`, `#critique-this`

**Project Tags**:
- `#dissertation`, `#paper1`, `#grant-proposal`

**Status Tags**:
- `#to-read`, `#reading`, `#read`, `#cited`

### Note-Taking in Reference Managers

**What to Record**:
- Brief summary (2-3 sentences)
- Key findings or arguments
- Relevant quotes (with page numbers)
- Methodology notes
- How it relates to your work
- Critiques or limitations

**Template**:
```markdown
## Summary
[2-3 sentence overview]

## Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Methodology
[Study design, sample, measures, analysis]

## Relevance to My Work
[How this paper connects to your research]

## Important Quotes
"Quote text" (p. 123)

## Critiques/Limitations
[Issues with the paper or areas for future research]
```

## Citation Workflow

### 1. Search and Import

**From Databases**:
- PubMed: Export as RIS or use PMID
- Google Scholar: Click "Cite" → Import to reference manager
- Web of Science: Export selected records

**From Browser**:
- Use reference manager browser extension
- One-click save of web pages, articles, books

**Manual Entry**:
- Use when import fails or for unusual sources
- Include DOI if available

### 2. Organize

- Move to appropriate collection/folder
- Add tags for categorization
- Check that all fields are complete
- Attach PDF if available

### 3. Read and Annotate

- Read paper
- Highlight key passages in PDF
- Add notes in reference manager
- Update tags (e.g., add `#read`)

### 4. Cite While Writing

**Word Processor Plugins**:
- Zotero: Insert Citation button
- Mendeley: Insert Citation from toolbar
- EndNote: Insert Citation from ribbon

**LaTeX**:
```latex
\documentclass{article}
\usepackage[style=apa]{biblatex}
\addbibresource{references.bib}

\begin{document}
Research shows \cite{smith2020effects} that...

\printbibliography
\end{document}
```

**Markdown/Pandoc**:
```markdown
Research shows [@smith2020effects] that...

# References
```

Compile with: `pandoc file.md --citeproc --bibliography=refs.bib -o output.pdf`

### 5. Generate Bibliography

- Select citation style
- Insert bibliography at end of document
- Verify formatting
- Check for missing references

### 6. Verify and Clean

**Check**:
- All in-text citations have reference list entry
- All reference list entries are cited in text (or remove)
- Formatting is consistent
- DOIs are included where available
- Page numbers are correct

## Common Issues and Solutions

### Issue 1: Incorrect Metadata

**Problem**: Imported citation has wrong author, title, or year

**Solution**:
- Manually correct in reference manager
- Check against original source
- Update will propagate to citations

### Issue 2: Duplicate Entries

**Problem**: Same paper imported multiple times

**Solution**:
- Use reference manager's duplicate detection
- Merge duplicates, keeping most complete entry
- Be careful with different editions or versions

### Issue 3: Missing DOI or Full-Text

**Problem**: Reference lacks DOI or attached PDF

**Solutions**:
- Use Zotero's "Find Available PDF" feature
- Search publisher website for DOI
- Use Sci-Hub or institutional access for PDF (where legal)
- Use CrossRef or Google Scholar to find DOI

### Issue 4: Citation Style Not Available

**Problem**: Needed style not in reference manager

**Solution**:
- Zotero: Browse Zotero Style Repository (>10,000 styles)
- EndNote: Import from EndNote website
- Create custom style (advanced)

### Issue 5: Collaboration Challenges

**Problem**: Sharing references with co-authors

**Solutions**:
- Zotero Groups (shared online library)
- Export and share `.bib` or `.ris` file
- Cloud-synced folder with reference manager library
- Shared Mendeley group library

## Best Practices

### 1. Cite as You Write

Don't wait until the end to add citations. Insert them while drafting.

### 2. Back Up Your Library

**Strategies**:
- Cloud sync (Zotero, Mendeley)
- Regular exports to `.bib` or proprietary format
- Version control for `.bib` files (Git)
- Institutional or cloud storage backup

### 3. Maintain Consistency

- Use one reference manager per project
- Stick to one citation style per document
- Be consistent with author name format (e.g., always include middle initials or never)

### 4. Include All Necessary Information

**For Every Citation**:
- Author(s)
- Year
- Title
- Source (journal, book, website)
- Volume, issue, pages (for articles)
- DOI (whenever available)
- URL and access date (for web sources)

### 5. Verify Publisher Requirements

Before submission:
- Check journal/publisher citation guidelines
- Verify required citation style
- Check if DOIs are required
- Ensure reference list formatting matches examples

### 6. Cite Primary Sources

Whenever possible, cite the original source rather than a paper that cited it.

**Avoid**: Smith (2020) found that [according to Jones (2022)]
**Better**: Read Smith (2020) and cite it directly

### 7. Keep Track of "To Read" Items

Maintain a queue of papers to read. Don't let it become overwhelming.

### 8. Use Notes for Your Future Self

Your notes should be detailed enough that you can understand the paper months later without re-reading it.

## Ethical Considerations

### Plagiarism

**Definition**: Using others' words or ideas without attribution

**Forms**:
- Direct copying without quotes and citation
- Paraphrasing without citation
- Using others' ideas without credit

**Prevention**:
- Always cite sources of ideas and information
- Use quotation marks for exact wording
- Paraphrase in your own words + cite
- Cite even for "common knowledge" in your field if unsure

### Self-Plagiarism

**Issue**: Reusing your own previously published work without disclosure

**Examples**:
- Submitting same paper to multiple journals
- Copying text from your previous publications
- Splitting one study into multiple papers ("salami slicing")

**Acceptable**:
- Building on your previous work (with citation)
- Reusing your methods section with disclosure
- Conference proceeding → full journal article (with disclosure)

### Citation Manipulation

**Unethical Practices**:
- Excessive self-citation to boost metrics
- Citing only friends/colleagues
- Citation rings (mutual citation agreements)
- Citing papers you haven't read

**Ethical Practice**:
- Cite what's relevant and important
- Include papers that disagree with you
- Give credit to originators of ideas
- Only cite what you've actually read

## Advanced Topics

### Citation Searching

**Find Papers That Cite a Key Work**:
- Google Scholar: "Cited by" link
- Web of Science: Citation report
- Scopus: Cited by feature

**Use Case**: Find recent papers building on seminal work

### Citation Network Analysis

Visualize relationships between papers:
- Connected Papers
- Citation Gecko (Zotero plugin)
- VOSviewer (bibliometric software)

### Systematic Review Citation Tracking

**PRISMA Guidelines** for reporting:
- Search strategy with all databases and terms
- Number of records identified, screened, included
- Reasons for exclusions
- Flow diagram

### Pre-Prints and Grey Literature

**Pre-prints** (arXiv, bioRxiv, PsyArXiv):
- Cite as: Author, A. A. (Year). Title. *Pre-print repository*. URL

**Theses/Dissertations**:
- Cite with university and degree type

**Conference Proceedings**:
- Include conference name, location, dates

**Technical Reports**:
- Include organization and report number

## Tools and Resources

### Citation Style Resources
- Purdue OWL (APA, MLA, Chicago guides)
- Citation Style Language (CSL) repository
- Journal-specific author guidelines

### Reference Manager Resources
- Zotero Documentation and Forums
- Mendeley Support Center
- EndNote Training Videos

### Citation Metrics
- Google Scholar Citations (author profiles, h-index)
- Web of Science (impact factors)
- Altmetric (social media attention)

### Plagiarism Detection
- Turnitin (institutional)
- iThenticate (pre-submission check)
- Grammarly plagiarism checker
- Quetext (free option)

## Documentation Template

Create `research/citations/citation-log.md`:

```markdown
# Citation Management Log

## Reference Manager
**Software**: Zotero 6.0
**Database Location**: ~/Zotero/
**Last Backup**: 2025-11-10
**Number of Items**: 342

## Citation Style
**Primary Style**: APA 7th edition
**Style File**: apa.csl
**Justification**: Required by target journal

## Organization Structure
- Collections: By project and chapter
- Tags: Methodology, content area, status
- Groups: Shared library with collaborators (link)

## Import Sources
- PubMed (primary database)
- PsycINFO (secondary database)
- Google Scholar (supplementary)
- Hand searches of key journals

## Review Status
- Total papers in library: 342
- Read and annotated: 215
- To read: 87
- Cited in current manuscript: 64

## Backup Schedule
- Daily: Automatic cloud sync (Zotero server)
- Weekly: Manual export to .bib file
- Monthly: Full library backup to external drive
```

## Integration with Writing Workflow

1. **Reading Phase**: Import → Organize → Read → Annotate
2. **Writing Phase**: Insert citations as you write
3. **Revision Phase**: Check all citations, remove unused
4. **Submission Phase**: Verify style, format bibliography
5. **Post-Publication**: Add your paper to library, note who cited you
