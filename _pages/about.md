---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I am a fourth-year PhD student in the Measurement, Evaluation, and Statistics program at Teachers College, Columbia University, where I am advised by Professor [Youmi Suk](https://youmisuk.com/). My research interests lie at the intersection of **causal machine learning**, **dynamic treatment regimes (DTR)**, and **generative AI for synthetic tabular data**.

Before pursuing my PhD, I spent nearly a decade at New Oriental Education & Technology Group in Beijing, where I held roles including business manager, instructor, and researcher for the graduate examination department. 


# 🔥 News  
- *2025.12*: &nbsp;🎉🎉 Chenguang was awarded the Morton T. Embree Outstanding Contribution to Student Learning Award in recognition of his service as a TA.  
- *2025.11*: &nbsp;🎉🎉 Chenguang will give oral presentations in both AERA 2026 and NCME 2026.
- *2025.06*: &nbsp;🎉🎉 Three works that Chenguang involved were accepted by SREE 2025 and Chenguang will give an oral and a poster presentation.
- *2025.06*: &nbsp;🎉🎉 Chenguang was invited to be a reviewer for 2026 AERA Annual Meeting.  

<div id="hidden-news" style="display: none;" markdown="1">

- *2025.05*: &nbsp;🎉🎉 Chenguang gave an oral and a poster presentation about his in-progress work *Designing Realistic and Interpretable Optimal Treatment Regimes for Personalized Education* in ACIC 2025, and [Foundations of Data Science Workshop organized by Columbia Data Science Institute](https://datascience.columbia.edu/event/foundations-of-data-science-workshop-spring-2025/)  
- *2025.05*: &nbsp;🎉🎉 Chenguang served as poster reviewer for American Causal Inference Conference (ACIC) at Detroit.
- *2025.01*: &nbsp;🎉🎉 Chenguang received a sponsored registration for the 2025 AERA Annual Meeting, AERA 2025.
- *2024.12*: &nbsp;🎉🎉 Chenguang was awarded the Provost's Grant for Conference presentation, Columbia University, NY, U.S.
- *2024.11*: &nbsp;🎉🎉 Chenguang's paper *Designing Optimal Dynamic Treatment Regimes Using TMLE for Personalized Math Course-taking Plans* (joint work with Youmi Suk) was accepted by the American Educational Research Association (AERA) conference 2025, Denver, CO, U.S.
- *2024.09*: &nbsp;🎉🎉 Chenguang's work (as second author) *Designing Personalized Math Course-taking Plans in High School Using Optimal Treatment Regimes* was accepted by and presented at the Society for Research on Educational Effectiveness (SREE) conference. Baltimore, MD, U.S.
- *2024.07*: &nbsp;🎉🎉 Chenguang's independent research paper *Examining the Algorithmic Fairness in Predicting High School Dropouts* was accepted by and presented at the 17th International Conference on Educational Data Mining (EDM) 2024. Additionally, he was awarded the IEDMS Scholarship by EDM. Atlanta, GA, U.S.

</div>

<button id="toggle-news-btn" onclick="toggleNews()" style="background: none; border: none; color: #007bff; cursor: pointer; text-decoration: underline; padding: 0; font-family: inherit; font-size: inherit;">Read more</button>

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

# 📝 Publications   
## Journal Papers
- [Learning Feasible Optimal Treatment Regimes for Personalized Decision-Making](https://osf.io/preprints/psyarxiv/arp48_v1), **Chenguang Pan**, Yuxuan Li, and Youmi Suk, **Under Review**
- [Fair and Robust Estimation of Heterogeneous Treatment Effects for Optimal Policies in Multilevel Studies](https://osf.io/preprints/psyarxiv/xz3jw), Youmi Suk, Chan Park, **Chenguang Pan**, and Kwangho Kim, **Under Review**  
- [Using Generative AI for Sequential Data Generation in Monte Carlo Simulation Studies](https://doi.org/10.3102/10769986251397559), Youmi Suk, **Chenguang Pan**, and Ke Yang. Accepted by *Journal of Educational and Behavioral Statistics* (JEBS)

## Proceedings
<div class="paper-box">
  <div class="paper-box-image">
    <div>
      <div class="badge">SREE 2025</div>
      <img src="images/SREE_2025.png" alt="SREE 2025 logo" width="100%">
    </div>
  </div>
  <div class="paper-box-text" markdown="1">
**[Investigating Interpretable Optimal Treatment Regimes Using Kolmogorov-Arnold Networks](https://builder.guidebook.com/g/#/guides/sree2025/schedule/730413/sessions/31565870)**  
**Chenguang Pan**, Yuxuan Li, and Youmi Suk  
*SREE 2025*
  </div>
</div>

<div class="paper-box">
  <div class="paper-box-image">
    <div>
      <div class="badge">AERA 2025</div>
      <img src="images/AERA_2025.png" alt="AERA 2025 logo" width="100%">
    </div>
  </div>
  <div class="paper-box-text" markdown="1">
**[Designing Optimal Dynamic Treatment Regimes Using TMLE for Personalized Math Course-Taking Plans](https://doi.org/10.3102/2190733)**  
**Chenguang Pan** and Youmi Suk  
*AERA 2025*
  </div>
</div>  

<div class="paper-box">
  <div class="paper-box-image">
    <div>
      <div class="badge">SREE 2025</div>
      <img src="images/SREE_2025.png" alt="SREE 2025 logo" width="100%">
    </div>
  </div>
  <div class="paper-box-text" markdown="1">
**[Improving the Feasibility of Optimal Treatment Regimes for Personalized Education](https://builder.guidebook.com/g/#/guides/sree2025/schedule/730413/sessions/31565650?scheduleDayPosition=2025-10-09&scheduleIndexInDayPosition=11)**  
Yuxuan Li, **Chenguang Pan**,and Youmi Suk  
*SREE 2025*
  </div>
</div>

<div class="paper-box">
  <div class="paper-box-image">
    <div>
      <div class="badge">EDM 2024</div>
      <img src="images/EDM_2024.png" alt="EDM 2024 logo" width="100%">
    </div>
  </div>
  <div class="paper-box-text" markdown="1">
**[Examining the Algorithmic Fairness in Predicting High School Dropouts](https://zenodo.org/records/12729810)**  
**Chenguang Pan** and Zhou Zhang  
[**Code**](https://github.com/cgpan/HSLSdropout)  
*EDM 2024*
  </div>
</div>

<div class="paper-box">
  <div class="paper-box-image">
    <div>
      <div class="badge">SREE 2024</div>
      <img src="images/SREE_2024.png" alt="SREE 2024 logo" width="100%">
    </div>
  </div>
  <div class="paper-box-text" markdown="1">
**[Designing Personalized Math Course-Taking Plans in High School Using Optimal Treatment Regimes](https://sree.confex.com/sree/2024/meetingapp.cgi/Paper/5320)**  
Youmi Suk and **Chenguang Pan**  
*SREE 2024*
  </div>
</div>



## Books  
- [GRE Text-Completion Essentials: Full Explanations of High-Frequency Questions](https://isbnsearch.org/isbn/9787553666433), Bing Han, **Chenguang Pan**, and Daiyuan Cheng, published in Chinese.
- [An Authentic Word List of High-Frequency GRE Vocabulary](https://isbnsearch.org/isbn/9787553662688), Bing Han and **Chenguang Pan**, published in Chinese.


# 🎖 Honors and Awards
- *2025* Morton T. Embree Outstanding Contribution to Student Learning Award, Teachers College, Columbia University
- *2025* Provost's Grant for Conference presentation, Teachers College, Columbia University.
- *2024* Provost's Grant for Conference presentation, Teachers College, Columbia University.
- *2024* IEDMS Scholarship, EDM Conference 2024, Atlanta, GA, U.S.
- *2023* Doctoral Research Fellowship Award, Teachers College, Columbia University.
- *2017* Outstanding Teacher Award (award rate: 1/400), New Oriental Education & Technology Group, Beijing, China.


# 🧐 Academic Service
- [Reviewer, 2026 American Institute of Research Forum](https://www.airweb.org/forum/2026/information/2026-proposal-reviewers)
- Discussant, 3rd Annual Conference of Advanced Quantitative Methods and Analytics for Public Policy Support
- Reviewer, AERA 2026 Annual Meeting
- Reviewer, American Causal Inference Conference (ACIC) 2025

# 📖 Educations
- *2022.09 - now*: Ph.D. in Measurement, Evaluation, and Statistics, Teachers College, Columbia University, NY, U.S.
- *2020.09 - 2021.09*: Master of Education in Quantitative Analytics, University of Virginia, VA, U.S.
- *2010.09 - 2024.06*: Bachelor of Science in Physics, Harbin Normal University, Harbin, China.

# 💬 Teaching Experiences
- *2025.09 - 2025.12*, Teaching Assistance for HUDM 5122 Applied Regression Analysis, Columbia University, NY, U.S.
- *2022.09 - 2022.12*, Teaching Assistance for QMSS GR5010 Quantitative Theory in Social Science, Columbia University, NY, U.S.
- *2021.01 - 2021.07*, Instructor of Python Programming and Machine Learning, New Oriental Education & Technology Group, Beijing, China.
- *2013.01 - 2022.07*, Instructor of GRE preparation in verbal and quantitative reasoning (teaching over 7,000 hours for over 10,000 students), New Oriental Education & Technology Group, Beijing, China.

# 💻 Industry Experiences
- *2018.05 - 2022.08*, Deputy Manager of American Graduate Tests Division, Full-time, New Oriental Education & Technology Group, Beijing, China.
- *2014.05 - 2018.05*, Senior Researcher of GRE Instruction and Curriculum Department, Full-time, New Oriental Education & Technology Group, Beijing, China.

