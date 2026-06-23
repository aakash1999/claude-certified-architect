# NotebookLM Generation Prompt

Generate a slide deck from this knowledge file for a YouTube bonus episode called "Exam Practice Questions & Tricks," part of the Claude Certified Architect Full Course Series. The tone is a warm, confident developer-educator talking directly to camera — plain layman's language, no unexplained jargon, contractions, short punchy sentences mixed with longer explanatory ones. This is a review-and-drill episode, not a new-concept episode, so the energy should feel like a coach running practice reps with a student before a big test: encouraging, a little playful, but taken seriously. Each slide heading below should become its own slide, used verbatim as the slide title. Speaker narration under each heading should read as flowing spoken narration, not bullet fragments — write it the way a person would actually talk it out loud. Preserve every ⚡ exam callout as a distinct emphasized moment in the narration, not buried in a paragraph.

---

## 1 · Can you actually pass?

You've sat through the entire Claude Certified Architect series — hooks, multi-agent coordinators, MCP tool design, CLAUDE.md hierarchies, structured output, context management, all of it. But here's the thing nobody tells you about exam day: the test doesn't ask you to recite facts back at it. It drops you into a scenario, gives you four answers that all sound reasonable, and makes you pick the one that's actually correct. That's a completely different skill from watching a video and nodding along.

So this bonus is pure reps. We're walking through all 12 official sample questions from the syllabus — not just the answers, but exactly why every wrong option is wrong, because that's what actually trains your pattern recognition. Then there are 4 brand-new practice questions covering ground the official syllabus never directly tests. And we'll close with the exam-day playbook — how to read a question, how to eliminate distractors fast, and how to manage your time.

⚡ This isn't "Episode 21" — the core 20-part series covering all five domains is already complete. Think of this as the final dress rehearsal before exam day.

## 2 · What's in this bonus

Four parts, building from recap to brand-new material. First, all 12 official sample questions, with a full breakdown of why the right answer wins and why each distractor loses, organized by domain. Second, 4 new practice questions covering scenarios the official 12 never directly tested, written specifically for this episode. Third, the 4 repeating distractor traps — once you can name the trap, the wrong answers stop looking tempting. And fourth, the exam-day playbook: time management, how to read a scenario, and the exact phrase to watch for that changes which answer is correct.

Try answering each question yourself before seeing the explanation — that's where the actual learning happens, not in reading someone else's reasoning.

## 3 · How the real exam actually works

Quick refresher before we drill, because this shapes how you should study. The passing score is 720 out of 1000 on a scaled score. Every question is multiple choice — one correct answer, three distractors. There are 6 total scenarios in the syllabus, and on any given sitting, the exam draws 4 of those 6 at random.

⚡ Here's the part people miss: you don't know which 4 of the 6 scenarios you'll get. That means you can't skip studying Scenario 4, Developer Productivity, or Scenario 6, Structured Extraction, just because the official 12 sample questions barely touch them. They're still fully in play on exam day, and we're fixing that gap later in this episode.

## 4 · Domain weighting = your study budget

If you're short on review time, spend it proportional to exam weight, not personal interest. Here's where the points actually live. Domain 1, Agentic Architecture and Orchestration, is 27 percent — the single biggest chunk of the exam. Domain 3, Claude Code Configuration, and Domain 4, Prompt Engineering and Structured Output, are tied at 20 percent each. Domain 2, Tool Design and MCP Integration, is 18 percent. And Domain 5, Context Management and Reliability, is 15 percent.

⚡ Domain 1 alone is over a quarter of your score. Domains 1, 3, and 4 combined are 67 percent of the exam. If your review time is limited, that's your priority order: multi-agent orchestration first, then Claude Code configuration and prompt engineering, then tool design, then context management last.

## 5 · The 4 distractor traps

Every single sample question, official and new, has at least one option built from one of these four traps. Learn to spot them and half the exam gets easier instantly.

Trap one: a prompt fix offered when enforcement is required. The scenario says a rule must never be violated, and the distractor offers "stronger wording" or "clearer instructions." Prompt instructions are always probabilistic — if the question demands a guarantee, the answer is code: a hook, a gate, a schema.

Trap two: an over-engineered answer to a "first step" question. Watch for the phrase "most effective first step." The correct answer is usually the cheapest, simplest fix, not the most complete one. A full architectural rebuild is rarely the right first step.

Trap three: infrastructure before optimization. A new routing layer, a new classifier, a new microservice, a new subagent — all offered before a much simpler fix, like better tool descriptions or scoped tool access, has even been tried.

Trap four: sentiment or self-confidence used as a decision signal. "Escalate when confidence drops below some percent" or "route based on detected frustration" — these are unreliable proxies. The exam consistently prefers explicit, observable criteria over a model's self-reported feelings about its own answer.

⚡ The one-line filter: when two options both seem plausible, ask "does this guarantee the outcome, or just make it more likely?" If the question uses words like must, never, or guarantee, the guarantee always wins.

## 6 · Domain 1 drills (Q1, Q7)

Two questions from the highest-weighted domain on the exam.

**Sample Q1.** A customer support agent uses get_customer, lookup_order, and process_refund. The system prompt says to always verify customer identity before processing any refund. Under high traffic, the agent occasionally calls process_refund before get_customer has returned a verified ID. The question: what's the most reliable approach to guarantee process_refund is never called without prior verification? The answer is a PreToolUse prerequisite gate in code that blocks process_refund unless get_customer has already returned a verified ID. Stronger prompt wording is still probabilistic, no matter how it's phrased — same failure mode. Few-shot examples improve consistency, not guaranteed compliance. And setting tool_choice to "any" only forces some tool call to happen, it has no control over sequence. ⚡ This is Trap 1 — a prompt fix offered when enforcement is required.

**Sample Q7.** A research coordinator decomposes "analyze the competitive landscape for EV batteries" into exactly three subagent tasks: battery chemistry, market share, and pricing. The final report completely omits regulatory policy and supply chain risk, even though the source documents discuss both at length. What's the root cause? It's that the coordinator's initial task decomposition was too narrow before any research even began. The fix is revising the decomposition step to include broader topic-coverage scoping. It's not a context window problem — the subagents that did run found plenty about their assigned sub-topics. It's not a communication problem either; letting subagents message each other directly breaks the hub-and-spoke model where everything routes through the coordinator for observability. And it's not a synthesis token limit, because that would show up as thin coverage of researched topics, not complete absence of topics that were never assigned at all. ⚡ Root cause first, then fix — never the reverse.

## 7 · Domain 2 drills (Q2, Q9)

**Sample Q2.** A customer support agent using four MCP tools — get_customer, lookup_order, process_refund, escalate_to_human — frequently escalates cases that should resolve automatically, and sometimes calls process_refund before verifying identity. All four tool definitions use single-sentence descriptions. What's the most effective first step? Expand the tool descriptions to include input formats, triggering conditions, prerequisites, and explicit "when not to use this tool" boundaries. The scenario hands you the root cause directly — single-sentence descriptions are the textbook cause of unreliable tool selection, and rewriting them is far lower effort than any architectural change. A tool-routing classifier is over-engineering before the cheap fix is tried. Few-shot examples help, but they're second-line. And splitting into four specialized subagents is the most expensive possible response to a description-quality problem. ⚡ Trap 2 — over-engineered fix to a "first step" question.

**Sample Q9.** In a multi-agent research system, the synthesis agent — whose only job is combining already-gathered findings into a final report — has access to every system tool: web_search, document_analysis, lookup_database, and a new verify_fact tool. Synthesis quality is dropping because the agent sometimes triggers fresh web searches mid-synthesis instead of finishing the report. The fix is scoping the synthesis agent's tool access down to only verify_fact, removing the search and database tools, since synthesis verifies existing findings rather than gathering new data. Better descriptions don't fix a structural overreach — the agent shouldn't have search capability available to reach for at all. Forcing a tool call every turn doesn't address which tools are available in the first place. And spawning a subagent for a single verification call is unnecessary indirection. ⚡ Trap 3 — added infrastructure before the simple scoping fix.

## 8 · Domain 3 drills A (Q4, Q5)

**Sample Q4.** A team wants a custom slash command, /review-pr, that every developer automatically gets the moment they clone the repository, no manual per-person setup. Where should it live? In .claude/commands/ in the project root, committed to version control. That's project-scoped and shared automatically with every clone. The personal commands folder in a developer's home directory is exactly the opposite of what's wanted. A note in CLAUDE.md is documentation, not an actual invokable command. And a shell alias isn't a Claude Code construct at all. ⚡ User-level is personal, project-level is shared via version control.

**Sample Q5.** A developer asks Claude Code to migrate a 40,000-line monolithic order-processing module into three separate microservices, with no pre-defined service boundaries. Should this be plan mode or direct execution? Plan mode — because multiple valid service-boundary decisions exist, the change spans many files, and getting it wrong is costly to undo. Saying the task is "well-defined enough" for direct execution ignores that the boundaries are explicitly undefined, which is the entire complexity of the task. Requiring permission before every file write adds friction without surfacing the actual architectural decision. And spawning three parallel subagents immediately doesn't work when the boundaries between those three services haven't even been decided yet. ⚡ Plan mode is for architectural, multi-file work with multiple valid approaches.

## 9 · Domain 3 drills B (Q6, Q10)

**Sample Q6.** One repo holds Terraform infrastructure code and a React frontend. The team wants strict infra security-review rules applied only when touching terraform paths, and separate testing conventions applied only when touching test files, without cluttering CLAUDE.md with irrelevant rules. The answer is creating separate rule files inside .claude/rules/ with YAML frontmatter paths fields, so each rule loads conditionally by file pattern. Putting everything in root CLAUDE.md means it's always loaded with no conditional scoping. Directory-level CLAUDE.md files are scoped by physical location, not by glob pattern, so they don't match a repo-wide test-file pattern. And @import loads its target unconditionally every time — no path-based gating. ⚡ .claude/rules/ plus frontmatter paths is conditional loading by file pattern.

**Sample Q10.** A team wires Claude Code into GitHub Actions to auto-review every pull request. The first CI run hangs indefinitely and the job times out. The fix is adding the -p, or --print, flag to run Claude Code in non-interactive mode so it doesn't wait for terminal input. CLAUDE_HEADLESS as an environment variable doesn't exist. A --batch flag doesn't exist either — it's a fabricated-sounding distractor. And increasing the CI timeout changes nothing, because the job isn't running slowly, it's waiting indefinitely for interactive input that will never arrive. ⚡ Watch for confidently-named flags that simply don't exist.

## 10 · Domain 4 drills (Q11, Q12)

**Sample Q11.** A team wants to move all of their Claude workloads onto the Message Batches API for the 50 percent cost savings, including a pre-merge CI check that currently blocks every pull request until review feedback comes back. What's wrong with this plan? The Batch API has no guaranteed latency SLA — results can take up to 24 hours — which makes it appropriate for overnight or non-blocking workloads, but fundamentally wrong for a blocking pre-merge check that needs a real-time response. It's not that the Batch API behaves identically to the standard API at a lower price; the savings come specifically from relaxing that latency guarantee. There's no content restriction on PR-related prompts. And there's no priority flag that lets you skip the queue. ⚡ Batch means cheaper and no latency SLA — never both speed and savings.

**Sample Q12.** A code review agent reviews a 14-file pull request in a single prompt, one pass. Quality is inconsistent, and cross-file issues — like a renamed function breaking a caller elsewhere — are frequently missed. The most effective restructuring is splitting into focused per-file review passes, followed by a separate cross-file integration pass that specifically checks for cross-references. Increasing max_tokens doesn't help because output length isn't the bottleneck — consistency of attention across a large input is. Adding a "be thorough" instruction is the same vague-instruction trap as a vague "be conservative" instruction. And having the same agent review the PR twice and average the findings doesn't help, because self-review retains the same reasoning context across both passes — it's less effective than an independent review. ⚡ Split by aspect, not by re-running the same pass twice.

## 11 · Domain 5 drills (Q3, Q8)

**Sample Q3.** A support agent generates a self-reported confidence score after each resolution attempt, escalating to a human whenever that score drops below 70 percent. Some easily-resolvable cases get escalated needlessly, while some genuinely complex billing disputes don't get escalated and get resolved incorrectly. The fix is replacing the confidence-score threshold with explicit, observable escalation criteria: the customer explicitly requests a human, the case falls into a known policy gap or exception, or the agent can't make progress after a defined number of attempts. Lowering the threshold from 70 to 50 percent is still the same unreliable proxy at a different number. Averaging two self-reported confidence scores together is still two self-reported confidence scores. And removing escalation entirely throws out a genuinely necessary safety valve. ⚡ Trap 4 — confidence score used as a decision signal.

**Sample Q8.** A document-analysis subagent sometimes fails to retrieve a document due to a network timeout, and sometimes retrieves it fine but finds no relevant information inside. Today both cases return the exact same empty result to the coordinator, which sometimes wrongly reports "no information found" when the real issue was a retrievable network failure. The fix is returning structured error context that distinguishes failure type — a transient failure versus a genuinely valid empty result — including what was attempted and whether a retry makes sense, so the coordinator can decide intelligently. Silent retries hide the failure signal from the coordinator entirely. Terminating on a single failure overreacts to something that might resolve on retry. And assuming any empty result means no information exists is literally the bug being described. ⚡ Two anti-patterns to remember: suppress silently, or terminate on one failure.

## 12 · The coverage gap

The official syllabus gives you 12 sample questions, but look closely at which scenarios they actually cover. Scenario 1, Customer Support, gets questions 1, 2, and 3. Scenario 2, Code Generation, gets questions 4, 5, and 6. Scenario 3, Multi-Agent Research, gets questions 7, 8, and 9. Scenario 5, CI/CD, gets questions 10, 11, and 12. But Scenario 4, Developer Productivity, and Scenario 6, Structured Extraction, get none.

⚡ Remember, the real exam draws 4 of all 6 scenarios at random. If you only drilled the 12 official questions, you've effectively skipped studying for two-sixths of the possible draw. So here are four new questions written for this bonus: two close the Scenario 4 and Scenario 6 gaps directly, and two more hit Scenarios 3 and 5 again from a fresh angle, because those two carry the most exam weight and the densest trap patterns.

## 13 · Extraction trap

**New Practice Q1.** An extraction pipeline pulls structured fields — vendor name, invoice amount, due date, line items — from scanned invoices using tool_use with a strict JSON schema. On a fresh batch, validation fails on 4 percent of documents: the model returns syntactically valid JSON, but the due_date field is fabricated — a plausible-looking date that doesn't actually appear anywhere in the source document. The team's current fix is a retry loop that resubmits the document on every validation failure. Will more retries fix this? No. Retries fix structural and syntax errors, not missing information. The model isn't fabricating the date due to a formatting mistake — there's simply no due date visible in this scan. The right fix is making the field nullable, so the model can return null instead of inventing a value, and routing those documents to human review. Raising the retry count doesn't help, because more attempts at an impossible task produce the same fabrication risk each time. Repeating the JSON schema improves schema compliance, not data that isn't present in the source. And lowering max_tokens is an unrelated lever that doesn't stop the model from inventing a value for a required field. ⚡ Retry fixes format errors, never missing information.

## 14 · Codebase exploration

**New Practice Q2.** A developer asks Claude Code to find where user authentication happens inside a 200,000-line legacy monorepo it has never seen before. Claude starts by calling Read on every Python file in the repository, one at a time, to build a mental model before answering. What's the better approach? Use Grep to search file contents for authentication-related terms first, to narrow candidate files, then Glob to confirm relevant file patterns, then Read only the specific files that surface. Incremental exploration beats bulk reading. A common mix-up here: Glob matches file paths and names by pattern, it does not search inside file contents — that keyword-search job belongs to Grep. Reading the entire repo in one batch burns context budget on overwhelmingly irrelevant files. And using the Edit tool to insert debug logging is wildly overengineered for an exploration question, plus Edit requires unique anchor text per file, which doesn't scale across an unknown codebase. ⚡ Grep is for contents, Glob is for paths and names, and incremental beats bulk.

## 15 · Parallel subagents

**New Practice Q3.** A coordinator needs three subagents to research three independent sub-topics ahead of a synthesis pass. The current implementation has the coordinator call the Task tool once, wait for that subagent's full result, then call Task again for the second subagent, then again for the third — one full turn at a time, in sequence. What's wrong with this? It isn't actually parallel execution. True parallel subagent spawning means emitting multiple Task tool calls within a single coordinator response, not issuing them across separate sequential turns. Spread across separate turns, each subagent runs to completion before the next one even starts, which is sequential no matter the intent. It's not that Task calls are inherently parallel regardless of turn count — execution order follows how the loop actually runs. Adding individual subagent tool names to the coordinator's allowedTools list is unrelated to the sequencing issue, and it breaks the model where the coordinator alone owns Task. And letting the three subagents message each other directly is a named anti-pattern that breaks the coordinator's observability and error-handling responsibility. ⚡ Parallel means multiple Task calls in one response, not multiple turns.

## 16 · False positives

**New Practice Q4.** An automated PR review agent flags too many false positives. The team's first fix was a system prompt instruction: only flag issues you're highly confident about, be conservative in your reporting. The false positive rate barely moves, and developers now ignore the bot's comments across every issue category, including the genuinely useful security and correctness flags. What should the team do instead? Replace the vague confidence instruction with explicit categorical criteria specifying exactly which issue types to report versus skip, and temporarily disable the specific high-false-positive category entirely rather than lowering the overall threshold. Lowering the temperature setting makes flagging more deterministic, but determinism isn't precision — a model consistently wrong in the same category is still wrong, just more predictably. Adding the word "strict" before "conservative" is the same vague-instruction trap with louder wording. And disabling the bot entirely overreacts to a fixable category-specific problem by throwing away a tool that's still doing good work elsewhere. ⚡ Being conservative never improves precision — explicit criteria does.

## 17 · Exam-day tactics

Six habits that matter more than any single fact you've memorized. Read the scenario setup twice — it tells you exactly which tools and constraints exist, and most distractors only reveal themselves as wrong once you re-read the setup carefully. Trace symptom to root cause to fix, in that order — don't jump straight to "what's the fix," or you'll pick an answer that treats the wrong problem. Remember that "most effective first step" is not "most complete solution" — when you see that phrase, eliminate any option that does more than the symptom actually requires. Guarantee beats probability — whenever a question uses must, never, or guarantee, code-level enforcement beats prompt-level wording every time. Watch for fabricated-sounding specifics — confidently-named flags, environment variables, or parameters that don't actually exist are a recurring distractor pattern. And flag and move on — don't let one hard question burn your pacing for the rest of the exam, you can always come back to it.

## 18 · One-page cheat sheet

Domain priority by weight: Agentic Architecture at 27 percent first, then Claude Code Configuration and Prompt Engineering tied at 20 percent each, then Tool Design and MCP at 18 percent, then Context and Reliability at 15 percent.

The 4 distractor traps: a prompt fix offered for a must-never rule, an over-engineered fix to a "first step" question, new infrastructure offered before a cheap fix is tried, and sentiment or confidence used as a decision signal.

Scenario coverage map: all 6 scenarios are in play on exam day — the official 12 questions only directly tested 4 of them. Scenarios 4, Developer Productivity, and 6, Structured Extraction, got their first direct practice questions right here in this bonus.

The one-line filter: does this guarantee the outcome, or just make it more likely? Guarantees win whenever the question says must, never, or guarantee.

## 19 · Go get certified

If you've made it through all 20 episodes and every drill in this bonus, you're not just exam-ready — you actually understand how these systems fail in production, which was the whole point from episode one. Twelve official questions, fully broken down. Four brand-new questions closing the gaps the syllabus left open. The trap patterns that show up over and over. You've got everything you need.

Drop a comment with whichever question tripped you up — that's the one worth reviewing again before exam day. And if this series helped you get here, a like genuinely helps it reach the next developer starting their own certification journey.

Good luck on exam day. You've earned it.

---

## Glossary

**Prerequisite gate** — a PreToolUse hook that blocks a tool call until a required prior tool call has succeeded, tracked via session state. Code-level, not prompt-level.

**Tool scoping** — restricting an agent's available tools to only what its specific role requires, rather than giving every agent access to every tool in the system.

**Structured error context** — an error response that distinguishes failure type (e.g. transient vs. permanent vs. valid-empty) so a coordinator can make an intelligent recovery decision, instead of receiving a generic failure signal.

**Nullable field** — a schema field allowed to return null instead of forcing the model to fabricate a plausible-looking value when the real value is genuinely absent from the source.

**Parallel subagent spawning** — emitting multiple Task tool calls within a single coordinator turn, as opposed to issuing them one at a time across separate sequential turns.

**Categorical criteria** — explicit, concrete rules about which issue types to flag versus skip, as opposed to a vague confidence-based filtering instruction like "be conservative."

## Task Statement Mapping

| Question | Domain | Task | Scenario |
|---|---|---|---|
| Sample Q1 | 1 | 1.4 | 1 |
| Sample Q2 | 2 | 2.1 | 1 |
| Sample Q3 | 5 | 5.2 | 1 |
| Sample Q4 | 3 | 3.2 | 2 |
| Sample Q5 | 3 | 3.4 | 2 |
| Sample Q6 | 3 | 3.3 | 2 |
| Sample Q7 | 1 | 1.2 | 3 |
| Sample Q8 | 5 | 5.3 | 3 |
| Sample Q9 | 2 | 2.3 | 3 |
| Sample Q10 | 3 | 3.6 | 5 |
| Sample Q11 | 4 | 4.5 | 5 |
| Sample Q12 | 4 | 4.6 | 5 |
| New Practice Q1 | 4/5 | 4.4, 5.6 | 6 |
| New Practice Q2 | 2 | 2.5 | 4 |
| New Practice Q3 | 1 | 1.3 | 3 |
| New Practice Q4 | 4 | 4.1 | 5 |

---

*Knowledge file for: Bonus — Exam Practice Questions & Tricks*
*Series: Claude Certified Architect Full Course Series*
*Headings above match the HTML carousel script verbatim, slide for slide.*
