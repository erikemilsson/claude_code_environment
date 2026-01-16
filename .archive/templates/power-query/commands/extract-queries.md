# Command: Extract Queries (Phase 0 - Step 4)

## Purpose
Guide user through extracting Power Query M code from Excel files and setting up watch mode.

## Prerequisites
- `generate-artifacts.md` has been run
- All Phase 0 artifacts exist
- Excel files in `excel-files/` directory
- Excel Power Query Editor extension installed in VS Code

## Phase 0 Progress

**BEFORE STARTING**: Display current progress from `.claude/tasks/_phase-0-status.md`

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 0 PROGRESS - Step 4 of 4 (Final Step!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Initialize Project        ✅  (Completed)
Step 2: Resolve Ambiguities       ✅  (Completed)
Step 3: Generate Artifacts        ✅  (Completed)
Step 4: Extract Queries           🔄  (Est. 10-15 min)

Starting Step 4: Extract Queries (Final Step)
Estimated time: 10-15 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Process

### 1. Verify Prerequisites
Check that required files exist:
- `.claude/context/glossary.md`
- `.claude/reference/data-contracts.md`
- `.claude/reference/query-manifest.md`
- `.claude/tasks/task-overview.md`

Check for Excel files in `excel-files/` directory.

If Excel Power Query Editor extension not installed, provide instructions to install.

### 2. Guide User Through Extraction

Present extraction instructions:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 0 - Step 4: Extract Power Query Code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Excel Files to Extract

Found [N] Excel file(s) in excel-files/:
- [file1.xlsx]
- [file2.xlsx]

## Extraction Steps

For EACH Excel file above:

### 1. Right-click the Excel file in VS Code Explorer
   - Navigate to: excel-files/[filename.xlsx]
   - Right-click on the file

### 2. Select "Extract Power Query from Excel"
   - This will extract all Power Query queries from the workbook
   - Files will be saved to the power-query/ directory
   - Each query becomes a separate .m file

### 3. Choose extraction location when prompted
   - Select: power-query/ (recommended)
   - This keeps all queries in one location

### Expected Output:
After extraction, you should see .m files in power-query/:
- [QueryName1].m
- [QueryName2].m
- ...

According to query-manifest.md, we expect [N] queries total.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏸️  PAUSE: Please perform the extraction steps above.

Once extraction is complete, respond with "Extraction complete" or let me know if you encountered any issues.
```

### 3. Wait for User Confirmation
User performs extraction manually using the VS Code extension.

### 4. Verify Extraction
After user confirms extraction, verify:

```
Checking extraction results...

Expected queries (from query-manifest.md):
- Bronze_Source_EmissionFactors
- Silver_Clean_EmissionFactors
- Gold_Calculate_CFF
[... list all expected queries]

Found in power-query/:
[List actual .m files found]

Status: [✅ All found / ⚠️ Missing queries / ❌ Extraction failed]
```

**If missing queries:**
- List which queries are missing
- Possible causes:
  - Queries might not exist in Excel file yet
  - Query names in Excel don't match expected names
  - Extraction location was different
- Suggest solutions

**If all queries found:**
- Proceed to watch mode setup

### 5. Set Up Watch Mode

Provide watch mode instructions:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Setting Up Auto-Sync (Watch Mode)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Watch mode automatically syncs changes from .m files back to Excel.

## Option A: Auto-Watch All Files (Recommended)

1. Open VS Code Settings (Ctrl+,)
2. Search for: excel-power-query-editor.watchAlways
3. Set to: true (check the box)
4. This will automatically watch all extracted .m files

## Option B: Manual Watch Per File

For each .m file you want to sync:
1. Right-click the .m file in VS Code Explorer
2. Select "Toggle Watch"
3. Watch icon (👁️) appears when active

## Verification

After setup, try this test:
1. Open any .m file in power-query/
2. Add a comment: // Test comment
3. Save the file (Ctrl+S)
4. Check the Excel file - it should update automatically

⚠️ Important Notes:
- Excel file must be CLOSED in Excel for sync to work
- Backup is created automatically before each sync
- Changes sync on file save

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏸️  PAUSE: Please set up watch mode using Option A or B.

Once configured, test with a small comment edit to verify sync works.
Respond with "Watch mode verified" when ready.
```

### 6. Wait for Watch Mode Confirmation
User sets up watch mode and verifies it works.

### 7. Prepare Git Commit

After verification, guide user on git commit:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Git Commit: Phase 0 Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 0 initialization is complete. Time to commit!

## Files to Commit

**Context Files:**
- .claude/context/glossary.md
- .claude/context/assumptions.md
- .claude/context/llm-pitfalls.md (if modified)
- .claude/context/overview.md

**Reference Files:**
- .claude/reference/data-contracts.md
- .claude/reference/query-manifest.md
- .claude/reference/dependency-graph.md
- .claude/reference/ambiguity-report.md

**Task Files:**
- .claude/tasks/task-overview.md
- .claude/tasks/task-*.json
- .claude/tasks/_phase-0-status.md

**Power Query Files:**
- power-query/*.m (all extracted queries)

**Project Files:**
- CLAUDE.md (updated with Phase 1 instructions)

## Suggested Commit Message

```
git add .claude/ power-query/ CLAUDE.md
git commit -m "Phase 0: Project initialization complete

- Resolved [N] ambiguities
- Generated glossary with [N] terms
- Created [N] data contracts
- Planned [N] queries (Bronze/Silver/Gold)
- Generated [N] initial tasks

Ready for Phase 1 task execution"
```

## Files to .gitignore

These should already be ignored (verify .gitignore):
- excel-files/*.xlsx (source Excel files)
- backups/ (extension backups)

.m files in power-query/ ARE tracked in git (source of truth).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8. Mark Phase 0 Complete

Update `.claude/tasks/_phase-0-status.md` with final completion:

```markdown
# Phase 0 Initialization Status

**Status:** ✅ COMPLETE
**Completed:** [Date]

## Progress
- [x] Initialize Project
- [x] Resolve Ambiguities ([N] batches)
- [x] Generate Artifacts
- [x] Extract Queries

## Extraction Summary
- Excel files processed: [N]
- Queries extracted: [N]
- Watch mode: ✅ Active
- Git commit: ✅ Ready

## Ready for Phase 1
All prerequisites complete. Project ready for task execution.

Next: Run `@.claude/commands/complete-task.md 1`
```

### 9. Final Summary

Present final summary to user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 Phase 0 Complete! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRESS:
Step 1: Initialize Project        ✅  (Completed)
Step 2: Resolve Ambiguities       ✅  (Completed)
Step 3: Generate Artifacts        ✅  (Completed)
Step 4: Extract Queries           ✅  (Completed in ~[X] min)

Total Phase 0 Time: ~[Total] minutes

INITIALIZATION SUMMARY:
📄 Documents Analyzed: [N]
❓ Ambiguities Resolved: [N]
📖 Terms Defined: [N]
📊 Queries Planned: [N]
✅ Tasks Generated: [N]
📁 .m Files Extracted: [N]
👁️  Watch Mode: Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your project is now fully initialized!

## What You Have

**Complete Context:**
- Every variable defined in glossary.md
- Every ambiguity resolved in assumptions.md
- Every query schema in data-contracts.md
- Complete dependency map in dependency-graph.md

**Ready to Code:**
- .m files extracted and ready to edit
- Auto-sync enabled (changes flow to Excel)
- Tasks broken down and prioritized
- Phase 1 workflow active in CLAUDE.md

## Next Steps

1. **Commit Phase 0 work** (see git instructions above)

2. **Start first task:**
   ```
   @.claude/commands/complete-task.md 1
   ```

3. **Claude will:**
   - Load all relevant context automatically
   - Implement query following specs
   - Validate against data contracts
   - Update task status
   - Auto-sync to Excel

## Tips for Phase 1

- Claude has COMPLETE context - no more ambiguity questions
- All variable names are standardized
- All schemas are defined
- Watch mode keeps Excel in sync
- Break down high-difficulty tasks (≥7) before starting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready when you are! 🚀

Run `@.claude/commands/complete-task.md 1` to begin.
```

## Output Files
- `.claude/tasks/_phase-0-status.md` - Final status
- `power-query/*.m` - Extracted query files
- Git ready for commit

## Troubleshooting

### Extension Not Found
```
⚠️ Excel Power Query Editor extension not detected.

Install from VS Code:
1. Press Ctrl+Shift+X (Extensions)
2. Search: "Excel Power Query Editor"
3. Install the extension by EWC3 Labs
4. Reload VS Code
5. Re-run this command
```

### Extraction Fails
```
❌ Extraction failed for [filename.xlsx]

Possible causes:
1. File is open in Excel (must be closed)
2. File is corrupted
3. File has no Power Query queries
4. File permissions issue

Solutions:
1. Close Excel completely
2. Check file can open normally in Excel
3. Verify file contains queries (Data > Queries & Connections)
4. Check file permissions
```

### Missing Queries
```
⚠️ Extracted [N] queries but expected [M]

Missing queries:
- [QueryName1]
- [QueryName2]

This might be normal if:
- Queries don't exist in Excel yet (will be created in Phase 1)
- Query names in Excel differ from expected names

Action: Review query-manifest.md and Excel file to reconcile.
```

### Watch Mode Not Working
```
⚠️ Watch mode sync test failed

Checklist:
1. Is Excel file closed? (Must be closed)
2. Is watch mode enabled? (Check for 👁️ icon)
3. Did you save the .m file? (Ctrl+S)
4. Check Output panel: "Excel Power Query Editor" for errors

If still failing:
- Toggle watch off and on again
- Restart VS Code
- Check extension settings
```

## Notes

- This is the final Phase 0 command
- After this, Phase 1 task execution begins
- User performs extraction manually (cannot be automated)
- Git commit marks Phase 0 boundary
- All future work uses extracted .m files as source of truth
