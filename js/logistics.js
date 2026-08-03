/* ============================================================
   SIMIER Logistics & Shipping — Dynamic Data Section
   ============================================================ */

(function () {
  'use strict';

  // ========== CONFIGURATION ==========
  // Set window.SIMIER_LOGISTICS_SHEETS = { routes: 'URL', schedule: 'URL', rail: 'URL', comparison: 'URL' }
  // to use Google Sheets. Otherwise embedded sample data is used.

  var CACHE_KEY = 'simier_logistics';
  var CACHE_TTL = 4 * 60 * 60 * 1000; // 4 hours

  // ========== EMBEDDED SAMPLE DATA (fallback) ==========
  var SAMPLE = {
    routes: [
      {region:'USA',sub:'West Coast · Los Angeles / Long Beach',transit:'18–22 days',method:'FCL Container · Sea Freight',path:'Foshan → Shenzhen (Yantian) → Pacific Route → Long Beach, CA',departure:'Shenzhen (Yantian)',arrival:'Long Beach, CA',highlight:'TRUE'},
      {region:'USA',sub:'East Coast · New York / Savannah',transit:'28–35 days',method:'FCL Container · Sea Freight',path:'Foshan → Shenzhen → Panama Canal → Savannah / NY',departure:'Shenzhen (Shekou)',arrival:'Savannah, GA / New York, NY',highlight:'FALSE'},
      {region:'Turkey',sub:'Istanbul · Mersin',transit:'22–25 days',method:'FCL / LCL · Sea Freight',path:'Foshan → Shenzhen → Suez Canal → Mersin / Istanbul',departure:'Shenzhen (Yantian)',arrival:'Mersin / Istanbul',highlight:'TRUE'},
      {region:'France',sub:'Marseille · Le Havre',transit:'28–32 days',method:'FCL / LCL · Sea Freight',path:'Foshan → Shenzhen → Suez Canal → Mediterranean → Marseille',departure:'Shenzhen (Yantian)',arrival:'Marseille / Le Havre',highlight:'FALSE'}
    ],
    schedule: [
      {vessel:'EVER FORTUNE',voyage:'0456W',departure_port:'Shenzhen (Yantian)',departure_date:'2026-08-15',cutoff_date:'2026-08-12',arrival_port:'Long Beach, CA',eta:'2026-09-05',status:'On Schedule',notes:'Early booking advised'},
      {vessel:'COSCO SHIPPING ARIES',voyage:'0123E',departure_port:'Shenzhen (Shekou)',departure_date:'2026-08-18',cutoff_date:'2026-08-15',arrival_port:'Savannah, GA',eta:'2026-09-20',status:'On Schedule',notes:''},
      {vessel:'CMA CGM JEAN MERMOZ',voyage:'089F',departure_port:'Shenzhen (Yantian)',departure_date:'2026-08-22',cutoff_date:'2026-08-19',arrival_port:'Marseille, France',eta:'2026-09-22',status:'On Schedule',notes:'Weekly service'},
      {vessel:'MSC DIANA',voyage:'345T',departure_port:'Shenzhen (Yantian)',departure_date:'2026-08-25',cutoff_date:'2026-08-22',arrival_port:'Mersin, Turkey',eta:'2026-09-18',status:'On Schedule',notes:''},
      {vessel:'MAERSK SEOUL',voyage:'678W',departure_port:'Shenzhen (Yantian)',departure_date:'2026-09-01',cutoff_date:'2026-08-28',arrival_port:'Long Beach, CA',eta:'2026-09-22',status:'Delayed',notes:'Port congestion — check back for updates'}
    ],
    rail: [
      {name:'Yiwu–Madrid Line',origin:'Yiwu, China',destination:'Madrid, Spain / Paris, France',transit:'16–18 days',frequency:'Weekly, every Friday',stops:'Alashankou → Kazakhstan → Russia → Belarus → Poland → Germany → France',cargo:'FCL & LCL',departure_schedule:'Aug: 7, 14, 21, 28 | Sep: 4, 11, 18, 25',best_for:'Cost-sensitive European orders, medium lead time'},
      {name:'Wuhan–Lyon Line',origin:'Wuhan, China',destination:'Lyon, France / Dourges',transit:'15–17 days',frequency:'Bi-weekly, Wed & Sat',stops:'Alashankou → Dostyk → Russia → Belarus → Poland → Germany → France',cargo:'FCL & LCL',departure_schedule:'Aug: 6, 9, 20, 23 | Sep: 3, 6, 17, 20',best_for:'Central Europe distribution, furniture in KD/flat-pack'},
      {name:'Chengdu–Istanbul Line',origin:'Chengdu, China',destination:'Istanbul, Turkey',transit:'12–14 days',frequency:'Weekly, every Tuesday',stops:'Khorgos → Altynkol → Kazakhstan → Caspian Sea → Baku → Tbilisi → Istanbul',cargo:'FCL',departure_schedule:'Aug: 4, 11, 18, 25 | Sep: 1, 8, 15, 22, 29',best_for:'Turkish market, bypasses Suez Canal congestion'}
    ],
    comparison: [
      {mode:'Sea Freight (FCL)',transit:'18–35 days',cost:'$$',best:'Full container loads, large orders, USA/Europe restocking',min_volume:'15–20 cbm minimum',tracking:'Full container tracking via bill of lading'},
      {mode:'Rail Freight',transit:'12–18 days',cost:'$$$',best:'Europe & Turkey orders, medium volume, faster than sea',min_volume:'5–10 cbm minimum',tracking:'Container tracking via rail waybill'},
      {mode:'Air Freight',transit:'3–7 days',cost:'$$$$',best:'Sample orders, urgent restocking, small high-value items',min_volume:'No minimum, per-kg pricing',tracking:'Real-time AWB tracking'}
    ]
  };

  // ========== CSV PARSER ==========
  function parseCSV(text) {
    var rows = [];
    var lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return rows;
    var headers = lines[0].split(',').map(function(h) { return h.trim().toLowerCase().replace(/[^a-z0-9_]/g,'_'); });
    for (var i = 1; i < lines.length; i++) {
      var cols = [];
      var current = '', inQuotes = false;
      for (var j = 0; j < lines[i].length; j++) {
        var ch = lines[i][j];
        if (ch === '"') { inQuotes = !inQuotes; }
        else if (ch === ',' && !inQuotes) { cols.push(current.trim()); current = ''; }
        else { current += ch; }
      }
      cols.push(current.trim());
      var row = {};
      for (var k = 0; k < headers.length; k++) {
        row[headers[k]] = cols[k] || '';
      }
      rows.push(row);
    }
    return rows;
  }

  // ========== FETCH ==========
  function fetchCSV(url) {
    return new Promise(function(resolve, reject) {
      var controller = new AbortController();
      var timer = setTimeout(function() { controller.abort(); }, 10000);
      fetch(url, { signal: controller.signal })
        .then(function(r) {
          clearTimeout(timer);
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.text();
        })
        .then(function(text) { resolve(parseCSV(text)); })
        .catch(function(e) { reject(e); });
    });
  }

  function getData() {
    // Check cache
    try {
      var cached = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      if (cached && Date.now() - cached.t < CACHE_TTL) {
        return Promise.resolve(cached.d);
      }
    } catch(e) {}

    // If Google Sheet URLs configured, fetch them
    var config = window.SIMIER_LOGISTICS_SHEETS;
    if (config && config.routes) {
      return Promise.allSettled([
        fetchCSV(config.routes),
        fetchCSV(config.schedule || config.routes),
        fetchCSV(config.rail || config.routes),
        fetchCSV(config.comparison || config.routes)
      ]).then(function(results) {
        var data = {
          routes: results[0].status === 'fulfilled' && results[0].value.length > 0 ? results[0].value : SAMPLE.routes,
          schedule: results[1].status === 'fulfilled' && results[1].value.length > 0 ? results[1].value : SAMPLE.schedule,
          rail: results[2].status === 'fulfilled' && results[2].value.length > 0 ? results[2].value : SAMPLE.rail,
          comparison: results[3].status === 'fulfilled' && results[3].value.length > 0 ? results[3].value : SAMPLE.comparison
        };
        try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({t: Date.now(), d: data})); } catch(e) {}
        return data;
      });
    }

    // Use sample data
    var sampleData = {
      routes: SAMPLE.routes,
      schedule: SAMPLE.schedule,
      rail: SAMPLE.rail,
      comparison: SAMPLE.comparison
    };
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({t: Date.now(), d: sampleData})); } catch(e) {}
    return Promise.resolve(sampleData);
  }

  // ========== i18n HELPERS ==========
  function t(key, fallback) {
    try {
      var lang = localStorage.getItem('simier_lang') || 'en';
      if (window.SIMIER_i18n && window.SIMIER_i18n.translations) {
        var tr = window.SIMIER_i18n.translations;
        return (tr[lang] && tr[lang][key]) || (tr['en'] && tr['en'][key]) || fallback || key;
      }
    } catch(e) {}
    return fallback || key;
  }

  function statusLabel(status) {
    var map = {
      'on schedule': t('logistics.status.on_schedule', 'On Schedule'),
      'delayed': t('logistics.status.delayed', 'Delayed'),
      'departed': t('logistics.status.departed', 'Departed'),
      'deprecated': t('logistics.status.deprecated', 'Deprecated')
    };
    return map[status.toLowerCase()] || status;
  }

  // ========== RENDERERS ==========
  function renderRoutes(container, routes) {
    if (!routes || routes.length === 0) {
      container.innerHTML = '<p class="logistics__empty">No route data available.</p>';
      return;
    }
    var html = '';
    routes.forEach(function(r) {
      var highlight = (r.highlight || '').toUpperCase() === 'TRUE' ? ' logistics__route-card--highlight' : '';
      html += '<div class="logistics__route-card reveal' + highlight + '">';
      html += '<div class="logistics__route-card__region">' + (r.region || r.sub_region || '') + '</div>';
      html += '<div class="logistics__route-card__sub">' + (r.sub || r.sub_region || '') + '</div>';
      html += '<div class="logistics__route-card__transit">' + (r.transit || r.transit_days || '') + '</div>';
      html += '<div class="logistics__route-card__label">Transit Time</div>';
      html += '<div class="logistics__route-card__path">' + (r.path || r.route_path || '') + '</div>';
      html += '<div class="logistics__route-card__ports"><span>' + (r.departure || r.port_of_departure || '') + '</span> → <span>' + (r.arrival || r.port_of_arrival || '') + '</span></div>';
      html += '<div class="logistics__route-card__method">' + (r.method || r.shipping_method || '') + '</div>';
      html += '</div>';
    });
    container.innerHTML = html;
  }

  function renderSchedule(container, schedule) {
    if (!schedule || schedule.length === 0) {
      container.innerHTML = '<p class="logistics__empty">No schedule data available.</p>';
      return;
    }
    // Sort by departure date
    schedule.sort(function(a, b) { return (a.departure_date || '') > (b.departure_date || '') ? 1 : -1; });
    // Filter: show upcoming only (departure >= yesterday)
    var yesterday = new Date(); yesterday.setDate(yesterday.getDate() - 1);
    var yStr = yesterday.toISOString().slice(0,10);
    var upcoming = schedule.filter(function(s) { return (s.departure_date || '') >= yStr; });
    if (upcoming.length === 0) { container.innerHTML = '<p class="logistics__empty">No upcoming departures.</p>'; return; }
    var html = '';
    upcoming.forEach(function(s) {
      var statusClass = (s.status || 'on schedule').toLowerCase().replace(/\s+/g, '-');
      html += '<tr class="reveal">';
      html += '<td><strong>' + (s.vessel || s.vessel_name || '') + '</strong><br><small>' + (s.voyage || s.voyage_number || '') + '</small></td>';
      html += '<td>' + formatDate(s.departure_date) + '<br><small>' + (s.departure_port || '') + '</small></td>';
      html += '<td>' + formatDate(s.cutoff_date) + '</td>';
      html += '<td>' + (s.arrival_port || '') + '</td>';
      html += '<td>' + formatDate(s.eta) + '</td>';
      html += '<td><span class="logistics__status logistics__status--' + statusClass + '">' + statusLabel(s.status) + '</span></td>';
      html += '</tr>';
    });
    container.innerHTML = html;
  }

  function renderRail(container, rail) {
    if (!rail || rail.length === 0) {
      container.innerHTML = '<p class="logistics__empty">No rail data available.</p>';
      return;
    }
    var html = '';
    rail.forEach(function(r) {
      html += '<div class="logistics__rail-card reveal">';
      html += '<h3 class="logistics__rail-card__name">' + (r.name || r.rail_route_name || '') + '</h3>';
      html += '<div class="logistics__rail-card__meta">';
      html += '<div><span>Route</span><span>' + (r.origin || '') + ' → ' + (r.destination || '') + '</span></div>';
      html += '<div><span>Transit</span><span>' + (r.transit || r.transit_days || '') + '</span></div>';
      html += '<div><span>Frequency</span><span>' + (r.frequency || '') + '</span></div>';
      html += '<div><span>Key Stops</span><span>' + (r.stops || r.key_stops || '') + '</span></div>';
      html += '<div><span>Departures</span><span>' + (r.departure_schedule || '') + '</span></div>';
      html += '<div><span>Cargo</span><span>' + (r.cargo || r.cargo_type || '') + '</span></div>';
      if (r.best_for) html += '<div><span>Best For</span><span>' + r.best_for + '</span></div>';
      html += '</div></div>';
    });
    container.innerHTML = html;
  }

  function renderComparison(container, comparison) {
    if (!comparison || comparison.length === 0) {
      container.innerHTML = '<p class="logistics__empty">No comparison data available.</p>';
      return;
    }
    var html = '<div class="logistics__compare-row logistics__compare-row--header">';
    html += '<div>' + t('logistics.compare.mode', 'Shipping Mode') + '</div>';
    html += '<div>' + t('logistics.compare.transit', 'Transit Time') + '</div>';
    html += '<div>' + t('logistics.compare.cost', 'Cost Level') + '</div>';
    html += '<div>' + t('logistics.compare.best', 'Best For') + '</div>';
    html += '</div>';
    comparison.forEach(function(c) {
      var mode = c.mode || c.shipping_mode || '';
      var transit = c.transit || c.transit_time || '';
      var costRaw = (c.cost || c.cost_level || '$$');
      var best = c.best || c.best_for || '';
      var tracking = c.tracking || '';
      var costHTML = '';
      for (var i = 0; i < costRaw.length; i++) { costHTML += '<span>' + costRaw[i] + '</span>'; }
      html += '<div class="logistics__compare-row reveal">';
      html += '<div class="logistics__compare__mode"><strong>' + mode + '</strong><br><small>' + tracking + '</small></div>';
      html += '<div class="logistics__compare__transit">' + transit + '</div>';
      html += '<div class="logistics__compare__cost">' + costHTML + '</div>';
      html += '<div class="logistics__compare__best">' + best + '</div>';
      html += '</div>';
    });
    container.innerHTML = html;
  }

  function formatDate(dateStr) {
    if (!dateStr) return '—';
    try {
      var d = new Date(dateStr + 'T00:00:00');
      if (isNaN(d.getTime())) return dateStr;
      var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      return months[d.getMonth()] + ' ' + d.getDate();
    } catch(e) { return dateStr; }
  }

  // ========== TAB SWITCHING ==========
  function setupTabs(section) {
    var tabs = section.querySelectorAll('.logistics__tab');
    var panels = section.querySelectorAll('.logistics__panel');
    var spinner = section.querySelector('.logistics__loading-indicator');
    var error = section.querySelector('.logistics__error');

    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        var target = tab.getAttribute('data-tab');
        tabs.forEach(function(t) { t.classList.remove('logistics__tab--active'); t.setAttribute('aria-selected','false'); });
        tab.classList.add('logistics__tab--active');
        tab.setAttribute('aria-selected','true');
        panels.forEach(function(p) {
          if (p.getAttribute('data-content') === target) {
            p.hidden = false;
            p.classList.add('logistics__panel--active');
            // Observe new reveal elements
            p.querySelectorAll('.reveal').forEach(function(el) {
              observeReveal(el);
            });
          } else {
            p.hidden = true;
            p.classList.remove('logistics__panel--active');
          }
        });
      });
    });

    // Restore last active tab from session
    try {
      var lastTab = sessionStorage.getItem('simier_logistics_tab');
      if (lastTab) {
        var tab = section.querySelector('.logistics__tab[data-tab="' + lastTab + '"]');
        if (tab) tab.click();
      }
    } catch(e) {}

    // Save tab on switch
    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        try { sessionStorage.setItem('simier_logistics_tab', tab.getAttribute('data-tab')); } catch(e) {}
      });
    });
  }

  // ========== REVEAL OBSERVER ==========
  var revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); }
    });
  }, { rootMargin: '60px', threshold: 0.1 });

  function observeReveal(el) {
    if (!el.classList.contains('reveal--observed')) {
      el.classList.add('reveal--observed');
      revealObserver.observe(el);
    }
  }

  // ========== INIT ==========
  function init() {
    var section = document.getElementById('logistics');
    if (!section) return;

    // Show loading
    section.classList.add('logistics--loading');
    var errorEl = section.querySelector('.logistics__error');
    if (errorEl) errorEl.hidden = true;

    // Setup tabs
    setupTabs(section);

    // Fetch data
    getData().then(function(data) {
      // Route cards
      var routeGrid = section.querySelector('[data-content="routes"] .logistics__route-grid');
      if (routeGrid) renderRoutes(routeGrid, data.routes);

      // Schedule
      var scheduleBody = section.querySelector('[data-content="schedule"] tbody');
      if (scheduleBody) renderSchedule(scheduleBody, data.schedule);

      // Rail
      var railGrid = section.querySelector('[data-content="rail"] .logistics__rail-grid');
      if (railGrid) renderRail(railGrid, data.rail);

      // Comparison
      var compareDiv = section.querySelector('[data-content="comparison"] .logistics__compare');
      if (compareDiv) renderComparison(compareDiv, data.comparison);

      // Observe reveal elements in active panel
      var activePanel = section.querySelector('.logistics__panel--active');
      if (activePanel) {
        activePanel.querySelectorAll('.reveal').forEach(function(el) { observeReveal(el); });
      }

      // Observe section header reveals
      section.querySelectorAll('.reveal').forEach(function(el) { observeReveal(el); });

      // Done loading
      section.classList.remove('logistics--loading');
      section.classList.add('logistics--loaded');
    }).catch(function() {
      section.classList.remove('logistics--loading');
      section.classList.add('logistics--error');
      if (errorEl) errorEl.hidden = false;
    });

    // Retry button
    var retryBtn = section.querySelector('.logistics__retry');
    if (retryBtn) {
      retryBtn.addEventListener('click', function() {
        section.classList.remove('logistics--error');
        section.classList.remove('logistics--loaded');
        try { sessionStorage.removeItem(CACHE_KEY); } catch(e) {}
        init();
      });
    }
  }

  // Start on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
