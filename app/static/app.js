async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}`);
  }
  return response.json();
}

function prettyPrint(elementId, payload) {
  document.getElementById(elementId).textContent = JSON.stringify(payload, null, 2);
}

function renderOverview(metrics) {
  const root = document.getElementById('overview-card');
  root.innerHTML = `
    <p class="eyebrow">Demo metrics</p>
    <div class="metric-grid">
      <div class="metric"><span>Products</span><strong>${metrics.products}</strong></div>
      <div class="metric"><span>Parts</span><strong>${metrics.parts}</strong></div>
      <div class="metric"><span>Open changes</span><strong>${metrics.open_changes}</strong></div>
      <div class="metric"><span>Demo cost</span><strong>$${metrics.aggregate_demo_cost_usd}</strong></div>
    </div>
  `;
}

async function loadProducts() {
  const products = await fetchJson('/api/products');
  const select = document.getElementById('product-select');
  select.innerHTML = products
    .map(product => `<option value="${product.id}">${product.name} (${product.id})</option>`)
    .join('');

  const refreshPassport = async () => {
    const passport = await fetchJson(`/api/passports/${select.value}`);
    prettyPrint('passport-output', passport);
  };

  select.addEventListener('change', refreshPassport);
  await refreshPassport();
}

async function loadChanges() {
  const changes = await fetchJson('/api/changes');
  const select = document.getElementById('change-select');
  select.innerHTML = changes
    .map(change => `<option value="${change.id}">${change.title} (${change.id})</option>`)
    .join('');

  const refreshImpact = async () => {
    const impact = await fetchJson(`/api/impact/${select.value}`);
    prettyPrint('impact-output', impact);
  };

  select.addEventListener('change', refreshImpact);
  await refreshImpact();
}

async function boot() {
  const metrics = await fetchJson('/api/overview');
  renderOverview(metrics);
  await Promise.all([loadProducts(), loadChanges()]);
}

boot().catch(error => {
  document.getElementById('overview-card').innerHTML = `<p>${error.message}</p>`;
});
