---
permalink: /research/
title: "Research"
excerpt: "Causal machine learning for education: policy learning, educational inequality, algorithmic fairness, generative simulation, and LLM multi-agent systems."
author_profile: true
---

# Research
<p class="pg-lede">I work on causal machine learning and educational data science. The four threads below run through my dissertation and my collaborations. Each card opens a short page with the methods, the data, and the papers.</p>

<div class="rgrid">

  <a class="rcard" href="{{ '/research/otr/' | relative_url }}" target="_self">
    {% include research/otr.svg %}
    <h2 class="rcard__title">Optimal and dynamic treatment regimes</h2>
    <p class="rcard__tags">#Policy Learning #Optimal Treatment Regimes #TMLE #Feasibility</p>
    <p class="rcard__blurb">Learning which sequence of courses to recommend to an individual student, and making the recommendation one a school could actually follow.</p>
    <span class="rcard__more">Read more</span>
  </a>

  <a class="rcard" href="{{ '/research/genai/' | relative_url }}" target="_self">
    {% include research/genai.svg %}
    <h2 class="rcard__title">Generative AI for synthetic data and method evaluation</h2>
    <p class="rcard__tags">#Synthetic Data #Monte Carlo #CTGAN #Diffusion Models</p>
    <p class="rcard__blurb">Using generative models to build simulation studies whose data behaves like the data researchers actually analyze.</p>
    <span class="rcard__more">Read more</span>
  </a>

  <a class="rcard" href="{{ '/research/agents/' | relative_url }}" target="_self">
    {% include research/agents.svg %}
    <h2 class="rcard__title">LLM multi-agent systems for automated quantitative research</h2>
    <p class="rcard__tags">#Multi-agent Systems #LLM Evaluation #Automated Research #Distillation</p>
    <p class="rcard__blurb">EDM-ARS carries a study from question to manuscript, and reviews its own methods on the way. Plus distilling a black-box model into one that explains itself.</p>
    <span class="rcard__more">Read more</span>
  </a>

  <a class="rcard" href="{{ '/research/fairness/' | relative_url }}" target="_self">
    {% include research/fairness.svg %}
    <h2 class="rcard__title">Algorithmic fairness in prediction and decision-making</h2>
    <p class="rcard__tags">#Algorithmic Fairness #Dropout Prediction #Auditing #Multilevel Data</p>
    <p class="rcard__blurb">A model can be accurate overall and wrong unevenly. Measuring that before anyone acts on its output.</p>
    <span class="rcard__more">Read more</span>
  </a>

</div>
