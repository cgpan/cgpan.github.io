---
permalink: /
title: ""
excerpt: "Chenguang Pan, PhD candidate in Measurement, Evaluation, and Statistics at Teachers College, Columbia University."
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

# Chenguang Pan

I am a fifth-year PhD candidate in the Measurement, Evaluation, and Statistics program at Teachers College, Columbia University, where I am advised by Professor [Youmi Suk](https://youmilab.ai/). I expect to graduate in May 2027.

I develop and extend quantitative methods at the intersection of causal inference, machine learning, and generative AI, and I apply them to
help schools make better decisions for individual students using the data they already collect. A tour of my research is on the [Research](/research/){:target="_self"} page.

Before pursuing my PhD, I spent nearly a decade at New Oriental Education & Technology Group in Beijing, where I was Deputy Manager of the American Graduate Test Department, as well as an instructor and researcher.

<div class="news-box" markdown="1">

## News

- *2026.10* Chenguang released [`pytlverse`](https://github.com/cgpan/pytlverse), a Python port of the R [tlverse](https://tlverse.org) packages for targeted maximum likelihood estimation (TMLE) and optimal treatment rules, in both single-stage and multi-stage (longitudinal) settings. In benchmarks against the R tlverse, it ran about 10 times faster while using about one-sixth of the memory, which makes large-scale simulation studies practical.
- *2026.10* Chenguang's paper [*Estimating Optimal Dynamic Treatment Regimes for Personalized Education: A Tutorial and Applications with Machine Learning*](https://arxiv.org/abs/2610.10843) (with Yuxuan Li, Thomas Harris, and Youmi Suk), accepted by *Zeitschrift für Psychologie*, is now in press. The preprint is available on arXiv.
- *2026.09* The syntax reference Chenguang built for HUDM 5001 Programming for Data Science is now open to everyone at [PythonTools](/python-tools/){:target="_self"}.

<div id="hidden-news" style="display: none;" markdown="1">

- *2026.07* Chenguang will be an instructor this fall for a graduate-level course, HUDM 5001 Programming for Data Science, at Teachers College, Columbia University.
- *2026.06* Chenguang will give two oral presentations at SREE 2026 in Baltimore.
- *2026.03*: &nbsp;🎉🎉 Excited to share [EDM-ARS (Educational Data Mining Automated Research System)](https://edmars.ai/) — a domain-specific, multi-agent LLM pipeline that turns a dataset + research prompt into a research paper.
- *2025.12*: &nbsp;🎉🎉 Chenguang was awarded the Morton T. Embree Outstanding Contribution to Student Learning Award in recognition of his service as a TA.
- *2025.11*: &nbsp;🎉🎉 Chenguang will give oral presentations at both AERA 2026 and NCME 2026.
- *2025.06*: &nbsp;🎉🎉 Three works that Chenguang was involved in were accepted by SREE 2025, and Chenguang will give an oral and a poster presentation.
- *2025.06*: &nbsp;🎉🎉 Chenguang was invited to be a reviewer for the 2026 AERA Annual Meeting.
- *2025.05*: &nbsp;🎉🎉 Chenguang gave an oral and a poster presentation about his in-progress work *Designing Realistic and Interpretable Optimal Treatment Regimes for Personalized Education* in ACIC 2025, and [Foundations of Data Science Workshop organized by Columbia Data Science Institute](https://datascience.columbia.edu/event/foundations-of-data-science-workshop-spring-2025/)
- *2025.05*: &nbsp;🎉🎉 Chenguang served as a poster reviewer for the American Causal Inference Conference (ACIC) in Detroit.
- *2025.01*: &nbsp;🎉🎉 Chenguang received a sponsored registration for the 2025 AERA Annual Meeting, AERA 2025.
- *2024.12*: &nbsp;🎉🎉 Chenguang was awarded the Provost's Grant for Conference presentation, Columbia University, NY, U.S.
- *2024.11*: &nbsp;🎉🎉 Chenguang's paper *Designing Optimal Dynamic Treatment Regimes Using TMLE for Personalized Math Course-taking Plans* (joint work with Youmi Suk) was accepted by the American Educational Research Association (AERA) conference 2025, Denver, CO, U.S.
- *2024.09*: &nbsp;🎉🎉 Chenguang's work (as second author) *Designing Personalized Math Course-taking Plans in High School Using Optimal Treatment Regimes* was accepted by and presented at the Society for Research on Educational Effectiveness (SREE) conference. Baltimore, MD, U.S.
- *2024.07*: &nbsp;🎉🎉 Chenguang's independent research paper *Examining Algorithmic Fairness in Predicting High School Dropouts* was accepted by and presented at the 17th International Conference on Educational Data Mining (EDM) 2024. Additionally, he was awarded the IEDMS Scholarship by EDM. Atlanta, GA, U.S.

</div>

<button id="toggle-news-btn" class="news-toggle" onclick="toggleNews()">Read more</button>

</div>

<script>
function toggleNews() {
  var hiddenNews = document.getElementById("hidden-news");
  var btn = document.getElementById("toggle-news-btn");

  if (hiddenNews.style.display === "none") {
    hiddenNews.style.display = "block";
    btn.innerHTML = "Show less";
  } else {
    hiddenNews.style.display = "none";
    btn.innerHTML = "Read more";
  }
}
</script>
