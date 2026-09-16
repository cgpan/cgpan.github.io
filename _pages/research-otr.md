---
permalink: /research/otr/
title: "Optimal and dynamic treatment regimes"
excerpt: "Learning which sequence of high school mathematics courses to recommend to an individual student, under constraints that make the recommendation implementable."
author_profile: true
---

<a class="pg-back" href="{{ '/research/' | relative_url }}" target="_self">All research</a>

# Optimal and dynamic treatment regimes

<div class="rfig-frame">{% include research/otr.svg %}</div>

<p class="pg-lede">A treatment regime is a rule that maps what we know about a student to a recommended action. An optimal regime is the rule that would produce the best outcome if everyone followed it. A dynamic regime makes that decision more than once, at each grade, using what happened before.</p>

The application I keep returning to is high school mathematics. Course-taking is sequential, the sequence a student follows is not random, and the consequences last. I estimate these regimes on the High School Longitudinal Study of 2009, which follows about 23,000 students in 944 schools, using targeted maximum likelihood estimation and doubly robust estimation so that the estimate survives a misspecified model of either the outcome or the course assignment.

## Feasibility

An estimated optimal rule is useless if it recommends a course the student cannot get into. Recent work adds feasibility constraints drawn from institutional rules and from propensity-score thresholds, so that a recommended plan stays inside what the data suggests is actually reachable for a student like this one, in a school like this one.

## Interpretability

A regime that no one can read will not be adopted. I have been using Kolmogorov-Arnold networks to make heterogeneous treatment effects legible, so that the rule can be inspected rather than merely trusted. This is also where the [distillation work](/research/agents/){:target="_self"} comes in: a small language model that returns an effect estimate together with an explanation of it.

## Papers and talks

<ul class="publist">
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Estimating Optimal Dynamic Treatment Regimes for Personalized Education: A Tutorial and Applications with Machine Learning</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Yuxuan Li, and Youmi Suk</p>
      <p class="pub__venue"><em>Zeitschrift für Psychologie</em></p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span><span class="pub-status pub-status--out">Accepted</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Learning Feasible Optimal Treatment Regimes for Personalized Decision-Making</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Yuxuan Li, and Youmi Suk</p>
      <p class="pub__links"><a href="https://osf.io/preprints/psyarxiv/arp48_v1">Preprint</a></p>
    </div>
    <div class="pub__side"><span class="pub-status">Under review</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Enhancing the Interpretability of Heterogeneous Treatment Effects Using Kolmogorov-Arnold Networks</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong>, Yuxuan Li, and Youmi Suk</p>
      <p class="pub__venue"><em>AERA 2026</em> (Division D) and the <em>Modern Modeling Methods Conference 2026</em>, oral presentations</p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Designing Optimal Dynamic Treatment Regimes Using TMLE for Personalized Math Course-Taking Plans</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong> and Youmi Suk</p>
      <p class="pub__venue"><em>AERA 2025</em>, Division D, roundtable presentation</p>
      <p class="pub__links"><a href="https://doi.org/10.3102/2190733">DOI</a></p>
    </div>
    <div class="pub__side"><span class="pub__year">2025</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Designing Personalized Math Course-Taking Plans in High School Using Optimal Treatment Regimes</p>
      <p class="pub__authors">Youmi Suk and <strong>Chenguang Pan</strong></p>
      <p class="pub__venue"><em>SREE 2024</em>, poster presentation</p>
    </div>
    <div class="pub__side"><span class="pub__year">2024</span></div>
  </li>
</ul>

<p class="pg-note">The lab's project page for this work, with the personalized plans themselves, is at <a href="https://youmilab.ai/personalized-plan/index.html">youmilab.ai/personalized-plan</a>. The full list is on the <a href="/publications/" target="_self">Publications</a> page.</p>
