# Qatar Vision 2030 Dashboard

An interactive bilingual dashboard to visualize and analyze Qatar's progress toward Vision 2030 goals across economic, environmental, human, and social development pillars from 2016 to 2023.
![englishbase](https://github.com/user-attachments/assets/2c3f620b-3cff-442e-ae91-9b16ecdd4912)
![startarabic](https://github.com/user-attachments/assets/d29aac76-e828-4f33-a434-f38a50c8a553)


## Features

- **Comprehensive Development Tracking**: Monitors Qatar's progress across all four Vision 2030 pillars
- **Bilingual Support**: Full Arabic and English interfaces with dynamic translation
- **Interactive Data Visualization**: Dynamic charts with year range selection
- **Global Context**: Benchmarking against global averages, regional peers, and leading nations
- **Rich Analytical Insights**: Pre-analyzed data with sentiment classification
- **Responsive Design**: Optimized for both desktop and mobile viewing
- **Modern UI**: Clean interface with intuitive color-coding for different development pillars

## Technologies

- **Frontend Framework**: Dash (Python)
- **UI Components**: Dash Bootstrap Components
- **Data Manipulation**: Pandas
- **Data Visualization**: Plotly Express, Plotly Graph Objects
- **Styling**: Custom CSS, Bootstrap 5
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Poppins, Amiri)

## Project Structure

```
qatar-vision-dashboard/
├── app.py                           # Main application file
├── data/                            # Data directory
│   ├── economic_development.csv     # Economic pillar data
│   ├── environmental_development.csv # Environmental pillar data
│   ├── human_development.csv        # Human pillar data
│   ├── social_development.csv       # Social pillar data
│   └── qatar_vision_key_indicators.csv # Key indicators across pillars
├── assets/                          # Static assets
│   └── qatar_vision_2030_logo.png   # Dashboard logo
├── translations.py                  # English-Arabic translation dictionary
├── benchmarks.py                    # Global and regional benchmark data
├── insight_sentiments.py            # Sentiment classification for insights
├── key_insights.py                  # Key indicator insights
├── economic_insights.py             # Economic development insights
├── environmental_insights.py        # Environmental development insights
├── human_insights.py                # Human development insights
├── social_insights.py               # Social development insights
├── requirements.txt                 # Project dependencies
└── README.md                        # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/WalidBenzineb/qatar-vision-2030.git
cd qatar-vision-2030
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Dash application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

3. Use the language toggle in the upper right corner to switch between English and Arabic interfaces.
4. Adjust the year range slider to view data for specific periods.
5. Navigate between development pillars using the tabs.
## Deployment

For production deployment, the application can be served with Gunicorn:
```bash
gunicorn app:server -b 0.0.0.0:$PORT
```

## Implementation Details

### Dashboard Architecture

The dashboard follows a modular architecture with the following components:

- **Main Application (app.py)**: Initializes the Dash application, defines the layout, and implements all callback functions for interactivity.
- **Data Loading and Processing**: Reads CSV files containing development indicators and processes them for visualization.
- **Translation System**: Implements a dictionary-based translation system between English and Arabic, with automatic RTL/LTR support.
- **Visualization Components**:
  - Line charts for trend analysis
  - Bar charts for comparative analysis
  - Area charts for composition analysis
  - Key Performance Indicator (KPI) cards for headline metrics
  - Insight cards with sentiment analysis
- **Benchmarking System**: Compares Qatar's performance against global averages, regional peers, and leading nations to provide context.

### Key Technical Features
The application is built with a modern Dash setup including Bootstrap integration and custom web font loading:

```python
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
```
#### Dynamic Language Switching

The application uses a callback-based language switching mechanism:

```python
@app.callback(
    Output('language-store', 'data'),
    [Input('btn-english', 'n_clicks'),
     Input('btn-arabic', 'n_clicks')],
    [State('language-store', 'data')]
)
def update_language(en_clicks, ar_clicks, current_language):
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
```
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/107448bd-7787-463d-acf0-17c8446ccf45" alt="GDP per capita English">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/2915db7c-e236-4065-91a2-3106012aa2f3" alt="GDP per capita Arabic">
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/25141f49-29b2-4070-8c8e-9f2ee33c625d" alt="English renewables">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/faec400b-ff00-471b-9bc6-4c52c7707762" alt="Arabic renewables">
    </td>
  </tr>
</table>

### Component Factory System

The dashboard uses component factory functions to dynamically generate UI elements:

- KPI Card Factory
- Insight Card Factory with Sentiment Analysis
- Benchmark Card Factory
- Advanced Chart Generation System
```python
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
```
### Callback Architecture

The dashboard implements a multi-level callback system:

- Language-State Callback
- Layout-Update Callback
- Tab-Content Callback
- Tab-Specific Rendering Functions

Example:

```python
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
```

#### Responsive Chart Creation

Dynamic chart creation with automatic styling and benchmark integration:

```python
def create_chart(dataframe, x_col, y_col, title, color, benchmarks=None, language='english'):
    fig = px.line(
        dataframe, 
        x=x_col, 
        y=y_col,
        title=get_translation(title, language),
        markers=True,
        color_discrete_sequence=[color],
        labels={y_col: get_translation(y_col, language), "variable": ""}
    )
    
    # Add benchmarks if provided
    if benchmarks and 'global_avg' in benchmarks:
        fig.add_hline(y=benchmarks['global_avg'], line_dash="dash", line_color=colors['global'],
                     annotation_text=get_translation(f"Global Average: {benchmarks['global_avg']}", language), 
                     annotation_position="bottom right")
    
    # Apply modern styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif", color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    
    return fig
```
![dynamic](https://github.com/user-attachments/assets/2aeda402-dbd4-4eaf-b774-627dca33919c)

#### Insight Card System with Sentiment Analysis

The dashboard includes pre-analyzed insights with sentiment classification (positive, negative, neutral):

```python
def create_insight_card(title, insights, pillar_color, language='english'):
    insight_elements = []
    for insight in insights:
        if insight in insight_sentiments:
            sentiment = insight_sentiments[insight]['sentiment']
        else:
            sentiment = 'neutral'
            
        # Choose icon based on sentiment
        if sentiment == 'positive':
            icon_class = "fas fa-arrow-up me-2"
            icon_color = colors['positive']
        elif sentiment == 'negative':
            icon_class = "fas fa-arrow-down me-2"
            icon_color = colors['negative']
        else:
            icon_class = "fas fa-minus me-2"
            icon_color = colors['neutral']
        
        # Translate the insight
        translated_insight = get_translation(insight, language)
        
        # Create insight element
        insight_elements.append(
            html.Div([
                html.I(className=icon_class, style={"color": icon_color}),
                html.Span(translated_insight)
            ], className="mb-3 d-flex align-items-center")
        )
    
    # Create card with translated title
    translated_title = get_translation(title, language)
    
    return dbc.Card([...])
```
![sentiments](https://github.com/user-attachments/assets/460df018-f11c-449a-aed0-025528b93ee9)

### Data Sources

The dashboard uses data compiled from several sources:

- World Bank Open Data
- UN Human Development Index Reports
- Qatar Planning and Statistics Authority
- International Energy Agency (IEA) Data
- UNESCO Institute for Statistics
- Our World in Data

Data is preprocessed and stored in CSV format in the `data/` directory.

### Performance Optimizations

- **Data Pre-processing**: Data is pre-processed and stored in optimized CSV files to reduce loading times.
- **Modular Callbacks**: The application uses modular callbacks to update only the necessary components when user interactions occur.
- **Efficient Styling**: CSS styles are consolidated and optimized for faster rendering.
- **Caching**: Frequently accessed data and translations are cached to improve performance.
- **Lazy Loading**: Charts are rendered only when their respective tab is active.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions about this project, please contact benzinebwal@gmail.com
