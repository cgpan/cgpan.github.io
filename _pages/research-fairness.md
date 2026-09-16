---
permalink: /research/fairness/
title: "Algorithmic fairness in prediction and decision-making"
excerpt: "A model can be accurate overall and wrong unevenly. Auditing that before anyone acts on its output."
author_profile: true
---

<a class="pg-back" href="{{ '/research/' | relative_url }}" target="_self">All research</a>

# Algorithmic fairness in prediction and decision-making

<div class="rfig-frame">{% include research/fairness.svg %}</div>

<p class="pg-lede">Schools increasingly use predictive models to decide who needs attention: who is likely to drop out, who should be flagged for an intervention. A model with good overall accuracy can still be much less accurate for some groups of students than others, and the students it fails are often the ones the system was built to help.</p>

My first independent paper took that concern to dropout prediction, examining algorithmic fairness in models that predict which students will leave high school. Fairness there is not one quantity: the competing definitions in the literature can disagree with each other, so which one you adopt changes the verdict on the same model.

The same concern reappears in causal work. When a treatment rule is learned from data, the rule inherits whatever unevenness the estimator had, and it then acts on students rather than merely describing them. So fairness belongs among the criteria an estimator is judged on, alongside bias and variance, which is how it enters the [simulation work](/research/genai/){:target="_self"}.

## Papers

<ul class="publist">
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Fair and Robust Estimation of Heterogeneous Treatment Effects for Optimal Policies in Multilevel Studies</p>
      <p class="pub__authors">Youmi Suk, Chan Park, <strong>Chenguang Pan</strong>, and Kwangho Kim</p>
      <p class="pub__venue"><em>Multivariate Behavioral Research</em></p>
      <p class="pub__links"><a href="https://doi.org/10.1080/00273171.2026.2669081">DOI</a></p>
    </div>
    <div class="pub__side"><span class="pub__year">2026</span><span class="pub-status pub-status--out">Published</span></div>
  </li>
  <li class="pub">
    <div class="pub__body">
      <p class="pub__title">Examining Algorithmic Fairness in Predicting High School Dropouts</p>
      <p class="pub__authors"><strong>Chenguang Pan</strong> and Zhou Zhang</p>
      <p class="pub__venue">Proceedings of the International Conference on Educational Data Mining (<em>EDM 2024</em>), oral presentation</p>
      <p class="pub__links"><a href="https://zenodo.org/records/12729810">Paper</a><a href="https://eric.ed.gov/?id=ED675520">ERIC</a><a href="https://github.com/cgpan/HSLSdropout">Code</a></p>
    </div>
    <div class="pub__side"><span class="pub__year">2024</span><span class="pub-status pub-status--out">Published</span></div>
  </li>
</ul>

<p class="pg-note">I received an IEDMS Scholarship from the International Educational Data Mining Society at EDM 2024.</p>
