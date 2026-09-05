/* PythonTools — HUDM 5001 syntax reference.
   Content lives in python-tools/data/*.json (one file per language).
   This file only loads, indexes, routes and renders. No dependencies. */
(function () {
  'use strict';

  var root = document.getElementById('python-tools');
  if (!root) { return; }
  var BASE = root.getAttribute('data-base') || '/python-tools/data/';
  var IMGBASE = BASE.replace(/data\/?$/, '');

  var els = {
    spec: document.getElementById('pt-spec'),
    search: document.getElementById('pt-search'),
    searchClear: document.getElementById('pt-search-clear'),
    viewLang: document.getElementById('pt-view-lang'),
    viewWeek: document.getElementById('pt-view-week'),
    tabs: document.getElementById('pt-tabs'),
    rail: document.getElementById('pt-rail'),
    main: document.getElementById('pt-main'),
    foot: document.getElementById('pt-foot')
  };

  var S = {
    manifest: null, weeks: [], langs: [], langById: {},
    entries: [], byId: {},
    view: 'lang', lang: null, topic: null, week: null, query: '',
    notice: ''
  };

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function pad2(n) { return n < 10 ? '0' + n : String(n); }
  function inline(s) {
    // escape, then turn `code` spans into <code> — the only markup allowed in prose fields
    return esc(s).replace(/`([^`]+)`/g, function (_, c) { return '<code>' + c + '</code>'; });
  }
  function fetchJSON(name) {
    return fetch(BASE + name, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) { throw new Error(name + ': HTTP ' + r.status); }
      return r.json();
    });
  }
  function weekInfo(n) {
    for (var i = 0; i < S.weeks.length; i++) { if (S.weeks[i].week === n) { return S.weeks[i]; } }
    return { week: n, date: '', topic: '' };
  }
  function topicOf(entry) {
    var lang = S.langById[entry.lang];
    for (var i = 0; i < lang.topics.length; i++) { if (lang.topics[i].id === entry.topic) { return lang.topics[i]; } }
    return { id: entry.topic, label: entry.topic };
  }
  function entriesOf(langId, topicId) {
    return S.entries.filter(function (e) { return e.lang === langId && (!topicId || e.topic === topicId); });
  }
  function shortDate(iso) {
    if (!iso) { return ''; }
    var m = /^\d{4}-(\d{2})-(\d{2})/.exec(iso);
    return m ? parseInt(m[1], 10) + '/' + parseInt(m[2], 10) : iso;
  }

  /* ---------- syntax highlighting (restrained) ---------- */
  var KW = {
    python: 'and as assert break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield True False None',
    sql: 'SELECT FROM WHERE GROUP BY ORDER LIMIT JOIN LEFT INNER OUTER RIGHT ON AS AND OR NOT NULL IS IN DISTINCT HAVING DESC ASC CREATE TABLE INSERT INTO VALUES DELETE UPDATE SET DROP IF EXISTS PRIMARY KEY INTEGER TEXT REAL COUNT AVG SUM MIN MAX ROUND BETWEEN LIKE'
  };
  var RX = {};
  function rxFor(lang) {
    if (RX[lang]) { return RX[lang]; }
    var parts = [];
    if (lang === 'sql') { parts.push('(--[^\\n]*)'); } else { parts.push('(#[^\\n]*)'); }
    parts.push('("""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\'|"(?:\\\\.|[^"\\\\\\n])*"|\'(?:\\\\.|[^\'\\\\\\n])*\')');
    parts.push('(\\b\\d+(?:\\.\\d+)?\\b)');
    if (KW[lang]) {
      var words = KW[lang].split(' ').join('|');
      parts.push('(\\b(?:' + words + ')\\b)');
    } else { parts.push('(\\b\\B)'); }
    parts.push('(^[%!][%\\w]+)');
    RX[lang] = new RegExp(parts.join('|'), lang === 'sql' ? 'gmi' : 'gm');
    return RX[lang];
  }
  function highlight(code, lang) {
    var safe = esc(code);
    if (lang === 'markdown' || lang === 'text') { return safe; }
    var rx = rxFor((lang === 'git' || lang === 'workflow' || lang === 'toml' || lang === 'yaml') ? 'shell' : lang);
    return safe.replace(rx, function (m, c, s, n, k, d) {
      if (c) { return '<span class="tk-c">' + c + '</span>'; }
      if (s) { return '<span class="tk-s">' + s + '</span>'; }
      if (n) { return '<span class="tk-n">' + n + '</span>'; }
      if (k) { return '<span class="tk-k">' + k + '</span>'; }
      if (d) { return '<span class="tk-d">' + d + '</span>'; }
      return m;
    });
  }

  /* ---------- rendering ---------- */
  function codeBlock(code, lang, cls, label) {
    return '<div class="pt-code ' + (cls || '') + '">' +
      '<button class="pt-copy" type="button" data-copy aria-label="Copy ' + esc(label || 'code') + '">copy</button>' +
      '<pre><code>' + highlight(code, lang) + '</code></pre></div>';
  }
  function row(label, body, cls) {
    return '<div class="pt-row ' + (cls || '') + '"><div class="pt-label">' + label + '</div><div class="pt-cell">' + body + '</div></div>';
  }
  function chipWeek(w) { return '<span class="pt-chip pt-chip--week">wk ' + pad2(w) + '</span>'; }

  function renderEntry(e) {
    var h = [];
    var tags = e.tags || [];
    h.push('<article class="pt-entry" id="pt-e-' + esc(e.id) + '" data-id="' + esc(e.id) + '">');
    h.push('<header class="pt-entry__head">');
    h.push('<h3 class="pt-entry__title">' + inline(e.title) + '</h3>');
    h.push(chipWeek(e.week));
    if (tags.indexOf('extra') !== -1) { h.push('<span class="pt-chip pt-chip--extra" title="Not taught in a lecture; used in an assignment">extra</span>'); }
    h.push('<a class="pt-entry__id" href="#' + esc(e.id) + '" target="_self" data-copylink title="Copy a link to this entry">' + esc(e.id) + '</a>');
    h.push('</header>');

    var cl = e.code_lang || e.lang;
    if (e.summary) { h.push(row('Summary', '<p>' + inline(e.summary) + '</p>')); }
    if (e.syntax) { h.push(row('Syntax', codeBlock(e.syntax, cl, '', 'syntax'))); }
    if (e.setup) {
      h.push(row('Setup', '<details class="pt-setup"><summary>' + inline(e.setup_note || 'Run this first') + '</summary>' + codeBlock(e.setup, cl, '', 'setup') + '</details>'));
    } else if (e.setup_note) {
      h.push(row('Setup', '<p class="pt-note">' + inline(e.setup_note) + '</p>'));
    }
    (e.files || []).forEach(function (f) {
      var n = f.content.split('\n').length;
      var long = n > 30;
      h.push(row('File', '<details class="pt-file"' + (long ? '' : ' open') + '><summary class="pt-file__path">' + esc(f.path) +
        '<span class="pt-file__n">' + n + ' lines' + (long ? ' · click to ' : '') + '</span></summary>' +
        codeBlock(f.content, f.lang || 'text', '', f.path) + '</details>'));
    });
    if (e.example) { h.push(row('Example', codeBlock(e.example, cl, '', 'example'))); }
    if (e.lines && e.lines.length) {
      h.push(row('Line by line', '<dl class="pt-lines">' + e.lines.map(function (l) {
        return '<div class="pt-line"><dt><code>' + esc(l[0]) + '</code></dt><dd>' + inline(l[1]) + '</dd></div>';
      }).join('') + '</dl>', 'pt-row--lines'));
    }
    if (e.output_html) {
      h.push(row('Renders as', '<div class="pt-rendered">' + e.output_html + '</div>'));
    } else if (e.image) {
      h.push(row('Output', '<figure class="pt-figure"><img src="' + esc(IMGBASE + e.image) + '" alt="Figure produced by the example" loading="lazy"></figure>' +
        (e.output ? codeBlock(e.output, 'text', 'pt-code--output', 'output') : '') +
        (e.output_note ? '<p class="pt-note">' + inline(e.output_note) + '</p>' : '')));
    } else if (e.output) {
      h.push(row('Output', codeBlock(e.output, 'text', 'pt-code--output', 'output') + (e.output_note ? '<p class="pt-note">' + inline(e.output_note) + '</p>' : '')));
    } else if (e.output_note) {
      h.push(row('Output', '<p class="pt-note">' + inline(e.output_note) + '</p>'));
    }
    if (e.gotcha) { h.push(row('Gotcha', '<p class="pt-cell--gotcha">' + inline(e.gotcha) + '</p>')); }
    if (e.related && e.related.length) {
      var links = e.related.map(function (id) {
        var t = S.byId[id];
        if (!t) { return ''; }
        return '<a href="#' + esc(id) + '" target="_self"><span class="pt-related__lang">' + esc(t.lang) + '/</span>' + esc(id.split('/').slice(1).join('/')) + '</a>';
      }).join('');
      if (links) { h.push(row('Related', '<div class="pt-related">' + links + '</div>')); }
    }
    var meta = [];
    if (e.source) { meta.push('Source: ' + inline(e.source)); }
    var ver = S.langById[e.lang] && S.langById[e.lang].verified;
    if (e.manual_run) { meta.push('Output recorded ' + inline(e.manual_run)); }
    else if (ver && e.output && !e.output_html) { meta.push('Output verified ' + esc(ver)); }
    if (meta.length) { h.push(row('Source', '<p>' + meta.join(' · ') + '</p>', 'pt-row--meta')); }
    h.push('</article>');
    return h.join('');
  }

  function renderSpec() {
    var m = S.manifest;
    var weeksWith = {};
    S.entries.forEach(function (e) { weeksWith[e.week] = true; });
    var wk = Object.keys(weeksWith).map(Number).sort(function (a, b) { return a - b; });
    var items = [
      '<span><b>' + esc(m.course) + '</b> · ' + esc(m.term) + '</span>',
      '<span><b>' + S.langs.length + '</b> languages</span>',
      '<span><b>' + S.entries.length + '</b> entries</span>',
      '<span>weeks <b>' + (wk.length ? wk[0] + '–' + wk[wk.length - 1] : '–') + '</b></span>'
    ];
    if (m.verified && m.verified.date) {
      items.push('<span>outputs verified <b>' + esc(m.verified.date) + '</b>' + (m.verified.python ? ' · python ' + esc(m.verified.python) : '') + '</span>');
    }
    els.spec.innerHTML = items.join('');
  }

  function renderTabs() {
    els.tabs.innerHTML = S.langs.map(function (l) {
      var n = entriesOf(l.id).length;
      return '<button class="pt-tab" role="tab" type="button" data-lang="' + esc(l.id) + '" aria-selected="' + (S.view === 'lang' && S.lang === l.id ? 'true' : 'false') + '">' +
        esc(l.label) + '<span class="pt-tab__n">' + n + '</span></button>';
    }).join('');
    els.tabs.hidden = (S.view !== 'lang');
    els.viewLang.setAttribute('aria-pressed', S.view === 'lang' ? 'true' : 'false');
    els.viewWeek.setAttribute('aria-pressed', S.view === 'week' ? 'true' : 'false');
  }

  function renderRail() {
    var h = [];
    if (S.view === 'lang') {
      var lang = S.langById[S.lang];
      h.push('<div class="pt-rail__head">' + esc(lang.label) + ' · topics</div><ul>');
      var opts = [];
      lang.topics.forEach(function (t) {
        var es = entriesOf(lang.id, t.id);
        if (!es.length) { return; }
        var active = t.id === S.topic;
        h.push('<li><a class="pt-rail__topic' + (active ? ' is-active' : '') + '" href="#' + esc(lang.id) + '/t/' + esc(t.id) + '" target="_self">' +
          '<span>' + esc(t.label) + '</span><span class="pt-rail__count">' + es.length + '</span></a>');
        if (active) {
          h.push('<ul class="pt-rail__entries">' + es.map(function (e) {
            return '<li><a class="pt-rail__entry" href="#' + esc(e.id) + '" target="_self">' + inline(e.title) + '</a></li>';
          }).join('') + '</ul>');
        }
        h.push('</li>');
        opts.push('<option value="#' + esc(lang.id) + '/t/' + esc(t.id) + '"' + (active ? ' selected' : '') + '>' + esc(t.label) + ' (' + es.length + ')</option>');
      });
      h.push('</ul>');
      h.push('<select class="pt-select" id="pt-select" aria-label="Topic">' + opts.join('') + '</select>');
    } else {
      h.push('<div class="pt-rail__head">Weeks</div><ul>');
      var opts2 = [];
      S.weeks.forEach(function (w) {
        var n = S.entries.filter(function (e) { return e.week === w.week; }).length;
        var active = w.week === S.week;
        h.push('<li><a class="pt-rail__topic pt-rail__week' + (active ? ' is-active' : '') + (n ? '' : ' is-empty') + '" href="#week/' + w.week + '" target="_self">' +
          '<span class="pt-rail__wk">wk ' + pad2(w.week) + '</span><span>' + esc(w.topic) + '</span><span class="pt-rail__count">' + n + '</span></a></li>');
        opts2.push('<option value="#week/' + w.week + '"' + (active ? ' selected' : '') + '>Week ' + w.week + ' · ' + esc(w.topic) + ' (' + n + ')</option>');
      });
      h.push('</ul>');
      h.push('<select class="pt-select" id="pt-select" aria-label="Week">' + opts2.join('') + '</select>');
    }
    els.rail.innerHTML = h.join('');
    var sel = document.getElementById('pt-select');
    if (sel) { sel.addEventListener('change', function () { go(sel.value); }); }
  }

  function renderMain() {
    var h = [];
    if (S.notice) { h.push('<div class="pt-notice">' + S.notice + '</div>'); S.notice = ''; }
    if (S.query) {
      h.push(renderResults(S.query));
    } else if (S.view === 'lang') {
      var lang = S.langById[S.lang];
      var t = null;
      lang.topics.forEach(function (x) { if (x.id === S.topic) { t = x; } });
      var es = entriesOf(lang.id, S.topic);
      h.push('<div class="pt-topic__head"><h2>' + esc(t ? t.label : S.topic) + '</h2>' +
        '<span class="pt-topic__meta">' + esc(lang.label) + ' · ' + es.length + (es.length === 1 ? ' entry' : ' entries') + (t && t.week ? ' · week ' + t.week : '') + '</span></div>');
      h.push(es.map(renderEntry).join(''));
    } else {
      var w = weekInfo(S.week);
      var wes = S.entries.filter(function (e) { return e.week === S.week; });
      h.push('<div class="pt-week__head"><h2>Week ' + w.week + '</h2><span class="pt-topic__meta">' + esc(shortDate(w.date)) + ' · ' + esc(w.topic) + ' · ' + wes.length + (wes.length === 1 ? ' entry' : ' entries') + '</span></div>');
      if (!wes.length) { h.push('<p class="pt-status">No entries are introduced this week.</p>'); }
      S.langs.forEach(function (l) {
        var les = wes.filter(function (e) { return e.lang === l.id; });
        if (!les.length) { return; }
        h.push('<section class="pt-lang-group"><h2>' + esc(l.label) + '</h2>' + les.map(renderEntry).join('') + '</section>');
      });
    }
    els.main.innerHTML = h.join('');
  }

  /* ---------- search ---------- */
  var FIELDS = [['head', 3], ['title', 5], ['keywords', 4], ['slug', 4], ['syntax', 3], ['summary', 2], ['topicLabel', 2], ['example', 1], ['gotcha', 1]];
  function indexEntry(e) {
    e._idx = {
      title: (e.title || '').toLowerCase(),
      head: (e.title || '').toLowerCase().split(/\s+/)[0],
      keywords: (e.keywords || []).join(' ').toLowerCase(),
      slug: e.id.split('/').slice(1).join(' ').replace(/-/g, ' ').toLowerCase() + ' ' + e.lang,
      syntax: (e.syntax || '').toLowerCase(),
      summary: (e.summary || '').toLowerCase(),
      topicLabel: topicOf(e).label.toLowerCase(),
      example: (e.example || '').toLowerCase(),
      gotcha: (e.gotcha || '').toLowerCase()
    };
  }
  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { return []; }
    var out = [];
    S.entries.forEach(function (e) {
      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        var term = terms[i], hit = 0;
        for (var j = 0; j < FIELDS.length; j++) {
          var f = FIELDS[j];
          if (e._idx[f[0]].indexOf(term) !== -1) { hit += f[1]; }
        }
        if (!hit) { return; }
        score += hit;
      }
      out.push({ e: e, score: score });
    });
    out.sort(function (a, b) { return b.score - a.score || a.e.week - b.e.week; });
    return out;
  }
  function renderResults(q) {
    var res = search(q);
    var h = ['<div class="pt-results__head"><h2>' + res.length + (res.length === 1 ? ' result' : ' results') + '</h2><span class="pt-topic__meta">for “' + esc(q) + '” · all languages</span></div>'];
    if (!res.length) { h.push('<p class="pt-status">Nothing matched. Try a shorter word — e.g. “group”, “join”, “loop”.</p>'); }
    res.slice(0, 60).forEach(function (r) {
      var e = r.e;
      h.push('<a class="pt-result" href="#' + esc(e.id) + '" target="_self">' +
        '<span class="pt-result__lang">' + esc(e.lang) + '</span>' +
        '<span class="pt-result__title">' + inline(e.title) + '</span>' + chipWeek(e.week) +
        (e.syntax ? '<span class="pt-result__syntax">' + esc(e.syntax.split('\n')[0]) + '</span>' : '') +
        '<span class="pt-result__summary">' + inline(e.summary || '') + '</span></a>');
    });
    return h.join('');
  }

  /* ---------- routing ---------- */
  function parseHash() {
    var h = decodeURIComponent((location.hash || '').replace(/^#/, ''));
    var def = { type: 'lang', lang: S.manifest.default_language };
    if (!h) { return def; }
    var parts = h.split('/');
    if (parts[0] === 'week') { return { type: 'week', week: parseInt(parts[1], 10) || 1 }; }
    if (parts[0] === 'search') { return { type: 'search', q: parts.slice(1).join('/') }; }
    if (!S.langById[parts[0]]) { def.missing = h; return def; }
    if (parts.length === 1) { return { type: 'lang', lang: parts[0] }; }
    if (parts[1] === 't') { return { type: 'topic', lang: parts[0], topic: parts[2] }; }
    if (S.byId[h]) { return { type: 'entry', lang: parts[0], id: h }; }
    return { type: 'lang', lang: parts[0], missing: h };
  }
  function firstTopic(langId) {
    var lang = S.langById[langId];
    for (var i = 0; i < lang.topics.length; i++) { if (entriesOf(langId, lang.topics[i].id).length) { return lang.topics[i].id; } }
    return lang.topics.length ? lang.topics[0].id : null;
  }
  function route() {
    var r = parseHash();
    var scrollTo = null;
    if (r.missing) { S.notice = 'No entry at <code>#' + esc(r.missing) + '</code> — showing ' + esc(S.langById[r.lang].label) + ' instead.'; }
    if (r.type === 'search') {
      S.query = r.q; els.search.value = r.q;
      if (!S.lang) { S.lang = S.manifest.default_language; S.topic = firstTopic(S.lang); }
    } else {
      S.query = ''; els.search.value = '';
      if (r.type === 'week') {
        S.view = 'week'; S.week = r.week;
        if (!S.lang) { S.lang = S.manifest.default_language; S.topic = firstTopic(S.lang); }
      } else {
        S.view = 'lang'; S.lang = r.lang;
        if (r.type === 'entry') { S.topic = S.byId[r.id].topic; scrollTo = r.id; }
        else if (r.type === 'topic' && entriesOf(r.lang, r.topic).length) { S.topic = r.topic; }
        else { S.topic = firstTopic(r.lang); }
      }
    }
    els.searchClear.hidden = !S.query;
    renderTabs(); renderRail(); renderMain();
    if (scrollTo) {
      var el = document.getElementById('pt-e-' + scrollTo);
      if (el) {
        el.classList.add('is-target');
        window.requestAnimationFrame(function () { el.scrollIntoView({ block: 'start' }); });
      }
    }
  }
  function go(hash) {
    if (location.hash === hash) { route(); } else { location.hash = hash; }
  }

  /* ---------- events ---------- */
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'pt-toast'; t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 1400);
  }
  function copyLegacy(text) {
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '-1000px';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
      ta.remove();
      if (ok) { resolve(); } else { reject(new Error('copy failed')); }
    });
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { return copyLegacy(text); });
    }
    return copyLegacy(text);
  }
  function flashButton(btn, label) {
    var original = btn.textContent;
    btn.textContent = label; btn.classList.add('is-done');
    setTimeout(function () { btn.textContent = original; btn.classList.remove('is-done'); }, 1300);
  }
  root.addEventListener('click', function (ev) {
    var btn = ev.target.closest('[data-copy]');
    if (btn) {
      var pre = btn.parentNode.querySelector('pre');
      copyText(pre.textContent).then(function () { flashButton(btn, 'copied'); }, function () { flashButton(btn, 'select & copy'); });
      return;
    }
    var link = ev.target.closest('[data-copylink]');
    if (link) {
      ev.preventDefault();
      var url = location.origin + location.pathname + link.getAttribute('href');
      copyText(url).then(function () { toast('link copied'); }, function () { toast('link: ' + url); });
      go(link.getAttribute('href'));
      return;
    }
    var tab = ev.target.closest('.pt-tab');
    if (tab) { go('#' + tab.getAttribute('data-lang')); }
  });
  els.viewLang.addEventListener('click', function () { go('#' + (S.lang || S.manifest.default_language)); });
  els.viewWeek.addEventListener('click', function () {
    var w = S.week;
    if (!w) {
      var es = entriesOf(S.lang, S.topic);
      w = es.length ? es[0].week : 1;
    }
    go('#week/' + w);
  });

  var debounce = null;
  els.search.addEventListener('input', function () {
    clearTimeout(debounce);
    debounce = setTimeout(function () {
      S.query = els.search.value.trim();
      els.searchClear.hidden = !S.query;
      renderMain();
    }, 90);
  });
  els.search.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { els.search.value = ''; S.query = ''; els.searchClear.hidden = true; renderMain(); els.search.blur(); }
  });
  els.searchClear.addEventListener('click', function () { els.search.value = ''; S.query = ''; els.searchClear.hidden = true; renderMain(); els.search.focus(); });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { ev.preventDefault(); els.search.focus(); }
  });
  // author-profile toggle: hides the theme's sidebar column so the reference spans the page
  var profileBtn = document.getElementById('pt-profile-toggle');
  function profileHidden() { return document.documentElement.classList.contains('pt-no-profile'); }
  function renderProfileBtn() {
    if (!profileBtn) { return; }
    var hidden = profileHidden();
    profileBtn.textContent = hidden ? 'Show profile' : 'Hide profile';
    profileBtn.setAttribute('aria-pressed', hidden ? 'true' : 'false');
  }
  if (profileBtn) {
    profileBtn.addEventListener('click', function () {
      document.documentElement.classList.toggle('pt-no-profile');
      try { localStorage.setItem('pt-profile', profileHidden() ? 'hidden' : 'shown'); } catch (e) { /* private mode */ }
      renderProfileBtn();
    });
    renderProfileBtn();
  }

  window.addEventListener('hashchange', route);

  /* ---------- load ---------- */
  fetchJSON('manifest.json').then(function (manifest) {
    S.manifest = manifest;
    return Promise.all([fetchJSON('weeks.json')].concat(manifest.languages.map(function (l) { return fetchJSON(l.file); })))
      .then(function (files) {
        S.weeks = files[0];
        manifest.languages.forEach(function (l, i) {
          var data = files[i + 1];
          var lang = { id: l.id, label: l.label, topics: data.topics || [], verified: data.verified || '' };
          S.langs.push(lang); S.langById[l.id] = lang;
          (data.entries || []).forEach(function (e) {
            e.lang = l.id;
            S.entries.push(e); S.byId[e.id] = e;
          });
        });
        S.entries.forEach(indexEntry);
        renderSpec();
        var foot = manifest.footer ? '<p>' + inline(manifest.footer) + '</p>' : '';
        if (manifest.credit && manifest.credit.text) {
          var c = manifest.credit, credit = esc(c.text);
          if (c.link_text && c.url) {
            credit = credit.replace(esc(c.link_text), '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">' + esc(c.link_text) + '</a>');
          }
          foot += '<p class="pt-foot__credit">' + credit + '</p>';
        }
        els.foot.innerHTML = foot;
        route();
      });
  }).catch(function (err) {
    els.main.innerHTML = '<p class="pt-status">Could not load the reference data (' + esc(err.message) + ').</p>';
  });
})();
