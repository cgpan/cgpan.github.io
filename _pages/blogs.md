---
permalink: /stats-tools/
title: "StatsTools"
excerpt: ""
author_profile: true
---

<style>
	.stats-tools {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 0 2.5rem;
	}
	.stats-tools__hero {
		margin-bottom: 1.75rem;
	}
	.stats-tools__hero h1 {
		margin: 0 0 0.4rem 0;
		font-size: 2.2rem;
	}
	.stats-tools__hero p {
		margin: 0;
		color: #4b5563;
		font-size: 1.05rem;
	}
	.stats-tools__grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 1.25rem;
	}
	.stats-card {
		border: 1px solid #e5e7eb;
		border-radius: 16px;
		padding: 1.25rem;
		background: #ffffff;
		box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}
	.stats-card h3 {
		margin: 0;
		font-size: 1.15rem;
	}
	.stats-card p {
		margin: 0;
		color: #6b7280;
		font-size: 0.98rem;
	}
	.stats-card__meta {
		font-size: 0.85rem;
		color: #9ca3af;
	}
	.stats-card__link {
		margin-top: 0.5rem;
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		color: #2563eb;
		font-weight: 600;
		text-decoration: none;
	}
	.stats-card__link:hover {
		text-decoration: underline;
	}
</style>

<div class="stats-tools">
	<div class="stats-tools__hero">
		<h1>StatsTools</h1>
		<p>Interactive tools for statistics and teaching.</p>
	</div>

	<div class="stats-tools__grid">
		<article class="stats-card">
			<h3>Sampling Distributions & Standard Error</h3>
			<p>Explore how sampling distributions behave as the sample size $n$ changes.</p>
			<div class="stats-card__meta">HTML interactive tool</div>
			<a class="stats-card__link" href="/stats-tools/sampling-and-se.html">Open tool →</a>
		</article>
		<article class="stats-card">
			<h3>t-Distribution Explorer</h3>
			<p>Compute p-values, critical t-values, and inspect a t-table for common significance levels.</p>
			<div class="stats-card__meta">HTML interactive tool</div>
			<a class="stats-card__link" href="/stats-tools/t-distribution-explorer.html">Open tool →</a>
		</article>
		<article class="stats-card">
			<h3>Simple Linear Regression Explorer</h3>
			<p>See how sampling, fitted lines, residuals, and MSE behave in a simple linear regression.</p>
			<div class="stats-card__meta">HTML interactive tool</div>
			<a class="stats-card__link" href="/stats-tools/simple-linear-regression-explorer.html">Open tool →</a>
		</article>
	</div>
</div>
