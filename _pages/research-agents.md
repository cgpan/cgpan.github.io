---
permalink: /research/agents/
title: "LLM multi-agent systems for automated quantitative research"
excerpt: "EDM-ARS carries a study from question to manuscript and reviews its own methods on the way, plus distilling a black-box model into one that explains itself."
author_profile: true
---

<a class="pg-back" href="{{ '/research/' | relative_url }}" target="_self">All research</a>

# LLM multi-agent systems for automated quantitative research

<div class="rfig-frame">{% include research/agents.svg %}</div>

<p class="pg-lede">Most of a quantitative paper is process: frame the question, prepare the data, choose an estimator, check that the choice was defensible, find the literature, write it up. Each step is describable, which makes the whole pipeline a reasonable target for a system of language-model agents. Whether the output is any good is an empirical question, and that is the part I care about.</p>

## EDM-ARS

I lead a four-person team building EDM-ARS, an open-source, domain-specific multi-agent system for educational data mining research. A state machine coordinates six specialized agents, each with its own prompt and model routing, from problem formulation through to a manuscript draft, with checkpoint-based recovery and code that runs in a sandbox rather than being pasted into the prose.

The agents run in order. A **problem formulator** searches Semantic Scholar and scopes the question and hypothesis. A **data engineer** cleans the features and emits the subgroup labels that later fairness analysis needs. An **analyst** runs the battery appropriate to the study type: machine learning with SHAP and subgroup fairness, causal estimators with balance and overlap diagnostics, or item response models through an R bridge. An **outline agent** plans the paper section by section against the results that actually came back, and a **writer** fills a LaTeX template rather than composing free-form prose.

What distinguishes it from a general-purpose research agent is the sixth agent, a **gatekeeper**. It reviews everything the others have produced and returns one of three verdicts: pass, revise, or abort. On revise, targeted instructions go back to whichever earlier agent needs them, for up to two cycles before the writer is unblocked regardless. Citations are verified against Semantic Scholar rather than trusted to the model's memory, and the backend is model-agnostic, running locally deployed open-weight models as well as hosted APIs.

We benchmarked EDM-ARS against two general-purpose automated research systems on federal education data, and used the comparison to build a defect taxonomy for AI-generated studies: a catalogue of the specific ways these systems go wrong, which is more useful than a single quality score.

<p class="pg-note">The system is at <a href="https://edmars.ai/">edmars.ai</a>, with a technical report at <a href="https://arxiv.org/abs/2603.18273">arXiv:2603.18273</a>.</p>

## Models that explain themselves

A second strand asks a narrower question. A causal machine learning model can estimate an individual treatment effect accurately and explain nothing. So we distilled one into a small open-weight language model, fine-tuned with LoRA, that returns three things at once: the effect estimate, a plain-language explanation of it, and a recommended action.

The interesting problem is not the fine-tuning but the guarantee. An explanation that sounds right and misdescribes the model is worse than no explanation, so a faithfulness audit gates what enters the training corpus, and the explanations are evaluated against the upstream estimator rather than judged on fluency.

## Papers and talks

<ul class="publist">
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">EDM-ARS: A Domain-Specific Multi-Agent System for Automated Educational Data Mining Research</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Zhou Zhang, Weixuan Xiao, Chengyuan Yao, and Youmi Suk</p>
      <p class="pub__venue">Technical report</p>
      <p class="pub__links"><a href="https://arxiv.org/abs/2603.18273">arXiv</a><a href="https://edmars.ai/">Project site</a></p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Domain-Specific Multi-Agent Systems for Automated Educational Data Mining Research and Review</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Zhou Zhang, Weixuan Xiao, Chengyuan Yao, and Youmi Suk</p>
      <p class="pub__venue"><em>SREE 2026</em>, oral presentation</p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Distilling Black-Box Machine Learning into a Small, Self-Explaining Language Model for Learning Analytics</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Airui Meng, and Youmi Suk</p>
      <p class="pub__links"><a href="https://arxiv.org/pdf/2608.21165">Preprint</a></p>
    </div>
    <div class="pub__side"><span class="pub-status">Under review</span></div>
  </li>
</ul>
