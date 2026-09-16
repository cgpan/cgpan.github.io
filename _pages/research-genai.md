---
permalink: /research/genai/
title: "Generative AI for synthetic data and method evaluation"
excerpt: "Using generative models to build simulation studies whose data behaves like the data researchers actually analyze."
author_profile: true
---

<a class="pg-back" href="{{ '/research/' | relative_url }}" target="_self">All research</a>

# Generative AI for synthetic data and method evaluation

<div class="rfig-frame">{% include research/genai.svg %}</div>

<p class="pg-lede">Every claim that a statistical method works rests on a simulation study, and every simulation study rests on a data-generating process that somebody wrote down. Those processes tend to be tidy in ways real data never is: normal errors, clean nesting, no missingness. A method that performs well there can disappoint on the data it was built for.</p>

The alternative is to learn the data-generating process instead of assuming it. A generative model fitted to one real sample can produce as many synthetic replicates as a Monte Carlo study needs, keeping the awkward structure of the original: skewed variables, categorical mixtures, and clustering of students within schools.

That makes a different kind of evaluation possible. Across replicates, an estimator can be scored not only on bias and variance but on fairness across groups and on the utility of the policy it implies, which are the quantities that matter when the estimate will be used to make a decision.

## Methods

<ul class="rowlist">
  <li class="row2">
    <div class="row2__when">tabular</div>
    <div class="row2__what"><strong>CTGAN and diffusion models</strong><p>Conditional generative models for tabular data, and ClavaDDPM for multi-table and multilevel structure.</p></div>
  </li>
  <li class="row2">
    <div class="row2__when">sequential</div>
    <div class="row2__what"><strong>Sequence generation</strong><p>Generating ordered records, such as course-taking histories, where each step depends on the ones before it.</p></div>
  </li>
  <li class="row2">
    <div class="row2__when">scale</div>
    <div class="row2__what"><strong>High-throughput computing</strong><p>Simulation campaigns run on the OSG Open Science Pool at roughly a thousand concurrent jobs, which is what makes large simulation campaigns affordable.</p></div>
  </li>
</ul>

## Papers and talks

<ul class="publist">
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Using Generative AI for Sequential Data Generation in Monte Carlo Simulation Studies</p>
      <p class="pub__authors">Youmi Suk, <strong>Chenguang Pan</strong>, and Ke Yang</p>
      <p class="pub__venue"><em>Journal of Educational and Behavioral Statistics</em></p>
      <p class="pub__links"><a href="https://doi.org/10.3102/10769986251397559">DOI</a></p>
    </div>
    <div class="pub__side"><span class="pub__year">2025</span><span class="pub-status pub-status--out">Published</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Generative AI-Based Monte Carlo Simulation for Method Evaluation Using Synthetic Multilevel Data</p>
      <p class="pub__authors">Youmi Suk, <strong>Chenguang Pan</strong>, and Weixuan Xiao</p>
      <p class="pub__links"><a href="https://arxiv.org/abs/2605.05752">Preprint</a></p>
    </div>
    <div class="pub__side"><span class="pub-status">Under review</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">AI-Based Monte Carlo Simulation for Method Evaluation Using Synthetic Multilevel Data</p>
      <p class="pub__authors">Youmi Suk, <strong>Chenguang Pan</strong>, and Weixuan Xiao</p>
      <p class="pub__venue"><em>SREE 2026</em>, oral presentation</p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span></div>
  </li>
</ul>
