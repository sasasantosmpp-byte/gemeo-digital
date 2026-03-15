import streamlit as st
import pandas as pd
import numpy as np

# ── Configuração da Página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Gêmeo Digital · Miguel Pereira",
    page_icon="🌿",
    layout="wide",
)

# ── CSS Customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
      background-color: #0d1117;
      color: #e6edf3;
  }

  .main { background-color: #0d1117; }

  h1, h2, h3 { font-family: 'Syne', sans-serif; }

  .header-box {
      background: linear-gradient(135deg, #1a2d1a 0%, #0f2318 60%, #0d1117 100%);
      border: 1px solid #2ea84340;
      border-radius: 16px;
      padding: 2rem 2.5rem;
      margin-bottom: 2rem;
  }
  .header-box h1 {
      font-size: 2.4rem;
      font-weight: 800;
      background: linear-gradient(90deg, #2ea843, #7ee89a);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0 0 0.3rem 0;
  }
  .header-box p {
      color: #8b949e;
      margin: 0;
      font-weight: 300;
      font-size: 0.95rem;
  }

  .alerta-ok {
      background: linear-gradient(135deg, #0d2818, #0f3320);
      border: 1.5px solid #2ea843;
      border-radius: 12px;
      padding: 1.2rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 1rem;
  }
  .alerta-ok .icon { font-size: 2rem; }
  .alerta-ok .titulo { font-family: 'Syne', sans-serif; font-weight: 700; color: #2ea843; font-size: 1.05rem; }
  .alerta-ok .desc { color: #7ee89a; font-size: 0.88rem; margin-top: 2px; }

  .alerta-perigo {
      background: linear-gradient(135deg, #2d0d0d, #3d1010);
      border: 1.5px solid #f85149;
      border-radius: 12px;
      padding: 1.2rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 1rem;
      animation: pulso 1.8s ease-in-out infinite;
  }
  .alerta-perigo .icon { font-size: 2rem; }
  .alerta-perigo .titulo { font-family: 'Syne', sans-serif; font-weight: 700; color: #f85149; font-size: 1.05rem; }
  .alerta-perigo .desc { color: #ffa198; font-size: 0.88rem; margin-top: 2px; }

  @keyframes pulso {
      0%, 100% { box-shadow: 0 0 0px #f8514900; }
      50%       { box-shadow: 0 0 18px #f8514966; }
  }

  .card-metrica {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 1.4rem;
      text-align: center;
  }
  .card-metrica .label {
      font-size: 0.78rem;
      color: #8b949e;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0.4rem;
  }
  .card-metrica .valor {
      font-family: 'Syne', sans-serif;
      font-size: 2rem;
      font-weight: 800;
      color: #7ee89a;
  }
  .card-metrica .unidade {
      font-size: 0.85rem;
      color: #8b949e;
      margin-top: 2px;
  }

  .secao-titulo {
      font-family: 'Syne', sans-serif;
      font-size: 1.1rem;
      font-weight: 700;
      color: #e6edf3;
      border-left: 3px solid #2ea843;
      padding-left: 0.75rem;
      margin-bottom: 1rem;
  }

  .risk-badge-alto   { background:#3d1010; color:#f85149; border:1px solid #f8514960; border-radius:6px; padding:2px 10px; font-size:0.8rem; font-weight:500; }
  .risk-badge-médio  { background:#2d2200; color:#e3b341; border:1px solid #e3b34160; border-radius:6px; padding:2px 10px; font-size:0.8rem; font-weight:500; }
  .risk-badge-baixo  { background:#0d2818; color:#2ea843; border:1px solid #2ea84360; border-radius:6px; padding:2px 10px; font-size:0.8rem; font-weight:500; }

  div[data-testid="stMetric"] {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 1rem;
  }
  div[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 0.8rem !important; }
  div[data-testid="stMetricValue"] { color: #7ee89a !important; font-family: 'Syne', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
  <h1>🌿 Gêmeo Digital · Miguel Pereira</h1>
  <p>Monitoramento Ambiental em Tempo Real · Rio de Janeiro, RJ · Setores: Centro · Portela · Javary</p>
</div>
""", unsafe_allow_html=True)

# ── Carregar Dados ───────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_miguel_pereira.csv")
    df.columns = df.columns.str.strip()
    return df

df = carregar_dados()

# ── Processamento ────────────────────────────────────────────────────────────
df_setor = df.groupby("id_setor", as_index=False).agg(
    chuva_media=("chuva_acumulada_mm", "mean"),
    chuva_max=("chuva_acumulada_mm", "max"),
    area_total=("area_reflorestada_ha", "sum"),
    umidade_media=("umidade_solo_%", "mean"),
)
df_setor["co2_sequestrado_t"] = df_setor["area_total"] * 5

chuva_max_global = df["chuva_acumulada_mm"].max()
setor_critico    = df.loc[df["chuva_acumulada_mm"].idxmax(), "id_setor"]
alerta_ativo     = chuva_max_global > 50

co2_total        = (df["area_reflorestada_ha"] * 5).sum()
area_total_ha    = df["area_reflorestada_ha"].sum()
umidade_media    = df["umidade_solo_%"].mean()
registros_alto   = (df["risco_deslizamento"] == "alto").sum()

# ── Linha 1: Alerta + Métricas ───────────────────────────────────────────────
col_alerta, col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1, 1, 1, 1])

with col_alerta:
    if alerta_ativo:
        st.markdown(f"""
        <div class="alerta-perigo">
          <div class="icon">🚨</div>
          <div>
            <div class="titulo">ALERTA DE EMERGÊNCIA ATIVO</div>
            <div class="desc">Chuva de <strong>{chuva_max_global:.1f} mm</strong> detectada em <strong>{setor_critico}</strong> — limiar de 50 mm superado!</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alerta-ok">
          <div class="icon">✅</div>
          <div>
            <div class="titulo">Sistema Estável</div>
            <div class="desc">Chuva máxima registrada: <strong>{chuva_max_global:.1f} mm</strong> — abaixo do limiar de 50 mm.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

with col_m1:
    st.metric("🌧️ Chuva Máxima", f"{chuva_max_global:.1f} mm", delta="limiar: 50 mm", delta_color="inverse")

with col_m2:
    st.metric("🌿 CO₂ Sequestrado", f"{co2_total:,.0f} t", delta=f"{area_total_ha:.0f} ha reflorest.")

with col_m3:
    st.metric("💧 Umidade Média", f"{umidade_media:.1f}%")

with col_m4:
    st.metric("⚠️ Registros Risco Alto", f"{registros_alto}", delta="ocorrências", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ── Linha 2: Gráfico de Barras + Tabela por Setor ───────────────────────────
col_grafico, col_tabela = st.columns([3, 2])

with col_grafico:
    st.markdown('<div class="secao-titulo">Chuva Acumulada Média por Setor (mm)</div>', unsafe_allow_html=True)

    import plotly.graph_objects as go

    cores = []
    for _, row in df_setor.iterrows():
        if row["chuva_media"] > 100:
            cores.append("#f85149")
        elif row["chuva_media"] > 60:
            cores.append("#e3b341")
        else:
            cores.append("#2ea843")

    fig = go.Figure()

    # Linha de limiar
    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color="#f85149",
        line_width=1.5,
        annotation_text="⚠️ Limiar de Alerta (50 mm)",
        annotation_position="top left",
        annotation_font_color="#f85149",
        annotation_font_size=11,
    )

    fig.add_trace(go.Bar(
        x=df_setor["id_setor"],
        y=df_setor["chuva_media"],
        marker_color=cores,
        marker_line_color="#0d1117",
        marker_line_width=2,
        text=[f"{v:.1f} mm" for v in df_setor["chuva_media"]],
        textposition="outside",
        textfont=dict(color="#e6edf3", size=12, family="Syne"),
        hovertemplate="<b>%{x}</b><br>Média: %{y:.1f} mm<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#161b22",
        font=dict(color="#8b949e", family="Inter"),
        xaxis=dict(showgrid=False, tickfont=dict(size=13, color="#e6edf3", family="Syne")),
        yaxis=dict(
            gridcolor="#21262d",
            title="mm",
            title_font=dict(color="#8b949e"),
        ),
        margin=dict(t=30, b=20, l=10, r=10),
        height=320,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.markdown('<div class="secao-titulo">Resumo por Setor</div>', unsafe_allow_html=True)

    for _, row in df_setor.iterrows():
        risco_counts = df[df["id_setor"] == row["id_setor"]]["risco_deslizamento"].value_counts()
        risco_dom = risco_counts.idxmax()
        badge_class = f"risk-badge-{risco_dom}"

        st.markdown(f"""
        <div style="background:#161b22; border:1px solid #30363d; border-radius:10px;
                    padding:0.9rem 1.1rem; margin-bottom:0.7rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; color:#e6edf3;">
              📍 {row['id_setor']}
            </span>
            <span class="{badge_class}">{risco_dom}</span>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.3rem; font-size:0.82rem; color:#8b949e;">
            <span>🌧️ Chuva média: <strong style="color:#e6edf3">{row['chuva_media']:.1f} mm</strong></span>
            <span>🌿 Área: <strong style="color:#7ee89a">{row['area_total']:.1f} ha</strong></span>
            <span>💧 Umidade: <strong style="color:#e6edf3">{row['umidade_media']:.1f}%</strong></span>
            <span>♻️ CO₂: <strong style="color:#7ee89a">{row['co2_sequestrado_t']:.0f} t</strong></span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Linha 3: Mapa + CO2 por Setor ───────────────────────────────────────────
col_mapa, col_co2 = st.columns([3, 2])

with col_mapa:
    st.markdown('<div class="secao-titulo">🗺️ Corredor Tinguá-Bocaina · Reflorestamento e Precipitação</div>', unsafe_allow_html=True)

    import folium
    from folium.plugins import FeatureGroupSubGroup
    from streamlit_folium import st_folium

    m = folium.Map(
        location=[-22.4650, -43.4700],
        zoom_start=11,
        tiles="CartoDB dark_matter",
    )

    # ── CAMADA 1: Corredor Tinguá-Bocaina (polígono amarelo-esverdeado) ───────
    camada_corredor = folium.FeatureGroup(name="🟡 Corredor Tinguá-Bocaina", show=True)

    # Polígono aproximado do trecho do corredor que passa por Miguel Pereira
    # Baseado nos limites reais entre Reserva Biológica do Tinguá e Serra da Bocaina
    corredor_mp = [
        [-22.3980, -43.5300], [-22.4050, -43.5100], [-22.4100, -43.4900],
        [-22.4150, -43.4700], [-22.4200, -43.4500], [-22.4300, -43.4300],
        [-22.4450, -43.4100], [-22.4600, -43.3950], [-22.4750, -43.3850],
        [-22.5000, -43.3800], [-22.5200, -43.3900], [-22.5350, -43.4100],
        [-22.5400, -43.4400], [-22.5300, -43.4700], [-22.5100, -43.4950],
        [-22.4900, -43.5150], [-22.4700, -43.5300], [-22.4500, -43.5400],
        [-22.4300, -43.5450], [-22.4100, -43.5400], [-22.3980, -43.5300],
    ]

    folium.Polygon(
        locations=corredor_mp,
        color="#d4a017",
        weight=2.5,
        dash_array="8 4",
        fill=True,
        fill_color="#d4a017",
        fill_opacity=0.10,
        tooltip="🌎 Corredor de Biodiversidade Tinguá-Bocaina",
        popup=folium.Popup(
            """<div style='font-family:sans-serif;font-size:12px;min-width:200px'>
            <b style='color:#d4a017'>Corredor Tinguá-Bocaina</b><br>
            <hr style='margin:4px 0;border-color:#ddd'>
            Extensão total: <b>195.000 ha</b><br>
            Municípios: <b>9</b><br>
            Bioma: <b>Mata Atlântica</b><br>
            Responsável: <b>ITPA</b>
            </div>""",
            max_width=220,
        ),
    ).add_to(camada_corredor)

    # Rótulo do corredor
    folium.Marker(
        location=[-22.4650, -43.4200],
        icon=folium.DivIcon(
            html='<div style="font-family:sans-serif;font-size:10px;font-weight:bold;color:#d4a017;'
                 'text-shadow:0 0 6px #000;white-space:nowrap;">CORREDOR TINGUÁ-BOCAINA</div>',
            icon_size=(200, 20),
            icon_anchor=(100, 10),
        ),
    ).add_to(camada_corredor)
    camada_corredor.add_to(m)

    # ── CAMADA 2: Áreas de reflorestamento (polígonos verdes) ─────────────────
    camada_reflor = folium.FeatureGroup(name="🌿 Áreas Reflorestadas", show=True)

    areas_reflor = [
        {
            "nome": "Reflorestamento Portela Norte",
            "setor": "Portela", "area_ha": 5.2,
            "coords": [
                [-22.4650, -43.4490], [-22.4590, -43.4465],
                [-22.4575, -43.4560], [-22.4640, -43.4585],
                [-22.4650, -43.4490],
            ],
        },
        {
            "nome": "Reflorestamento Portela Sul",
            "setor": "Portela", "area_ha": 4.1,
            "coords": [
                [-22.4840, -43.4370], [-22.4790, -43.4350],
                [-22.4770, -43.4430], [-22.4825, -43.4455],
                [-22.4840, -43.4370],
            ],
        },
        {
            "nome": "Mata Ciliar Rio Guandu — Centro",
            "setor": "Centro", "area_ha": 16.3,
            "coords": [
                [-22.4420, -43.4870], [-22.4350, -43.4840],
                [-22.4320, -43.4980], [-22.4390, -43.5020],
                [-22.4450, -43.4940], [-22.4420, -43.4870],
            ],
        },
        {
            "nome": "Mata Ciliar Centro Leste",
            "setor": "Centro", "area_ha": 9.6,
            "coords": [
                [-22.4530, -43.4590], [-22.4480, -43.4570],
                [-22.4460, -43.4660], [-22.4515, -43.4690],
                [-22.4545, -43.4630], [-22.4530, -43.4590],
            ],
        },
        {
            "nome": "Reserva Javary — Núcleo",
            "setor": "Javary", "area_ha": 17.2,
            "coords": [
                [-22.4260, -43.5030], [-22.4180, -43.4990],
                [-22.4160, -43.5110], [-22.4230, -43.5160],
                [-22.4300, -43.5090], [-22.4260, -43.5030],
            ],
        },
        {
            "nome": "Mata Javary Sul",
            "setor": "Javary", "area_ha": 13.0,
            "coords": [
                [-22.4390, -43.4870], [-22.4330, -43.4850],
                [-22.4310, -43.4940], [-22.4370, -43.4970],
                [-22.4400, -43.4910], [-22.4390, -43.4870],
            ],
        },
    ]

    for area in areas_reflor:
        co2 = area["area_ha"] * 5
        folium.Polygon(
            locations=area["coords"],
            color="#2ea843",
            weight=1.5,
            fill=True,
            fill_color="#2ea843",
            fill_opacity=0.45,
            tooltip=f"🌿 {area['nome']} — {area['area_ha']} ha",
            popup=folium.Popup(
                f"""<div style='font-family:sans-serif;font-size:12px;min-width:190px'>
                <b style='color:#2ea843'>{area['nome']}</b><br>
                <hr style='margin:4px 0;border-color:#ddd'>
                Setor: <b>{area['setor']}</b><br>
                Área reflorestada: <b>{area['area_ha']} ha</b><br>
                CO₂ sequestrado: <b>{co2:.0f} t</b><br>
                Responsável: <b>ITPA</b>
                </div>""",
                max_width=210,
            ),
        ).add_to(camada_reflor)

    camada_reflor.add_to(m)

    # ── CAMADA 3: Sensores de precipitação ────────────────────────────────────
    camada_chuva = folium.FeatureGroup(name="🌧️ Precipitação (Sensores)", show=True)

    sensores = [
        {"setor": "Centro",  "lat": -22.4546, "lon": -43.4716},
        {"setor": "Portela", "lat": -22.4812, "lon": -43.4423},
        {"setor": "Javary",  "lat": -22.4350, "lon": -43.4950},
    ]

    for s in sensores:
        row = df_setor[df_setor["id_setor"] == s["setor"]].iloc[0]
        chuva = row["chuva_media"]
        cor = "#f85149" if chuva > 100 else "#e3b341" if chuva > 50 else "#2ea843"
        raio = max(300, int(chuva * 5))

        # Círculo de área de influência da chuva
        folium.Circle(
            location=[s["lat"], s["lon"]],
            radius=raio,
            color=cor,
            weight=1,
            fill=True,
            fill_color=cor,
            fill_opacity=0.15,
            tooltip=f"🌧️ Precipitação — {s['setor']}: {chuva:.1f} mm",
        ).add_to(camada_chuva)

        # Marcador do sensor
        folium.CircleMarker(
            location=[s["lat"], s["lon"]],
            radius=9,
            color="#0d1117",
            weight=2,
            fill=True,
            fill_color=cor,
            fill_opacity=0.95,
            tooltip=f"📡 Sensor {s['setor']}: {chuva:.1f} mm",
            popup=folium.Popup(
                f"""<div style='font-family:sans-serif;font-size:12px;min-width:190px'>
                <b style='color:{cor}'>📡 Sensor Pluviométrico — {s['setor']}</b><br>
                <hr style='margin:4px 0;border-color:#ddd'>
                🌧️ Chuva média: <b>{chuva:.1f} mm</b><br>
                💧 Umidade do solo: <b>{row['umidade_media']:.1f}%</b><br>
                🌿 Área reflorestada: <b>{row['area_total']:.1f} ha</b><br>
                ♻️ CO₂ sequestrado: <b>{row['co2_sequestrado_t']:.0f} t</b><br>
                ⚠️ Risco: <b>{'ALTO' if chuva > 100 else 'MÉDIO' if chuva > 50 else 'BAIXO'}</b>
                </div>""",
                max_width=210,
            ),
        ).add_to(camada_chuva)

        # Rótulo do setor
        folium.Marker(
            location=[s["lat"] - 0.004, s["lon"]],
            icon=folium.DivIcon(
                html=f'<div style="font-family:sans-serif;font-size:11px;font-weight:bold;'
                     f'color:{cor};text-shadow:0 0 5px #000,0 0 5px #000;">{s["setor"]}</div>',
                icon_size=(80, 20),
                icon_anchor=(40, 0),
            ),
        ).add_to(camada_chuva)

    camada_chuva.add_to(m)

    # ── Controle de camadas ───────────────────────────────────────────────────
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # ── Legenda ───────────────────────────────────────────────────────────────
    legenda_html = """
    <div style="position:fixed;bottom:20px;left:20px;z-index:9999;
                background:rgba(13,17,23,0.92);border:1px solid #30363d;
                border-radius:10px;padding:12px 16px;font-family:sans-serif;
                font-size:11px;color:#e6edf3;line-height:1.8">
      <b style="font-size:12px;display:block;margin-bottom:6px">Legenda</b>
      <span style="color:#d4a017">⬚</span> Corredor Tinguá-Bocaina (195 mil ha)<br>
      <span style="color:#2ea843">■</span> Área reflorestada (ITPA)<br>
      <span style="color:#f85149">●</span> Precipitação alta (&gt;100 mm)<br>
      <span style="color:#e3b341">●</span> Precipitação média (50–100 mm)<br>
      <span style="color:#2ea843">●</span> Precipitação baixa (&lt;50 mm)<br>
      <span style="opacity:.6;font-size:13px">◯</span> Raio proporcional à chuva
    </div>
    """
    m.get_root().html.add_child(folium.Element(legenda_html))

    st_folium(m, height=500, use_container_width=True)
    st.caption("🟡 Corredor Tinguá-Bocaina · 🌿 Reflorestamento ITPA · 🌧️ Sensores pluviométricos · Controle de camadas no canto superior direito")

with col_co2:
    st.markdown('<div class="secao-titulo">♻️ CO₂ Sequestrado por Setor</div>', unsafe_allow_html=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_setor["co2_sequestrado_t"],
        y=df_setor["id_setor"],
        orientation="h",
        marker_color=["#2ea843", "#3fb857", "#56d46e"],
        marker_line_color="#0d1117",
        marker_line_width=2,
        text=[f"{v:,.0f} t" for v in df_setor["co2_sequestrado_t"]],
        textposition="outside",
        textfont=dict(color="#7ee89a", size=12, family="Syne"),
        hovertemplate="<b>%{y}</b><br>CO₂: %{x:,.0f} t<extra></extra>",
    ))

    fig2.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#161b22",
        font=dict(color="#8b949e", family="Inter"),
        xaxis=dict(gridcolor="#21262d", title="toneladas", title_font=dict(color="#8b949e")),
        yaxis=dict(showgrid=False, tickfont=dict(size=13, color="#e6edf3", family="Syne")),
        margin=dict(t=10, b=20, l=10, r=60),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div style="background:#0d2818; border:1px solid #2ea84340; border-radius:10px;
                padding:0.9rem 1.2rem; text-align:center; margin-top:0.5rem;">
      <div style="font-size:0.75rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.08em;">
        Total Sequestrado
      </div>
      <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#7ee89a;">
        {co2_total:,.0f} t
      </div>
      <div style="font-size:0.8rem; color:#8b949e;">5 t CO₂ / ha reflorestado</div>
    </div>
    """, unsafe_allow_html=True)

# ── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#484f58; font-size:0.78rem; border-top:1px solid #21262d; padding-top:1rem;">
  Gêmeo Digital · Miguel Pereira, RJ · Dados: INMET / CPRM / SGB · Desenvolvido com Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
