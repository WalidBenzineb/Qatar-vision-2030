"""
Qatar Vision 2030 Dashboard
----------------------------
A comprehensive visualization dashboard built with Dash to monitor Qatar's progress
towards its Vision 2030 goals across Economic, Environmental, Human, and Social
development pillars. The dashboard presents key indicators with benchmark comparisons
and expert insights derived from data analysis.

Author: Walid Benzineb
benzinebwal@gmail.com
"""


import os
import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from translations import translations
from benchmarks import benchmarks  
from insight_sentiments import insight_sentiments
# Import Key Indicators insights
from key_insights import (
    gdp_insights, 
    hci_insights, 
    co2_insights, 
    renewable_insights, 
    energy_production_insights, 
    education_metrics_insights, 
    stem_graduates_insights,
    overall_insights
)

# Import Economic Development insights
from economic_insights import (
    gdp_insights as economic_gdp_insights,
    oil_insights,
    gas_insights,
    energy_consumption_insights,
    energy_growth_insights,
    agriculture_insights,
    business_graduates_insights,
    overall_economic_insights
)

# Import environmental insights
from environmental_insights import (
    co2_insights,
    electricity_insights,
    solar_insights,
    energy_change_insights,
    renewable_detail_insights,
    agricultural_insights,
    overall_environmental_insights
)
# Import Human Development insights
from human_insights import (
    educational_attainment_insights,
    education_quality_insights,
    human_capital_insights,
    gender_equity_insights,
    advanced_education_insights,
    completion_rates_insights,
    overall_human_development_insights
)
# Import Social Development insights
from social_insights import (
    sanitation_insights,
    gender_equality_insights,
    stem_insights,
    digital_skills_insights,
    ict_graduates_insights,
    overall_social_insights
)

# Define a modern color palette
colors = {
    'bg': '#f8f9fa',
    'card': '#ffffff',
    'text': '#2c3e50',
    'subtext': '#6c757d',
    
    # Enhanced pillar colors - more vibrant with better contrast
    'key': '#8b5cf6',       # Vibrant purple
    'economic': '#3b82f6',   # Bright blue
    'environmental': '#10b981', # Rich green
    'human': '#f59e0b',     # Warm orange
    'social': '#ef4444',    # Modern red
    'highlight': '#0ea5e9', # Bright teal
    
    # Supporting colors
    'global': '#94a3b8',    # Slate gray
    'regional': '#334155',  # Dark slate
    'leading': '#eab308',   # Golden yellow
    'positive': '#10b981',  # Green
    'negative': '#ef4444',  # Red
    'neutral': '#3b82f6',   # Blue
    
    # Gradients and backgrounds
    'gradient_start': 'rgba(255, 255, 255, 0.9)',
    'gradient_end': 'rgba(249, 250, 251, 0.9)',
    
    # Additional UI colors
    'card_hover': '#f1f5f9',
    'border': '#e2e8f0',
    'muted': '#64748b',
}

# Initialize Dash app with a modern bootstrap theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
        'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
        'https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap'
    ],
    suppress_callback_exceptions=True
) 
app.title = "Qatar Vision 2030 Dashboard"
server = app.server

# Read the CSV files
economic_df = pd.read_csv('data/economic_development.csv')
environmental_df = pd.read_csv('data/environmental_development.csv')
human_df = pd.read_csv('data/human_development.csv')
social_df = pd.read_csv('data/social_development.csv')
key_indicators_df = pd.read_csv('data/qatar_vision_key_indicators.csv')

# Function to get translation for a text element based on the selected language
def get_translation(text, language='english'):
    if language == 'arabic':
        # Check for exact match first
        if text in translations:
            return translations[text]
        
        # Try to translate benchmark strings that contain numbers
        if "Global Average:" in text:
            prefix = "Global Average:"
            suffix = text.replace(prefix, "").strip()
            return f"{translations.get(prefix, prefix)} {suffix}"
        
        return translations.get(text, text)  # Return translation or original text
    return text  # Return original English text

# Helper function to create insight cards that display the PDF analysis with sentiment icons
def create_insight_card(title, insights, pillar_color, language='english'):
    insight_elements = []
    for insight in insights:
        if insight in insight_sentiments:
            sentiment = insight_sentiments[insight]['sentiment']
        else:
            sentiment = 'neutral'
            
        # Choose icon based on sentiment with enhanced styling
        if sentiment == 'positive':
            icon_class = "fas fa-arrow-up me-2"
            icon_color = colors['positive']
            bg_color = f"{colors['positive']}10"
            icon_style = {"color": icon_color, "backgroundColor": bg_color, "padding": "6px", 
                         "borderRadius": "50%", "width": "28px", "height": "28px", 
                         "display": "flex", "alignItems": "center", "justifyContent": "center",
                         "marginRight": "12px", "fontSize": "0.8rem"}
        elif sentiment == 'negative':
            icon_class = "fas fa-arrow-down me-2"
            icon_color = colors['negative']
            bg_color = f"{colors['negative']}10"
            icon_style = {"color": icon_color, "backgroundColor": bg_color, "padding": "6px", 
                         "borderRadius": "50%", "width": "28px", "height": "28px", 
                         "display": "flex", "alignItems": "center", "justifyContent": "center",
                         "marginRight": "12px", "fontSize": "0.8rem"}
        else:
            icon_class = "fas fa-minus me-2"
            icon_color = colors['neutral']
            bg_color = f"{colors['neutral']}10"
            icon_style = {"color": icon_color, "backgroundColor": bg_color, "padding": "6px", 
                         "borderRadius": "50%", "width": "28px", "height": "28px", 
                         "display": "flex", "alignItems": "center", "justifyContent": "center",
                         "marginRight": "12px", "fontSize": "0.8rem"}
        
        # Translate the insight if language is Arabic
        translated_insight = get_translation(insight, language)
        
        insight_elements.append(
            html.Div([
                html.Div([
                    html.I(className=icon_class)
                ], style=icon_style),
                html.Span(translated_insight, style={"color": colors['text'], "flex": "1"})
            ], className="mb-3 d-flex align-items-start insight-item")
        )
    
    # Translate the title
    translated_title = get_translation(title, language)
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5(translated_title, className="mb-0 card-title", 
                   style={"color": colors['text'], "fontWeight": "600", "letterSpacing": "-0.01em"})
        ], style={"borderLeft": f"4px solid {pillar_color}", "borderRadius": "12px 12px 0 0", 
                 "background": f"linear-gradient(to right, {pillar_color}10, {colors['gradient_start']}"}),
        dbc.CardBody(insight_elements, className="py-4")
    ], className="mb-4 shadow-sm hover-card", 
       style={"borderRadius": "12px", "overflow": "hidden", "backgroundColor": colors['card']})

# Helper function to create benchmark comparison cards
def create_benchmark_card(title, benchmark_data, pillar_color, language='english'):
    if not benchmark_data:
        return None
    
    benchmark_items = []
    if 'global_avg' in benchmark_data:
        global_avg_text = f"Global average: {benchmark_data['global_avg']}"
        benchmark_items.append(
            html.Div([
                html.Div([
                    html.I(className="fas fa-globe", 
                          style={"fontSize": "0.8rem"})
                ], style={"color": colors['global'], "backgroundColor": f"{colors['global']}15", 
                         "padding": "8px", "borderRadius": "50%", "width": "32px", "height": "32px", 
                         "display": "flex", "alignItems": "center", "justifyContent": "center",
                         "marginRight": "12px"}),
                html.Span(get_translation(global_avg_text, language),
                         style={"color": colors['text'], "fontWeight": "500"})
            ], className="mb-3 d-flex align-items-center")
        )
    
    if 'regional' in benchmark_data:
        for region, value in benchmark_data['regional'].items():
            regional_text = f"{region}: {value}"
            benchmark_items.append(
                html.Div([
                    html.Div([
                        html.I(className="fas fa-map-marker-alt", 
                              style={"fontSize": "0.8rem"})
                    ], style={"color": colors['regional'], "backgroundColor": f"{colors['regional']}15", 
                             "padding": "8px", "borderRadius": "50%", "width": "32px", "height": "32px", 
                             "display": "flex", "alignItems": "center", "justifyContent": "center",
                             "marginRight": "12px"}),
                    html.Span(get_translation(regional_text, language), 
                             style={"color": colors['text'], "fontWeight": "500"})
                ], className="mb-3 d-flex align-items-center")
            )
    
    if 'leading' in benchmark_data:
        for leader, value in benchmark_data['leading'].items():
            leader_text = f"{leader}: {value}"
            benchmark_items.append(
                html.Div([
                    html.Div([
                        html.I(className="fas fa-trophy", 
                              style={"fontSize": "0.8rem"})
                    ], style={"color": colors['leading'], "backgroundColor": f"{colors['leading']}15", 
                             "padding": "8px", "borderRadius": "50%", "width": "32px", "height": "32px", 
                             "display": "flex", "alignItems": "center", "justifyContent": "center",
                             "marginRight": "12px"}),
                    html.Span(get_translation(leader_text, language), 
                             style={"color": colors['text'], "fontWeight": "500"})
                ], className="mb-3 d-flex align-items-center")
            )
    
    # Translate the title
    translated_title = get_translation(title, language)
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5(translated_title, className="mb-0 card-title", 
                   style={"color": colors['text'], "fontWeight": "600"})
        ], style={"borderLeft": f"4px solid {pillar_color}", "borderRadius": "12px 12px 0 0", 
                 "background": f"linear-gradient(to right, {pillar_color}10, {colors['gradient_start']}"}),
        dbc.CardBody(benchmark_items, className="py-3")
    ], className="mb-4 shadow-sm hover-card", 
       style={"borderRadius": "12px", "overflow": "hidden", "backgroundColor": colors['card']})

# Create a header 
def create_header(language='english'):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                # Language toggle button in the upper right
                dbc.ButtonGroup(
                    [
                        dbc.Button("English", id="btn-english", 
                                  color="primary" if language == "english" else "outline-primary",
                                  className="rounded-start language-btn"),
                        dbc.Button("العربية", id="btn-arabic", 
                                  color="primary" if language == "arabic" else "outline-primary",
                                  className="rounded-end language-btn"),
                    ],
                    className="mb-3"
                ),
            ], width=12, className="d-flex justify-content-end"),
        ]),
        dbc.Row([
            dbc.Col(html.Img(src='assets/qatar_vision_2030_logo.png', height='120px', 
                           style={"filter": "drop-shadow(0 4px 6px rgba(0,0,0,0.1))"}), 
                   width={"size": 2, "order": 1 if language == "english" else 12}, 
                   className="d-flex align-items-center justify-content-center"),
            dbc.Col([
                html.H1(get_translation("Qatar Vision 2030 Dashboard", language), 
                       className="mb-2 header-title"),
                html.P(get_translation("Monitoring Progress Across Economic, Environmental, Human, and Social Development Pillars", language), 
                      className="lead mb-0 header-subtitle")
            ], width={"size": 10, "order": 12 if language == "english" else 1},
              className="d-flex flex-column justify-content-center")
        ], className="py-4 header-row align-items-center")
    ], fluid=True, className="header-container mb-4")

# Create tabs with a modern style
def create_tabs(language='english', active_tab="key-indicators"):
    return dbc.Tabs([
        dbc.Tab(label=get_translation("Key Indicators", language), tab_id="key-indicators", 
               label_style={"fontWeight": "500", "fontSize": "1.05rem", "padding": "14px 20px"},
               active_label_style={"borderBottom": f"3px solid {colors['key']}", "fontWeight": "600"},
               className="custom-tab"),
        dbc.Tab(label=get_translation("Economic Development", language), tab_id="economic", 
               label_style={"fontWeight": "500", "fontSize": "1.05rem", "padding": "14px 20px"},
               active_label_style={"borderBottom": f"3px solid {colors['economic']}", "fontWeight": "600"},
               className="custom-tab"),
        dbc.Tab(label=get_translation("Environmental Development", language), tab_id="environmental", 
               label_style={"fontWeight": "500", "fontSize": "1.05rem", "padding": "14px 20px"},
               active_label_style={"borderBottom": f"3px solid {colors['environmental']}", "fontWeight": "600"},
               className="custom-tab"),
        dbc.Tab(label=get_translation("Human Development", language), tab_id="human", 
               label_style={"fontWeight": "500", "fontSize": "1.05rem", "padding": "14px 20px"},
               active_label_style={"borderBottom": f"3px solid {colors['human']}", "fontWeight": "600"},
               className="custom-tab"),
        dbc.Tab(label=get_translation("Social Development", language), tab_id="social", 
               label_style={"fontWeight": "500", "fontSize": "1.05rem", "padding": "14px 20px"},
               active_label_style={"borderBottom": f"3px solid {colors['social']}", "fontWeight": "600"},
               className="custom-tab"),
    ], id="tabs", active_tab=active_tab, className="mb-4 nav-tabs-modern")

# Create year slider
def create_year_slider(language='english'):
    return dbc.Card(
        dbc.CardBody([
            html.H5(get_translation("Select Year Range", language), className="card-title mb-3", 
                   style={"color": colors['text'], "fontWeight": "600", "fontSize": "1.1rem"}),
            dcc.RangeSlider(
                id='year-slider',
                min=min(key_indicators_df['Year']),
                max=max(key_indicators_df['Year']),
                step=1,
                marks={int(year): {"label": str(year), "style": {"transform": "rotate(45deg)", 
                                                              "color": colors['text'],
                                                              "margin-top": "8px",
                                                              "font-weight": "500"}} 
                       for year in key_indicators_df['Year'].unique()},
                value=[min(key_indicators_df['Year']), max(key_indicators_df['Year'])],
                className="mt-4 mb-2 px-2 modern-slider",
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], className="py-4 px-4"),
        className="mb-4 shadow-sm slider-card", 
        style={"borderRadius": "16px", "backgroundColor": colors['card'], "border": "none"}
    )

# Main layout with styling and structure and language support

app.layout = html.Div([
    # Store the current language
    dcc.Store(id='language-store', data='english'),
    
    # Header - Initialize with English version
    html.Div(create_header('english'), id="header-container"),
    
    # Main content area
    dbc.Container([
        # Year slider - Initialize with English version
        html.Div(create_year_slider('english'), id="slider-container"),
        
        # Tabs - Initialize with English version and "key-indicators" as active tab
        html.Div(create_tabs('english', "key-indicators"), id="tabs-container"),
        
        # Tab content - Will be populated by callback
        html.Div(id="tab-content", className="mt-4 fade-in")
    ], fluid=True, className="main-container pb-5"),
    
    # Footer
    html.Footer([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P("Qatar Vision 2030 Dashboard © 2025", className="text-center mb-0 footer-text")
                ], width=12)
            ], className="py-3")
        ], fluid=True)
    ], className="footer mt-5")
], className="app-container", style={"backgroundColor": colors['bg']})

# Callback to handle language selection and update the store
@app.callback(
    Output('language-store', 'data'),
    [Input('btn-english', 'n_clicks'),
     Input('btn-arabic', 'n_clicks')],
    [State('language-store', 'data')]
)
def update_language(en_clicks, ar_clicks, current_language):
    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_language
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'btn-english':
            return 'english'
        elif button_id == 'btn-arabic':
            return 'arabic'
        return current_language

# Callback to update all layout elements based on language and active tab
@app.callback(
    [Output('header-container', 'children'),
     Output('slider-container', 'children'),
     Output('tabs-container', 'children')],
    [Input('language-store', 'data')],
    [State('tabs', 'active_tab')]
)
def update_layout_components(language, active_tab):
    # Use active_tab if available, otherwise default to "key-indicators"
    current_tab = active_tab if active_tab else "key-indicators"
    
    header = create_header(language)
    slider = create_year_slider(language)
    tabs = create_tabs(language, current_tab)
    
    return header, slider, tabs

# Callback to update the content based on active tab and language
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("year-slider", "value"),
     Input('language-store', 'data')]
)
def render_tab_content(active_tab, year_range, language):
    min_year, max_year = year_range
    
    # Default to key-indicators if active_tab is None
    current_tab = active_tab if active_tab is not None else "key-indicators"
    
    if current_tab == "key-indicators":
        return render_key_indicators(min_year, max_year, language)
    elif current_tab == "economic":
        return render_economic(min_year, max_year, language)
    elif current_tab == "environmental":
        return render_environmental(min_year, max_year, language)
    elif current_tab == "human":
        return render_human(min_year, max_year, language)
    elif current_tab == "social":
        return render_social(min_year, max_year, language)
    
    return html.P(get_translation("This tab has no content.", language))

# Function to create a KPI card 
def create_kpi_card(title, value, subtitle, comparison, icon, color, language='english'):
    translated_title = get_translation(title, language)
    translated_subtitle = get_translation(subtitle, language)
    translated_comparison = get_translation(comparison, language) if comparison else ""
    
    # Determine comparison color
    if "global average" in comparison.lower() and "x" in comparison:
        try:
            multiplier = float(comparison.split('x')[0].strip())
            comparison_color = colors['positive'] if multiplier > 1 else colors['negative']
        except:
            comparison_color = colors['neutral']
    elif any(pos_word in comparison.lower() for pos_word in ["increase", "growth", "improvement", "higher", "better", "above"]):
        comparison_color = colors['positive']
    elif any(neg_word in comparison.lower() for neg_word in ["decrease", "decline", "lower", "below", "worse"]):
        comparison_color = colors['negative']
    else:
        comparison_color = colors['neutral']
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon} fa-2x", 
                      style={"color": color, "backgroundColor": f"{color}15", 
                             "padding": "18px", "borderRadius": "50%", "filter": "drop-shadow(0 4px 6px rgba(0,0,0,0.08))"}),
            ], className="text-center mb-3 icon-container"),
            html.H5(translated_title, className="text-center text-muted mb-2 kpi-title", 
                   style={"fontSize": "0.92rem", "fontWeight": "500", "letterSpacing": "-0.01em"}),
            html.H3(value, className="text-center mb-2 kpi-value", 
                   style={"fontWeight": "700", "color": colors['text'], "letterSpacing": "-0.02em"}),
            html.P(translated_subtitle, className="text-center text-muted small kpi-subtitle"),
            html.Div([
                html.P(translated_comparison, 
                      className="text-center mt-2 small kpi-comparison mb-0",
                      style={"color": comparison_color, "fontWeight": "500"})
            ], className="comparison-container")
        ], className="p-4")
    ], className="h-100 kpi-card shadow-sm", 
       style={"borderRadius": "16px", "border": "none", "overflow": "hidden", "backgroundColor": colors['card']})

# Function to render Key Indicators tab with insights
def render_key_indicators(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = key_indicators_df[(key_indicators_df['Year'] >= min_year) & (key_indicators_df['Year'] <= max_year)]
    
    # Create GDP per capita chart with benchmark comparisons
    gdp_fig = px.line(
        filtered_df, 
        x='Year', 
        y='GDP per capita, PPP (constant 2021 international $)', 
        title=get_translation('GDP per Capita (PPP)', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
        labels={"GDP per capita, PPP (constant 2021 international $)": get_translation("GDP per capita, PPP (2021 international $)", language), "variable": ""}
    )
    
    if language == 'arabic':
        gdp_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))

    # Add benchmark lines for GDP per capita
    gdp_fig.add_hline(y=benchmarks["gdp_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                     annotation_text=get_translation(f"Global Average: ${benchmarks['gdp_per_capita']['global_avg']:,}", language), 
                     annotation_position="bottom right")
    
    for region, value in benchmarks["gdp_per_capita"]["regional"].items():
        gdp_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                         annotation_text=get_translation(f"{region}: ${value:,}", language), 
                         annotation_position="bottom right")
    
    # Apply modern styling to chart
    gdp_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    gdp_fig.update_traces(line=dict(width=3), marker=dict(size=8))
    
    # Create Human Capital Index chart
    hci_df = filtered_df.dropna(subset=['Human Capital Index (HCI) (scale 0-1)'])
    
    hci_fig = px.line(
        hci_df,
        x='Year',
        y='Human Capital Index (HCI) (scale 0-1)',
        title=get_translation('Human Capital Index', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
        labels={"Human Capital Index (HCI) (scale 0-1)": get_translation("Human Capital Index (HCI) (scale 0-1)", language), "variable": ""}
    )
   
    if language == 'arabic':
        hci_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for HCI
    hci_fig.add_hline(y=benchmarks["human_capital_index"]["global_avg"], line_dash="dash", line_color=colors['global'],
                    annotation_text=get_translation(f"Global Average: {benchmarks['human_capital_index']['global_avg']}", language), 
                    annotation_position="top right")
    
    for region, value in benchmarks["human_capital_index"]["regional"].items():
        hci_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                        annotation_text=get_translation(f"{region}: {value}", language), 
                        annotation_position="bottom left")
    
    for leader, value in benchmarks["human_capital_index"]["leading"].items():
        hci_fig.add_hline(y=value, line_dash="dot", line_color=colors['leading'],
                        annotation_text=get_translation(f"{leader}: {value}", language), 
                        annotation_position="top right")
    
    # Apply modern styling to HCI chart
    hci_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    hci_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create CO2 Emissions per capita chart
    co2_fig = px.line(
        filtered_df, 
        x='Year', 
        y='Annual CO₂ emissions (per capita)',
        title=get_translation('CO₂ Emissions per Capita', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
        labels={"Annual CO₂ emissions (per capita)": get_translation("Annual CO₂ emissions (per capita)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        co2_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for CO2 per capita
    co2_fig.add_hline(y=benchmarks["co2_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                    annotation_text=get_translation(f"Global Average: {benchmarks['co2_per_capita']['global_avg']} tonnes", language), 
                    annotation_position="bottom right")
    
    for region, value in benchmarks["co2_per_capita"]["regional"].items():
        co2_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                        annotation_text=get_translation(f"{region}: {value} tonnes", language), 
                        annotation_position="bottom right")
    
    # Apply modern styling to CO2 chart
    co2_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,
            xanchor="center", 
            x=0.5,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    co2_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Renewable Electricity chart
    renewable_fig = px.line(
        filtered_df, 
        x='Year', 
        y='Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)',
        title=get_translation('Electricity from Renewables (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
        labels={"Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)": get_translation("Electricity from renewables - TWh", language), "variable": ""}
    )

    if language == 'arabic':
        renewable_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add contextual annotations for renewables with translations
    renewable_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df['Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)'].max(),
        text=get_translation(f"Qatar targets 20% of electricity from renewables by 2030<br>Global average: {benchmarks['renewables_share']['global_avg']}%<br>Middle East: {benchmarks['renewables_share']['regional']['Middle East Avg']}%", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to renewable chart
    renewable_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    renewable_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Energy Production chart (Oil & Gas)
    energy_fig = px.line(
        filtered_df, 
        x='Year', 
        y=['Oil production (TWh)','Gas production - TWh'],
        title=get_translation('Energy Production: Oil & Gas (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['key'], '#17becf'],
        labels={"value": get_translation("Oil production (TWh), Gas production - TWh", language), "variable": ""}
    )

    if language == 'arabic':
        energy_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation for LNG expansion plans with translation
    energy_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df['Gas production - TWh'].max(),
        text=get_translation("Qatar plans 85% LNG<br>expansion by 2030", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to energy chart
    energy_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    energy_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Education metrics chart
    education_fig = px.line(
        filtered_df,
        x='Year',
        y=['Expected Years of School', 'Learning-Adjusted Years of School', 'School enrollment, tertiary (% gross)'],
        title=get_translation('Education Metrics', language),
        markers=True,
        color_discrete_sequence=[colors['key'], '#17becf', '#ff7f0e'],
        labels={"value": get_translation('Expected Years of School, Learning-Adjusted and enrollment', language), "variable": ""}
    )

    if language == 'arabic':
        education_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for education metrics with translations
    education_fig.add_hline(y=benchmarks["education_years"]["expected"]["global_avg"], line_dash="dash", line_color=colors['global'],
                          annotation_text=get_translation(f"Global Avg Expected: {benchmarks['education_years']['expected']['global_avg']} years", language), 
                          annotation_position="bottom right")
    
    education_fig.add_hline(y=benchmarks["education_years"]["learning_adjusted"]["global_avg"], line_dash="dash", line_color=colors['global'],
                          annotation_text=get_translation(f"Global Avg Learning-Adjusted: {benchmarks['education_years']['learning_adjusted']['global_avg']} years", language), 
                          annotation_position="bottom right")
    
    # Apply modern styling to education chart
    education_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    education_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create STEM graduates percentage chart
    stem_fig = px.line(
        filtered_df,
        x='Year',
        y='Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, (%)',
        title=get_translation('STEM Graduates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
        labels={"Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, (%)": get_translation("Percentage of graduates from STEM programmes in tertiary", language), "variable": ""}
    )

    if language == 'arabic':
        stem_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for STEM graduates with translations
    stem_fig.add_hline(y=benchmarks["stem_graduates"]["global_avg"], line_dash="dash", line_color=colors['global'],
                      annotation_text=get_translation(f"Global Average: {benchmarks['stem_graduates']['global_avg']}%", language), 
                      annotation_position="bottom right")
    
    stem_fig.add_hline(y=benchmarks["stem_graduates"]["regional"]["Saudi Arabia"], line_dash="dot", line_color=colors['regional'],
                      annotation_text=get_translation(f"Saudi Arabia: {benchmarks['stem_graduates']['regional']['Saudi Arabia']}%", language), 
                      annotation_position="bottom right")
    
    for leader, value in benchmarks["stem_graduates"]["leading"].items():
        stem_fig.add_hline(y=value, line_dash="dot", line_color=colors['leading'],
                          annotation_text=get_translation(f"{leader}: {value}%", language), 
                          annotation_position="top right")
    
    # Apply modern styling to STEM chart
    stem_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    stem_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create cards for latest values with improved styling
    latest_year = filtered_df['Year'].max()
    latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
    
    # Safely extract values with fallbacks to handle NaN
    try:
        gdp_value = f"${latest_data['GDP per capita, PPP (constant 2021 international $)']:,.0f}"
        gdp_global_compare = f"{latest_data['GDP per capita, PPP (constant 2021 international $)'] / benchmarks['gdp_per_capita']['global_avg']:.1f}x global average"
    except (ValueError, KeyError, TypeError):
        gdp_value = get_translation("Data unavailable", language)
        gdp_global_compare = ""
        
    try:
        # Find the latest non-NaN HCI value
        hci_years = filtered_df.dropna(subset=['Human Capital Index (HCI) (scale 0-1)'])
        if not hci_years.empty:
            latest_hci_year = hci_years['Year'].max()
            latest_hci = filtered_df[filtered_df['Year'] == latest_hci_year]['Human Capital Index (HCI) (scale 0-1)'].iloc[0]
            hci_value = f"{latest_hci:.2f} ({latest_hci_year})"
            hci_global_compare = f"{latest_hci / benchmarks['human_capital_index']['global_avg']:.1f}x global average"
        else:
            hci_value = get_translation("Data unavailable", language)
            hci_global_compare = ""
    except (ValueError, KeyError, TypeError, IndexError):
        hci_value = get_translation("Data unavailable", language)
        hci_global_compare = ""
        
    try:
        co2_value = f"{latest_data['Annual CO₂ emissions (per capita)']:.1f} {get_translation('tonnes', language)}"
        co2_global_compare = f"{latest_data['Annual CO₂ emissions (per capita)'] / benchmarks['co2_per_capita']['global_avg']:.1f}x global average"
    except (ValueError, KeyError, TypeError):
        co2_value = get_translation("Data unavailable", language)
        co2_global_compare = ""
        
    try:
        # Find the latest non-NaN sanitation value
        sanit_years = filtered_df.dropna(subset=['Share of the population using safely managed sanitation services'])
        if not sanit_years.empty:
            latest_sanit_year = sanit_years['Year'].max()
            latest_sanit = filtered_df[filtered_df['Year'] == latest_sanit_year]['Share of the population using safely managed sanitation services'].iloc[0]
            sanit_value = f"{latest_sanit:.1f}% ({latest_sanit_year})"
            sanit_global_compare = f"{latest_sanit / benchmarks['sanitation']['global_avg']:.1f}x global average"
        else:
            sanit_value = get_translation("Data unavailable", language)
            sanit_global_compare = ""
    except (ValueError, KeyError, TypeError, IndexError):
        sanit_value = get_translation("Data unavailable", language)
        sanit_global_compare = ""
    
    # Create key metric cards with icons and comparisons
    key_cards = dbc.Row([
        dbc.Col(
            create_kpi_card(
                title="GDP per Capita (PPP)",
                value=gdp_value,
                subtitle="Latest value",
                comparison=gdp_global_compare,
                icon="fas fa-money-bill-wave",
                color=colors['key'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Human Capital Index",
                value=hci_value,
                subtitle="Scale: 0-1",
                comparison=hci_global_compare,
                icon="fas fa-user-graduate",
                color=colors['key'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="CO₂ Emissions per Capita",
                value=co2_value,
                subtitle="Latest value",
                comparison=co2_global_compare,
                icon="fas fa-smog",
                color=colors['key'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Sanitation Access",
                value=sanit_value,
                subtitle="Latest value",
                comparison=sanit_global_compare,
                icon="fas fa-hands-wash",
                color=colors['key'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
    ], className="mb-4 g-4")
    
    # Create benchmark comparison cards with translations
    gdp_benchmark_card = create_benchmark_card("GDP per Capita (PPP) Benchmarks", benchmarks["gdp_per_capita"], colors['key'], language)
    hci_benchmark_card = create_benchmark_card("Human Capital Index Benchmarks", benchmarks["human_capital_index"], colors['key'], language)
    co2_benchmark_card = create_benchmark_card("CO₂ Emissions per Capita Benchmarks", benchmarks["co2_per_capita"], colors['key'], language)
    renewables_benchmark_card = create_benchmark_card("Renewables Share Benchmarks", benchmarks["renewables_share"], colors['key'], language)
    stem_benchmark_card = create_benchmark_card("STEM Graduates Benchmarks", benchmarks["stem_graduates"], colors['key'], language)
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Dashboard Insights", overall_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader([
            html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0", style={"color": colors['text']})
        ], style={"borderLeft": f"4px solid {colors['highlight']}", "borderRadius": "8px 8px 0 0", 
                 "background": f"linear-gradient(to right, {colors['highlight']}15, {colors['gradient_start']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
        ])
    ], className="mb-4 shadow-sm hover-card", style={"borderRadius": "8px", "overflow": "hidden", "backgroundColor": colors['card']})
    
    # Create layout with paired insights and charts
    layout = html.Div([
        key_cards,
        dbc.Row([
            dbc.Col([
                html.H4(get_translation("Key Indicators Analysis", language), 
                       className="mt-4 mb-4 text-center section-title", 
                       style={"color": colors['text'], "fontWeight": "600"})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # GDP insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("GDP per Capita", gdp_insights, colors['key'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=gdp_fig), className="chart-container shadow-sm mb-3"),
                gdp_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # HCI insights and chart
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(figure=hci_fig), className="chart-container shadow-sm mb-3"),
                hci_benchmark_card
            ], width={"size": 7, "order": 1 if language == "english" else 12}, className="mb-4"),
            dbc.Col(create_insight_card("Human Capital Index", hci_insights, colors['key'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # CO2 insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("CO₂ Emissions", co2_insights, colors['key'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=co2_fig), className="chart-container shadow-sm mb-3"),
                co2_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Renewable insights and chart
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(figure=renewable_fig), className="chart-container shadow-sm mb-3"),
                renewables_benchmark_card
            ], width={"size": 7, "order": 1 if language == "english" else 12}, className="mb-4"),
            dbc.Col(create_insight_card("Renewable Energy", renewable_insights, colors['key'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Energy production chart with added insights
        dbc.Row([
            dbc.Col(create_insight_card("Energy Production", energy_production_insights, colors['key'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=energy_fig), className="chart-container shadow-sm")
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Education metrics chart with added insights
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(figure=education_fig), className="chart-container shadow-sm")
            ], width={"size": 7, "order": 1 if language == "english" else 12}, className="mb-4"),
            dbc.Col(create_insight_card("Education Metrics", education_metrics_insights, colors['key'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # STEM graduates chart with added insights
        dbc.Row([
            dbc.Col(create_insight_card("STEM Graduates", stem_graduates_insights, colors['key'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=stem_fig), className="chart-container shadow-sm mb-3"),
                stem_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Overall insights
        overall_insights_card,
    ], className="tab-content")
    
    return layout

# Function to render Economic Development tab with insights from PDF
def render_economic(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = economic_df[(economic_df['Year'] >= min_year) & (economic_df['Year'] <= max_year)]
    
    # Create GDP charts with improved styling and translations
    gdp_fig = px.line(
        filtered_df, 
        x='Year', 
        y=['GDP per capita, PPP (constant 2021 international $)', 'GDP per capita'],
        title=get_translation('GDP per Capita Trends', language),
        markers=True,
        color_discrete_sequence=[colors['economic'], '#17becf'],
        labels={"value": get_translation("GDP per capita, PPP (2021 international $)", language), "variable": ""}
    )

    if language == 'arabic':
        gdp_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for GDP per capita with translations
    gdp_fig.add_hline(y=benchmarks["gdp_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                     annotation_text=get_translation(f"Global Average: ${benchmarks['gdp_per_capita']['global_avg']:,}", language), 
                     annotation_position="bottom right")
    
    for region, value in benchmarks["gdp_per_capita"]["regional"].items():
        gdp_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                         annotation_text=get_translation(f"{region}: ${value:,}", language), 
                         annotation_position="bottom right")
    
    # Apply modern styling to chart
    gdp_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    gdp_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Energy Production chart with improved styling
    energy_production_fig = px.line(
        filtered_df,
        x='Year',
        y=['Oil production (TWh)', 'Gas production - TWh'],
        title=get_translation('Energy Production (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['economic'], '#17becf'],
        labels={"value": get_translation("Oil production and Gas production - TWh", language), "variable": ""}
    )

    if language == 'arabic':
        energy_production_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation for LNG expansion plans with translation
    energy_production_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df['Gas production - TWh'].max(),
        text=get_translation("Qatar plans to boost LNG output<br>by 85% by 2030 (126-142M tons)", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to energy production chart
    energy_production_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    energy_production_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)

    # Add coal consumption as a separate trace with secondary y-axis
    coal_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add primary energy traces
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Primary energy consumption - TWh'],
            name=get_translation("Primary Energy", language),
            line=dict(color=colors['economic'], width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=False
    )
    
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Oil consumption - TWh'],
            name=get_translation("Oil Consumption", language),
            line=dict(color='#17becf', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=False
    )
    
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Gas consumption - TWh'],
            name=get_translation("Gas Consumption", language),
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=False
    )
    
    # Add coal consumption on secondary y-axis
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Coal consumption - TWh'],
            name=get_translation("Coal Consumption", language),
            line=dict(color='#d62728', dash='dot', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=True
    )
    
    # Update layout with modern styling and translations
    coal_fig.update_layout(
        title_text=get_translation("Energy Consumption", language),
        title_font=dict(size=18, family="Poppins, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    coal_fig.update_xaxes(
        title_text=get_translation("Year", language),
        gridcolor='rgba(220, 220, 220, 0.2)',
        tickfont=dict(family="Poppins, sans-serif")
    )
    coal_fig.update_yaxes(
        title_text=get_translation("Energy Consumption (TWh)", language), 
        secondary_y=False,
        gridcolor='rgba(220, 220, 220, 0.2)',
        tickfont=dict(family="Poppins, sans-serif")
    )
    coal_fig.update_yaxes(
        title_text=get_translation("Coal Consumption (TWh)", language), 
        secondary_y=True,
        tickfont=dict(family="Poppins, sans-serif")
    )
    
    # Connect gaps between points for better trend visualization
    coal_fig.update_traces(connectgaps=True)
    
    # Create Energy Growth chart with improved styling
    energy_growth_fig = px.bar(
        filtered_df,
        x='Year',
        y=['Oil (% growth)', 'Gas (% growth)', 'Coal (% growth)'],
        title=get_translation('Energy Growth Rates (%)', language),
        barmode='group',
        color_discrete_sequence=[colors['economic'], '#17becf', '#ff7f0e'],
        labels={"value": get_translation("Oil, Gas and Coal (% growth)", language), "variable": ""}
    )

    if language == 'arabic':
        energy_growth_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison
    energy_growth_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df[['Oil (% growth)', 'Gas (% growth)', 'Coal (% growth)']].max().max(),
        text=get_translation("Global energy demand growth: ~1-2% per year<br>Qatar targets: 2-3% growth by 2030<br>Past Qatar growth: ~6-7% annually", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to energy growth chart
    energy_growth_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    
    # Create Agriculture Value chart 
    agriculture_fig = px.line(
        filtered_df,
        x='Year',
        y='Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)',
        title=get_translation('Agriculture, Forestry, and Fishing Value Added per Worker', language),
        markers=True,
        color_discrete_sequence=[colors['economic']],
        labels={"Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)": get_translation("Agriculture, forestry, and fishing, value per worker 2015 US$", language), "variable": ""}
    )

    if language == 'arabic':
        agriculture_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison
    agriculture_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)'].max(),
        text=get_translation("Qatar's per-worker ag value: $10-11K<br>Regional peer (Oman): ~$6K<br>Advanced economies: >$50K", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to agriculture chart
    agriculture_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    agriculture_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Business Graduates chart
    business_fig = px.line(
        filtered_df,
        x='Year',
        y='Percentage of graduates from tertiary education graduating from Business, Administration and Law programmes, (%)',
        title=get_translation('Business, Administration and Law Graduates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['economic']],
        labels={"value": "", "variable": ""}
    )

    if language == 'arabic':
        business_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotations for business graduate percentage
    business_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Percentage of graduates from tertiary education graduating from Business, Administration and Law programmes, (%)'].mean(),
        text=get_translation("Qatar 2018: ~26% business/law graduates<br>Regional comparison (Bahrain): ~50%<br>Vision 2030 aims to balance with STEM fields", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to business chart
    business_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            title=get_translation("Business & Law Graduates (%)", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    business_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Extract latest values for KPI cards
    try:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
        
        gdp_value = f"${latest_data['GDP per capita, PPP (constant 2021 international $)']:,.0f}"
        gdp_global_compare = f"{latest_data['GDP per capita, PPP (constant 2021 international $)'] / benchmarks['gdp_per_capita']['global_avg']:.1f}x global average"
        oil_prod = f"{latest_data['Oil production (TWh)']:,.1f} TWh"
        gas_prod = f"{latest_data['Gas production - TWh']:,.1f} TWh"
        energy_cons = f"{latest_data['Primary energy consumption - TWh']:,.1f} TWh"
    except:
        gdp_value = get_translation("N/A", language)
        gdp_global_compare = ""
        oil_prod = get_translation("N/A", language)
        gas_prod = get_translation("N/A", language)
        energy_cons = get_translation("N/A", language)
    
    # Create KPI cards for economic section
    kpi_cards = dbc.Row([
        dbc.Col(
            create_kpi_card(
                title="GDP per Capita (PPP)",
                value=gdp_value,
                subtitle="Latest value",
                comparison=gdp_global_compare,
                icon="fas fa-money-bill-wave",
                color=colors['economic'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Oil Production",
                value=oil_prod,
                subtitle="Latest value",
                comparison="0.67M barrels/day (modest for GCC)",
                icon="fas fa-oil-can",
                color=colors['economic'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Gas Production",
                value=gas_prod,
                subtitle="Latest value",
                comparison="177 billion m³ (globally significant)",
                icon="fas fa-burn",
                color=colors['economic'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Energy Consumption",
                value=energy_cons,
                subtitle="Latest value",
                comparison="Among GCC's highest per capita",
                icon="fas fa-bolt",
                color=colors['economic'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
    ], className="mb-4 g-4")
    
    # Create benchmark comparison cards with translations
    gdp_benchmark_card = create_benchmark_card("GDP per Capita (PPP) Benchmarks", benchmarks["gdp_per_capita"], colors['economic'], language)
    agriculture_benchmark_card = create_benchmark_card("Agricultural Productivity", benchmarks["agriculture_value"], colors['economic'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader([
            html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0", style={"color": colors['text']})
        ], style={"borderLeft": f"4px solid {colors['highlight']}", "borderRadius": "8px 8px 0 0", 
                 "background": f"linear-gradient(to right, {colors['highlight']}15, {colors['gradient_start']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
        ])
    ], className="mb-4 shadow-sm hover-card", style={"borderRadius": "8px", "overflow": "hidden", "backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Economic Development Insights", overall_economic_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        
        dbc.Row([
            dbc.Col([
                html.H4(get_translation("Economic Development Analysis", language), 
                       className="mt-4 mb-4 text-center section-title", 
                       style={"color": colors['text'], "fontWeight": "600"})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # GDP insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("GDP per Capita Trends", economic_gdp_insights, colors['economic'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=gdp_fig), className="chart-container shadow-sm mb-3"),
                gdp_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Oil production insights and chart
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=energy_production_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(
                create_insight_card("Energy Production", oil_insights, colors['economic'], language), 
                width={"size": 5, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # Energy consumption chart and insights
        dbc.Row([
            dbc.Col(
                create_insight_card("Energy Consumption", energy_consumption_insights, colors['economic'], language), 
                width={"size": 5, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(
                html.Div(dcc.Graph(figure=coal_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # Energy growth chart and insights
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=energy_growth_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(
                create_insight_card("Energy Growth Rates", energy_growth_insights, colors['economic'], language), 
                width={"size": 5, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # Agriculture and business charts with insights
        dbc.Row([
            dbc.Col(
                create_insight_card("Agricultural Productivity", agriculture_insights, colors['economic'], language), 
                width={"size": 5, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col([
                html.Div(dcc.Graph(figure=agriculture_fig), className="chart-container shadow-sm mb-3"),
                agriculture_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=business_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(
                create_insight_card("Business, Administration and Law Graduates", business_graduates_insights, colors['economic'], language), 
                width={"size": 5, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # Overall insights
        overall_insights_card,
    ], className="tab-content")
    
    return layout

# Function to render Environmental Development tab with insights
def render_environmental(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = environmental_df[(environmental_df['Year'] >= min_year) & (environmental_df['Year'] <= max_year)]
    
    # Create CO2 Emissions charts with improved styling
    co2_fig = px.line(
        filtered_df,
        x='Year',
        y=['Annual CO₂ emissions', 'Annual CO₂ emissions from oil'],
        title=get_translation('Annual CO₂ Emissions (tonnes)', language),
        markers=True,
        color_discrete_sequence=[colors['environmental'], '#17becf'],
        labels={"value": get_translation("Annual CO₂ emissions and Annual CO₂ emissions from oil", language), "variable": ""}
    )

    if language == 'arabic':
        co2_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison
    co2_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Annual CO₂ emissions'].max(),
        text=get_translation("Qatar 2023: ~128M tonnes CO₂<br>Global total: 36.8B tonnes<br>Saudi Arabia: ~600M tonnes<br>UAE: ~230M tonnes", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to CO2 chart
    co2_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    co2_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create CO2 Emissions per capita chart
    co2_per_capita_fig = px.line(
        filtered_df,
        x='Year',
        y=['Annual CO₂ emissions (per capita)', 'Annual CO₂ emissions from oil (per capita)'],
        title=get_translation('Annual CO₂ Emissions per Capita', language),
        markers=True,
        color_discrete_sequence=[colors['environmental'], '#17becf'],
        labels={"value": get_translation("Annual CO₂ emissions and CO₂ emissions from oil per capita", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        co2_per_capita_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))

    # Add benchmark lines for CO2 per capita
    co2_per_capita_fig.add_hline(y=benchmarks["co2_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                               annotation_text=get_translation(f"Global Average: {benchmarks['co2_per_capita']['global_avg']} tonnes", language), 
                               annotation_position="top right")
    
    for region, value in benchmarks["co2_per_capita"]["regional"].items():
        co2_per_capita_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                                   annotation_text=get_translation(f"{region}: {value} tonnes", language), 
                                   annotation_position="bottom right")
    
    # Apply modern styling to CO2 per capita chart
    co2_per_capita_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=0.95,
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    co2_per_capita_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Energy Change chart
    energy_change_fig = px.bar(
        filtered_df,
        x='Year',
        y=['Annual change in primary energy consumption (%)'],
        title=get_translation('Annual Change in Primary Energy Consumption (%)', language),
        color_discrete_sequence=[colors['environmental']],
        labels={"value": get_translation("Annual change in primary energy consumption (%)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        energy_change_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison
    energy_change_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Annual change in primary energy consumption (%)'].max(),
        text=get_translation("Global energy demand growth: ~1.9% (2022)<br>Qatar's historical growth: ~5-6% in 2010s<br>Qatar's 2030 target: <3% annually", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to energy change chart
    energy_change_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    
    # Create Electricity Production chart with labels
    elec_df = filtered_df.copy()
    elec_df['Fossil Fuels (TWh)'] = elec_df['Electricity from fossil fuels - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']
    elec_df['Nuclear (TWh)'] = elec_df['Electricity from nuclear - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']
    elec_df['Renewables (TWh)'] = elec_df['Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']

    electricity_fig = px.area(
        elec_df,
        x='Year',
        y=['Fossil Fuels (TWh)', 'Nuclear (TWh)', 'Renewables (TWh)'],
        title=get_translation('Electricity Production by Source (TWh)', language),
        color_discrete_sequence=['#636EFA', '#EF553B', colors['environmental']],
        labels={"Electricity Production (TWh) - Log Scale": "", "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        electricity_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison
    electricity_fig.add_annotation(
        x=elec_df['Year'].median(),
        y=elec_df['Fossil Fuels (TWh)'].max(),
        text=get_translation("Qatar 2023: >99% fossil fuels<br>Global mix: 61% non-renewables<br>Qatar's 2030 target: 20% renewables", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to electricity chart
    electricity_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            title=get_translation("Electricity Production (TWh)", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    
    # Create Renewable Electricity detail chart with labels
    renew_df = filtered_df.copy()
    renew_df['Solar (TWh)'] = renew_df['Electricity from solar - TWh (adapted for visualization of chart electricity-prod-source-stacked)']
    renew_df['Bioenergy (TWh)'] = renew_df['Electricity from bioenergy - TWh (adapted for visualization of chart electricity-prod-source-stacked)']

    renewable_detail_fig = px.area(
        renew_df,
        x='Year',
        y=['Solar (TWh)', 'Bioenergy (TWh)'],
        title=get_translation('Renewable Electricity Production Detail (TWh)', language),
        color_discrete_sequence=[colors['environmental'], '#17becf'],
        labels={"value": get_translation("Solar, Bioenergy (TWh)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        renewable_detail_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation with global comparison
    renewable_detail_fig.add_annotation(
        x=renew_df['Year'].median(),
        y=renew_df['Solar (TWh)'].max() * 1.5,
        text=get_translation("Qatar renewable output: ~0.15 TWh<br>Global renewables: 7,858 TWh (2021)<br>Middle East renewables: 47 TWh (2022)", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to renewable detail chart
    renewable_detail_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    renewable_detail_fig.update_traces(connectgaps=True)
    
    # Create Solar capacity and growth chart
    solar_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    solar_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Solar capacity (total) (GW)'], 
            name=get_translation("Solar Capacity (GW)", language), 
            line=dict(color=colors['environmental'], width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=False,
    )
    
    solar_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Solar (% growth)'], 
            name=get_translation("Solar Growth (%)", language), 
            line=dict(color="#17becf", dash="dash", width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=True,
    )
    
    # Add annotation with target
    solar_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df['Solar capacity (total) (GW)'].max(),
        text=get_translation("Qatar 2023: 0.8 GW<br>Qatar target 2030: 4 GW<br>15,686% growth from 2016-2023", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to solar chart
    solar_fig.update_layout(
        title_text=get_translation("Solar Capacity and Growth", language),
        title_font=dict(size=18, family="Poppins, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    solar_fig.update_xaxes(
        title_text=get_translation("Year", language),
        gridcolor='rgba(220, 220, 220, 0.2)',
        tickfont=dict(family="Poppins, sans-serif")
    )
    solar_fig.update_yaxes(
        title_text=get_translation("Capacity (GW)", language), 
        secondary_y=False,
        gridcolor='rgba(220, 220, 220, 0.2)',
        tickfont=dict(family="Poppins, sans-serif")
    )
    solar_fig.update_yaxes(
        title_text=get_translation("Growth (%)", language), 
        secondary_y=True,
        tickfont=dict(family="Poppins, sans-serif")
    )
    solar_fig.update_traces(connectgaps=True)
    
    # Extract latest values for KPI cards
    try:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
        
        co2_emissions = f"{latest_data['Annual CO₂ emissions']:,.1f} {get_translation('tonnes', language)}"
        co2_per_capita = f"{latest_data['Annual CO₂ emissions (per capita)']:,.1f} {get_translation('tonnes', language)}"
        co2_global_compare = f"{latest_data['Annual CO₂ emissions (per capita)'] / benchmarks['co2_per_capita']['global_avg']:.1f}x global average"
        renewable_electricity = f"{latest_data['Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']:,.2f} TWh"
        solar_capacity = f"{latest_data['Solar capacity (total) (GW)']:,.4f} GW"
    except:
        co2_emissions = get_translation("N/A", language)
        co2_global_compare = ""
        co2_per_capita = get_translation("N/A", language)
        renewable_electricity = get_translation("N/A", language)
        solar_capacity = get_translation("N/A", language)
    
    # Create KPI cards for environmental section
    kpi_cards = dbc.Row([
        dbc.Col(
            create_kpi_card(
                title="CO₂ Emissions",
                value=co2_emissions,
                subtitle="Latest value",
                comparison="Small share of global total",
                icon="fas fa-smog",
                color=colors['environmental'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="CO₂ per Capita",
                value=co2_per_capita,
                subtitle="Latest value",
                comparison=co2_global_compare,
                icon="fas fa-user-alt",
                color=colors['environmental'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Renewable Electricity",
                value=renewable_electricity,
                subtitle="Latest value",
                comparison="0.3% of electricity mix",
                icon="fas fa-solar-panel",
                color=colors['environmental'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Solar Capacity",
                value=solar_capacity,
                subtitle="Latest value",
                comparison="Target: 4GW by 2030",
                icon="fas fa-sun",
                color=colors['environmental'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
    ], className="mb-4 g-4")
    
    # Create benchmark comparison cards with translations
    co2_benchmark_card = create_benchmark_card("CO₂ Emissions per Capita Benchmarks", benchmarks["co2_per_capita"], colors['environmental'], language)
    renewables_benchmark_card = create_benchmark_card("Renewables Share Benchmarks", benchmarks["renewables_share"], colors['environmental'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader([
            html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0", style={"color": colors['text']})
        ], style={"borderLeft": f"4px solid {colors['highlight']}", "borderRadius": "8px 8px 0 0", 
                 "background": f"linear-gradient(to right, {colors['highlight']}15, {colors['gradient_start']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
        ])
    ], className="mb-4 shadow-sm hover-card", style={"borderRadius": "8px", "overflow": "hidden", "backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Environmental Development Insights", overall_environmental_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        
        dbc.Row([
            dbc.Col([
                html.H4(get_translation("Environmental Development Analysis", language), 
                       className="mt-4 mb-4 text-center section-title", 
                       style={"color": colors['text'], "fontWeight": "600"})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # CO2 emissions insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("CO₂ Emissions", co2_insights, colors['environmental'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col(
                html.Div(dcc.Graph(figure=co2_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(figure=co2_per_capita_fig), className="chart-container shadow-sm mb-3"),
                co2_benchmark_card
            ], width={"size": 7, "order": 1 if language == "english" else 12}, className="mb-4"),
            dbc.Col(
                html.Div(dcc.Graph(figure=energy_change_fig), className="chart-container shadow-sm"),
                width={"size": 5, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # Energy Change insights and card
        dbc.Row([
            dbc.Col(create_insight_card("Energy Consumption Change", energy_change_insights, colors['environmental'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col(create_insight_card("Agricultural Development", agricultural_insights, colors['environmental'], language), 
                   width={"size": 7, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Electricity production insights and charts
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=electricity_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(create_insight_card("Electricity Production", electricity_insights, colors['environmental'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Renewable and solar insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Solar Energy Development", solar_insights, colors['environmental'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=solar_fig), className="chart-container shadow-sm mb-3"),
                renewables_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Renewable detail chart with insights
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=renewable_detail_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(create_insight_card("Renewable Energy Detail", renewable_detail_insights, colors['environmental'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Overall insights
        overall_insights_card,
    ], className="tab-content")
    
    return layout

# Function to render Human Development tab with insights
def render_human(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = human_df[(human_df['Year'] >= min_year) & (human_df['Year'] <= max_year)]
    
    # Create Education Level charts with labels layout
    # Create a copy of the dataframe with shorter column names
    edu_df = filtered_df.copy()
    edu_df['Primary Education (%)'] = edu_df['UIS: Percentage of population age 25+ with at least completed primary education (ISCED 1 or higher). Total']
    edu_df['Secondary Education (%)'] = edu_df['UIS: Percentage of population age 25+ with at least completed upper secondary education (ISCED 3 or higher). Total'] 
    edu_df['Bachelor Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with at least a completed bachelor\'s or equivalent degree (ISCED 6 or higher). Total']

    education_level_fig = px.line(
        edu_df,
        x='Year',
        y=['Primary Education (%)', 'Secondary Education (%)', 'Bachelor Degree (%)'],
        title=get_translation('Population Education Levels (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf', '#ff7f0e'],
        labels={"value": get_translation("Primary Education, Secondary Education and Bachelor Degree (%)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        education_level_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation with global comparison
    education_level_fig.add_annotation(
        x=edu_df['Year'].median(),
        y=edu_df['Bachelor Degree (%)'].max(),
        text=get_translation("Qatar tertiary attainment: ~30%<br>High-income countries: 30-45%<br>Leading countries (Canada/Korea): >55%", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to education level chart
    education_level_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    education_level_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Advanced education with shortened labels and improved layout
    edu_df['Master Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with at least a completed master\'s degree or equivalent (ISCED 7 or higher). Total']
    edu_df['Doctoral Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with a doctoral degree or equivalent (ISCED 8). Total']

    advanced_edu_fig = px.line(
        edu_df,
        x='Year',
        y=['Master Degree (%)', 'Doctoral Degree (%)'],
        title=get_translation('Advanced Education Levels (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf'],
        labels={"value": get_translation("Master Degree and Doctoral Degree (%)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        advanced_edu_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation with OECD comparison
    advanced_edu_fig.add_annotation(
        x=edu_df['Year'].median(),
        y=edu_df['Master Degree (%)'].max(),
        text=get_translation("OECD tertiary attainment: ~39%<br>Qatar aims to lead Arab world<br>in higher education outcomes", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to advanced education chart
    advanced_edu_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    advanced_edu_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Completion Rate charts
    completion_rate_fig = px.line(
        filtered_df,
        x='Year',
        y=['Primary completion rate, total (% of relevant age group)',
           'Lower secondary completion rate, total (% of relevant age group)'],
        title=get_translation('Education Completion Rates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf'],
        labels={"value": get_translation("Primary and Lower secondary completion rate total", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        completion_rate_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation with global comparison
    completion_rate_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Primary completion rate, total (% of relevant age group)'].max(),
        text=get_translation("Qatar primary: ~98-99%<br>Global average: ~89%<br>Global secondary: ~75%", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to completion rate chart
    completion_rate_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    completion_rate_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create School Life Expectancy chart
    school_life_fig = px.line(
        filtered_df,
        x='Year',
        y=['School life expectancy, primary to tertiary, both sexes (years)',
           'Expected Years of School',
           'Learning-Adjusted Years of School'],
        title=get_translation('School Life Expectancy and Learning Years', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf', '#ff7f0e'],
        labels={"value": get_translation("'School life expectancy, primary to tertiary and Learning-Adjusted", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        school_life_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add benchmark lines for education years with translations
    school_life_fig.add_hline(y=benchmarks["education_years"]["expected"]["global_avg"], line_dash="dash", line_color=colors['global'],
                            annotation_text=get_translation(f"Global Avg Expected: {benchmarks['education_years']['expected']['global_avg']} years", language), 
                            annotation_position="bottom left")
    
    school_life_fig.add_hline(y=benchmarks["education_years"]["learning_adjusted"]["global_avg"], line_dash="dash", line_color=colors['global'],
                            annotation_text=get_translation(f"Global Avg Learning-Adjusted: {benchmarks['education_years']['learning_adjusted']['global_avg']} years", language), 
                            annotation_position="bottom right")
    
    school_life_fig.add_hline(y=benchmarks["education_years"]["expected"]["leading"], line_dash="dot", line_color=colors['leading'],
                            annotation_text=get_translation(f"Leading Countries Expected: {benchmarks['education_years']['expected']['leading']} years", language), 
                            annotation_position="top right")
    
    school_life_fig.add_hline(y=benchmarks["education_years"]["learning_adjusted"]["leading"], line_dash="dot", line_color=colors['leading'],
                            annotation_text=get_translation(f"Leading Countries Learning-Adjusted: {benchmarks['education_years']['learning_adjusted']['leading']} years", language), 
                            annotation_position="bottom left")
    
    # Apply modern styling to school life expectancy chart
    school_life_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=0.95,
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    school_life_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Extract latest values for KPI cards
    try:
        # Find years with non-null values for each metric
        bachelor_years = edu_df.dropna(subset=['Bachelor Degree (%)']).sort_values('Year')
        if not bachelor_years.empty:
            latest_bachelor_year = bachelor_years['Year'].max()
            latest_bachelor = bachelor_years[bachelor_years['Year'] == latest_bachelor_year]['Bachelor Degree (%)'].iloc[0]
            bachelor_value = f"{latest_bachelor:.1f}%"
            # Compare to global benchmarks
            bachelor_global_compare = "Above global average, below leading countries"
        else:
            bachelor_value = get_translation("N/A", language)
            bachelor_global_compare = ""
            
        hci_years = filtered_df.dropna(subset=['Human Capital Index (HCI) (scale 0-1)']).sort_values('Year')
        if not hci_years.empty:
            latest_hci_year = hci_years['Year'].max()
            latest_hci = hci_years[hci_years['Year'] == latest_hci_year]['Human Capital Index (HCI) (scale 0-1)'].iloc[0]
            hci_value = f"{latest_hci:.3f}"
            hci_global_compare = f"{latest_hci / benchmarks['human_capital_index']['global_avg']:.1f}x global average"
        else:
            hci_value = get_translation("N/A", language)
            hci_global_compare = ""
            
        school_years = filtered_df.dropna(subset=['Expected Years of School']).sort_values('Year')
        if not school_years.empty:
            latest_school_year = school_years['Year'].max()
            latest_expected = school_years[school_years['Year'] == latest_school_year]['Expected Years of School'].iloc[0]
            expected_value = f"{latest_expected:.1f} {get_translation('years', language)}"
            expected_global_compare = f"{latest_expected / benchmarks['education_years']['expected']['global_avg']:.1f}x global average"
        else:
            expected_value = get_translation("N/A", language)
            expected_global_compare = ""
            
        learning_years = filtered_df.dropna(subset=['Learning-Adjusted Years of School']).sort_values('Year')
        if not learning_years.empty:
            latest_learning_year = learning_years['Year'].max()
            latest_learning = learning_years[learning_years['Year'] == latest_learning_year]['Learning-Adjusted Years of School'].iloc[0]
            learning_value = f"{latest_learning:.1f} {get_translation('years', language)}"
            learning_global_compare = f"{latest_learning / benchmarks['education_years']['learning_adjusted']['global_avg']:.1f}x global average"
        else:
            learning_value = get_translation("N/A", language)
            learning_global_compare = ""
    except:
        bachelor_value = get_translation("N/A", language)
        bachelor_global_compare = ""
        hci_value = get_translation("N/A", language)
        hci_global_compare = ""
        expected_value = get_translation("N/A", language)
        expected_global_compare = ""
        learning_value = get_translation("N/A", language)
        learning_global_compare = ""
    
    # Create KPI cards for human development section
    kpi_cards = dbc.Row([
        dbc.Col(
            create_kpi_card(
                title="Bachelor's Degree or Higher",
                value=bachelor_value,
                subtitle="of adult population",
                comparison=bachelor_global_compare,
                icon="fas fa-user-graduate",
                color=colors['human'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Human Capital Index",
                value=hci_value,
                subtitle="Scale: 0-1",
                comparison=hci_global_compare,
                icon="fas fa-brain",
                color=colors['human'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Expected Years of School",
                value=expected_value,
                subtitle="Latest value",
                comparison=expected_global_compare,
                icon="fas fa-school",
                color=colors['human'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Learning-Adjusted Years",
                value=learning_value,
                subtitle="Latest value",
                comparison=learning_global_compare,
                icon="fas fa-book-reader",
                color=colors['human'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
    ], className="mb-4 g-4")
    
    # Create benchmark comparison cards with translations
    hci_benchmark_card = create_benchmark_card("Human Capital Index Benchmarks", benchmarks["human_capital_index"], colors['human'], language)
    tertiary_benchmark_card = create_benchmark_card("Tertiary Education", benchmarks["tertiary_enrollment"], colors['human'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader([
            html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0", style={"color": colors['text']})
        ], style={"borderLeft": f"4px solid {colors['highlight']}", "borderRadius": "8px 8px 0 0", 
                 "background": f"linear-gradient(to right, {colors['highlight']}15, {colors['gradient_start']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
        ])
    ], className="mb-4 shadow-sm hover-card", style={"borderRadius": "8px", "overflow": "hidden", "backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Human Development Insights", overall_human_development_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        
        dbc.Row([
            dbc.Col([
                html.H4(get_translation("Human Development Analysis", language), 
                       className="mt-4 mb-4 text-center section-title", 
                       style={"color": colors['text'], "fontWeight": "600"})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # Educational attainment insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Educational Attainment", educational_attainment_insights, colors['human'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=education_level_fig), className="chart-container shadow-sm mb-3"),
                tertiary_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Advanced education levels with insights
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=advanced_edu_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(create_insight_card("Advanced Education", advanced_education_insights, colors['human'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Education quality insights
        dbc.Row([
            dbc.Col(create_insight_card("Education Quality", education_quality_insights, colors['human'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col(
                html.Div(dcc.Graph(figure=school_life_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 12 if language == "english" else 1}, 
                className="mb-4"
            ),
        ], className="chart-row align-items-stretch"),
        
        # School completion and human capital development
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=completion_rate_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(create_insight_card("Completion Rates", completion_rates_insights, colors['human'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Human capital and gender equity
        dbc.Row([
            dbc.Col([
                create_insight_card("Human Capital Development", human_capital_insights, colors['human'], language),
                hci_benchmark_card
            ], width={"size": 5, "order": 1 if language == "english" else 12}, className="mb-4"),
            dbc.Col(create_insight_card("Gender Equity in Education", gender_equity_insights, colors['human'], language), 
                   width={"size": 7, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Overall insights
        overall_insights_card,
    ], className="tab-content")
    
    return layout

# Function to render Social Development tab with insights
def render_social(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = social_df[(social_df['Year'] >= min_year) & (social_df['Year'] <= max_year)]
    
    # Create Sanitation Services chart with handling for NaN values and connected gaps
    sanitation_df = filtered_df.dropna(subset=['Share of the population using safely managed sanitation services'])
    
    if not sanitation_df.empty:
        sanitation_fig = px.line(
            sanitation_df,
            x='Year',
            y='Share of the population using safely managed sanitation services',
            title=get_translation('Population with Safely Managed Sanitation Services (%)', language),
            markers=True,
            color_discrete_sequence=[colors['social']],
            labels={"Share of the population using safely managed sanitation services": get_translation("Share of the population using safely managed sanitation services", language), "variable": ""}
        )
        
        # Translate trace names for Arabic
        if language == 'arabic':
            sanitation_fig.for_each_trace(lambda t: t.update(
                name=get_translation(t.name, language)
            ))
            
        # Add benchmark lines for sanitation with translations
        sanitation_fig.add_hline(y=benchmarks["sanitation"]["global_avg"], line_dash="dash", line_color=colors['global'],
                               annotation_text=get_translation(f"Global Average: {benchmarks['sanitation']['global_avg']}%", language), 
                               annotation_position="bottom right")
        
        for region, value in benchmarks["sanitation"]["regional"].items():
            sanitation_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                                   annotation_text=get_translation(f"{region}: {value}%", language), 
                                   annotation_position="bottom right")
        
        for leader, value in benchmarks["sanitation"]["leading"].items():
            sanitation_fig.add_hline(y=value, line_dash="dot", line_color=colors['leading'],
                                   annotation_text=get_translation(f"{leader}: {value}%", language), 
                                   annotation_position="top left")
        
        # Apply modern styling to sanitation chart
        sanitation_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins, sans-serif", color=colors['text']),
            margin=dict(l=40, r=40, t=40, b=40),
            hovermode="x unified",
            title=dict(font=dict(size=18, family="Poppins, sans-serif")),
            xaxis=dict(
                title=get_translation("Year", language),
                gridcolor='rgba(220, 220, 220, 0.2)',
                tickfont=dict(family="Poppins, sans-serif")
            ),
            yaxis=dict(
                gridcolor='rgba(220, 220, 220, 0.2)',
                tickfont=dict(family="Poppins, sans-serif")
            )
        )
        sanitation_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    else:
        # Create an empty figure with a message if no data is available
        sanitation_fig = go.Figure()
        sanitation_fig.update_layout(
            title=get_translation("Population with Safely Managed Sanitation Services (%)", language),
            title_font=dict(size=18, family="Poppins, sans-serif"),
            annotations=[dict(
                text=get_translation("No data available for sanitation services", language),
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, family="Poppins, sans-serif")
            )],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins, sans-serif", color=colors['text']),
            margin=dict(l=40, r=40, t=40, b=40),
        )
    
    # Create Gender Parity charts with shortened labels and improved layout
    gpi_df = filtered_df.copy()
    gpi_df['Primary Education GPI'] = gpi_df['School enrollment, primary (gross), gender parity index (GPI)']
    gpi_df['Tertiary Education GPI'] = gpi_df['Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, gender parity index (GPI)']

    gender_parity_fig = px.line(
        gpi_df,
        x='Year',
        y=['Primary Education GPI', 'Tertiary Education GPI'],
        title=get_translation('Gender Parity Indices in Education', language),
        markers=True,
        color_discrete_sequence=[colors['social'], '#17becf'],
        labels={"value": get_translation("Primary and Tertiary Education GPI", language), "variable": ""}
    )

    if language == 'arabic':
        gender_parity_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation for gender parity (GPI = 1.0 line)
    gender_parity_fig.add_hline(y=1.0, line_dash="dash", line_color="#888888",
                              annotation_text=get_translation("Gender Parity (GPI = 1.0)", language), 
                              annotation_position="bottom right")
    
    # Add annotation for Qatar's gender equity in education
    gender_parity_fig.add_annotation(
        x=gpi_df['Year'].median(),
        y=gpi_df['Primary Education GPI'].max(),
        text=get_translation("Qatar 2019: GPI >1.0 indicates slight<br>advantage for female students<br>Women: 51.6% of engineering students", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to gender parity chart
    gender_parity_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    gender_parity_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create STEM & ICT graduates chart with shortened labels
    grad_df = filtered_df.copy()
    grad_df['STEM Graduates (%)'] = grad_df['Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, (%)']
    grad_df['ICT Graduates (%)'] = grad_df['Percentage of graduates from tertiary education graduating from Information and Communication Technologies programmes, (%)']

    stem_ict_fig = px.line(
        grad_df,
        x='Year',
        y=['STEM Graduates (%)', 'ICT Graduates (%)'],
        title=get_translation('STEM & ICT Graduates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['social'], '#17becf'],
        labels={"value": get_translation("STEM and ICT Graduates (%)", language), "variable": ""}
    )

    if language == 'arabic':
        stem_ict_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add benchmark lines for STEM graduates
    stem_ict_fig.add_hline(y=benchmarks["stem_graduates"]["global_avg"], line_dash="dash", line_color=colors['global'],
                         annotation_text=get_translation(f"Global Average STEM: {benchmarks['stem_graduates']['global_avg']}%", language), 
                         annotation_position="top right")
    
    stem_ict_fig.add_hline(y=benchmarks["stem_graduates"]["regional"]["Saudi Arabia"], line_dash="dot", line_color=colors['regional'],
                         annotation_text=get_translation(f"Saudi Arabia: {benchmarks['stem_graduates']['regional']['Saudi Arabia']}%", language), 
                         annotation_position="bottom right")
    
    for leader, value in benchmarks["stem_graduates"]["leading"].items():
        stem_ict_fig.add_hline(y=value, line_dash="dot", line_color=colors['leading'],
                             annotation_text=get_translation(f"{leader}: {value}%", language), 
                             annotation_position="top right")
    
    # Apply modern styling to STEM chart
    stem_ict_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(family="Poppins, sans-serif", size=12)
        )
    )
    stem_ict_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Create Programming Skills chart
    programming_fig = px.line(
        filtered_df,
        x='Year',
        y='Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)',
        title=get_translation('Programming Skills (%)', language),
        markers=True,
        color_discrete_sequence=[colors['social']],
        labels={"Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)": get_translation("Proportion of youth and adults who wrote a computer program", language), "variable": ""}
    )
    
    # Translate trace names for Arabic
    if language == 'arabic':
        programming_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
        ))
    
    # Add annotation for digital skills context
    programming_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)'].max(),
        text=get_translation("Qatar's divergent digital skills:<br>Improving basic skills (email: 58.72%)<br>Declining advanced skills (programming: 5.06%)", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=12, family="Poppins, sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        
    )
    
    # Apply modern styling to programming chart
    programming_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        title=dict(font=dict(size=18, family="Poppins, sans-serif")),
        xaxis=dict(
            title=get_translation("Year", language),
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        ),
        yaxis=dict(
            gridcolor='rgba(220, 220, 220, 0.2)',
            tickfont=dict(family="Poppins, sans-serif")
        )
    )
    programming_fig.update_traces(line=dict(width=3), marker=dict(size=8), connectgaps=True)
    
    # Extract latest values for KPI cards
    try:
        # Find years with non-null values for each metric
        sanitation_years = filtered_df.dropna(subset=['Share of the population using safely managed sanitation services']).sort_values('Year')
        if not sanitation_years.empty:
            latest_sanitation_year = sanitation_years['Year'].max()
            latest_sanitation = sanitation_years[sanitation_years['Year'] == latest_sanitation_year]['Share of the population using safely managed sanitation services'].iloc[0]
            sanitation_value = f"{latest_sanitation:.1f}%"
            sanitation_global_compare = f"{latest_sanitation / benchmarks['sanitation']['global_avg']:.1f}x global average"
        else:
            sanitation_value = get_translation("N/A", language)
            sanitation_global_compare = ""
            
        stem_years = grad_df.dropna(subset=['STEM Graduates (%)']).sort_values('Year')
        if not stem_years.empty:
            latest_stem_year = stem_years['Year'].max()
            latest_stem = stem_years[stem_years['Year'] == latest_stem_year]['STEM Graduates (%)'].iloc[0]
            stem_value = f"{latest_stem:.1f}%"
            if latest_stem < benchmarks["stem_graduates"]["global_avg"]:
                stem_global_compare = f"{latest_stem / benchmarks['stem_graduates']['global_avg']:.1f}x global average (below avg)"
            else:
                stem_global_compare = f"{latest_stem / benchmarks['stem_graduates']['global_avg']:.1f}x global average"
        else:
            stem_value = get_translation("N/A", language)
            stem_global_compare = ""
            
        gpi_years = gpi_df.dropna(subset=['Primary Education GPI']).sort_values('Year')
        if not gpi_years.empty:
            latest_gpi_year = gpi_years['Year'].max()
            latest_gpi = gpi_years[gpi_years['Year'] == latest_gpi_year]['Primary Education GPI'].iloc[0]
            gpi_value = f"{latest_gpi:.2f}"
            if latest_gpi > 1:
                gpi_global_compare = "Favors female students"
            elif latest_gpi < 1:
                gpi_global_compare = "Favors male students"
            else:
                gpi_global_compare = "Perfect gender parity"
        else:
            gpi_value = get_translation("N/A", language)
            gpi_global_compare = ""
            
        prog_years = filtered_df.dropna(subset=['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)']).sort_values('Year')
        if not prog_years.empty:
            latest_prog_year = prog_years['Year'].max()
            latest_prog = prog_years[prog_years['Year'] == latest_prog_year]['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)'].iloc[0]
            prog_value = f"{latest_prog:.1f}%"
            prog_global_compare = "8.25% decline from 2016"
        else:
            prog_value = get_translation("N/A", language)
            prog_global_compare = ""
    except:
        sanitation_value = get_translation("N/A", language)
        sanitation_global_compare = ""
        stem_value = get_translation("N/A", language)
        stem_global_compare = ""
        gpi_value = get_translation("N/A", language)
        gpi_global_compare = ""
        prog_value = get_translation("N/A", language)
        prog_global_compare = ""
    
    # Create KPI cards for social development section
    kpi_cards = dbc.Row([
        dbc.Col(
            create_kpi_card(
                title="Sanitation Access",
                value=sanitation_value,
                subtitle="of population",
                comparison=sanitation_global_compare,
                icon="fas fa-hands-wash",
                color=colors['social'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="STEM Graduates",
                value=stem_value,
                subtitle="of all graduates",
                comparison=stem_global_compare,
                icon="fas fa-microscope",
                color=colors['social'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Gender Parity Index",
                value=gpi_value,
                subtitle="Primary education",
                comparison=gpi_global_compare,
                icon="fas fa-venus-mars",
                color=colors['social'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
        dbc.Col(
            create_kpi_card(
                title="Programming Skills",
                value=prog_value,
                subtitle="of population",
                comparison=prog_global_compare,
                icon="fas fa-laptop-code",
                color=colors['social'],
                language=language
            ), 
            width=3, className="mb-4"
        ),
    ], className="mb-4 g-4")
    
    # Create benchmark comparison cards with translations
    sanitation_benchmark_card = create_benchmark_card("Sanitation Access Benchmarks", benchmarks["sanitation"], colors['social'], language)
    stem_benchmark_card = create_benchmark_card("STEM Graduates Benchmarks", benchmarks["stem_graduates"], colors['social'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader([
            html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0", style={"color": colors['text']})
        ], style={"borderLeft": f"4px solid {colors['highlight']}", "borderRadius": "8px 8px 0 0", 
                 "background": f"linear-gradient(to right, {colors['highlight']}15, {colors['gradient_start']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-3 d-flex align-items-center"),
        ])
    ], className="mb-4 shadow-sm hover-card", style={"borderRadius": "8px", "overflow": "hidden", "backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Social Development Insights", overall_social_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        
        dbc.Row([
            dbc.Col([
                html.H4(get_translation("Social Development Analysis", language), 
                       className="mt-4 mb-4 text-center section-title", 
                       style={"color": colors['text'], "fontWeight": "600"})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # Sanitation insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Sanitation Services", sanitation_insights, colors['social'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=sanitation_fig), className="chart-container shadow-sm mb-3"),
                sanitation_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Gender parity insights and charts
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=gender_parity_fig), className="chart-container shadow-sm"),
                width={"size": 7, "order": 1 if language == "english" else 12}, 
                className="mb-4"
            ),
            dbc.Col(create_insight_card("Gender Equality in Education", gender_equality_insights, colors['social'], language), 
                   width={"size": 5, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # STEM and ICT graduates insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("STEM Education", stem_insights, colors['social'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col([
                html.Div(dcc.Graph(figure=stem_ict_fig), className="chart-container shadow-sm mb-3"),
                stem_benchmark_card
            ], width={"size": 7, "order": 12 if language == "english" else 1}, className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # ICT graduates and digital skills
        dbc.Row([
            dbc.Col(create_insight_card("ICT Graduates", ict_graduates_insights, colors['social'], language), 
                   width={"size": 5, "order": 1 if language == "english" else 12}, 
                   className="mb-4"),
            dbc.Col(create_insight_card("Digital Skills", digital_skills_insights, colors['social'], language), 
                   width={"size": 7, "order": 12 if language == "english" else 1}, 
                   className="mb-4"),
        ], className="chart-row align-items-stretch"),
        
        # Programming skills chart
        dbc.Row([
            dbc.Col(
                html.Div(dcc.Graph(figure=programming_fig), className="chart-container shadow-sm"),
                width=12, 
                className="mb-4"
            ),
        ]),
        
        # Overall insights
        overall_insights_card,
    ], className="tab-content")
    
    return layout

# Add custom CSS for icons and better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Enhanced Dashboard Styles */
:root {
    --primary-font: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    --arabic-font: 'Amiri', 'Traditional Arabic', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --bg-color: #f8f9fa;
    --card-bg: #ffffff;
    --text-color: #2c3e50;
    --text-muted: #6c757d;
    --border-radius: 12px;
    --border-radius-sm: 8px;
    --transition-speed: 0.3s;
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.1);
    --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    --gradient-header: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
}

body {
    font-family: var(--primary-font);
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    transition: background-color var(--transition-speed);
}

.app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Enhanced Header */
.header-container {
    background: var(--gradient-header);
    border-bottom: 1px solid rgba(0,0,0,0.03);
    padding: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.header-row {
    position: relative;
}

.header-title {
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-size: 2.4rem;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.header-subtitle {
    color: var(--text-muted);
    font-weight: 400;
    font-size: 1.15rem;
}

.main-container {
    flex: 1;
    padding-top: 2rem;
}

/* Improved Language Buttons */
.language-btn {
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    font-weight: 500;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-speed);
    border: none;
}

.language-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* Year Slider Card */
.slider-card {
    background: #ffffff;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: none;
    transition: all var(--transition-speed);
    padding: 0.5rem;
}

.slider-card:hover {
    box-shadow: var(--shadow-md);
}

.modern-slider .rc-slider-rail {
    height: 8px;
    background-color: #e9ecef;
    border-radius: 4px;
}

.modern-slider .rc-slider-track {
    height: 8px;
    background-color: #6366f1;
    border-radius: 4px;
}

.modern-slider .rc-slider-handle {
    width: 20px;
    height: 20px;
    margin-top: -6px;
    background-color: #fff;
    border: 2px solid #6366f1;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.2);
}

.modern-slider .rc-slider-handle:hover,
.modern-slider .rc-slider-handle:active {
    border-color: #4f46e5;
    box-shadow: 0 2px 12px rgba(99, 102, 241, 0.3);
    transform: scale(1.1);
}

/* Enhanced Tabs */
.nav-tabs-modern {
    border-bottom: 1px solid rgba(0,0,0,0.06);
}

.nav-tabs-modern .custom-tab {
    transition: all var(--transition-speed);
    margin-right: 4px;
    border-radius: 8px 8px 0 0;
}

.nav-tabs-modern .nav-link {
    border: none;
    border-bottom: 3px solid transparent;
    color: var(--text-muted);
    font-weight: 500;
    transition: all var(--transition-speed);
    border-radius: 8px 8px 0 0;
    padding: 0.75rem 1.25rem;
}

.nav-tabs-modern .nav-link.active {
    background-color: transparent;
    color: var(--text-color);
    font-weight: 600;
}

.nav-tabs-modern .nav-link:hover:not(.active) {
    background-color: rgba(0,0,0,0.02);
    border-color: rgba(0,0,0,0.05);
    color: #495057;
}

/* KPI Cards */
.kpi-card {
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: none;
    transition: all var(--transition-speed);
    height: 100%;
    position: relative;
}

.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-md);
}

.kpi-card:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--gradient-primary);
    opacity: 0;
    transition: opacity var(--transition-speed);
}

.kpi-card:hover:before {
    opacity: 1;
}

.kpi-title {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 0.3rem;
    letter-spacing: -0.01em;
}

.kpi-subtitle {
    color: #95a5a6;
    font-size: 0.85rem;
}

.kpi-comparison {
    font-size: 0.85rem;
    font-weight: 500;
}

.icon-container {
    margin-bottom: 1.25rem;
}

.icon-container i {
    transition: transform 0.3s ease;
}

.kpi-card:hover .icon-container i {
    transform: scale(1.1);
}

/* Chart and Insight Cards */
.hover-card {
    transition: all var(--transition-speed);
    border: none;
    border-radius: var(--border-radius);
    overflow: hidden;
}

.hover-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.chart-container {
    background-color: #fff;
    border-radius: var(--border-radius);
    overflow: hidden;
    border: none;
    transition: all var(--transition-speed);
    box-shadow: var(--shadow-sm);
}

.chart-container:hover {
    box-shadow: var(--shadow-md);
}

.chart-row {
    margin-bottom: 2.5rem;
}

/* Enhanced Section Title */
.section-title {
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 2rem;
    position: relative;
    display: inline-block;
    font-size: 1.75rem;
    letter-spacing: -0.01em;
}

.section-title:after {
    content: '';
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: var(--gradient-primary);
    border-radius: 4px;
}

.card-title {
    font-weight: 600;
    font-size: 1.15rem;
    letter-spacing: -0.01em;
}

/* Beautiful Card Headers */
.card-header {
    background: linear-gradient(to right, rgba(99, 102, 241, 0.05), transparent);
    border-bottom: none;
    padding: 1.25rem;
}

/* Enhanced Footer */
.footer {
    background: linear-gradient(135deg, #2c3e50 0%, #1a2530 100%);
    color: #ecf0f1;
    margin-top: 3rem;
    padding: 1.5rem 0;
}

.footer-text {
    font-size: 0.9rem;
    color: rgba(236, 240, 241, 0.7);
}

.comparison-container {
    min-height: 2rem;
}

/* Animated Fade-In Effects */
.tab-content {
    opacity: 0;
    animation: fadeIn 0.5s forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Enhanced Chart Animations */
.chart-container {
    opacity: 0;
    animation: fadeInChart 0.8s forwards;
    animation-delay: 0.2s;
}

@keyframes fadeInChart {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Card Loading Animation */
.kpi-card, .hover-card {
    opacity: 0;
    animation: cardFadeIn 0.6s ease forwards;
}

@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Staggered Card Animations */
.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.kpi-card:nth-child(3) { animation-delay: 0.3s; }
.kpi-card:nth-child(4) { animation-delay: 0.4s; }

/* Enhanced Insights Cards */
.card-body {
    padding: 1.5rem;
}

.mb-3 {
    margin-bottom: 1rem !important;
}

/* Scroll Effects */
html {
    scroll-behavior: smooth;
}

/* RTL Support for Arabic */
[dir="rtl"] {
    font-family: var(--arabic-font);
}

[dir="rtl"] .header-title,
[dir="rtl"] .header-subtitle,
[dir="rtl"] .section-title,
[dir="rtl"] .card-title {
    font-family: var(--arabic-font);
}

[dir="rtl"] .fa-arrow-right:before {
    content: "\f060"; /* FontAwesome arrow left */
}

[dir="rtl"] .fa-arrow-left:before {
    content: "\f061"; /* FontAwesome arrow right */
}

/* Beautiful Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #6366f1, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #4f46e5, #7c3aed);
}

/* Responsive Refinements */
@media (max-width: 992px) {
    .header-title {
        font-size: 2rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
    }
    
    .section-title {
        font-size: 1.5rem;
    }
    
    .kpi-value {
        font-size: 1.6rem;
    }
}

@media (max-width: 768px) {
    .header-title {
        font-size: 1.8rem;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
    }
    
    .kpi-value {
        font-size: 1.5rem;
    }
    
    .card-title {
        font-size: 1rem;
    }
    
    .chart-row {
        margin-bottom: 1.5rem;
    }
}
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)