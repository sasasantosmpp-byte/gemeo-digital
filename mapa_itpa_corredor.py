import streamlit as st
import folium
from streamlit_folium import st_folium

# ── Configuração da Página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="ITPA · Corredor Tinguá-Bocaina",
    page_icon="🌿",
    layout="wide",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
      background-color: #f5f7f2;
      color: #1a2e1a;
  }
  .main { background-color: #f5f7f2; }

  .header-box {
      background: linear-gradient(135deg, #1a4d2e 0%, #2d6a4f 100%);
      border-radius: 16px;
      padding: 1.8rem 2.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 1.5rem;
  }
  .header-box h1 {
      font-family: 'Syne', sans-serif;
      font-size: 1.9rem;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 0.3rem 0;
  }
  .header-box p { color: #b7d4c0; margin: 0; font-size: 0.9rem; }

  .stat-card {
      background: white;
      border: 1px solid #d4e8d4;
      border-radius: 12px;
      padding: 1.2rem;
      text-align: center;
      box-shadow: 0 2px 8px #1a4d2e12;
  }
  .stat-card .valor {
      font-family: 'Syne', sans-serif;
      font-size: 1.7rem;
      font-weight: 800;
      color: #1a4d2e;
  }
  .stat-card .label { font-size: 0.78rem; color: #5a7a5a; text-transform: uppercase; letter-spacing: 0.06em; }

  .legenda-box {
      background: white;
      border: 1px solid #d4e8d4;
      border-radius: 12px;
      padding: 1.2rem 1.5rem;
      box-shadow: 0 2px 8px #1a4d2e12;
  }
  .legenda-box h4 {
      font-family: 'Syne', sans-serif;
      font-weight: 700;
      color: #1a4d2e;
      margin: 0 0 0.8rem 0;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
  }
  .legenda-item {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.5rem;
      font-size: 0.84rem;
      color: #2d4a2d;
  }
  .dot { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
  <div style="font-size:3.5rem;">🌿</div>
  <div>
    <h1>Corredor de Biodiversidade Tinguá-Bocaina</h1>
    <p>Instituto Terra de Preservação Ambiental (ITPA) · 195 mil hectares · 9 municípios fluminenses · Mata Atlântica</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Métricas ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
stats = [
    ("🌳", "5 milhões", "Árvores Plantadas"),
    ("🔄", "12,3 milhões", "Árvores em Regeneração"),
    ("🏞️", "100 mil ha", "Hectares Protegidos"),
    ("🌱", "165.000", "Mudas em Manguezais"),
    ("👷", "+1.000", "Postos de Trabalho Verde"),
]
for col, (icon, val, label) in zip([c1, c2, c3, c4, c5], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
          <div style="font-size:1.5rem;">{icon}</div>
          <div class="valor">{val}</div>
          <div class="label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Dados dos Municípios do Corredor ─────────────────────────────────────────
# Coordenadas geográficas reais (sedes municipais) dos 9 municípios do CBTB
municipios = [
    {
        "nome": "Miguel Pereira",
        "lat": -22.4546, "lon": -43.4716,
        "desc": "Principal município de atuação do ITPA. Sede da organização e maior empregador local.",
        "arvores": "1.2M",
        "area_ha": 28.000,
        "tipo": "sede",
    },
    {
        "nome": "Vassouras",
        "lat": -22.4039, "lon": -43.6636,
        "desc": "Município histórico integrante do Corredor Tinguá-Bocaina.",
        "arvores": "450K",
        "area_ha": 17.500,
        "tipo": "corredor",
    },
    {
        "nome": "Paty do Alferes",
        "lat": -22.4267, "lon": -43.4289,
        "desc": "Município vizinho a Miguel Pereira, parte essencial do corredor ecológico.",
        "arvores": "380K",
        "area_ha": 14.200,
        "tipo": "corredor",
    },
    {
        "nome": "Barra do Piraí",
        "lat": -22.4706, "lon": -43.8256,
        "desc": "Município na bacia do Rio Paraíba do Sul, integrado ao corredor.",
        "arvores": "310K",
        "area_ha": 12.800,
        "tipo": "corredor",
    },
    {
        "nome": "Piraí",
        "lat": -22.6289, "lon": -43.8994,
        "desc": "Área de transição entre o corredor e o Parque Nacional da Serra da Bocaina.",
        "arvores": "290K",
        "area_ha": 11.500,
        "tipo": "corredor",
    },
    {
        "nome": "Paracambi",
        "lat": -22.6111, "lon": -43.7111,
        "desc": "Município da baixada, com foco em restauração de matas ciliares.",
        "arvores": "420K",
        "area_ha": 16.000,
        "tipo": "corredor",
    },
    {
        "nome": "Eng. Paulo de Frontin",
        "lat": -22.5394, "lon": -43.6794,
        "desc": "Pequeno município com alta cobertura florestal relativa.",
        "arvores": "180K",
        "area_ha": 8.700,
        "tipo": "corredor",
    },
    {
        "nome": "Mendes",
        "lat": -22.5242, "lon": -43.7303,
        "desc": "Município integrante do corredor com projetos de agricultura sustentável.",
        "arvores": "160K",
        "area_ha": 7.900,
        "tipo": "corredor",
    },
    {
        "nome": "Rio Claro",
        "lat": -22.7200, "lon": -44.1400,
        "desc": "Município limítrofe ao Parque Nacional da Serra da Bocaina, extremo sul do corredor.",
        "arvores": "610K",
        "area_ha": 22.400,
        "tipo": "corredor",
    },
]

# Unidades de Conservação do corredor
ucs = [
    {"nome": "Reserva Biológica do Tinguá",      "lat": -22.5500, "lon": -43.4800, "tipo": "protecao_integral"},
    {"nome": "Parque Nacional Serra da Bocaina",  "lat": -22.7500, "lon": -44.6000, "tipo": "protecao_integral"},
    {"nome": "APA do Rio Guandu",                 "lat": -22.6200, "lon": -43.5500, "tipo": "uso_sustentavel"},
    {"nome": "RPPN Serra do Palmital",            "lat": -22.4800, "lon": -43.5200, "tipo": "rppn"},
    {"nome": "APA Tinguá-Bocaina",                "lat": -22.5900, "lon": -44.0000, "tipo": "uso_sustentavel"},
]

# ── Mapa Folium ───────────────────────────────────────────────────────────────
col_mapa, col_info = st.columns([3, 1])

with col_mapa:
    st.markdown("#### 🗺️ Mapa Interativo do Corredor")

    m = folium.Map(
        location=[-22.5700, -43.7500],
        zoom_start=9,
        tiles="CartoDB positron",
    )

    # Polígono aproximado do Corredor Tinguá-Bocaina
    corredor_coords = [
        [-22.38, -43.35], [-22.35, -43.55], [-22.38, -43.72],
        [-22.42, -43.85], [-22.50, -44.00], [-22.58, -44.20],
        [-22.65, -44.45], [-22.75, -44.65], [-22.82, -44.55],
        [-22.75, -44.30], [-22.68, -44.05], [-22.62, -43.85],
        [-22.55, -43.65], [-22.50, -43.45], [-22.45, -43.30],
        [-22.40, -43.28], [-22.38, -43.35],
    ]

    folium.Polygon(
        locations=corredor_coords,
        color="#2d6a4f",
        weight=2,
        fill=True,
        fill_color="#52b788",
        fill_opacity=0.18,
        tooltip="Corredor de Biodiversidade Tinguá-Bocaina (195 mil ha)",
    ).add_to(m)

    # Marcadores dos municípios
    for mun in municipios:
        cor = "#d62828" if mun["tipo"] == "sede" else "#2d6a4f"
        icone = "star" if mun["tipo"] == "sede" else "leaf"
        popup_html = f"""
        <div style="font-family:Inter,sans-serif; width:200px;">
          <b style="color:{cor}; font-size:1rem;">📍 {mun['nome']}</b><br>
          <hr style="margin:6px 0; border-color:#d4e8d4;">
          <span style="font-size:0.82rem; color:#444;">{mun['desc']}</span><br><br>
          <span style="background:#e8f5e9; padding:2px 8px; border-radius:4px; font-size:0.78rem; color:#1a4d2e;">
            🌳 {mun['arvores']} árvores
          </span>
          <span style="background:#e3f2fd; padding:2px 8px; border-radius:4px; font-size:0.78rem; color:#1565c0; margin-left:4px;">
            🏞️ {mun['area_ha']:,.0f} ha
          </span>
        </div>
        """
        folium.Marker(
            location=[mun["lat"], mun["lon"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=mun["nome"],
            icon=folium.Icon(color="red" if mun["tipo"] == "sede" else "green", icon=icone, prefix="fa"),
        ).add_to(m)

    # Marcadores das UCs
    cor_uc = {
        "protecao_integral": ("#1565c0", "shield", "darkblue"),
        "uso_sustentavel":   ("#e65100", "tree",   "orange"),
        "rppn":              ("#6a1b9a", "home",   "purple"),
    }
    for uc in ucs:
        hex_c, icone_uc, folium_cor = cor_uc[uc["tipo"]]
        folium.CircleMarker(
            location=[uc["lat"], uc["lon"]],
            radius=9,
            color=hex_c,
            fill=True,
            fill_color=hex_c,
            fill_opacity=0.75,
            tooltip=uc["nome"],
            popup=folium.Popup(f"<b style='color:{hex_c}'>{uc['nome']}</b><br><small>Unidade de Conservação</small>", max_width=200),
        ).add_to(m)

    # Linha do Rio Guandu (esquemática)
    guandu = [
        [-22.60, -43.48], [-22.62, -43.55], [-22.64, -43.62],
        [-22.66, -43.72], [-22.68, -43.82],
    ]
    folium.PolyLine(
        locations=guandu,
        color="#0077b6",
        weight=3,
        opacity=0.6,
        tooltip="Bacia Hidrográfica do Rio Guandu",
        dash_array="6 4",
    ).add_to(m)

    st_folium(m, width=None, height=540, use_container_width=True)

with col_info:
    # Legenda
    st.markdown("""
    <div class="legenda-box">
      <h4>Legenda</h4>

      <div class="legenda-item">
        <div class="dot" style="background:#d62828;"></div>
        <span>Sede ITPA (Miguel Pereira)</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#2d6a4f;"></div>
        <span>Municípios do Corredor</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#52b788; border:2px solid #2d6a4f;"></div>
        <span>Corredor Tinguá-Bocaina</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#1565c0;"></div>
        <span>UC Proteção Integral</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#e65100;"></div>
        <span>UC Uso Sustentável</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#6a1b9a;"></div>
        <span>RPPN</span>
      </div>
      <div class="legenda-item">
        <div class="dot" style="background:#0077b6; border-radius:2px; height:4px; margin-top:5px;"></div>
        <span>Rio Guandu</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Lista de municípios
    st.markdown("""
    <div class="legenda-box">
      <h4>9 Municípios do CBTB</h4>
    """, unsafe_allow_html=True)
    for mun in municipios:
        cor = "#d62828" if mun["tipo"] == "sede" else "#2d6a4f"
        st.markdown(f"""
      <div class="legenda-item">
        <div class="dot" style="background:{cor};"></div>
        <span><strong>{mun['nome']}</strong> — {mun['arvores']}</span>
      </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#5a7a5a; font-size:0.78rem; border-top:1px solid #d4e8d4; padding-top:1rem;">
  Fonte: <a href="https://www.itpa.org.br/onde-atuamos/" target="_blank" style="color:#2d6a4f;">ITPA · itpa.org.br</a> ·
  Corredor de Biodiversidade Tinguá-Bocaina · Mata Atlântica · Rio de Janeiro, RJ
</div>
""", unsafe_allow_html=True)
