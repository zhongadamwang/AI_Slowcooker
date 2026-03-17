/**
 * EDPS Enhanced NLP - Core Processing Engine
 * Multi-modal intent analysis with entity extraction, context-aware recommendations,
 * and natural language workflow specification with continuous learning.
 *
 * @fileOverview Main NLP engine coordinating intent analysis, entity extraction,
 *               recommendation generation, and workflow specification parsing.
 * @version 1.0.0
 * @integration T06 (edps-skill-navigator), T07 (edps-workflow-orchestrator), T08 (edps-quality-gates)
 */

import fs from 'fs-extra';
import path from 'path';
import { EventEmitter } from 'events';

// ─────────────────────────────────────────────────────────────────────────────
// Main NLP Engine
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Core orchestrator for all NLP operations.
 * Coordinates intent analysis, entity extraction, context building,
 * recommendation ranking, and continuous learning.
 */
export class EDPSNLPEngine extends EventEmitter {
    constructor(config = {}) {
        super();

        this.config = {
            confidenceThreshold: config.confidenceThreshold ?? 0.70,
            maxClarifications: config.maxClarifications ?? 2,
            learningEnabled: config.learningEnabled ?? true,
            responseTimeTarget: config.responseTimeTarget ?? 3000, // ms
            patternLibraryPath: config.patternLibraryPath ??
                path.join(process.cwd(), '.github', 'skills', 'edps-enhanced-nlp', 'intent-patterns.json'),
            ...config
        };

        this.intentAnalyzer = new IntentAnalyzer(this.config);
        this.entityExtractor = new EntityExtractor(this.config);
        this.contextBuilder = new ProjectContextBuilder(this.config);
        this.recommendationEngine = new RecommendationEngine(this.config);
        this.workflowBuilder = new NLWorkflowBuilder(this.config);
        this.learningSystem = new LearningSystem(this.config);
        this.clarificationGenerator = new ClarificationGenerator(this.config);

        this._patternLibrary = null;
        this._initialized = false;
    }

    async initialize() {
        if (this._initialized) return;

        this._patternLibrary = await this._loadPatternLibrary();

        // Inject shared pattern library into subsystems
        this.intentAnalyzer.setPatternLibrary(this._patternLibrary);
        this.entityExtractor.setPatternLibrary(this._patternLibrary);
        this.recommendationEngine.setPatternLibrary(this._patternLibrary);
        this.workflowBuilder.setPatternLibrary(this._patternLibrary);

        // Wire up T06/T07/T08 integration layers
        await this._connectIntegrations();

        this._initialized = true;
        this.emit('initialized', { pattern_categories: Object.keys(this._patternLibrary.intent_categories).length });
    }

    // ─── Public API ───────────────────────────────────────────────────────────

    /**
     * Primary entry point: analyse a user prompt and return ranked recommendations.
     * Meets the <3 second response time requirement for 95th percentile queries.
     */
    async analyzePrompt(userPrompt, executionContext = {}) {
        await this._ensureInitialized();
        const t0 = Date.now();

        // Parallel phase: intent + entities do not depend on each other
        const [intentAnalysis, extractedEntities] = await Promise.all([
            this.intentAnalyzer.analyze(userPrompt, executionContext),
            this.entityExtractor.extract(userPrompt, executionContext)
        ]);

        // Context enrichment uses both intent and entities
        const projectContext = await this.contextBuilder.build(
            executionContext,
            intentAnalysis,
            extractedEntities
        );

        // Recommendations use all three inputs in parallel sub-tasks
        const [skillRecs, workflowRecs] = await Promise.all([
            this.recommendationEngine.generateSkillRecommendations(intentAnalysis, extractedEntities, projectContext),
            this.recommendationEngine.generateWorkflowRecommendations(intentAnalysis, extractedEntities, projectContext)
        ]);

        // Clarification questions only generated when confidence is low enough to need them
        const clarifications = await this.clarificationGenerator.generate(
            intentAnalysis,
            extractedEntities,
            skillRecs,
            workflowRecs,
            projectContext
        );

        const analysisTime = Date.now() - t0;

        const result = {
            prompt: userPrompt,
            intent: intentAnalysis,
            entities: extractedEntities,
            recommendations: {
                skills: skillRecs,
                workflows: workflowRecs,
                primary_action: skillRecs[0] ?? null
            },
            clarifications,
            analysis_time_ms: analysisTime,
            context_applied: projectContext.applied_factors,
            metadata: {
                nlp_engine_version: '1.0.0',
                pattern_library_version: this._patternLibrary.pattern_library_version,
                meets_response_sla: analysisTime < this.config.responseTimeTarget
            }
        };

        this.emit('prompt_analyzed', result);

        // Fire-and-forget learning event (do not block response)
        if (this.config.learningEnabled) {
            this.learningSystem.recordAnalysis(result).catch(() => {});
        }

        return result;
    }

    /**
     * Parse a natural language workflow description into an executable workflow config.
     */
    async parseWorkflowDescription(description, context = {}) {
        await this._ensureInitialized();
        return this.workflowBuilder.parse(description, context);
    }

    /**
     * Analyse a modification request against an existing workflow definition.
     */
    async parseWorkflowModification(modificationText, existingWorkflow, context = {}) {
        await this._ensureInitialized();
        return this.workflowBuilder.parseModification(modificationText, existingWorkflow, context);
    }

    /**
     * Record user feedback for the learning system.
     */
    async recordFeedback(feedbackEvent) {
        await this._ensureInitialized();
        return this.learningSystem.recordFeedback(feedbackEvent);
    }

    /**
     * Return current performance metrics from the learning system.
     */
    async getPerformanceMetrics() {
        await this._ensureInitialized();
        return this.learningSystem.getMetrics();
    }

    // ─── Private helpers ──────────────────────────────────────────────────────

    async _loadPatternLibrary() {
        const raw = await fs.readFile(this.config.patternLibraryPath, 'utf8');
        return JSON.parse(raw);
    }

    async _connectIntegrations() {
        // T06 Navigator
        if (this.config.t06Integration) {
            this.recommendationEngine.setNavigator(this.config.t06Integration);
        }
        // T07 Orchestrator
        if (this.config.t07Integration) {
            this.workflowBuilder.setOrchestrator(this.config.t07Integration);
            this.recommendationEngine.setOrchestrator(this.config.t07Integration);
        }
        // T08 Quality Gates
        if (this.config.t08Integration) {
            this.recommendationEngine.setGateSystem(this.config.t08Integration);
        }
    }

    async _ensureInitialized() {
        if (!this._initialized) await this.initialize();
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Intent Analyser
// ─────────────────────────────────────────────────────────────────────────────

export class IntentAnalyzer {
    constructor(config = {}) {
        this.config = config;
        this._patternLibrary = null;
    }

    setPatternLibrary(library) {
        this._patternLibrary = library;
        // Pre-compile all patterns for performance
        this._compiled = this._compilePatterns(library.intent_categories);
    }

    _compilePatterns(categories) {
        const compiled = new Map();
        for (const [catId, cat] of Object.entries(categories)) {
            const primary = cat.primary_patterns.map(p => new RegExp(p, 'i'));
            const negative = (cat.negative_patterns ?? []).map(p => new RegExp(p, 'i'));
            const subs = new Map();
            for (const [subId, sub] of Object.entries(cat.subcategories ?? {})) {
                subs.set(subId, {
                    ...sub,
                    compiled: sub.patterns.map(p => new RegExp(p, 'i'))
                });
            }
            compiled.set(catId, { ...cat, primary, negative, subs });
        }
        return compiled;
    }

    async analyze(prompt, context = {}) {
        if (!this._compiled) throw new NLPError('Pattern library not loaded');

        const normalizedPrompt = prompt.trim().toLowerCase();
        const scores = [];

        for (const [catId, cat] of this._compiled) {
            const primaryHits = cat.primary.filter(re => re.test(prompt)).length;
            if (primaryHits === 0) continue;

            const negativeHits = cat.negative.filter(re => re.test(prompt)).length;
            const baseScore = (primaryHits / cat.primary.length) * cat.base_confidence;
            const penalised = baseScore * (1 - negativeHits * 0.3);

            // Identify matching sub-categories
            const matchedSubs = [];
            for (const [subId, sub] of cat.subs) {
                const subHits = sub.compiled.filter(re => re.test(prompt)).length;
                if (subHits > 0) {
                    matchedSubs.push({
                        id: subId,
                        score: (subHits / sub.compiled.length) * sub.weight,
                        recommended_skills: sub.recommended_skills,
                        workflow_patterns: sub.workflow_patterns
                    });
                }
            }

            scores.push({
                category: catId,
                name: cat.name,
                score: penalised,
                primary_hits: primaryHits,
                negative_hits: negativeHits,
                matched_subcategories: matchedSubs.sort((a, b) => b.score - a.score)
            });
        }

        scores.sort((a, b) => b.score - a.score);

        const top = scores[0];
        const confidence = top
            ? this._computeConfidence(top, scores)
            : 0;

        // Extract quality and urgency signals for downstream use
        const qualityLevel = this._detectQualityLevel(prompt);
        const urgencyLevel = this._detectUrgencyLevel(prompt);

        return {
            primary_intent: top?.category ?? 'unknown',
            primary_intent_name: top?.name ?? 'Unknown',
            confidence,
            top_candidates: scores.slice(0, 3),
            matched_subcategories: top?.matched_subcategories ?? [],
            quality_level: qualityLevel,
            urgency_level: urgencyLevel,
            multi_intent: this._detectMultiIntent(scores),
            raw_scores: scores
        };
    }

    _computeConfidence(top, allScores) {
        if (allScores.length === 1) return Math.min(top.score, 0.95);
        // Confidence increases with the margin over the second-best score
        const second = allScores[1]?.score ?? 0;
        const margin = top.score - second;
        return Math.min(top.score * (1 + margin * 0.5), 0.98);
    }

    _detectMultiIntent(scores) {
        const threshold = scores[0]?.score * 0.75 ?? 0;
        return scores.filter(s => s.score >= threshold).length > 1;
    }

    _detectQualityLevel(prompt) {
        const lib = this._patternLibrary?.entity_patterns?.quality_requirements?.quality_level;
        if (!lib) return 'standard';
        for (const [level, patterns] of Object.entries(lib)) {
            if (patterns.some(p => new RegExp(p, 'i').test(prompt))) return level;
        }
        return 'standard';
    }

    _detectUrgencyLevel(prompt) {
        const lib = this._patternLibrary?.entity_patterns?.quality_requirements?.urgency_indicators;
        if (!lib) return 'medium';
        for (const [level, patterns] of Object.entries(lib)) {
            if (patterns.some(p => new RegExp(p, 'i').test(prompt))) return level;
        }
        return 'medium';
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Entity Extractor
// ─────────────────────────────────────────────────────────────────────────────

export class EntityExtractor {
    constructor(config = {}) {
        this.config = config;
        this._patternLibrary = null;
    }

    setPatternLibrary(library) {
        this._patternLibrary = library;
        this._compiled = this._compileEntityPatterns(library.entity_patterns);
    }

    _compileEntityPatterns(entityPatterns) {
        const compiled = [];
        for (const [groupName, group] of Object.entries(entityPatterns)) {
            for (const [typeName, patterns] of Object.entries(group)) {
                // patterns may be an array of strings OR a nested obj
                if (Array.isArray(patterns)) {
                    compiled.push({
                        group: groupName,
                        type: typeName,
                        regexes: patterns.map(p => new RegExp(p, 'i'))
                    });
                } else if (typeof patterns === 'object') {
                    for (const [subType, subPatterns] of Object.entries(patterns)) {
                        if (Array.isArray(subPatterns)) {
                            compiled.push({
                                group: groupName,
                                type: typeName,
                                sub_type: subType,
                                regexes: subPatterns.map(p => new RegExp(p, 'i'))
                            });
                        }
                    }
                }
            }
        }
        return compiled;
    }

    async extract(prompt, context = {}) {
        if (!this._compiled) throw new NLPError('Pattern library not loaded');

        const entities = [];

        for (const entry of this._compiled) {
            for (const regex of entry.regexes) {
                const match = regex.exec(prompt);
                if (match) {
                    entities.push({
                        group: entry.group,
                        type: entry.type,
                        sub_type: entry.sub_type ?? null,
                        value: match[0],
                        start: match.index,
                        end: match.index + match[0].length,
                        confidence: 0.85
                    });
                    break; // Only one match per pattern entry
                }
            }
        }

        // Deduplicate overlapping spans (keep highest-confidence)
        const deduped = this._deduplicateEntities(entities);

        return this._categorize(deduped);
    }

    _deduplicateEntities(entities) {
        const deduped = [];
        for (const ent of entities) {
            const overlaps = deduped.some(
                e => e.start < ent.end && ent.start < e.end
            );
            if (!overlaps) deduped.push(ent);
        }
        return deduped;
    }

    _categorize(entities) {
        return {
            all: entities,
            edps_components: entities.filter(e => e.group === 'edps_components'),
            project_context: entities.filter(e => e.group === 'project_context'),
            quality_requirements: entities.filter(e => e.group === 'quality_requirements'),
            constraints: entities.filter(e => e.group === 'constraints'),
            skills_mentioned: entities.filter(e => e.type === 'edps_skills').map(e => e.value)
        };
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Project Context Builder
// ─────────────────────────────────────────────────────────────────────────────

export class ProjectContextBuilder {
    constructor(config = {}) {
        this.config = config;
    }

    async build(executionContext, intentAnalysis, extractedEntities) {
        const appliedFactors = [];

        // Determine project phase from context or entity extraction
        let projectPhase = executionContext.project_phase;
        if (!projectPhase) {
            const phaseEntity = extractedEntities.project_context
                .find(e => e.type === 'phase_indicators');
            projectPhase = phaseEntity?.sub_type ?? 'unknown';
        }
        if (projectPhase !== 'unknown') appliedFactors.push('project_phase');

        // Determine quality level
        const qualityLevel = intentAnalysis.quality_level ??
            executionContext.quality_requirements ?? 'standard';
        appliedFactors.push('quality_level');

        // Determine urgency
        const urgencyLevel = intentAnalysis.urgency_level ??
            executionContext.urgency ?? 'medium';
        appliedFactors.push('urgency_level');

        // Gather completed artifacts from context history
        const completedArtifacts = executionContext.completed_artifacts ?? [];
        if (completedArtifacts.length > 0) appliedFactors.push('completed_artifacts');

        // Load phase-specific adaptations from pattern library
        const adaptations = this._getPhaseAdaptations(projectPhase, qualityLevel, urgencyLevel);

        return {
            project_phase: projectPhase,
            quality_level: qualityLevel,
            urgency_level: urgencyLevel,
            completed_artifacts: completedArtifacts,
            available_resources: executionContext.available_resources ?? [],
            adaptations,
            applied_factors: appliedFactors
        };
    }

    _getPhaseAdaptations(phase, quality, urgency) {
        // Consolidate skill boosts / suppressions and workflow modifiers
        return {
            boosted_skills: this._phaseBoosts[phase] ?? [],
            suppressed_skills: this._phaseSuppresses[phase] ?? [],
            quality_gates: this._qualityGates[quality] ?? this._qualityGates.standard,
            workflow_modifiers: this._urgencyModifiers[urgency] ?? [],
            max_clarification_questions: this._urgencyMaxQuestions[urgency] ?? 2
        };
    }

    _phaseBoosts = {
        early: ['requirements-ingest', 'goals-extract', 'process-w5h', 'domain-extractconcepts'],
        analysis: ['requirements-ingest', 'process-w5h', 'goals-extract'],
        design: ['diagram-generatecollaboration', 'domain-alignentities', 'hierarchy-management'],
        implementation: ['hierarchy-validation', 'edps-compliance', 'edps-quality-gates'],
        testing: ['edps-compliance', 'hierarchy-validation', 'edps-quality-gates'],
        completion: ['documentation-automation', 'project-status-reporting', 'edps-compliance']
    };

    _phaseSuppresses = {
        completion: ['requirements-ingest', 'process-w5h'],
        implementation: ['process-w5h', 'goals-extract']
    };

    _qualityGates = {
        high: ['content_completeness_gate', 'format_validation_gate', 'quality_scoring_gate',
               'vr1_boundary_compliance_gate', 'quality_threshold_gate'],
        standard: ['content_completeness_gate', 'format_validation_gate', 'quality_scoring_gate'],
        expedited: ['content_completeness_gate']
    };

    _urgencyModifiers = {
        high: ['maximum_parallelism', 'skip_optional_quality_gates', 'fast_path_preferred'],
        medium: ['moderate_parallelism'],
        low: ['thorough_validation', 'include_all_quality_gates']
    };

    _urgencyMaxQuestions = { high: 1, medium: 2, low: 3 };
}

// ─────────────────────────────────────────────────────────────────────────────
// Recommendation Engine
// ─────────────────────────────────────────────────────────────────────────────

export class RecommendationEngine {
    constructor(config = {}) {
        this.config = config;
        this._patternLibrary = null;
        this._navigator = null;
        this._orchestrator = null;
        this._gateSystem = null;
    }

    setPatternLibrary(lib) { this._patternLibrary = lib; }
    setNavigator(nav) { this._navigator = nav; }
    setOrchestrator(orch) { this._orchestrator = orch; }
    setGateSystem(gates) { this._gateSystem = gates; }

    async generateSkillRecommendations(intentAnalysis, entities, projectContext) {
        const candidates = new Map(); // skill_id → candidate object

        // 1. Add skills from matched sub-categories
        for (const sub of intentAnalysis.matched_subcategories) {
            for (const skillId of sub.recommended_skills ?? []) {
                const score = sub.score * this._phaseMultiplier(skillId, projectContext);
                this._upsert(candidates, skillId, score, `Matched ${intentAnalysis.primary_intent}:${sub.id}`);
            }
        }

        // 2. Boost / suppress based on phase adaptations
        for (const skillId of projectContext.adaptations?.boosted_skills ?? []) {
            if (candidates.has(skillId)) {
                candidates.get(skillId).score *= 1.2;
                candidates.get(skillId).phase_boosted = true;
            }
        }
        for (const skillId of projectContext.adaptations?.suppressed_skills ?? []) {
            if (candidates.has(skillId)) {
                candidates.get(skillId).score *= 0.5;
                candidates.get(skillId).phase_suppressed = true;
            }
        }

        // 3. Boost skills explicitly mentioned in user prompt
        for (const mentionedSkill of entities.skills_mentioned ?? []) {
            const normalized = mentionedSkill.toLowerCase().replace(/[^a-z0-9-]/g, '');
            if (candidates.has(normalized)) {
                candidates.get(normalized).score *= 1.4;
                candidates.get(normalized).explicitly_mentioned = true;
            }
        }

        return Array.from(candidates.values())
            .sort((a, b) => b.score - a.score)
            .slice(0, 5)  // Return at most 5 recommendations
            .map(c => ({ ...c, confidence: Math.min(c.score * intentAnalysis.confidence, 0.99) }));
    }

    async generateWorkflowRecommendations(intentAnalysis, entities, projectContext) {
        if (!this._patternLibrary) return [];

        const workflowKeywords = this._patternLibrary.workflow_pattern_keywords ?? {};
        const prompt = intentAnalysis.raw_scores[0]?.category + ' ' + intentAnalysis.primary_intent; // best proxy without re-passing prompt

        const matches = [];
        for (const [wfId, wfConfig] of Object.entries(workflowKeywords)) {
            const hit = wfConfig.patterns.some(p => new RegExp(p, 'i').test(prompt));
            if (hit) {
                matches.push({
                    pattern_id: wfId,
                    workflow_options: wfConfig.matched_workflows,
                    confidence: 0.8
                });
            }
        }

        // Always add workflows from sub-category definitions
        for (const sub of intentAnalysis.matched_subcategories.slice(0, 2)) {
            for (const wfPattern of sub.workflow_patterns ?? []) {
                if (!matches.some(m => m.workflow_options.includes(wfPattern))) {
                    matches.push({
                        pattern_id: wfPattern,
                        workflow_options: [wfPattern],
                        confidence: sub.score * intentAnalysis.confidence
                    });
                }
            }
        }

        return matches.sort((a, b) => b.confidence - a.confidence).slice(0, 3);
    }

    _upsert(map, skillId, score, reason) {
        if (map.has(skillId)) {
            const existing = map.get(skillId);
            existing.score = Math.max(existing.score, score);
        } else {
            map.set(skillId, { skill_id: skillId, score, reason });
        }
    }

    _phaseMultiplier(skillId, projectContext) {
        const boosted = projectContext.adaptations?.boosted_skills ?? [];
        const suppressed = projectContext.adaptations?.suppressed_skills ?? [];
        if (boosted.includes(skillId)) return 1.2;
        if (suppressed.includes(skillId)) return 0.6;
        return 1.0;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Natural Language Workflow Builder
// ─────────────────────────────────────────────────────────────────────────────

export class NLWorkflowBuilder {
    constructor(config = {}) {
        this.config = config;
        this._patternLibrary = null;
        this._orchestrator = null;
    }

    setPatternLibrary(lib) { this._patternLibrary = lib; }
    setOrchestrator(orch) { this._orchestrator = orch; }

    async parse(description, context = {}) {
        const components = {
            starting_point: this._extractStartingPoint(description),
            end_goal: this._extractEndGoal(description),
            constraints: this._extractConstraints(description),
            quality_level: this._extractQualityLevel(description),
            explicit_steps: this._extractExplicitSteps(description)
        };

        // High-confidence match against known workflow patterns
        const patternMatch = this._matchWorkflowPattern(description);
        if (patternMatch && patternMatch.confidence > 0.85) {
            return {
                type: 'pattern_match',
                pattern_id: patternMatch.pattern_id,
                workflow_ids: patternMatch.workflow_options,
                components,
                confidence: patternMatch.confidence,
                needs_adaptation: Object.values(components).some(v => v !== null)
            };
        }

        // Custom workflow assembly from components
        return {
            type: 'custom_build',
            components,
            skill_sequence: this._resolveSkillSequence(components),
            confidence: 0.7,
            needs_review: true
        };
    }

    async parseModification(modificationText, existingWorkflow, context = {}) {
        const modType = this._classifyModification(modificationText);
        return {
            modification_type: modType,
            workflow_id: existingWorkflow.id ?? existingWorkflow.pattern_id,
            change_description: modificationText,
            change_details: this._extractModificationDetails(modType, modificationText),
            confidence: 0.8,
            needs_validation: true
        };
    }

    _matchWorkflowPattern(description) {
        const keywords = this._patternLibrary?.workflow_pattern_keywords ?? {};
        for (const [wfId, wfConfig] of Object.entries(keywords)) {
            const matched = wfConfig.patterns.some(p => new RegExp(p, 'i').test(description));
            if (matched) {
                return { pattern_id: wfId, workflow_options: wfConfig.matched_workflows, confidence: 0.90 };
            }
        }
        return null;
    }

    _extractStartingPoint(description) {
        const fromPattern = /\b(from|starting (from|with)|beginning with|given|taking)\b\s+(.+?)(?:\s+(to|into|and|,)|$)/i;
        const m = fromPattern.exec(description);
        return m ? m[3].trim() : null;
    }

    _extractEndGoal(description) {
        const toPattern = /\b(to produce|resulting in|so that|in order to|create|generate|output)\b\s+(.+?)(?:\.|$)/i;
        const m = toPattern.exec(description);
        return m ? m[2].trim() : null;
    }

    _extractConstraints(description) {
        const constraintPatterns = this._patternLibrary?.entity_patterns?.constraints?.technical_constraints ?? [];
        return constraintPatterns
            .filter(p => new RegExp(p, 'i').test(description))
            .map(p => ({ pattern: p, matched: true }));
    }

    _extractQualityLevel(description) {
        const lib = this._patternLibrary?.entity_patterns?.quality_requirements?.quality_level ?? {};
        for (const [level, patterns] of Object.entries(lib)) {
            if (patterns.some(p => new RegExp(p, 'i').test(description))) return level;
        }
        return 'standard';
    }

    _extractExplicitSteps(description) {
        // Poor man's step detector: numbered or bulleted items in the description
        const stepPattern = /(?:^|\n)\s*(?:\d+[.)]\s+|[-*]\s+)(.+)/gm;
        const steps = [];
        let m;
        while ((m = stepPattern.exec(description)) !== null) {
            steps.push(m[1].trim());
        }
        return steps;
    }

    _resolveSkillSequence(components) {
        // Thin heuristic: map starting points and goals to skill IDs
        const sequence = [];
        if (/requirement[s]?/i.test(components.starting_point ?? '')) {
            sequence.push('requirements-ingest');
        }
        if (/diagram/i.test(components.end_goal ?? '')) {
            sequence.push('diagram-generatecollaboration');
        }
        if (/validat/i.test(components.end_goal ?? '')) {
            sequence.push('edps-compliance', 'hierarchy-validation');
        }
        if (/document/i.test(components.end_goal ?? '')) {
            sequence.push('documentation-automation');
        }
        return sequence;
    }

    _classifyModification(text) {
        if (/\b(add|include|insert|append)\b/i.test(text)) return 'add_step';
        if (/\b(remove|delete|drop|skip|exclude)\b/i.test(text)) return 'remove_step';
        if (/\b(higher quality|more thorough|comprehensive)\b/i.test(text)) return 'change_quality';
        if (/\b(must|should not|constrain|limit)\b/i.test(text)) return 'add_constraint';
        if (/\b(before|after|reorder|swap|move.*step)\b/i.test(text)) return 'change_sequence';
        return 'general_change';
    }

    _extractModificationDetails(modType, text) {
        return { raw_text: text, modification_type: modType };
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Clarification Generator
// ─────────────────────────────────────────────────────────────────────────────

export class ClarificationGenerator {
    constructor(config = {}) {
        this.config = config;
        this._patternLibrary = null;
    }

    setPatternLibrary(lib) { this._patternLibrary = lib; }

    async generate(intentAnalysis, entities, skillRecs, workflowRecs, projectContext) {
        const questions = [];
        const maxQ = projectContext.adaptations?.max_clarification_questions ?? this.config.maxClarifications ?? 2;
        const templates = this._patternLibrary?.clarification_templates ?? {};
        const thresholds = this._patternLibrary?.confidence_thresholds ?? {};

        // 1. Low confidence intent
        if (intentAnalysis.confidence < (thresholds.require_single_clarification ?? 0.70)) {
            const opts = intentAnalysis.top_candidates.slice(0, 3).map(c => c.name).join(' / ');
            questions.push({
                type: 'intent_clarification',
                question: `Your request could relate to multiple areas (${opts}). Which best describes what you need?`,
                priority: 1
            });
        }

        // 2. No project context detected
        if (!entities.project_context?.length) {
            questions.push({
                type: 'entity_clarification',
                question: templates.missing_entities?.missing_project_context ?? 'Which project or process should I focus on?',
                priority: 2
            });
        }

        // 3. Multiple workflows found and no scope entity
        if (workflowRecs.length > 1 && !entities.constraints?.length) {
            questions.push({
                type: 'scope_clarification',
                question: templates.missing_entities?.missing_scope ??
                    'What\'s the scope? (single step / selected skills / full workflow)',
                options: ['single step', 'selected skills', 'full end-to-end workflow'],
                priority: 3
            });
        }

        return questions
            .sort((a, b) => a.priority - b.priority)
            .slice(0, maxQ);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Learning System
// ─────────────────────────────────────────────────────────────────────────────

export class LearningSystem {
    constructor(config = {}) {
        this.config = config;
        this._history = [];         // In-memory store; replace with persistent store in production
        this._patternBoosts = new Map();
        this._accuracyHistory = [];
        this._batchThreshold = config.batchLearningThreshold ?? 10;
    }

    async recordAnalysis(result) {
        this._history.push({
            timestamp: new Date(),
            intent: result.intent.primary_intent,
            confidence: result.intent.confidence,
            top_skill: result.recommendations.primary_action?.skill_id,
            analysis_time_ms: result.analysis_time_ms
        });
    }

    async recordFeedback(event) {
        const record = {
            ...event,
            timestamp: new Date()
        };

        this._history.push(record);

        if (event.feedback_confidence > 0.8) {
            this._applyImmediateLearning(record);
        }

        if (this._pendingFeedback().length >= this._batchThreshold) {
            this._runBatchUpdate();
        }

        return { recorded: true, pending_feedback: this._pendingFeedback().length };
    }

    _pendingFeedback() {
        return this._history.filter(h => h.outcome && !h.batch_processed);
    }

    _applyImmediateLearning(record) {
        const key = `${record.intent}:${record.top_skill}`;
        const current = this._patternBoosts.get(key) ?? 1.0;
        const delta = record.outcome === 'accepted' ? 0.05 : -0.03;
        this._patternBoosts.set(key, Math.max(0.5, Math.min(1.5, current + delta)));
    }

    _runBatchUpdate() {
        const pending = this._pendingFeedback();
        const acceptedCount = pending.filter(f => f.outcome === 'accepted').length;
        const accuracy = pending.length > 0 ? acceptedCount / pending.length : 0;
        this._accuracyHistory.push({ timestamp: new Date(), accuracy, sample_size: pending.length });
        pending.forEach(f => { f.batch_processed = true; });
    }

    async getMetrics() {
        const recent = this._history.filter(h => h.outcome).slice(-100);
        const accepted = recent.filter(h => h.outcome === 'accepted').length;
        return {
            total_interactions: this._history.length,
            total_feedback: recent.length,
            acceptance_rate: recent.length > 0 ? accepted / recent.length : null,
            accuracy_trend: this._accuracyHistory.slice(-10),
            active_pattern_boosts: this._patternBoosts.size
        };
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Error types
// ─────────────────────────────────────────────────────────────────────────────

export class NLPError extends Error {
    constructor(message) { super(message); this.name = 'NLPError'; }
}
