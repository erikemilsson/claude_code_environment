# Phase 3: Analysis & Workshops (April - May Week 1)

## Overview
Analyze collected data, identify system constraints, and conduct stakeholder validation workshops.

## Critical Path Tasks

### Pre-Workshop Analysis (April Weeks 1-3)

1. **Factor Prioritization**
   - Calculate significance scores
   - Apply weighting (prevalence, impact, centrality)
   - Select top 150 barriers + 50 drivers
   - Validate selections

2. **Network Analysis**
   - Build causal links matrix
   - Calculate centrality metrics
   - Identify feedback loops
   - Find candidate constraints (3-5)

3. **Current Reality Tree (CRT) Development**
   - Map causal relationships
   - Create visual network
   - Identify root causes
   - Document logic chains

4. **Workshop Preparation**
   - Create presentation materials
   - Design voting mechanisms
   - Prepare breakout activities
   - Test technical setup
   - Send pre-read materials

### Workshop Execution (April Week 4 - May Week 1)

#### Workshop 1: Constraint Identification (April Week 4)
**Duration: 4 hours**

**Agenda:**
- 30 min: ToC introduction
- 45 min: Factor network presentation
- 90 min: Breakout groups - causal mapping
- 45 min: Core constraint consensus
- 30 min: Break

**Deliverables:**
- Validated CRT
- Identified core constraint
- Initial solution ideas

#### Workshop 2: Solution Development (May Week 1)
**Duration: 4 hours**

**Agenda:**
- 20 min: Constraint validation
- 60 min: Intervention brainstorming
- 90 min: Future Reality Tree building
- 40 min: Solution ranking
- 30 min: Next steps

**Deliverables:**
- Priority interventions
- Validated FRT
- Implementation roadmap

## Analysis Methods

### Constraint Identification Criteria
1. **System Impact**: Affects multiple value chain stages
2. **Bottleneck Effect**: Limits flow regardless of other improvements
3. **Root Cause**: Not just symptom of deeper issues
4. **Addressable**: Can be influenced through interventions

### Network Metrics
```python
# Key calculations
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
clustering = nx.clustering(G)
communities = nx.community.louvain_communities(G)
```

## Workshop Logistics

### Technical Requirements
- Video conferencing platform
- Online whiteboard (Miro/Mural)
- Real-time voting system
- Recording capability
- Backup communication channel

### Participant Management
- Send calendar invites 3 weeks prior
- Reminder 1 week before
- Pre-read materials 3 days before
- Technical test option day before
- Follow-up summary within 48 hours

## Checklist
- [ ] Factor prioritization complete
- [ ] Network analysis done
- [ ] 3+ constraint candidates identified
- [ ] CRT created and validated
- [ ] Workshop materials ready
- [ ] 15+ participants confirmed
- [ ] Technical setup tested
- [ ] Workshop 1 conducted
- [ ] Workshop 2 conducted
- [ ] Core constraint validated
- [ ] Primary intervention selected
- [ ] FRT completed

## Quality Assurance
- Minimum 15 workshop participants
- Representation from all stakeholder types
- Consensus score >70% on constraint
- Clear causal logic in trees
- Documented rationale for all decisions

## Commands to Run
```bash
# Note: The /run_analysis command has been deprecated
# These analyses should be performed manually:
# - Generate network analysis
# - Prepare workshop materials

# After workshops
python scripts/process_workshop_feedback.py
```

## Common Challenges
| Challenge | Mitigation |
|-----------|------------|
| Low workshop attendance | Have backup dates ready |
| Technical difficulties | Test systems, have IT support |
| No consensus reached | Use structured voting |
| Time overrun | Strict facilitation, parking lot |

## Files to Reference
- `/toc_methodology.md` - CRT/FRT construction
- `/data_collection_templates.md` - Workshop forms
- Network analysis outputs

## Time Estimate
- Factor prioritization: 8 hours
- Network analysis: 12 hours
- CRT development: 10 hours
- Workshop prep: 15 hours
- Workshop facilitation: 8 hours
- Post-workshop processing: 5 hours
- **Total: 58 hours**

## Outputs
- Validated Current Reality Tree
- Core system constraint identified
- Future Reality Tree with interventions
- Stakeholder consensus documentation
- Workshop recordings and notes

## Next Phase Trigger
When workshops complete and interventions validated, begin Phase 4: Results & Dissemination