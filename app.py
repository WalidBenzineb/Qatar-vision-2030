import os
import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

# Initialize Dash app with a more modern bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],suppress_callback_exceptions=True) 
app.title = "Qatar Vision 2030 Dashboard"
server = app.server

# Read the CSV files
economic_df = pd.read_csv('data/economic_development.csv')
environmental_df = pd.read_csv('data/environmental_development.csv')
human_df = pd.read_csv('data/human_development.csv')
social_df = pd.read_csv('data/social_development.csv')
key_indicators_df = pd.read_csv('data/qatar_vision_key_indicators.csv')

# Define colors for different pillars with a more cohesive color palette
colors = {
    'economic': '#3498db',    # Brighter blue
    'environmental': '#2ecc71', # Vibrant green
    'human': '#f39c12',       # Warmer orange
    'social': '#e74c3c',      # More vivid red
    'key': '#9b59b6',         # Rich purple
    'bg': '#f8f9fa',          # Light background color
    'card': '#ffffff',        # White for cards
    'text': '#2c3e50',        # Dark blue-gray for text
    'highlight': '#18bc9c',   # Teal highlight color
    'global': '#34495e',      # Dark blue for global comparisons
    'regional': '#7f8c8d',    # Grey for regional comparisons
    'leading': '#8e44ad',     # Purple for leading country comparisons
    'positive': '#2ecc71',    # Green for positive insights
    'negative': '#e74c3c',    # Red for negative insights
    'neutral': '#3498db'      # Blue for neutral insights
}

# Translation dictionary for English to Arabic
translations = {
    # App title and header
    'Qatar Vision 2030 Dashboard': 'لوحة معلومات رؤية قطر 2030',
    'Monitoring Progress Across Economic, Environmental, Human, and Social Development Pillars': 'مراقبة التقدم عبر ركائز التنمية الاقتصادية والبيئية والبشرية والاجتماعية',
    'English': 'الإنجليزية',
    
    # Tab labels
    'Key Indicators': 'المؤشرات الرئيسية',
    'Economic Development': 'التنمية الاقتصادية',
    'Environmental Development': 'التنمية البيئية',
    'Human Development': 'التنمية البشرية',
    'Social Development': 'التنمية الاجتماعية',
    
    # Year slider
    'Select Year Range': 'حدد نطاق السنوات',
    
    # Button labels
    'English': 'English',
    'Arabic': 'العربية',
    
    # Chart titles and common terms
    'GDP per Capita (PPP)': 'الناتج المحلي الإجمالي للفرد (تعادل القوة الشرائية)',
    'GDP per Capita Trends': 'اتجاهات الناتج المحلي الإجمالي للفرد',
    'Human Capital Index': 'مؤشر رأس المال البشري',
    'CO₂ Emissions per Capita': 'انبعاثات ثاني أكسيد الكربون للفرد',
    'CO₂ Emissions': 'انبعاثات ثاني أكسيد الكربون',
    'Annual CO₂ Emissions (tonnes)': 'انبعاثات ثاني أكسيد الكربون السنوية (طن)',
    'Annual CO₂ Emissions per Capita': 'انبعاثات ثاني أكسيد الكربون السنوية للفرد',
    'Electricity from Renewables (TWh)': 'الكهرباء من مصادر الطاقة المتجددة (تيراواط ساعة)',
    'Energy Production: Oil & Gas (TWh)': 'إنتاج الطاقة: النفط والغاز (تيراواط ساعة)',
    'Energy Production (TWh)': 'إنتاج الطاقة (تيراواط ساعة)',
    'Energy Consumption (TWh)': 'استهلاك الطاقة (تيراواط ساعة)',
    'Annual Change in Primary Energy Consumption (%)': 'التغير السنوي في استهلاك الطاقة الأولية (%)',
    'Energy Growth Rates (%)': 'معدلات نمو الطاقة (%)',
    'Education Metrics': 'مقاييس التعليم',
    'STEM Graduates (%)': 'خريجو العلوم والتكنولوجيا والهندسة والرياضيات (%)',
    'School Life Expectancy and Learning Years': 'العمر المتوقع للدراسة وسنوات التعلم',
    'Education Completion Rates (%)': 'معدلات إتمام التعليم (%)',
    'Education Levels (%)': 'مستويات التعليم (%)',
    'Population Education Levels (%)': 'مستويات تعليم السكان (%)',
    'Advanced Education Levels (%)': 'مستويات التعليم المتقدم (%)',
    'Electricity Production by Source (TWh)': 'إنتاج الكهرباء حسب المصدر (تيراواط ساعة)',
    'Renewable Electricity Production Detail (TWh)': 'تفاصيل إنتاج الكهرباء المتجددة (تيراواط ساعة)',
    'Solar Capacity and Growth': 'قدرة الطاقة الشمسية ونموها',
    'STEM & ICT Graduates (%)': 'خريجو العلوم والتكنولوجيا والهندسة والرياضيات وتكنولوجيا المعلومات والاتصالات (%)',
    'Population with Safely Managed Sanitation Services (%)': 'السكان الذين يحصلون على خدمات الصرف الصحي المدارة بأمان (%)',
    'Gender Parity Indices in Education': 'مؤشرات التكافؤ بين الجنسين في التعليم',
    'Agriculture, Forestry, and Fishing Value Added per Worker': 'القيمة المضافة للزراعة والغابات وصيد الأسماك لكل عامل',
    'Business, Administration and Law Graduates (%)': 'خريجو الأعمال والإدارة والقانون (%)',
    'Programming Skills (%)': 'مهارات البرمجة (%)',
    'Programming Skills': 'مهارات البرمجة',
    'of population': 'من السكان',
    'Annual CO₂ emissions':'الانبعاثات السنوية لثاني أكسيد الكربون',
    'Annual CO₂ emissions from oil':'الانبعاثات السنوية لثاني أكسيد الكربون من النفط',
    'Annual change in primary energy consumption (%)':'التغير السنوي في استهلاك الطاقة الأولية (%)',
    'Annual CO₂ emissions (per capita)':'الانبعاثات السنوية لثاني أكسيد الكربون (لكل فرد)',
    'Annual CO₂ emissions from oil (per capita)':'الانبعاثات السنوية لثاني أكسيد الكربون من النفط (لكل فرد',
    'School enrollment, tertiary (% gross)':'الالتحاق بالتعليم العالي (% إجمالي)',
    'variable':'متغير',
    'years': 'سنوات',
    'tonnes':"طن",
    
    # KPI card labels
    'GDP per Capita': 'الناتج المحلي الإجمالي للفرد',
    'Oil Production': 'إنتاج النفط',
    'Gas Production': 'إنتاج الغاز',
    'Energy Consumption': 'استهلاك الطاقة',
    'CO₂ per Capita': 'ثاني أكسيد الكربون للفرد',
    'Renewable Electricity': 'الكهرباء المتجددة',
    'Solar Capacity': 'قدرة الطاقة الشمسية',
    "Bachelor's Degree or Higher": 'درجة البكالوريوس أو أعلى',
    'Expected Years of School': 'سنوات الدراسة المتوقعة',
    'Learning-Adjusted Years': 'سنوات التعلم المعدلة',
    'Sanitation Access': 'الوصول إلى الصرف الصحي',
    'Gender Parity Index': 'مؤشر التكافؤ بين الجنسين',
    
    # Legend and Benchmark terms
    'Benchmark Comparison Legend': 'مفتاح مقارنة المعايير',
    'Global Average': 'المتوسط العالمي',
    'Regional Comparison': 'المقارنة الإقليمية',
    'Leading Country': 'الدولة الرائدة',
    'GDP per Capita (PPP) Benchmarks': 'معايير الناتج المحلي الإجمالي للفرد (تعادل القوة الشرائية)',
    'Human Capital Index Benchmarks': 'معايير مؤشر رأس المال البشري',
    'CO₂ Emissions per Capita Benchmarks': 'معايير انبعاثات ثاني أكسيد الكربون للفرد',
    'Renewables Share Benchmarks': 'معايير حصة الطاقة المتجددة',
    'Energy Production Targets': 'أهداف إنتاج الطاقة',
    'STEM Graduates Benchmarks': 'معايير خريجي العلوم والتكنولوجيا والهندسة والرياضيات',
    'Sanitation Access Benchmarks': 'معايير الوصول إلى الصرف الصحي',
    'Agricultural Productivity': 'الإنتاجية الزراعية',
    'Tertiary Education': 'التعليم العالي',
    "Hydrocarbon resources": "الموارد الهيدروكربونية",
    "Capital-intensive": "كثيف رأس المال",
    "Climate-adapted": "المتكيفة مع المناخ",
    "Arable land": "الأراضي الصالحة للزراعة",
    "Tertiary enrollment": "الالتحاق بالتعليم العالي",

    
    # Analysis titles
    'Key Indicators Analysis': 'تحليل المؤشرات الرئيسية',
    'Economic Development Analysis': 'تحليل التنمية الاقتصادية',
    'Environmental Development Analysis': 'تحليل التنمية البيئية',
    'Human Development Analysis': 'تحليل التنمية البشرية',
    'Social Development Analysis': 'تحليل التنمية الاجتماعية',
    
    # Insight card titles
    'Overall Dashboard Insights': 'رؤى لوحة المعلومات العامة',
    'GDP per Capita': 'الناتج المحلي الإجمالي للفرد',
    'GDP per capita': 'الناتج المحلي الإجمالي للفرد',
    'Human Capital Index': 'مؤشر رأس المال البشري',
    'CO₂ Emissions': 'انبعاثات ثاني أكسيد الكربون',
    'Renewable Energy': 'الطاقة المتجددة',
    'Energy Production': 'إنتاج الطاقة',
    'Education Metrics': 'مقاييس التعليم',
    'STEM Graduates': 'خريجو العلوم والتكنولوجيا والهندسة والرياضيات',
    'Overall Economic Development Insights': 'رؤى التنمية الاقتصادية العامة',
    'GDP per Capita Trends': 'اتجاهات الناتج المحلي الإجمالي للفرد',
    'Energy Consumption': 'استهلاك الطاقة',
    'Energy Growth Rates': 'معدلات نمو الطاقة',
    'Agricultural Productivity': 'الإنتاجية الزراعية',
    'Business, Administration and Law Graduates': 'خريجو الأعمال والإدارة والقانون',
    'Overall Environmental Development Insights': 'رؤى التنمية البيئية العامة',
    'Energy Consumption Change': 'تغير استهلاك الطاقة',
    'Agricultural Development': 'التنمية الزراعية',
    'Electricity Production': 'إنتاج الكهرباء',
    'Solar Energy Development': 'تطوير الطاقة الشمسية',
    'Renewable Energy Detail': 'تفاصيل الطاقة المتجددة',
    'Overall Human Development Insights': 'رؤى التنمية البشرية العامة',
    'Educational Attainment': 'التحصيل التعليمي',
    'Advanced Education': 'التعليم المتقدم',
    'Education Quality': 'جودة التعليم',
    'Completion Rates': 'معدلات الإتمام',
    'Human Capital Development': 'تنمية رأس المال البشري',
    'Gender Equity in Education': 'المساواة بين الجنسين في التعليم',
    'Overall Social Development Insights': 'رؤى التنمية الاجتماعية العامة',
    'Sanitation Services': 'خدمات الصرف الصحي',
    'Gender Equality in Education': 'المساواة بين الجنسين في التعليم',
    'STEM Education': 'تعليم العلوم والتكنولوجيا والهندسة والرياضيات',
    'ICT Graduates': 'خريجو تكنولوجيا المعلومات والاتصالات',
    'Digital Skills': 'المهارات الرقمية',
    'Gas Production': 'إنتاج الغاز',
    
    # Common UI elements
    'Latest value': 'أحدث قيمة',
    'Scale: 0-1': 'المقياس: 0-1',
    'of adult population': 'من السكان البالغين',
    'of all graduates': 'من جميع الخريجين',
    'Primary education': 'التعليم الابتدائي',
    'of population': 'من السكان',
    'This tab has no content.': 'لا توجد محتويات في هذه التبويبة.',
    'N/A': 'غير متوفر',
    'Data unavailable': 'البيانات غير متوفرة',
    
    # Common chart labels
    'Year': 'السنة',
    'Capacity (GW)': 'القدرة (جيجاواط)',
    'Growth (%)': 'النمو (%)',
    'Electricity Production (TWh)': 'إنتاج الكهرباء (TWh)',
    'variable':'متغير',
    
    # Specific benchmark texts
    'Global Average: $22,450': 'المتوسط العالمي: $22,450',
    'Global average: 22450':'المتوسط العالمي: 22450',
    'Global Average:':'المتوسط العالمي:',
    'UAE: 83900': 'الإمارات العربية المتحدة: $83900',
    'UAE: 83900': 'الإمارات العربية المتحدة: $83900',
    'Saudi Arabia: 54992': 'المملكة العربية السعودية: $54992',
    'Global Average: 0.56': 'المتوسط العالمي: 0.56',
    'Global average: 0.56': 'المتوسط العالمي: 0.56',
     'Japan: 0.8':'اليابان: 0.8',
    'Saudi Arabia: 0.58': 'المملكة العربية السعودية: 0.58',
    'Middle East Avg: 0.55': 'متوسط الشرق الأوسط: 0.55',
    'Singapore: 0.88': 'سنغافورة: 0.88',
    'Japan: 0.80': 'اليابان: 0.80',
    'Global Average: 4.8 tonnes': 'المتوسط العالمي: 4.8 طن',
    'Global average: 40':'المتوسط العالمي: 40',
    'Global average: 4.8': 'المتوسط العالمي: 4.8 طن',
    'Kuwait: 25': 'الكويت: 25 طن',
    'UAE: 20': 'الإمارات العربية المتحدة: 20 طن',
    'Saudi Arabia: 18': 'المملكة العربية السعودية: 18 طن',
    'Kuwait: 25 tonnes':'الكويت: 25 طن',
    'UAE: 20 tonnes':'الإمارات: 20 طن',
    'Saudi Arabia: 18 tonnes':'المملكة العربية السعودية: 18 طن',
    'EU Average: 6.5': 'متوسط الاتحاد الأوروبي: 6.5 طن',
    'Global average: 29': 'المتوسط العالمي: 29',
    'Middle East Avg: 4': 'متوسط الشرق الأوسط: 4',
    'Brazil: 85': 'البرازيل: 85',
    'Norway: 90': 'النرويج: 90',
    'Global average: 23': 'المتوسط العالمي: 23',
    'Saudi Arabia: 32': 'المملكة العربية السعودية: 32',
    'Oman: 43': 'عمان: 43',
    'Germany: 37': 'ألمانيا: 37',
    'Global average: 75': 'المتوسط العالمي: 75',
    'GCC Avg: 98': 'متوسط دول مجلس التعاون الخليجي: 98',
    'North America/Europe: 99': 'أمريكا الشمالية/أوروبا: 99',
    'Global Avg Expected: 12 years': 'متوسط العالمي المتوقع: 12 سنة',
    'Global Avg Learning-Adjusted: 7.8 years': 'متوسط العالمي المعدل للتعلم: 7.8 سنة',
    'Leading Countries Expected: 15 years': 'الدول الرائدة متوقع: 15 سنة',
    'Leading Countries Learning-Adjusted: 11 years': 'الدول الرائدة المعدل للتعلم: 11 سنة',
    'Luxembourg: 140000':'لوكسمبورغ: 140000',
    'Singapore: 140000':'سنغافورة: 140000',
    'GDP per capita, PPP (constant 2021 international $)':'الناتج المحلي الإجمالي للفرد، حسب تعادل القوة الشرائية (ثابت بالدولار الدولي لعام 2021)',
    'Oil production (TWh)':'إنتاج النفط (TWh)',
    'Gas production - TWh':'إنتاج الغاز - TWh',
    'Primary energy consumption - TWh':'استهلاك الطاقة الأولية - TWh',
    'Oil consumption - TWh':'استهلاك النفط - TWh',
    'UAE: $83,900':'الإمارات: $83,900',
    'Saudi Arabia: $54,992':'المملكة العربية السعودية: $54,992',
    'North America/Europe: 99%':'أمريكا الشمالية/أوروبا: 99%',
    'GCC Avg: 98%':'متوسط دول مجلس التعاون الخليجي: 98%',
    'Oman: 43%':'عُمان: 43%',
    'Germany: 37%':'ألمانيا: 37%',
    'Saudi Arabia: 32%':'المملكة العربية السعودية: 32%',
    'Global Average STEM: 23%':'المتوسط العالمي STEM: 23%',
    'Qatar 2023: ~128M tonnes CO₂<br>Global total: 36.8B tonnes<br>Saudi Arabia: ~600M tonnes<br>UAE: ~230M tonnes':'قطر 2023: ~128 مليون طن CO₂<br>المجموع العالمي: 36.8 مليار طن<br>المملكة العربية السعودية: ~600 مليون طن<br>الإمارات: ~230 مليون طن',
    'Human Capital Index (HCI) (scale 0-1)':'مؤشر رأس المال البشري (HCI) (المقياس من 0 إلى 1)',
    "Solar, Bioenergy (TWh)":"الطاقة الشمسية، والطاقة الحيوية (TWh)",
    "Primary and Lower secondary completion rate total":"معدل إتمام المرحلة الابتدائية والثانوية الدنيا الإجمالي",
    "Primary and Tertiary Education GPI":"مؤشر المساواة بين الجنسين في التعليم الابتدائي والتعليم العالي",
    "12.8 years":"12.8 سنة",
    "8.8 years":"8.8 سنة",
    # Comparative phrases
    'global average': 'المتوسط العالمي',
    'Small share of global total': 'حصة صغيرة من المجموع العالمي',
    '0.3% of electricity mix': '0.3% من مزيج الكهرباء',
    'Target: 4GW by 2030': 'الهدف: 4 جيجاواط بحلول عام 2030',
    '0.67M barrels/day (modest for GCC)': '0.67 مليون برميل/يوم (متواضع لدول مجلس التعاون الخليجي)',
    '177 billion m³ (globally significant)': '177 مليار متر مكعب (مهم عالمياً)',
    'Among GCC\'s highest per capita': 'من بين أعلى المعدلات للفرد في دول مجلس التعاون الخليجي',
    'Favors female students': 'لصالح الطالبات',
    'Favors male students': 'لصالح الطلاب',
    'Perfect gender parity': 'تكافؤ تام بين الجنسين',
    '8.25% decline from 2016': 'انخفاض بنسبة 8.25% من عام 2016',
    'Above global average, below leading countries': 'أعلى من المتوسط العالمي، أقل من الدول الرائدة',
    'below avg': 'أقل من المتوسط',
    
    # Chart annotations
    'Global energy demand growth: ~1-2% per year': 'نمو الطلب العالمي على الطاقة: ~1-2% سنوياً',
    'Qatar targets: 2-3% growth by 2030': 'أهداف قطر: نمو 2-3% بحلول عام 2030',
    'Past Qatar growth: ~6-7% annually': 'نمو قطر السابق: ~6-7% سنوياً',
    'Qatar\'s per-worker ag value: $10-11K': 'قيمة العمالة الزراعية في قطر: $10-11 ألف',
    'Regional peer (Oman): ~$6K': 'النظير الإقليمي (عمان): ~$6 آلاف',
    'Advanced economies: >$50K': 'الاقتصادات المتقدمة: >$50 ألف',
    'Qatar 2018: ~26% business/law graduates': 'قطر 2018: ~26% خريجي الأعمال/القانون',
    'Qatar 2018: ~26% business/law graduates<br>Regional comparison (Bahrain): ~50%<br>Vision 2030 aims to balance with STEM fields':'قطر 2018: ~26% من خريجي الأعمال/القانون<br>المقارنة الإقليمية (البحرين): ~50%<br>تهدف رؤية 2030 إلى تحقيق التوازن مع مجالات STEM',
    'Regional comparison (Bahrain): ~50%': 'المقارنة الإقليمية (البحرين): ~50%',
    'Vision 2030 aims to balance with STEM fields': 'تهدف رؤية 2030 إلى التوازن مع مجالات العلوم والتكنولوجيا والهندسة والرياضيات',
    'Qatar 2023: ~128M tonnes CO₂': 'قطر 2023: ~128 مليون طن من ثاني أكسيد الكربون',
    'Global total: 36.8B tonnes': 'المجموع العالمي: 36.8 مليار طن',
    'Saudi Arabia: ~600M tonnes': 'المملكة العربية السعودية: ~600 مليون طن',
    'UAE: ~230M tonnes': 'الإمارات العربية المتحدة: ~230 مليون طن',
    'Qatar 2023: >99% fossil fuels': 'قطر 2023: >99% وقود أحفوري',
    "Qatar 2023: >99% fossil fuels<br>Global mix: 61% non-renewables<br>Qatar's 2030 target: 20% renewables":"قطر 2023: >99% من الوقود الأحفوري<br>المزيج العالمي: 61% من المصادر غير المتجددة<br>هدف قطر لعام 2030: 20% من الطاقة المتجددة",
    'Global mix: 61% non-renewables': 'المزيج العالمي: 61% غير متجددة',
    'Qatar\'s 2030 target: 20% renewables': 'هدف قطر لعام 2030: 20% طاقة متجددة',
    'Qatar renewable output: ~0.15 TWh': 'إنتاج قطر من الطاقة المتجددة: ~0.15 تيراواط ساعة',
    'Global renewables: 7,858 TWh (2021)': 'الطاقة المتجددة العالمية: 7,858 تيراواط ساعة (2021)',
    'Middle East renewables: 47 TWh (2022)': 'الطاقة المتجددة في الشرق الأوسط: 47 تيراواط ساعة (2022)',
    'Qatar 2023: 0.8 GW': 'قطر 2023: 0.8 جيجاواط',
    'Qatar target 2030: 4 GW': 'هدف قطر 2030: 4 جيجاواط',
    '15,686% growth from 2016-2023': 'نمو بنسبة 15,686% من 2016-2023',
    "Qatar 2023: 0.8 GW<br>Qatar target 2030: 4 GW<br>15,686% growth from 2016-2023":"قطر 2023: 0.8 GW<br>هدف قطر 2030: 4 GW<br>نمو بنسبة 15,686% من 2016-2023",
    'Qatar tertiary attainment: ~30%': 'التحصيل العالي في قطر: ~30%',
    'High-income countries: 30-45%': 'الدول ذات الدخل المرتفع: 30-45%',
    'Leading countries (Canada/Korea): >55%': 'الدول الرائدة (كندا/كوريا): >55%',
    "Qatar tertiary attainment: ~30%<br>High-income countries: 30-45%<br>Leading countries (Canada/Korea): >55%":"تحصيل التعليم العالي في قطر: ~30%<br>الدول ذات الدخل المرتفع: 30-45%<br>الدول الرائدة (كندا/كوريا): >55%",
    'OECD tertiary attainment: ~39%': 'التحصيل العالي في منظمة التعاون الاقتصادي والتنمية: ~39%',
    'OECD tertiary attainment: ~39%<br>Qatar aims to lead Arab world<br>in higher education outcomes':'تحصيل التعليم العالي في منظمة التعاون الاقتصادي والتنمية: ~39%<br>تهدف قطر إلى قيادة العالم العربي<br>في نتائج التعليم العالي',
    'Qatar aims to lead Arab world': 'تهدف قطر إلى قيادة العالم العربي',
    'in higher education outcomes': 'في نتائج التعليم العالي',
    'Qatar primary: ~98-99%': 'التعليم الابتدائي في قطر: ~98-99%',
    'Global average: ~89%': 'المتوسط العالمي: ~89%',
    'Global secondary: ~75%': 'التعليم الثانوي العالمي: ~75%',
    '5.2x global average':'5.2 ضعف المتوسط العالمي',
    '1.1x global average':'1.1 ضعف المتوسط العالمي',
    '8.1x global average':'8.1 ضعف المتوسط العالمي',
    '0.8x global average (below avg)':'0.8x المتوسط العالمي (أقل من المتوسط)',
    "Qatar primary: ~98-99%<br>Global average: ~89%<br>Global secondary: ~75%":"قطر الابتدائي: ~98-99%<br>المتوسط العالمي: ~89%<br>الثانوي العالمي: ~75%",
    'Qatar plans to boost LNG output': 'تخطط قطر لزيادة إنتاج الغاز الطبيعي المسال',
    'by 85% by 2030 (126-142M tons)': 'بنسبة 85% بحلول عام 2030 (126-142 مليون طن)',
    'Qatar has one of GCC\'s highest': 'قطر لديها واحدة من أعلى معدلات',
    'per-capita energy consumption rates': 'استهلاك الطاقة للفرد في دول مجلس التعاون الخليجي',
    'Global energy demand growth: ~1.9% (2022)': 'نمو الطلب العالمي على الطاقة: ~1.9% (2022)',
    'Global energy demand growth: ~1-2% per year<br>Qatar targets: 2-3% growth by 2030<br>Past Qatar growth: ~6-7% annually':'النمو العالمي في الطلب على الطاقة: ~1-2% سنويًا<br>تستهدف قطر: نمو بنسبة 2-3% بحلول عام 2030<br>النمو السابق في قطر: ~6-7% سنويًا',
    'Qatar\'s historical growth: ~5-6% in 2010s': 'النمو التاريخي لقطر: ~5-6% في 2010s',
    'Qatar\'s 2030 target: <3% annually': 'هدف قطر لعام 2030: <3% سنوياً',
    'Qatar 2019: GPI >1.0 indicates slight': 'قطر 2019: مؤشر التكافؤ بين الجنسين >1.0 يشير إلى تفوق طفيف',
    'Qatar 2019: GPI >1.0 indicates slight<br>advantage for female students<br>Women: 51.6% of engineering students':'قطر 2019: GPI >1.0 يشير إلى ميزة طفيفة للطالبات<br>النساء: 51.6% من طلاب الهندسة',
    'advantage for female students': 'للطالبات',
    'Women: 51.6% of engineering students': 'النساء: 51.6% من طلاب الهندسة',
    'Qatar targets 20% of electricity from renewables by 2030': 'تستهدف قطر 20% من الكهرباء من مصادر الطاقة المتجددة بحلول عام 2030',
    'Global average: 29%': 'المتوسط العالمي: 29%',
    'Middle East: 4%': 'الشرق الأوسط: 4%',
    'Qatar plans 85% LNG': 'تخطط قطر لزيادة 85% في الغاز الطبيعي المسال',
    'expansion by 2030': 'بحلول عام 2030',
    'Qatar\'s divergent digital skills:': 'مهارات قطر الرقمية المتباينة:',
    'Improving basic skills (email: 58.72%)': 'تحسين المهارات الأساسية (البريد الإلكتروني: 58.72%)',
    'Declining advanced skills (programming: 5.06%)': 'تراجع المهارات المتقدمة (البرمجة: 5.06%)',
    'Gender Parity (GPI = 1.0)': 'التكافؤ بين الجنسين (مؤشر التكافؤ = 1.0)',
    "Qatar's divergent digital skills:<br>Improving basic skills (email: 58.72%)<br>Declining advanced skills (programming: 5.06%)": "مهارات قطر الرقمية المتباينة:<br>تحسين المهارات الأساسية (البريد الإلكتروني: 58.72%)<br>تراجع المهارات المتقدمة (البرمجة: 5.06%)",
    'Qatar has one of GCC\'s highest<br>per-capita energy consumption rates': 'تمتلك قطر واحدة من أعلى معدلات استهلاك الطاقة للفرد في دول مجلس التعاون الخليجي',
    'Primary completion rate, total (% of relevant age group)':'معدل إتمام المرحلة الابتدائية، الإجمالي (% من الفئة العمرية ذات الصلة)',
    'Lower secondary completion rate, total (% of relevant age group)':'معدل إتمام المرحلة الثانوية الدنيا، الإجمالي (% من الفئة العمرية ذات الصلة)',
    'School life expectancy, primary to tertiary, both sexes (years)':'متوسط سنوات التعليم، من الابتدائية إلى التعليم العالي، لكلا الجنسين (بالسنوات)',
    'Learning-Adjusted Years of School':'سنوات التعليم المعدلة وفقًا للتعلم',
    'Qatar targets 20% of electricity from renewables by 2030<br>Global average: 29%<br>Middle East: 4%':'تستهدف قطر الحصول على 20% من الكهرباء من المصادر المتجددة بحلول عام 2030<br>المتوسط العالمي: 29%<br>الشرق الأوسط: 4%',
    'Qatar plans 85% LNG<br>expansion by 2030':'تخطط قطر لتوسيع الغاز الطبيعي المسال بنسبة 85%<br>بحلول عام 2030',
    'Qatar plans to boost LNG output<br>by 85% by 2030 (126-142M tons)':'تخطط قطر لزيادة إنتاج الغاز الطبيعي المسال<br>بنسبة 85% بحلول عام 2030 (126-142 مليون طن)',
    "Qatar's per-worker ag value: $10-11K<br>Regional peer (Oman): ~$6K<br>Advanced economies: >$50K":"القيمة الزراعية لكل عامل في قطر: $10000-11000<br>ند إقليمي (عُمان): ~$6000<br>الاقتصادات المتقدمة: >$50000",
    "Global energy demand growth: ~1.9% (2022)<br>Qatar's historical growth: ~5-6% in 2010s<br>Qatar's 2030 target: <3% annually":"النمو العالمي في الطلب على الطاقة: ~1.9% (2022)<br>النمو التاريخي في قطر: ~5-6% في عقد 2010<br>هدف قطر لعام 2030: أقل من 3% سنويًا",
    "Electricity from renewables - TWh":"الكهرباء من مصادر الطاقة المتجددة - TWh",
    "Oil production (TWh), Gas production - TWh":"إنتاج النفط (TWh)، إنتاج الغاز - TWh",
    "Expected Years of School, Learning-Adjusted and enrollment":"سنوات الدراسة المتوقعة، المعدلة وفقًا للتعلم، والالتحاق",
    "Percentage of graduates from STEM programmes in tertiary":"نسبة الخريجين من برامج STEM في التعليم العالي",
    "GDP per capita, PPP (2021 international $)":"الناتج المحلي الإجمالي للفرد، حسب تعادل القوة الشرائية (2021 الدولار الدولي)",
    "Oil production and Gas production - TWh":"إنتاج النفط وإنتاج الغاز - TWh",
    "Primary energy consumption, Oil consumption and Gas consumption - TWh":"استهلاك الطاقة الأولية، استهلاك النفط واستهلاك الغاز - TWh",
    "Agriculture, forestry, and fishing, value per worker 2015 US$":"الزراعة، والحراجة، والصيد، القيمة لكل عامل (بالدولار الأمريكي لعام 2015)",
    "Annual CO₂ emissions and CO₂ emissions from oil per capita":"الانبعاثات السنوية لثاني أكسيد الكربون والانبعاثات السنوية لثاني أكسيد الكربون من النفط لكل فرد",
    "Annual change in primary energy consumption (%)":"التغير السنوي في استهلاك الطاقة الأولية (%)",
    "Primary Education, Secondary Education and Bachelor Degree (%)":"التعليم الابتدائي، التعليم الثانوي ودرجة البكالوريوس (%)",
    "Master Degree and Doctoral Degree (%)":"درجة الماجستير والدكتوراه (%)",
    "'School life expectancy, primary to tertiary and Learning-Adjusted":"متوسط سنوات التعليم من المرحلة الابتدائية إلى التعليم العالي والتعلم المعدل",
    "Share of the population using safely managed sanitation services":"نسبة السكان الذين يستخدمون خدمات الصرف الصحي المُدارة بأمان",
    "Proportion of youth and adults who wrote a computer program":"النسبة المئوية للشباب والبالغين الذين كتبوا برنامجاً حاسوبياً",
    
    # Key indicator card text
    'Economic Resilience': 'المرونة الاقتصادية',
    'Environmental Challenges': 'التحديات البيئية',
    'Human Development Progress': 'تقدم التنمية البشرية',
    'Infrastructural Achievements': 'الإنجازات في البنية التحتية',
    "Oil, Gas and Coal (% growth)":"النفط، الغاز والفحم (% نمو)",
    # Oil and Gas production units
    'Primary Energy': 'الطاقة الأولية',
    'Oil Consumption': 'استهلاك النفط',
    'Gas Consumption': 'استهلاك الغاز',
    'Gas consumption - TWh': 'TWh استهلاك الغاز',
    'Coal Consumption': 'استهلاك الفحم',
    'Energy Consumption (TWh)': 'استهلاك الطاقة (تيراواط ساعة)',
    'Coal Consumption (TWh)': 'استهلاك الفحم (تيراواط ساعة)',
    'Oil (% growth)': 'النفط (% نمو)',
    'Gas (% growth)': 'الغاز (% نمو)',
    'Coal (% growth)': 'الفحم (% نمو)',
    "Annual CO₂ emissions and Annual CO₂ emissions from oil":"الانبعاثات السنوية لثاني أكسيد الكربون والانبعاثات السنوية لثاني أكسيد الكربون من النفط",
    "STEM and ICT Graduates (%)":"الخريجين في مجالات STEM وتكنولوجيا المعلومات والاتصالات (%)",
    
    # Education chart labels
    'Primary Education (%)': 'التعليم الابتدائي (%)',
    'Secondary Education (%)': 'التعليم الثانوي (%)',
    'Bachelor Degree (%)': 'درجة البكالوريوس (%)',
    'Master Degree (%)': 'درجة الماجستير (%)',
    'Doctoral Degree (%)': 'درجة الدكتوراه (%)',
    'Primary Education GPI': 'مؤشر التكافؤ بين الجنسين في التعليم الابتدائي',
    'Tertiary Education GPI': 'مؤشر التكافؤ بين الجنسين في التعليم العالي',
    'STEM Graduates (%)': 'خريجو العلوم والتكنولوجيا والهندسة والرياضيات (%)',
    'ICT Graduates (%)': 'خريجو تكنولوجيا المعلومات والاتصالات (%)',
    'Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)': 'نسبة الشباب والبالغين الذين كتبوا برنامجًا حاسوبيًا باستخدام لغة برمجة متخصصة، (%)',
    
    # Renewable energy chart labels
    'Fossil Fuels (TWh)': 'الوقود الأحفوري (تيراواط ساعة)',
    'Nuclear (TWh)': 'الطاقة النووية (تيراواط ساعة)',
    'Renewables (TWh)': 'الطاقة المتجددة (تيراواط ساعة)',
    'Solar (TWh)': 'الطاقة الشمسية (تيراواط ساعة)',
    'Bioenergy (TWh)': 'الطاقة الحيوية (تيراواط ساعة)',
    'Solar Capacity (GW)': 'قدرة الطاقة الشمسية (جيجاواط)',
    'Solar Growth (%)': 'نمو الطاقة الشمسية (%)',
    
    # No data available message
    'No data available for sanitation services': 'لا توجد بيانات متاحة لخدمات الصرف الصحي',
    
    # Key insights - Key Indicators
    "Qatar maintained one of the world's highest GDP per capita levels throughout the period (over $100,000), but experienced a slight overall decline of 3.24% from 2016 to 2023.": "حافظت قطر على واحدة من أعلى مستويات الناتج المحلي الإجمالي للفرد في العالم طوال الفترة (أكثر من 100,000 دولار)، لكنها شهدت انخفاضًا إجماليًا طفيفًا بنسبة 3.24% من 2016 إلى 2023.",
    "A significant drop occurred in 2020 (down to $103,061), representing a 14.2% decrease from 2016 levels, clearly showing the pandemic's impact.": "حدث انخفاض كبير في عام 2020 (وصل إلى 103,061 دولارًا)، مما يمثل انخفاضًا بنسبة 14.2% من مستويات عام 2016، مما يوضح بوضوح تأثير الجائحة.",
    "The economy rebounded strongly in 2021 to $116,832, nearly returning to pre-pandemic levels, demonstrating economic resilience.": "انتعش الاقتصاد بقوة في عام 2021 ليصل إلى 116,832 دولارًا، عائدًا تقريبًا إلى مستويات ما قبل الجائحة، مما يدل على المرونة الاقتصادية.",
    "Qatar's GDP per capita is approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992).": "يبلغ الناتج المحلي الإجمالي للفرد في قطر حوالي 5.4 أضعاف المتوسط العالمي (22,450 دولارًا) وأعلى بكثير من الدول المجاورة (الإمارات: 83,900 دولار، المملكة العربية السعودية: 54,992 دولارًا).",
    
    "The HCI data is only available for 2017, 2018, and 2020, which limits comprehensive trend analysis.": "بيانات مؤشر رأس المال البشري متوفرة فقط للأعوام 2017 و2018 و2020، مما يحد من تحليل الاتجاهات الشامل.",
    "There was a steady improvement in HCI from 0.615 in 2017 to 0.638 in 2020, representing a 3.7% increase.": "كان هناك تحسن مستمر في مؤشر رأس المال البشري من 0.615 في عام 2017 إلى 0.638 في عام 2020، بزيادة قدرها 3.7%.",
    "A score of 0.638 means that a child born in Qatar today will be 63.8% as productive as they could be with complete education and full health.": "تعني درجة 0.638 أن الطفل المولود في قطر اليوم سيكون إنتاجه بنسبة 63.8% مما يمكن أن يكون عليه مع التعليم الكامل والصحة الكاملة.",
    "Qatar's HCI (0.64) is above the global average (0.56) and Middle East average, but remains below leading countries like Singapore (0.88) and Japan (0.80).": "مؤشر رأس المال البشري في قطر (0.64) أعلى من المتوسط العالمي (0.56) ومتوسط الشرق الأوسط، لكنه لا يزال أقل من الدول الرائدة مثل سنغافورة (0.88) واليابان (0.80).",
    
    "CO₂ emissions per capita increased by 15.54% from 2016 to 2023, reaching 38.84 tonnes per person in 2023.": "ارتفعت انبعاثات ثاني أكسيد الكربون للفرد بنسبة 15.54% من 2016 إلى 2023، لتصل إلى 38.84 طن للشخص في عام 2023.",
    "Emissions showed significant year-to-year variability, suggesting changing energy usage patterns.": "أظهرت الانبعاثات تقلبات كبيرة من سنة لأخرى، مما يشير إلى تغير أنماط استخدام الطاقة.",
    "The upward trend contradicts Qatar's environmental sustainability goals and presents a major challenge for Vision 2030's environmental pillar.": "يتناقض الاتجاه التصاعدي مع أهداف الاستدامة البيئية في قطر ويمثل تحديًا كبيرًا لركيزة البيئة في رؤية 2030.",
    "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes).": "انبعاثات قطر للفرد (38.84 طن) تعادل تقريبًا 8 أضعاف المتوسط العالمي (4.8 طن) وأعلى من الدول الإقليمية المماثلة (الكويت: 25 طن، الإمارات: 20 طن، المملكة العربية السعودية: 18 طن).",
    
    "Renewable electricity production increased slightly from 0.13 TWh in 2016 to 0.15 TWh in 2023 (15.38% increase).": "ارتفع إنتاج الكهرباء المتجددة قليلاً من 0.13 تيراواط ساعة في عام 2016 إلى 0.15 تيراواط ساعة في عام 2023 (زيادة بنسبة 15.38%).",
    "After increasing to 0.15 TWh in 2018, renewable electricity production has plateaued without further growth through 2023.": "بعد زيادته إلى 0.15 تيراواط ساعة في عام 2018، استقر إنتاج الكهرباء المتجددة دون مزيد من النمو حتى عام 2023.",
    "Given Qatar's climate, there's significant untapped potential for solar energy expansion.": "نظرًا لمناخ قطر، هناك إمكانات كبيرة غير مستغلة لتوسيع الطاقة الشمسية.",
    "Qatar targets 20% of electricity from renewables by 2030, which would exceed the current Middle East average (4%) but remain below the global average (29%) and far behind leading countries like Brazil and Norway (80-95%).": "تستهدف قطر 20% من الكهرباء من مصادر الطاقة المتجددة بحلول عام 2030، وهو ما يتجاوز متوسط الشرق الأوسط الحالي (4%) ولكنه يظل أقل من المتوسط العالمي (29%) وبعيدًا عن الدول الرائدة مثل البرازيل والنرويج (80-95%).",
    
    "Qatar's energy production is dominated by natural gas, with a significant focus on LNG exports where Qatar is a global leader.": "يهيمن الغاز الطبيعي على إنتاج الطاقة في قطر، مع تركيز كبير على صادرات الغاز الطبيعي المسال حيث تعتبر قطر رائدة عالمية.",
    "Oil production experienced a decline from 582.57 TWh in 2016 to 511.54 TWh in 2020 (-12.2%), before rebounding to 616.21 TWh in 2023.": "شهد إنتاج النفط انخفاضًا من 582.57 تيراواط ساعة في عام 2016 إلى 511.54 تيراواط ساعة في عام 2020 (-12.2%)، قبل أن ينتعش إلى 616.21 تيراواط ساعة في عام 2023.",
    "Gas production has been more stable, reflecting Qatar's strategic emphasis on its vast North Field gas reserves.": "كان إنتاج الغاز أكثر استقرارًا، مما يعكس التركيز الاستراتيجي لقطر على احتياطيات حقل الشمال الضخمة من الغاز.",
    "Qatar plans to boost LNG output by 85% from current 77 million tons to 126-142 million tons by 2030, aiming to reclaim its position as the world's top LNG exporter.": "تخطط قطر لزيادة إنتاج الغاز الطبيعي المسال بنسبة 85% من 77 مليون طن حاليًا إلى 126-142 مليون طن بحلول عام 2030، وتهدف إلى استعادة مكانتها كأكبر مصدر للغاز الطبيعي المسال في العالم.",
    "This expansion will cement Qatar's position in global energy markets, targeting approximately 25% of global LNG trade by 2030.": "سيعزز هذا التوسع مكانة قطر في أسواق الطاقة العالمية، مستهدفًا حوالي 25% من تجارة الغاز الطبيعي المسال العالمية بحلول عام 2030.",
    
    "Qatar has shown steady improvement in expected years of schooling, increasing from 12.46 years in 2016 to 13.26 years in 2020 (6.4% growth).": "أظهرت قطر تحسنًا مطردًا في سنوات الدراسة المتوقعة، بزيادة من 12.46 سنة في عام 2016 إلى 13.26 سنة في عام 2020 (نمو بنسبة 6.4%).",
    "The Learning-Adjusted Years of School metric improved from 12.31 years in 2017 to 12.83 years in 2020, indicating enhanced education quality.": "تحسن مقياس سنوات الدراسة المعدلة للتعلم من 12.31 سنة في عام 2017 إلى 12.83 سنة في عام 2020، مما يشير إلى تحسن جودة التعليم.",
    "The gap between expected and learning-adjusted years decreased from 0.69 to 0.43 years, showing a reduction in learning loss from 5.31% to 3.24%.": "انخفضت الفجوة بين السنوات المتوقعة والسنوات المعدلة للتعلم من 0.69 إلى 0.43 سنة، مما يظهر انخفاضًا في فقدان التعلم من 5.31% إلى 3.24%.",
    "Qatar's tertiary enrollment has grown substantially, from approximately 20% in the mid-2010s to over 40% recently, approaching the global average.": "نما الالتحاق بالتعليم العالي في قطر بشكل كبير، من حوالي 20% في منتصف 2010s إلى أكثر من 40% مؤخرًا، مقتربًا من المتوسط العالمي.",
    "Qatar's education metrics now exceed global averages (12 expected years globally vs. 13.26 in Qatar; 7.8 learning-adjusted years globally vs. 12.83 in Qatar).": "تتجاوز مقاييس التعليم في قطر الآن المتوسطات العالمية (12 سنة متوقعة عالميًا مقابل 13.26 في قطر؛ 7.8 سنة معدلة للتعلم عالميًا مقابل 12.83 في قطر).",
    
    "The percentage of graduates from STEM programs has declined dramatically from 29.70% in 2016 to 17.83% in 2022, representing a 39.96% decrease.": "انخفضت نسبة الخريجين من برامج العلوم والتكنولوجيا والهندسة والرياضيات بشكل كبير من 29.70% في عام 2016 إلى 17.83% في عام 2022، مما يمثل انخفاضًا بنسبة 39.96%.",
    "This consistent downward trend in STEM graduates contradicts Qatar's Vision 2030 goal of building a knowledge-based economy and innovation ecosystem.": "يتناقض هذا الاتجاه التنازلي المستمر في خريجي العلوم والتكنولوجيا والهندسة والرياضيات مع هدف رؤية قطر 2030 المتمثل في بناء اقتصاد قائم على المعرفة ونظام بيئي للابتكار.",
    "At 17.83%, Qatar's STEM graduate percentage has fallen below the global average (23%) and significantly trails regional competitor Saudi Arabia (32%).": "عند 17.83%، انخفضت نسبة خريجي العلوم والتكنولوجيا والهندسة والرياضيات في قطر إلى ما دون المتوسط العالمي (23%) وتتخلف بشكل كبير عن المنافس الإقليمي المملكة العربية السعودية (32%).",
    "Leading countries in STEM education, such as Oman (43%) and Germany (37%), far outpace Qatar's current performance in this critical metric.": "تتفوق الدول الرائدة في تعليم العلوم والتكنولوجيا والهندسة والرياضيات، مثل عمان (43%) وألمانيا (37%)، بشكل كبير على أداء قطر الحالي في هذا المقياس الحاسم.",
    "The decline in STEM graduates represents a major challenge for Qatar's economic diversification goals and may hinder the country's competitiveness in high-tech sectors.": "يمثل انخفاض خريجي العلوم والتكنولوجيا والهندسة والرياضيات تحديًا كبيرًا لأهداف التنويع الاقتصادي في قطر وقد يعيق قدرة البلاد التنافسية في القطاعات عالية التقنية.",
    
    "Economic Resilience: Despite fluctuations, Qatar maintains exceptionally high living standards (5.4x global average GDP per capita) while navigating energy transitions.": "المرونة الاقتصادية: رغم التقلبات، تحافظ قطر على مستويات معيشية مرتفعة بشكل استثنائي (5.4 أضعاف متوسط الناتج المحلي الإجمالي العالمي للفرد) أثناء التنقل في تحولات الطاقة.",
    "Environmental Challenges: Rising CO₂ emissions (8x global average) and limited renewable energy growth present the most significant challenges to Qatar Vision 2030 goals.": "التحديات البيئية: تمثل انبعاثات ثاني أكسيد الكربون المتزايدة (8 أضعاف المتوسط العالمي) والنمو المحدود للطاقة المتجددة التحديات الأكثر أهمية لأهداف رؤية قطر 2030.",
    "Human Development Progress: Education access is improving substantially, with Qatar's Human Capital Index (0.64) exceeding the global average (0.56), but quality metrics and STEM graduate percentages require attention.": "تقدم التنمية البشرية: يتحسن الوصول إلى التعليم بشكل كبير، حيث يتجاوز مؤشر رأس المال البشري في قطر (0.64) المتوسط العالمي (0.56)، لكن مقاييس الجودة ونسب خريجي العلوم والتكنولوجيا والهندسة والرياضيات تتطلب اهتمامًا.",
    "Infrastructural Achievements: Near-universal sanitation (1.3x global average) and dramatic solar capacity expansion demonstrate Qatar's ability to rapidly develop infrastructure.": "إنجازات البنية التحتية: تظهر الصرف الصحي شبه الشامل (1.3 ضعف المتوسط العالمي) والتوسع الدراماتيكي في قدرة الطاقة الشمسية قدرة قطر على تطوير البنية التحتية بسرعة.",
    
    # Key insights - Economic Development
    "Qatar's GDP per capita has shown notable volatility between 2016-2023, with a 3.24% overall decline.": "أظهر الناتج المحلي الإجمالي للفرد في قطر تقلبات ملحوظة بين عامي 2016-2023، مع انخفاض إجمالي بنسبة 3.24%.",
    "The most significant drop occurred in 2020 (to $103,062), representing a 14% decline from 2016 levels.": "حدث أكبر انخفاض في عام 2020 (إلى 103,062 دولار)، بما يمثل انخفاضًا بنسبة 14% من مستويات عام 2016.",
    "The economy showed strong resilience with a rapid recovery to $116,833 in 2021.": "أظهر الاقتصاد مرونة قوية مع تعافٍ سريع إلى 116,833 دولار في عام 2021.",
    "The stabilization around $115,000 in recent years suggests a 'new normal' that balances energy market realities with economic diversification efforts.": "يشير الاستقرار حول 115,000 دولار في السنوات الأخيرة إلى 'وضع طبيعي جديد' يوازن بين واقع سوق الطاقة وجهود التنويع الاقتصادي.",
    "Qatar's GDP per capita remains approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992).": "لا يزال الناتج المحلي الإجمالي للفرد في قطر يمثل حوالي 5.4 ضعف المتوسط العالمي (22,450 دولار) وأعلى بكثير من الدول المجاورة (الإمارات: 83,900 دولار، المملكة العربية السعودية: 54,992 دولار).",
    
    "Oil production declined from 582.57 TWh in 2016 to a low of 511.54 TWh in 2020 (-12.2%), but has since recovered to 616.21 TWh in 2023.": "انخفض إنتاج النفط من 582.57 تيراواط ساعة في عام 2016 إلى 511.54 تيراواط ساعة في عام 2020 (-12.2%)، ولكنه تعافى منذ ذلك الحين ليصل إلى 616.21 تيراواط ساعة في عام 2023.",
    "The initial reduction reflects Qatar's strategic decision to focus more on natural gas, where it holds comparative advantage.": "يعكس الانخفاض الأولي القرار الاستراتيجي لقطر للتركيز أكثر على الغاز الطبيعي، حيث تتمتع بميزة نسبية.",
    "The 20.5% increase from 2020 to 2023 shows Qatar's response to higher global energy demand and prices after the pandemic.": "تُظهر الزيادة البالغة 20.5% من 2020 إلى 2023 استجابة قطر لارتفاع الطلب العالمي على الطاقة والأسعار بعد الجائحة.",
    "The upward trend in recent years raises questions about alignment with climate commitments and sustainability goals.": "يثير الاتجاه التصاعدي في السنوات الأخيرة تساؤلات حول التوافق مع الالتزامات المناخية وأهداف الاستدامة.",
    "Qatar's oil output (~0.67 million barrels/day) is modest compared to other GCC producers, reflecting its strategic focus on natural gas production.": "يعتبر إنتاج قطر من النفط (~0.67 مليون برميل/يوم) متواضعًا مقارنة بمنتجي دول مجلس التعاون الخليجي الآخرين، مما يعكس تركيزها الاستراتيجي على إنتاج الغاز الطبيعي.",
    
    "Qatar has been investing heavily in liquefied natural gas (LNG) infrastructure, aiming to increase production capacity from 77 to 126 million tons annually by 2027.": "استثمرت قطر بكثافة في البنية التحتية للغاز الطبيعي المسال، بهدف زيادة الطاقة الإنتاجية من 77 إلى 126 مليون طن سنويًا بحلول عام 2027.",
    "The focus on gas aligns with Qatar's positioning of natural gas as a 'transition fuel' with lower carbon emissions than oil or coal.": "يتماشى التركيز على الغاز مع موقع قطر للغاز الطبيعي كـ 'وقود انتقالي' بانبعاثات كربونية أقل من النفط أو الفحم.",
    "Sustained gas production provides Qatar with economic stability as global demand for cleaner burning fuels increases.": "يوفر إنتاج الغاز المستدام لقطر استقرارًا اقتصاديًا مع زيادة الطلب العالمي على الوقود الأنظف احتراقًا.",
    "The vast majority of Qatar's gas production is destined for export markets, making it a critical component of the country's revenue stream.": "الغالبية العظمى من إنتاج الغاز في قطر مخصصة لأسواق التصدير، مما يجعلها عنصرًا حاسمًا في تدفق إيرادات البلاد.",
    "Qatar aims to maintain its position as one of the world's largest LNG exporters, competing with the U.S. which surpassed Qatar as the top LNG exporter in 2023.": "تهدف قطر إلى الحفاظ على مكانتها كواحدة من أكبر مصدري الغاز الطبيعي المسال في العالم، متنافسة مع الولايات المتحدة التي تجاوزت قطر كأكبر مصدر للغاز الطبيعي المسال في عام 2023.",
    
    "Energy consumption fluctuated significantly, from 168.92 TWh in 2016 to a low of 126.88 TWh in 2020 (-24.9%), before rebounding to 170.21 TWh in 2023.": "تقلب استهلاك الطاقة بشكل كبير، من 168.92 تيراواط ساعة في عام 2016 إلى أدنى مستوى له عند 126.88 تيراواط ساعة في عام 2020 (-24.9%)، قبل أن ينتعش إلى 170.21 تيراواط ساعة في عام 2023.",
    "The consumption pattern closely mirrors GDP trends, with the 2020 pandemic-related drop and subsequent recovery.": "يعكس نمط الاستهلاك بشكل وثيق اتجاهات الناتج المحلي الإجمالي، مع الانخفاض المرتبط بالجائحة في عام 2020 والتعافي اللاحق.",
    "The data suggests limited progress in improving energy efficiency, as consumption has grown in line with economic recovery.": "تشير البيانات إلى تقدم محدود في تحسين كفاءة الطاقة، حيث نما الاستهلاك بما يتماشى مع التعافي الاقتصادي.",
    "Qatar has one of the world's highest per capita energy consumption rates, reflecting its energy-intensive industries and high standard of living.": "تمتلك قطر واحدة من أعلى معدلات استهلاك الطاقة للفرد في العالم، مما يعكس صناعاتها كثيفة الاستهلاك للطاقة ومستوى المعيشة المرتفع.",
    "Global energy demand typically grows at 1-2% annually, while Qatar experienced 6-7% annual growth in the 2010s, though it targets moderating to 2-3% by the late 2020s.": "ينمو الطلب العالمي على الطاقة عادة بنسبة 1-2% سنويًا، بينما شهدت قطر نموًا سنويًا بنسبة 6-7% في العقد 2010، على الرغم من أنها تستهدف التخفيف إلى 2-3% بحلول أواخر عشرينيات القرن الحالي.",
    
    "Qatar's energy growth rates show significant volatility, reflecting both global energy market fluctuations and domestic economic changes.": "تُظهر معدلات نمو الطاقة في قطر تقلبات كبيرة، مما يعكس تقلبات سوق الطاقة العالمية والتغيرات الاقتصادية المحلية.",
    "Growth rates were particularly negative during the 2020 pandemic period, with sharp contractions across all energy sources.": "كانت معدلات النمو سلبية بشكل خاص خلال فترة جائحة عام 2020، مع انكماشات حادة عبر جميع مصادر الطاقة.",
    "Post-pandemic recovery shows positive growth rates, particularly in oil consumption, which may contradict Vision 2030's sustainability goals.": "يُظهر التعافي بعد الجائحة معدلات نمو إيجابية، خاصة في استهلاك النفط، مما قد يتناقض مع أهداف الاستدامة في رؤية 2030.",
    "Qatar's historical energy demand growth of 6-7% annually significantly exceeds the global average (1-2%), highlighting the challenge of energy-intensive development.": "يتجاوز النمو التاريخي للطلب على الطاقة في قطر البالغ 6-7% سنويًا المتوسط العالمي (1-2%) بشكل كبير، مما يسلط الضوء على تحدي التنمية كثيفة الاستهلاك للطاقة.",
    "Vision 2030 and the National Environment and Climate Strategy aim to reduce these high growth rates to a more sustainable 2-3% annually by 2030, still higher than typical OECD countries that have achieved near-zero growth through efficiency measures.": "تهدف رؤية 2030 والاستراتيجية الوطنية للبيئة والمناخ إلى خفض معدلات النمو المرتفعة هذه إلى 2-3% سنويًا بشكل أكثر استدامة بحلول عام 2030، وهي لا تزال أعلى من دول منظمة التعاون الاقتصادي والتنمية النموذجية التي حققت نموًا شبه صفري من خلال تدابير الكفاءة.",
    
    "Despite Qatar's challenging desert environment, agricultural productivity per worker is relatively high at $10,000-$11,000 (2015 US$) in value-added terms.": "على الرغم من بيئة الصحراء الصعبة في قطر، فإن الإنتاجية الزراعية لكل عامل مرتفعة نسبيًا عند 10,000-11,000 دولار (بالدولار الأمريكي لعام 2015) من حيث القيمة المضافة.",
    "Qatar's agricultural productivity exceeds regional peers like Oman (~$6,000) but remains well below advanced economies (>$50,000 per worker).": "تتجاوز الإنتاجية الزراعية في قطر نظرائها الإقليميين مثل عمان (~6,000 دولار) ولكنها تظل أقل بكثير من الاقتصادات المتقدمة (>50,000 دولار لكل عامل).",
    "The high per-worker value reflects Qatar's capital-intensive agricultural approach, utilizing advanced technologies like hydroponics and climate-controlled greenhouses.": "تعكس القيمة المرتفعة لكل عامل النهج الزراعي كثيف رأس المال في قطر، واستخدام تقنيات متقدمة مثل الزراعة المائية والبيوت المحمية المتحكم في مناخها.",
    "Following the 2017 blockade, Qatar has heavily invested in agricultural self-sufficiency, with arable land increasing by 14.75% (18,300 to 21,000 hectares).": "بعد حصار عام 2017، استثمرت قطر بكثافة في الاكتفاء الذاتي الزراعي، مع زيادة الأراضي الصالحة للزراعة بنسبة 14.75% (من 18,300 إلى 21,000 هكتار).",
    "By 2030, Qatar aims to further improve agricultural efficiency through high-yield technology to enhance food security, even as the sector remains <1% of GDP.": "بحلول عام 2030، تهدف قطر إلى تحسين الكفاءة الزراعية من خلال تكنولوجيا عالية الإنتاجية لتعزيز الأمن الغذائي، حتى مع بقاء القطاع <1% من الناتج المحلي الإجمالي.",
    
    "Business, administration, and law have historically been popular fields of study in Qatar, with approximately 26% of tertiary graduates specializing in these areas in 2018.": "كانت الأعمال والإدارة والقانون تاريخيًا من المجالات الدراسية الشائعة في قطر، حيث تخصص حوالي 26% من خريجي التعليم العالي في هذه المجالات في عام 2018.",
    "This proportion is lower than in some other service-driven Gulf economies, such as Bahrain, where nearly 50% of graduates focus on business and law.": "هذه النسبة أقل منها في بعض اقتصادات الخليج الأخرى التي تعتمد على الخدمات، مثل البحرين، حيث يركز ما يقرب من 50% من الخريجين على الأعمال والقانون.",
    "Vision 2030 doesn't discourage these fields but seeks a better balance with STEM subjects to support innovation and knowledge economy development.": "لا تثبط رؤية 2030 هذه المجالات ولكنها تسعى إلى توازن أفضل مع مواد العلوم والتكنولوجيا والهندسة والرياضيات لدعم الابتكار وتطوير اقتصاد المعرفة.",
    "The inverse relationship between business/law and STEM graduates represents a challenge for Qatar's diversification - as one increases, the other tends to decrease.": "تمثل العلاقة العكسية بين خريجي الأعمال/القانون وخريجي العلوم والتكنولوجيا والهندسة والرياضيات تحديًا لتنويع قطر - فكلما زاد أحدهما، يميل الآخر إلى الانخفاض.",
    "Qatar aims to keep business/law graduates around or below one-third of total graduates while boosting STEM and technical fields to better align with labor market needs in a diversifying economy.": "تهدف قطر إلى الحفاظ على خريجي الأعمال/القانون حول أو أقل من ثلث إجمالي الخريجين مع تعزيز مجالات العلوم والتكنولوجيا والهندسة والرياضيات والمجالات التقنية لتتماشى بشكل أفضل مع احتياجات سوق العمل في اقتصاد متنوع.",
    
    "The data confirms Qatar's continued heavy reliance on oil and gas, despite diversification efforts under Vision 2030.": "تؤكد البيانات استمرار الاعتماد الكبير لقطر على النفط والغاز، على الرغم من جهود التنويع في إطار رؤية 2030.",
    "Qatar has demonstrated economic resilience, quickly recovering from the 2020 pandemic-induced downturn.": "أظهرت قطر مرونة اقتصادية، متعافية بسرعة من الانكماش الناجم عن جائحة عام 2020.",
    "While educational reforms show progress, the economic structure remains heavily tilted toward energy production.": "في حين تظهر الإصلاحات التعليمية تقدمًا، يظل الهيكل الاقتصادي مائلًا بشدة نحو إنتاج الطاقة.",
    "Qatar is pursuing a careful balance between maximizing short-term revenue from its hydrocarbon resources while investing in long-term diversification.": "تسعى قطر إلى تحقيق توازن دقيق بين تعظيم الإيرادات قصيرة المدى من مواردها الهيدروكربونية مع الاستثمار في التنويع طويل المدى.",
    "There remains an inherent tension between Qatar's role as a major hydrocarbon producer and its sustainability ambitions under Vision 2030.": "لا يزال هناك توتر متأصل بين دور قطر كمنتج رئيسي للهيدروكربونات وطموحاتها في الاستدامة بموجب رؤية 2030.",
    "Qatar's GDP per capita (5.4x global average) and per-worker agricultural value (higher than regional peers) demonstrate its economic efficiency.": "يُظهر الناتج المحلي الإجمالي للفرد في قطر (5.4 أضعاف المتوسط العالمي) والقيمة الزراعية لكل عامل (أعلى من النظراء الإقليميين) كفاءتها الاقتصادية.",
    
    'Oman: ~6K per worker':'عُمان: ~6000 لكل عامل',
    'Advanced economies: >50K per worker':'الاقتصادات المتقدمة: >50000 لكل عامل',
    # Key insights - Environmental Development
    "Total CO₂ emissions rose by 32.42% from 87.4 million tonnes in 2016 to 115.7 million tonnes in 2023, showing a concerning upward trajectory.": "ارتفعت انبعاثات ثاني أكسيد الكربون الإجمالية بنسبة 32.42% من 87.4 مليون طن في عام 2016 إلى 115.7 مليون طن في عام 2023، مما يظهر مسارًا تصاعديًا مثيرًا للقلق.",
    "CO₂ emissions per capita increased by 15.54% from 33.62 tonnes in 2016 to 38.84 tonnes in 2023, maintaining Qatar's position among the world's highest per capita emitters.": "ارتفعت انبعاثات ثاني أكسيد الكربون للفرد بنسبة 15.54% من 33.62 طنًا في عام 2016 إلى 38.84 طنًا في عام 2023، مما حافظ على مكانة قطر بين أعلى الدول المنبعثة للفرد في العالم.",
    "The data shows an accelerating emissions trend, with the most significant jump occurring between 2022 and 2023 (9% increase in just one year).": "تظهر البيانات اتجاهًا متسارعًا للانبعاثات، حيث حدثت أكبر قفزة بين عامي 2022 و2023 (زيادة بنسبة 9% في عام واحد فقط).",
    "The rising emissions directly conflict with Qatar's environmental sustainability goals under Vision 2030 and its international climate commitments.": "تتعارض الانبعاثات المتزايدة مباشرة مع أهداف الاستدامة البيئية في قطر بموجب رؤية 2030 والتزاماتها المناخية الدولية.",
    "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes).": "تبلغ انبعاثات قطر للفرد (38.84 طنًا) حوالي 8 أضعاف المتوسط العالمي (4.8 طن) وأعلى من نظرائها الإقليميين (الكويت: 25 طنًا، الإمارات: 20 طنًا، المملكة العربية السعودية: 18 طنًا).",
    
    "Fossil fuels generate over 99.7% of Qatar's electricity, with renewables contributing a minimal 0.28-0.31% throughout the period.": "يولد الوقود الأحفوري أكثر من 99.7% من كهرباء قطر، مع مساهمة الطاقة المتجددة بنسبة ضئيلة تبلغ 0.28-0.31% طوال الفترة.",
    "Total electricity production increased by 28.2% from 42.44 TWh in 2016 to 54.39 TWh in 2023, driving up absolute emissions.": "ارتفع إجمالي إنتاج الكهرباء بنسبة 28.2% من 42.44 تيراواط ساعة في عام 2016 إلى 54.39 تيراواط ساعة في عام 2023، مما أدى إلى زيادة الانبعاثات المطلقة.",
    "Despite global renewable energy trends, Qatar's renewable electricity generation has plateaued at around 0.15 TWh since 2018.": "على الرغم من اتجاهات الطاقة المتجددة العالمية، فقد استقر توليد الكهرباء المتجددة في قطر عند حوالي 0.15 تيراواط ساعة منذ عام 2018.",
    "The data reveals a significant gap between Qatar's sustainability rhetoric and actual energy transformation progress.": "تكشف البيانات عن فجوة كبيرة بين خطاب الاستدامة في قطر والتقدم الفعلي في تحول الطاقة.",
    "Global electricity mix shows 61% non-renewables vs 39% renewables, while Qatar targets 20% renewables by 2030, significantly above the Middle East average (4%) but below global average (29%).": "يُظهر مزيج الكهرباء العالمي 61% من الطاقة غير المتجددة مقابل 39% من الطاقة المتجددة، بينما تستهدف قطر 20% من الطاقة المتجددة بحلول عام 2030، وهو ما يفوق بشكل كبير متوسط الشرق الأوسط (4%) ولكنه أقل من المتوسط العالمي (29%).",
    
    "Solar capacity experienced a remarkable 15,686% increase from 0.0051 GW in 2016 to 0.8051 GW in 2023.": "شهدت قدرة الطاقة الشمسية زيادة ملحوظة بنسبة 15,686% من 0.0051 جيجاواط في عام 2016 إلى 0.8051 جيجاواط في عام 2023.",
    "Almost all capacity growth occurred in a single year (2022), indicating a major infrastructure commissioning.": "حدث ما يقرب من جميع نمو القدرة في عام واحد (2022)، مما يشير إلى تكليف بنية تحتية رئيسية.",
    "Despite the capacity increase, the solar electricity generation data doesn't yet show a corresponding production increase, suggesting the new capacity may be at early operational stages.": "على الرغم من زيادة القدرة، لا تظهر بيانات توليد الكهرباء بالطاقة الشمسية حتى الآن زيادة مقابلة في الإنتاج، مما يشير إلى أن القدرة الجديدة قد تكون في مراحل تشغيلية مبكرة.",
    "This dramatic solar expansion aligns with Qatar's National Development Strategy and preparations for hosting the 2022 FIFA World Cup.": "يتماشى هذا التوسع الكبير في الطاقة الشمسية مع استراتيجية التنمية الوطنية لقطر والاستعدادات لاستضافة كأس العالم FIFA 2022.",
    "Qatar's 2030 target of 4 GW solar capacity would place it among the regional leaders in renewable capacity per capita, though still modest by global standards.": "سيضع هدف قطر 2030 المتمثل في 4 جيجاواط من قدرة الطاقة الشمسية بين الرواد الإقليميين في قدرة الطاقة المتجددة للفرد، على الرغم من أنه لا يزال متواضعًا وفقًا للمعايير العالمية.",
    
    "Qatar's annual change in primary energy consumption shows significant volatility, with both substantial growth and contraction periods.": "يُظهر التغير السنوي في استهلاك الطاقة الأولية في قطر تقلبات كبيرة، مع فترات نمو وانكماش كبيرة.",
    "The 2020 pandemic year saw the most dramatic energy consumption contraction, reflecting global economic slowdown and reduced industrial activity.": "شهد عام الجائحة 2020 أكثر انكماش في استهلاك الطاقة دراماتيكية، مما يعكس التباطؤ الاقتصادي العالمي وانخفاض النشاط الصناعي.",
    "Post-pandemic recovery shows a return to positive growth rates in energy consumption, potentially challenging sustainability targets.": "يُظهر التعافي بعد الجائحة عودة إلى معدلات نمو إيجابية في استهلاك الطاقة، مما قد يتحدى أهداف الاستدامة.",
    "Qatar's typical annual energy consumption growth (5-6% in the 2010s) far exceeds the global average (1.9% in 2022), reflecting Qatar's rapid development and energy-intensive economy.": "يتجاوز النمو السنوي النموذجي لاستهلاك الطاقة في قطر (5-6% في العقد 2010) المتوسط العالمي بكثير (1.9% في عام 2022)، مما يعكس التطور السريع في قطر واقتصادها كثيف الاستهلاك للطاقة.",
    "Vision 2030 initiatives aim to moderate Qatar's energy consumption growth to below 3% annually by the late 2020s through efficiency improvements and renewable integration, though this would still exceed typical developed economy growth rates.": "تهدف مبادرات رؤية 2030 إلى تخفيف نمو استهلاك الطاقة في قطر إلى أقل من 3% سنويًا بحلول أواخر عشرينيات القرن الحالي من خلال تحسينات الكفاءة ودمج الطاقة المتجددة، على الرغم من أن هذا سيظل يتجاوز معدلات نمو الاقتصاد المتطور النموذجية.",
    
    "Qatar's renewable electricity generation is dominated by solar power, accounting for nearly all renewable output since 2018.": "يهيمن على توليد الكهرباء المتجددة في قطر الطاقة الشمسية، التي تمثل ما يقرب من كل الإنتاج المتجدد منذ عام 2018.",
    "Bioenergy makes a minimal contribution to Qatar's renewable mix, with very limited growth over the monitoring period.": "تساهم الطاقة الحيوية بشكل ضئيل في مزيج الطاقة المتجددة في قطر، مع نمو محدود للغاية خلال فترة المراقبة.",
    "Qatar's total renewable electricity production (0.15 TWh) is a fraction of the Middle East's already low renewable generation (47 TWh in 2022) and insignificant compared to global renewables (7,858 TWh in 2021).": "يمثل إجمالي إنتاج الكهرباء المتجددة في قطر (0.15 تيراواط ساعة) جزءًا صغيرًا من توليد الطاقة المتجددة المنخفض بالفعل في الشرق الأوسط (47 تيراواط ساعة في عام 2022) وغير مهم مقارنة بالطاقة المتجددة العالمية (7,858 تيراواط ساعة في عام 2021).",
    "The dramatic increase in solar capacity in 2022-2023 has not yet translated to substantial increases in electricity generation, suggesting early operational stages or potential utilization challenges.": "لم تترجم الزيادة الكبيرة في قدرة الطاقة الشمسية في 2022-2023 بعد إلى زيادات كبيرة في توليد الكهرباء، مما يشير إلى مراحل تشغيلية مبكرة أو تحديات محتملة في الاستخدام.",
    "Qatar's National Renewable Energy Strategy target of 4 GW solar capacity by 2030 would dramatically increase renewable electricity production, helping Qatar progress from its current 0.3% renewable share toward its 20% target.": "سيؤدي هدف استراتيجية الطاقة المتجددة الوطنية في قطر المتمثل في 4 جيجاواط من قدرة الطاقة الشمسية بحلول عام 2030 إلى زيادة إنتاج الكهرباء المتجددة بشكل كبير، مما يساعد قطر على التقدم من حصتها الحالية البالغة 0.3% من الطاقة المتجددة نحو هدفها البالغ 20%.",
    
    "Agricultural land increased from 71,000 hectares in 2016 to 74,000 hectares in 2021 (4.23% growth), reflecting Qatar's food security strategy.": "زادت الأراضي الزراعية من 71,000 هكتار في عام 2016 إلى 74,000 هكتار في عام 2021 (نمو بنسبة 4.23%)، مما يعكس استراتيجية الأمن الغذائي في قطر.",
    "Arable land saw more significant growth of 14.75% (18,300 to 21,000 hectares), indicating intensified cultivation efforts.": "شهدت الأراضي الصالحة للزراعة نموًا أكثر أهمية بنسبة 14.75% (من 18,300 إلى 21,000 هكتار)، مما يشير إلى تكثيف جهود الزراعة.",
    "These increases align with Qatar's post-2017 blockade strategy to enhance domestic food production and reduce import dependence.": "تتماشى هذه الزيادات مع استراتيجية قطر بعد حصار عام 2017 لتعزيز إنتاج الغذاء المحلي وتقليل الاعتماد على الواردات.",
    "The expansion of agriculture in Qatar's challenging desert environment demonstrates technological innovation in climate-adapted farming.": "يُظهر توسع الزراعة في بيئة الصحراء الصعبة في قطر الابتكار التكنولوجي في الزراعة المتكيفة مع المناخ.",
    "Qatar's agricultural productivity (~$10-11K per worker) exceeds regional peers like Oman (~$6K) but remains below advanced economies (>$50K per worker).": "تتجاوز الإنتاجية الزراعية في قطر (~10-11 ألف دولار لكل عامل) نظرائها الإقليميين مثل عمان (~6 آلاف دولار) ولكنها تظل أقل من الاقتصادات المتقدمة (>50 ألف دولار لكل عامل).",
    
    "The data reveals a significant disconnect between Qatar's Vision 2030 environmental sustainability goals and actual progress, particularly in emissions and energy transition.": "تكشف البيانات عن انفصال كبير بين أهداف الاستدامة البيئية في رؤية قطر 2030 والتقدم الفعلي، خاصة في الانبعاثات وتحول الطاقة.",
    "While showing impressive progress in solar capacity expansion and agricultural development, Qatar has made limited headway in overall emissions reduction and renewable energy integration.": "في حين أظهرت تقدمًا مثيرًا للإعجاب في توسيع قدرة الطاقة الشمسية والتنمية الزراعية، حققت قطر تقدمًا محدودًا في خفض الانبعاثات الكلية ودمج الطاقة المتجددة.",
    "With CO₂ emissions accelerating rather than decreasing, Qatar faces a critical decision point regarding its climate strategy credibility.": "مع تسارع انبعاثات ثاني أكسيد الكربون بدلاً من انخفاضها، تواجه قطر نقطة قرار حاسمة بشأن مصداقية استراتيجيتها المناخية.",
    "Despite significant investments in renewable capacity (particularly solar), the impact on the overall energy mix remains minimal.": "على الرغم من الاستثمارات الكبيرة في قدرة الطاقة المتجددة (وخاصة الطاقة الشمسية)، يظل التأثير على مزيج الطاقة الإجمالي ضئيلاً.",
    "The data highlights Qatar's complex sustainability challenge in balancing food security, water conservation, and energy transition in a desert environment.": "تسلط البيانات الضوء على تحدي الاستدامة المعقد في قطر في تحقيق التوازن بين الأمن الغذائي والحفاظ على المياه وتحول الطاقة في بيئة صحراوية.",
    "Qatar's per capita emissions (8x global average) and fossil-fuel dominated electricity mix (99.7%) contrast with its ambitious Vision 2030 sustainability goals.": "تتناقض انبعاثات قطر للفرد (8 أضعاف المتوسط العالمي) ومزيج الكهرباء الذي يهيمن عليه الوقود الأحفوري (99.7%) مع أهداف الاستدامة الطموحة في رؤية 2030.",

    # Key insights - Human Development
    "Mean years of schooling increased significantly by 11.44% from 9.67 years in 2016 to 10.77 years in 2022, indicating substantial progress in Qatar's educational development.": "زادت متوسط سنوات الدراسة بشكل كبير بنسبة 11.44% من 9.67 سنة في عام 2016 إلى 10.77 سنة في عام 2022، مما يشير إلى تقدم كبير في التطوير التعليمي في قطر.",
    "Primary education completion rates have steadily improved from 87.03% in 2016 to 90.47% in 2022, moving closer to universal basic education.": "تحسنت معدلات إكمال التعليم الابتدائي باستمرار من 87.03% في عام 2016 إلى 90.47% في عام 2022، مقتربة من التعليم الأساسي الشامل.",
    "The population with at least upper secondary education increased dramatically from 41.01% in 2016 to 51.43% in 2022, representing a 25.4% improvement.": "زادت نسبة السكان الحاصلين على تعليم ثانوي على الأقل بشكل كبير من 41.01% في عام 2016 إلى 51.43% في عام 2022، مما يمثل تحسنًا بنسبة 25.4%.",
    "The percentage of adults with at least a bachelor's degree saw remarkable growth of 60.95%, from 18.88% in 2016 to 30.39% in 2022, one of the most impressive gains among all indicators.": "شهدت نسبة البالغين الحاصلين على درجة البكالوريوس على الأقل نموًا ملحوظًا بنسبة 60.95%، من 18.88% في عام 2016 إلى 30.39% في عام 2022، وهي من أكثر المكاسب إثارة للإعجاب بين جميع المؤشرات.",
    "Qatar's tertiary attainment (~30%) is comparable to high-income countries (30-45%) but remains below leading nations like Canada and Korea (>55%).": "تُعد نسبة التحصيل العالي في قطر (~30%) مماثلة للدول ذات الدخل المرتفع (30-45%) ولكنها لا تزال أقل من الدول الرائدة مثل كندا وكوريا (>55%).",
    
    "The learning gap (difference between expected and learning-adjusted years of schooling) decreased from 0.69 years in 2017 to 0.43 years in 2020, representing a reduction in learning loss from 5.31% to 3.24%.": "انخفضت فجوة التعلم (الفرق بين سنوات الدراسة المتوقعة وسنوات الدراسة المعدلة للتعلم) من 0.69 سنة في عام 2017 إلى 0.43 سنة في عام 2020، مما يمثل انخفاضًا في فقد التعلم من 5.31% إلى 3.24%.",
    "Expected years of schooling increased from 12.46 years in 2016 to 13.26 years in 2020, reflecting expanded educational opportunities.": "ارتفعت سنوات الدراسة المتوقعة من 12.46 سنة في عام 2016 إلى 13.26 سنة في عام 2020، مما يعكس توسع الفرص التعليمية.",
    "Learning-adjusted years of schooling improved from 12.31 years in 2017 to 12.83 years in 2020, indicating not just more education but better quality education.": "تحسنت سنوات الدراسة المعدلة للتعلم من 12.31 سنة في عام 2017 إلى 12.83 سنة في عام 2020، مما يشير إلى ليس فقط المزيد من التعليم ولكن تعليم أفضل جودة.",
    "Despite improvements, the persistence of a learning gap suggests ongoing challenges in education quality that need addressing.": "على الرغم من التحسينات، فإن استمرار فجوة التعلم يشير إلى تحديات مستمرة في جودة التعليم تحتاج إلى معالجة.",
    "Qatar's expected years of schooling (13.26) exceeds the global average (12) but remains below leading countries (15), while learning-adjusted years (12.83) significantly outperform the global average (7.8).": "تتجاوز سنوات الدراسة المتوقعة في قطر (13.26) المتوسط العالمي (12) ولكنها تظل أقل من الدول الرائدة (15)، بينما تتفوق سنوات الدراسة المعدلة للتعلم (12.83) بشكل كبير على المتوسط العالمي (7.8).",
    
    "Qatar's Human Capital Index remained high and stable, changing only marginally from 0.992 in 2017 to 0.993 in 2020, indicating already strong human capital foundations.": "ظل مؤشر رأس المال البشري في قطر مرتفعًا ومستقرًا، مع تغير طفيف فقط من 0.992 في عام 2017 إلى 0.993 في عام 2020، مما يشير إلى أسس قوية بالفعل لرأس المال البشري.",
    "Survival rates show positive trends, with the probability of survival to age 5 increasing from 94.05% in 2017 to 96.14% in 2020.": "تُظهر معدلات البقاء على قيد الحياة اتجاهات إيجابية، مع زيادة احتمالية البقاء على قيد الحياة حتى سن 5 من 94.05% في عام 2017 إلى 96.14% في عام 2020.",
    "The survival rate from age 15-60 improved from 85.0% in 2017 to 87.8% in 2020, reflecting advancements in healthcare and quality of life.": "تحسن معدل البقاء على قيد الحياة من سن 15-60 من 85.0% في عام 2017 إلى 87.8% في عام 2020، مما يعكس التطورات في الرعاية الصحية وجودة الحياة.",
    "A child born in Qatar today can expect to achieve 99.3% of their potential productivity as an adult, one of the highest rates globally.": "يمكن للطفل المولود في قطر اليوم أن يتوقع تحقيق 99.3% من إنتاجيته المحتملة كشخص بالغ، وهي من أعلى المعدلات عالميًا.",
    "Qatar's HCI (0.64) exceeds both the global average (0.56) and regional benchmarks (Saudi Arabia: 0.58) but remains below leading countries like Singapore (0.88) and Japan (0.80).": "يتجاوز مؤشر رأس المال البشري في قطر (0.64) كلاً من المتوسط العالمي (0.56) والمعايير الإقليمية (المملكة العربية السعودية: 0.58) ولكنه يظل أقل من الدول الرائدة مثل سنغافورة (0.88) واليابان (0.80).",
    
    "The pre-primary gender parity index consistently favors females, increasing from 0.979 in 2016 to 1.077 in 2020, indicating strong early educational opportunities for girls.": "يميل مؤشر التكافؤ بين الجنسين في مرحلة ما قبل الابتدائي باستمرار لصالح الإناث، حيث ارتفع من 0.979 في عام 2016 إلى 1.077 في عام 2020، مما يشير إلى فرص تعليمية مبكرة قوية للفتيات.",
    "The trend shows an increasing female advantage in pre-primary enrollment, with the gender parity index growing by 10% from 2016 to 2020.": "يُظهر الاتجاه ميزة متزايدة للإناث في الالتحاق بمرحلة ما قبل الابتدائي، مع نمو مؤشر التكافؤ بين الجنسين بنسبة 10% من 2016 إلى 2020.",
    "Strong female participation in early education creates a foundation for gender equality throughout the educational system.": "تخلق المشاركة القوية للإناث في التعليم المبكر أساسًا للمساواة بين الجنسين في جميع أنحاء النظام التعليمي.",
    "The data suggests Qatar's educational policies have been particularly successful in promoting female participation in education from an early age.": "تشير البيانات إلى أن السياسات التعليمية في قطر كانت ناجحة بشكل خاص في تعزيز مشاركة الإناث في التعليم من سن مبكرة.",
    "Women comprise 51.6% of engineering students in Qatar, and Qatari women's enrollment in higher education is one of the highest in the region, even outnumbering men at public universities.": "تشكل النساء 51.6% من طلاب الهندسة في قطر، ويعد التحاق المرأة القطرية بالتعليم العالي من أعلى المعدلات في المنطقة، حتى أنهن يفوقن عدد الرجال في الجامعات العامة.",
    
    "Qatar has made progress in developing its postgraduate education capacity, with modest increases in both master's and doctoral degree holders.": "أحرزت قطر تقدمًا في تطوير قدرتها في مجال التعليم العالي، مع زيادات متواضعة في كل من حاملي درجة الماجستير والدكتوراه.",
    "The percentage of adults with at least a master's degree is still relatively small but growing steadily as Qatar develops its knowledge economy workforce.": "لا تزال نسبة البالغين الحاصلين على درجة الماجستير على الأقل صغيرة نسبيًا ولكنها تنمو بثبات مع تطوير قطر لقوتها العاملة في اقتصاد المعرفة.",
    "Doctoral education remains at an early stage of development, with a very small percentage of the population holding PhDs.": "لا يزال التعليم في مرحلة الدكتوراه في مرحلة مبكرة من التطوير، مع نسبة صغيرة جدًا من السكان الحاصلين على درجة الدكتوراه.",
    "The OECD average tertiary attainment is approximately 39%, with Qatar aiming to reach similar levels for its citizen population.": "يبلغ متوسط التحصيل العالي في منظمة التعاون الاقتصادي والتنمية حوالي 39%، وتهدف قطر إلى الوصول إلى مستويات مماثلة لسكانها المواطنين.",
    "Qatar's investment in Education City branch campuses and international educational partnerships demonstrates its commitment to developing advanced education, with a goal of leading the Arab world in higher education outcomes by 2030.": "يُظهر استثمار قطر في حرم المدينة التعليمية الفرعية والشراكات التعليمية الدولية التزامها بتطوير التعليم المتقدم، بهدف قيادة العالم العربي في نتائج التعليم العالي بحلول عام 2030.",
    
    "Qatar's primary education completion rates have shown steady improvement, approaching universal completion (98-99%) for nationals.": "أظهرت معدلات إكمال التعليم الابتدائي في قطر تحسنًا مطردًا، مقتربة من الإكمال الشامل (98-99%) للمواطنين.",
    "Lower secondary completion rates have also improved but show greater room for growth compared to primary rates.": "تحسنت معدلات إكمال المرحلة الإعدادية أيضًا ولكنها تُظهر مجالًا أكبر للنمو مقارنة بمعدلات المرحلة الابتدائية.",
    "Qatar outperforms the global average in both primary (89% globally) and secondary (75% globally) completion rates.": "تتفوق قطر على المتوسط العالمي في معدلات إكمال كل من المرحلة الابتدائية (89% عالميًا) والثانوية (75% عالميًا).",
    "Completion rate improvements reflect both better retention of students and expanded access to education for all residents.": "تعكس تحسينات معدل الإكمال كلاً من الاحتفاظ الأفضل بالطلاب وتوسيع فرص الوصول إلى التعليم لجميع المقيمين.",
    "Qatar's investments in free public schooling and education scholarships have been key factors in maximizing completion rates.": "كانت استثمارات قطر في التعليم العام المجاني والمنح التعليمية عوامل رئيسية في تعظيم معدلات الإكمال.",
    
    "The substantial increase in higher education attainment (especially bachelor's degrees) aligns with Qatar's Vision 2030 goal of transitioning to a knowledge-based economy.": "يتماشى الارتفاع الكبير في التحصيل العالي (خاصة درجات البكالوريوس) مع هدف رؤية قطر 2030 المتمثل في الانتقال إلى اقتصاد قائم على المعرفة.",
    "The decreasing learning gap suggests a focus on quality of education, not just increased enrollment numbers.": "تشير فجوة التعلم المتناقصة إلى التركيز على جودة التعليم، وليس فقط زيادة أعداد الملتحقين.",
    "Improvements across multiple indicators (educational attainment, expected years of schooling, survival rates) demonstrate Qatar's multifaceted approach to human development.": "تُظهر التحسينات عبر مؤشرات متعددة (التحصيل التعليمي، وسنوات الدراسة المتوقعة، ومعدلات البقاء على قيد الحياة) نهج قطر متعدد الأوجه للتنمية البشرية.",
    "The strong performance in gender parity indicates attention to educational equity, though more comprehensive equity measures would be valuable.": "يشير الأداء القوي في المساواة بين الجنسين إلى الاهتمام بالإنصاف التعليمي، على الرغم من أن تدابير الإنصاف الأكثر شمولاً ستكون قيّمة.",
    "The consistent improvements across indicators reflect sustained investment in Qatar's human capital, a core component of Vision 2030.": "تعكس التحسينات المستمرة عبر المؤشرات الاستثمار المستدام في رأس المال البشري في قطر، وهو مكون أساسي من رؤية 2030.",
    "Qatar's human development metrics generally exceed global and regional averages but remain below those of leading countries, indicating both achievement and continued room for growth.": "تتجاوز مقاييس التنمية البشرية في قطر عمومًا المتوسطات العالمية والإقليمية ولكنها تظل أقل من تلك الموجودة في الدول الرائدة، مما يشير إلى الإنجاز واستمرار مجال النمو.",
    
    # Key insights - Social Development
    "Qatar has made remarkable progress in sanitation services, increasing coverage from 94.68% in 2016 to 99.94% in 2022 (5.55% improvement).": "أحرزت قطر تقدمًا ملحوظًا في خدمات الصرف الصحي، حيث زادت التغطية من 94.68% في عام 2016 إلى 99.94% في عام 2022 (تحسن بنسبة 5.55%).",
    "The data shows consistent year-on-year improvements, with approximately 0.9 percentage point gains annually.": "تُظهر البيانات تحسينات متسقة من سنة إلى أخرى، مع مكاسب سنوية تبلغ حوالي 0.9 نقطة مئوية.",
    "Qatar has effectively achieved the UN Sustainable Development Goal target for universal access to safely managed sanitation.": "حققت قطر بشكل فعال هدف التنمية المستدامة للأمم المتحدة المتمثل في الوصول الشامل إلى خدمات الصرف الصحي المدارة بأمان.",
    "Near-universal sanitation coverage represents a significant public health achievement that contributes to disease prevention and overall quality of life.": "تمثل تغطية الصرف الصحي شبه الشاملة إنجازًا كبيرًا في مجال الصحة العامة يسهم في الوقاية من الأمراض وجودة الحياة بشكل عام.",
    "Qatar's sanitation access (99.94%) significantly exceeds the global average (75%) and is comparable to leading regions like North America and Europe (99%).": "يتجاوز وصول قطر إلى خدمات الصرف الصحي (99.94%) بشكل كبير المتوسط العالمي (75%) ويمكن مقارنته بالمناطق الرائدة مثل أمريكا الشمالية وأوروبا (99%).",
    
    "Qatar has achieved gender parity in primary education, with the Gender Parity Index (GPI) improving from 0.994 in 2016 to 1.030 in 2019, indicating a slight advantage for female students.": "حققت قطر المساواة بين الجنسين في التعليم الابتدائي، مع تحسن مؤشر التكافؤ بين الجنسين (GPI) من 0.994 في عام 2016 إلى 1.030 في عام 2019، مما يشير إلى ميزة طفيفة للطالبات.",
    "The 3.64% improvement in GPI reflects Qatar's commitment to equal educational opportunities regardless of gender.": "يعكس التحسن بنسبة 3.64% في مؤشر التكافؤ بين الجنسين التزام قطر بفرص تعليمية متساوية بغض النظر عن الجنس.",
    "By 2019, the GPI exceeded 1.0, indicating that girls slightly outnumber boys in primary education enrollment.": "بحلول عام 2019، تجاوز مؤشر التكافؤ بين الجنسين 1.0، مما يشير إلى أن عدد الفتيات يفوق عدد الأولاد قليلاً في الالتحاق بالتعليم الابتدائي.",
    "The data suggests Qatar's educational policies have been effective in eliminating gender-based barriers to basic education.": "تشير البيانات إلى أن السياسات التعليمية في قطر كانت فعالة في إزالة الحواجز القائمة على نوع الجنس أمام التعليم الأساسي.",
    "Women comprise 51.6% of engineering students in Qatar, and female enrollment in tertiary education is among the highest in the region, with women often outnumbering men in university enrollment.": "تشكل النساء 51.6% من طلاب الهندسة في قطر، ويعد التحاق الإناث بالتعليم العالي من بين أعلى المعدلات في المنطقة، حيث غالبًا ما يفوق عدد النساء عدد الرجال في الالتحاق بالجامعات.",
    
    "The percentage of graduates from STEM programs has decreased dramatically by 39.96%, from 29.70% in 2016 to 17.83% in 2022.": "انخفضت نسبة الخريجين من برامج العلوم والتكنولوجيا والهندسة والرياضيات بشكل كبير بنسبة 39.96%، من 29.70% في عام 2016 إلى 17.83% في عام 2022.",
    "The decline has been persistent across all years, indicating a systematic shift in student preferences away from STEM fields.": "كان الانخفاض مستمرًا عبر جميع السنوات، مما يشير إلى تحول منهجي في تفضيلات الطلاب بعيدًا عن مجالات العلوم والتكنولوجيا والهندسة والرياضيات.",
    "This trend poses a significant challenge to Qatar's ambition to develop a knowledge-based economy with strong scientific and technological foundations.": "يشكل هذا الاتجاه تحديًا كبيرًا لطموح قطر في تطوير اقتصاد قائم على المعرفة بأسس علمية وتكنولوجية قوية.",
    "The consistent decline suggests an urgent need for interventions to increase interest and enrollment in STEM fields.": "يشير الانخفاض المستمر إلى الحاجة الملحة لتدخلات لزيادة الاهتمام والالتحاق بمجالات العلوم والتكنولوجيا والهندسة والرياضيات.",
    "Qatar's current STEM graduate percentage (17.83%) is below both the global average (23%) and regional peer Saudi Arabia (32%), and significantly trails leading countries like Oman (43%) and Germany (37%).": "تقل النسبة الحالية لخريجي العلوم والتكنولوجيا والهندسة والرياضيات في قطر (17.83%) عن كل من المتوسط العالمي (23%) والمملكة العربية السعودية (32%)، وتتخلف بشكل كبير عن الدول الرائدة مثل عمان (43%) وألمانيا (37%).",
    
    "Email skills have shown steady improvement, increasing from 56.55% in 2016 to 58.72% in 2020 (3.84% growth).": "أظهرت مهارات البريد الإلكتروني تحسنًا مطردًا، بزيادة من 56.55% في عام 2016 إلى 58.72% في عام 2020 (نمو بنسبة 3.84%).",
    "Programming skills have decreased from 5.51% in 2016 to 5.06% in 2019 (-8.25%), indicating challenges in developing advanced digital capabilities.": "انخفضت مهارات البرمجة من 5.51% في عام 2016 إلى 5.06% في عام 2019 (-8.25%)، مما يشير إلى تحديات في تطوير القدرات الرقمية المتقدمة.",
    "The divergence between improving basic skills and declining advanced skills suggests a digital skills gap that could impact innovation capacity.": "يشير التباعد بين تحسين المهارات الأساسية وتراجع المهارات المتقدمة إلى فجوة في المهارات الرقمية التي يمكن أن تؤثر على قدرة الابتكار.",
    "While basic digital literacy is improving, the relatively low levels of advanced digital skills may limit Qatar's digital transformation ambitions.": "في حين تتحسن محو الأمية الرقمية الأساسية، فإن المستويات المنخفضة نسبيًا من المهارات الرقمية المتقدمة قد تحد من طموحات التحول الرقمي في قطر.",
    "Qatar's vision for a knowledge economy requires stronger development of advanced technical skills to support digitization initiatives and AI/robotics adoption.": "تتطلب رؤية قطر لاقتصاد المعرفة تطويرًا أقوى للمهارات التقنية المتقدمة لدعم مبادرات الرقمنة واعتماد الذكاء الاصطناعي/الروبوتات.",
    
    "ICT (Information & Communication Technologies) graduates represent a relatively small percentage of Qatar's total tertiary graduates.": "يمثل خريجو تكنولوجيا المعلومات والاتصالات نسبة صغيرة نسبيًا من إجمالي خريجي التعليم العالي في قطر.",
    "ICT graduate percentages have shown fluctuations without a clear upward trend, failing to match the growing importance of digital skills in the global economy.": "أظهرت نسب خريجي تكنولوجيا المعلومات والاتصالات تقلبات دون اتجاه تصاعدي واضح، وفشلت في مطابقة الأهمية المتزايدة للمهارات الرقمية في الاقتصاد العالمي.",
    "The gap between Qatar's ICT graduate production and its digital economy ambitions poses a challenge for the country's knowledge economy transition.": "تشكل الفجوة بين إنتاج خريجي تكنولوجيا المعلومات والاتصالات في قطر وطموحات الاقتصاد الرقمي تحديًا لانتقال البلاد إلى اقتصاد المعرفة.",
    "Qatar's partnerships with technology companies (Microsoft, Google Cloud) are creating demand for ICT specialists that may exceed domestic graduate production.": "تخلق شراكات قطر مع شركات التكنولوجيا (مايكروسوفت، جوجل كلاود) طلبًا على متخصصي تكنولوجيا المعلومات والاتصالات قد يتجاوز إنتاج الخريجين المحليين.",
    "Targeted programs to encourage ICT specialization will be crucial for Qatar to develop the skilled workforce needed for its digital future.": "ستكون البرامج المستهدفة لتشجيع التخصص في تكنولوجيا المعلومات والاتصالات حاسمة لقطر لتطوير القوى العاملة الماهرة اللازمة لمستقبلها الرقمي.",
    
    "Qatar shows impressive achievements in basic social infrastructure (sanitation) and gender equity in education, but concerning trends in STEM education and advanced digital skills.": "تُظهر قطر إنجازات مثيرة للإعجاب في البنية التحتية الاجتماعية الأساسية (الصرف الصحي) والإنصاف بين الجنسين في التعليم، ولكن اتجاهات مقلقة في تعليم العلوم والتكنولوجيا والهندسة والرياضيات والمهارات الرقمية المتقدمة.",
    "The data suggests that Qatar has successfully built social development foundations but faces challenges in developing the innovation capabilities needed for a knowledge economy.": "تشير البيانات إلى أن قطر قد نجحت في بناء أسس التنمية الاجتماعية ولكنها تواجه تحديات في تطوير قدرات الابتكار اللازمة لاقتصاد المعرفة.",
    "The achievement of gender parity in primary education represents a significant milestone in Qatar's social development journey.": "يمثل تحقيق المساواة بين الجنسين في التعليم الابتدائي معلمًا مهمًا في رحلة التنمية الاجتماعية في قطر.",
    "The consistent decline in STEM and ICT graduates represents one of the most significant challenges to Qatar Vision 2030's knowledge economy objectives.": "يمثل الانخفاض المستمر في خريجي العلوم والتكنولوجيا والهندسة والرياضيات وتكنولوجيا المعلومات والاتصالات أحد أهم التحديات التي تواجه أهداف اقتصاد المعرفة في رؤية قطر 2030.",
    "The data reveals a potential gap between Qatar's educational system outputs and its economic diversification requirements, particularly in technical fields.": "تكشف البيانات عن فجوة محتملة بين مخرجات النظام التعليمي في قطر ومتطلبات التنويع الاقتصادي، خاصة في المجالات التقنية.",
    "Qatar's sanitation access (1.3x global average) is world-class, while its STEM graduate percentage (0.78x global average) indicates a critical area for improvement.": "يعد وصول قطر إلى خدمات الصرف الصحي (1.3 ضعف المتوسط العالمي) من الطراز العالمي، بينما تشير نسبة خريجي العلوم والتكنولوجيا والهندسة والرياضيات (0.78 ضعف المتوسط العالمي) إلى مجال حرج للتحسين.",
    
    # Business & Law Graduates
    "Business & Law Graduates (%)": "خريجو الأعمال والقانون (%)",
    
    # Global average comparisons with multipliers
    "5.4x global average": "5.4 أضعاف المتوسط العالمي",
    "8x global average": "8 أضعاف المتوسط العالمي",
    "1.3x global average": "1.3 ضعف المتوسط العالمي",
    "0.78x global average": "0.78 ضعف المتوسط العالمي",
}

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
        # Add similar handling for other patterns
        
        return translations.get(text, text)  # Return translation or original text
    return text  # Return original English text

# Create a more modern header with better spacing and layout
def create_header(language='english'):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                # Language toggle button in the upper right
                dbc.ButtonGroup(
                    [
                        dbc.Button("English", id="btn-english", color="primary" if language == "english" else "outline-primary"),
                        dbc.Button("العربية", id="btn-arabic", color="primary" if language == "arabic" else "outline-primary"),
                    ],
                    className="mb-3"
                ),
            ], width=12, className="d-flex justify-content-end"),
        ]),
        dbc.Row([
            dbc.Col(html.Img(src='assets/qatar_vision_2030_logo.png', height='100px'), width=2, className="d-flex align-items-center"),
            dbc.Col([
                html.H1(get_translation("Qatar Vision 2030 Dashboard", language), className="mb-0", 
                       style={"color": colors['text'], "fontWeight": "bold"}),
                html.P(get_translation("Monitoring Progress Across Economic, Environmental, Human, and Social Development Pillars", language), 
                      className="lead mb-0")
            ], width=10)
        ], className="py-4 border-bottom mb-4")
    ], fluid=True, style={"backgroundColor": colors['card']})

# Create tabs with a more modern style
def create_tabs(language='english'):
    return dbc.Tabs([
        dbc.Tab(label=get_translation("Key Indicators", language), tab_id="key-indicators", 
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label=get_translation("Economic Development", language), tab_id="economic", 
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label=get_translation("Environmental Development", language), tab_id="environmental", 
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label=get_translation("Human Development", language), tab_id="human", 
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label=get_translation("Social Development", language), tab_id="social", 
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
    ], id="tabs", active_tab="key-indicators", className="mb-4")

# Create year slider with improved styling
def create_year_slider(language='english'):
    return dbc.Card(
        dbc.CardBody([
            html.H5(get_translation("Select Year Range", language), className="card-title", style={"color": colors['text']}),
            dcc.RangeSlider(
                id='year-slider',
                min=min(key_indicators_df['Year']),
                max=max(key_indicators_df['Year']),
                step=1,
                marks={int(year): {"label": str(year), "style": {"transform": "rotate(45deg)", "color": colors['text']}} 
                       for year in key_indicators_df['Year'].unique()},
                value=[min(key_indicators_df['Year']), max(key_indicators_df['Year'])],
                className="mt-3"
            )
        ]), className="mb-4 shadow-sm", style={"backgroundColor": colors['card']}
    )

# Helper function to create insight cards that display the PDF analysis with sentiment icons
def create_insight_card(title, insights, pillar_color, language='english'):
    # Dictionary to categorize each insight by sentiment
    # Format: 'insight text': {'sentiment': 'positive', 'negative', or 'neutral'}
    insight_sentiments = {}
    
    # Economic insights sentiments
    insight_sentiments.update({
        "Qatar's GDP per capita has shown notable volatility between 2016-2023, with a 3.24% overall decline.": {'sentiment': 'negative'},
        "The most significant drop occurred in 2020 (to $103,062), representing a 14% decline from 2016 levels.": {'sentiment': 'negative'},
        "The economy showed strong resilience with a rapid recovery to $116,833 in 2021.": {'sentiment': 'positive'},
        "The stabilization around $115,000 in recent years suggests a 'new normal' that balances energy market realities with economic diversification efforts.": {'sentiment': 'neutral'},
        "Qatar's GDP per capita remains approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992).": {'sentiment': 'positive'},
        
        "Oil production declined from 582.57 TWh in 2016 to a low of 511.54 TWh in 2020 (-12.2%), but has since recovered to 616.21 TWh in 2023.": {'sentiment': 'neutral'},
        "The initial reduction reflects Qatar's strategic decision to focus more on natural gas, where it holds comparative advantage.": {'sentiment': 'positive'},
        "The 20.5% increase from 2020 to 2023 shows Qatar's response to higher global energy demand and prices after the pandemic.": {'sentiment': 'positive'},
        "The upward trend in recent years raises questions about alignment with climate commitments and sustainability goals.": {'sentiment': 'negative'},
        "Qatar's oil output (~0.67 million barrels/day) is modest compared to other GCC producers, reflecting its strategic focus on natural gas production.": {'sentiment': 'neutral'},
        
        "Qatar has been investing heavily in liquefied natural gas (LNG) infrastructure, aiming to increase production capacity from 77 to 126 million tons annually by 2027.": {'sentiment': 'positive'},
        "The focus on gas aligns with Qatar's positioning of natural gas as a 'transition fuel' with lower carbon emissions than oil or coal.": {'sentiment': 'positive'},
        "Sustained gas production provides Qatar with economic stability as global demand for cleaner burning fuels increases.": {'sentiment': 'positive'},
        "The vast majority of Qatar's gas production is destined for export markets, making it a critical component of the country's revenue stream.": {'sentiment': 'positive'},
        "Qatar aims to maintain its position as one of the world's largest LNG exporters, competing with the U.S. which surpassed Qatar as the top LNG exporter in 2023.": {'sentiment': 'neutral'},
        
        "Energy consumption fluctuated significantly, from 168.92 TWh in 2016 to a low of 126.88 TWh in 2020 (-24.9%), before rebounding to 170.21 TWh in 2023.": {'sentiment': 'neutral'},
        "The consumption pattern closely mirrors GDP trends, with the 2020 pandemic-related drop and subsequent recovery.": {'sentiment': 'neutral'},
        "The data suggests limited progress in improving energy efficiency, as consumption has grown in line with economic recovery.": {'sentiment': 'negative'},
        "Qatar has one of the world's highest per capita energy consumption rates, reflecting its energy-intensive industries and high standard of living.": {'sentiment': 'negative'},
        "Global energy demand typically grows at 1-2% annually, while Qatar experienced 6-7% annual growth in the 2010s, though it targets moderating to 2-3% by the late 2020s.": {'sentiment': 'neutral'},
        
        "Qatar's energy growth rates show significant volatility, reflecting both global energy market fluctuations and domestic economic changes.": {'sentiment': 'neutral'},
        "Growth rates were particularly negative during the 2020 pandemic period, with sharp contractions across all energy sources.": {'sentiment': 'negative'},
        "Post-pandemic recovery shows positive growth rates, particularly in oil consumption, which may contradict Vision 2030's sustainability goals.": {'sentiment': 'negative'},
        "Qatar's historical energy demand growth of 6-7% annually significantly exceeds the global average (1-2%), highlighting the challenge of energy-intensive development.": {'sentiment': 'negative'},
        "Vision 2030 and the National Environment and Climate Strategy aim to reduce these high growth rates to a more sustainable 2-3% annually by 2030, still higher than typical OECD countries that have achieved near-zero growth through efficiency measures.": {'sentiment': 'neutral'},
        
        "Despite Qatar's challenging desert environment, agricultural productivity per worker is relatively high at $10,000-$11,000 (2015 US$) in value-added terms.": {'sentiment': 'positive'},
        "Qatar's agricultural productivity exceeds regional peers like Oman (~$6,000) but remains well below advanced economies (>$50,000 per worker).": {'sentiment': 'neutral'},
        "The high per-worker value reflects Qatar's capital-intensive agricultural approach, utilizing advanced technologies like hydroponics and climate-controlled greenhouses.": {'sentiment': 'positive'},
        "Following the 2017 blockade, Qatar has heavily invested in agricultural self-sufficiency, with arable land increasing by 14.75% (18,300 to 21,000 hectares).": {'sentiment': 'positive'},
        "By 2030, Qatar aims to further improve agricultural efficiency through high-yield technology to enhance food security, even as the sector remains <1% of GDP.": {'sentiment': 'positive'},
        
        "Business, administration, and law have historically been popular fields of study in Qatar, with approximately 26% of tertiary graduates specializing in these areas in 2018.": {'sentiment': 'neutral'},
        "This proportion is lower than in some other service-driven Gulf economies, such as Bahrain, where nearly 50% of graduates focus on business and law.": {'sentiment': 'neutral'},
        "Vision 2030 doesn't discourage these fields but seeks a better balance with STEM subjects to support innovation and knowledge economy development.": {'sentiment': 'positive'},
        "The inverse relationship between business/law and STEM graduates represents a challenge for Qatar's diversification - as one increases, the other tends to decrease.": {'sentiment': 'negative'},
        "Qatar aims to keep business/law graduates around or below one-third of total graduates while boosting STEM and technical fields to better align with labor market needs in a diversifying economy.": {'sentiment': 'positive'},
    })
    
    # Environmental insights sentiments
    insight_sentiments.update({
        "Total CO₂ emissions rose by 32.42% from 87.4 million tonnes in 2016 to 115.7 million tonnes in 2023, showing a concerning upward trajectory.": {'sentiment': 'negative'},
        "CO₂ emissions per capita increased by 15.54% from 33.62 tonnes in 2016 to 38.84 tonnes in 2023, maintaining Qatar's position among the world's highest per capita emitters.": {'sentiment': 'negative'},
        "The data shows an accelerating emissions trend, with the most significant jump occurring between 2022 and 2023 (9% increase in just one year).": {'sentiment': 'negative'},
        "The rising emissions directly conflict with Qatar's environmental sustainability goals under Vision 2030 and its international climate commitments.": {'sentiment': 'negative'},
        "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes).": {'sentiment': 'negative'},
        
        "Fossil fuels generate over 99.7% of Qatar's electricity, with renewables contributing a minimal 0.28-0.31% throughout the period.": {'sentiment': 'negative'},
        "Total electricity production increased by 28.2% from 42.44 TWh in 2016 to 54.39 TWh in 2023, driving up absolute emissions.": {'sentiment': 'negative'},
        "Despite global renewable energy trends, Qatar's renewable electricity generation has plateaued at around 0.15 TWh since 2018.": {'sentiment': 'negative'},
        "The data reveals a significant gap between Qatar's sustainability rhetoric and actual energy transformation progress.": {'sentiment': 'negative'},
        "Global electricity mix shows 61% non-renewables vs 39% renewables, while Qatar targets 20% renewables by 2030, significantly above the Middle East average (4%) but below global average (29%).": {'sentiment': 'neutral'},
        
        "Solar capacity experienced a remarkable 15,686% increase from 0.0051 GW in 2016 to 0.8051 GW in 2023.": {'sentiment': 'positive'},
        "Almost all capacity growth occurred in a single year (2022), indicating a major infrastructure commissioning.": {'sentiment': 'positive'},
        "Despite the capacity increase, the solar electricity generation data doesn't yet show a corresponding production increase, suggesting the new capacity may be at early operational stages.": {'sentiment': 'neutral'},
        "This dramatic solar expansion aligns with Qatar's National Development Strategy and preparations for hosting the 2022 FIFA World Cup.": {'sentiment': 'positive'},
        "Qatar's 2030 target of 4 GW solar capacity would place it among the regional leaders in renewable capacity per capita, though still modest by global standards.": {'sentiment': 'positive'},
        
        "Qatar's annual change in primary energy consumption shows significant volatility, with both substantial growth and contraction periods.": {'sentiment': 'neutral'},
        "The 2020 pandemic year saw the most dramatic energy consumption contraction, reflecting global economic slowdown and reduced industrial activity.": {'sentiment': 'neutral'},
        "Post-pandemic recovery shows a return to positive growth rates in energy consumption, potentially challenging sustainability targets.": {'sentiment': 'negative'},
        "Qatar's typical annual energy consumption growth (5-6% in the 2010s) far exceeds the global average (1.9% in 2022), reflecting Qatar's rapid development and energy-intensive economy.": {'sentiment': 'negative'},
        "Vision 2030 initiatives aim to moderate Qatar's energy consumption growth to below 3% annually by the late 2020s through efficiency improvements and renewable integration, though this would still exceed typical developed economy growth rates.": {'sentiment': 'neutral'},
        
        "Qatar's renewable electricity generation is dominated by solar power, accounting for nearly all renewable output since 2018.": {'sentiment': 'neutral'},
        "Bioenergy makes a minimal contribution to Qatar's renewable mix, with very limited growth over the monitoring period.": {'sentiment': 'negative'},
        "Qatar's total renewable electricity production (0.15 TWh) is a fraction of the Middle East's already low renewable generation (47 TWh in 2022) and insignificant compared to global renewables (7,858 TWh in 2021).": {'sentiment': 'negative'},
        "The dramatic increase in solar capacity in 2022-2023 has not yet translated to substantial increases in electricity generation, suggesting early operational stages or potential utilization challenges.": {'sentiment': 'neutral'},
        "Qatar's National Renewable Energy Strategy target of 4 GW solar capacity by 2030 would dramatically increase renewable electricity production, helping Qatar progress from its current 0.3% renewable share toward its 20% target.": {'sentiment': 'positive'},
        
        "Agricultural land increased from 71,000 hectares in 2016 to 74,000 hectares in 2021 (4.23% growth), reflecting Qatar's food security strategy.": {'sentiment': 'positive'},
        "Arable land saw more significant growth of 14.75% (18,300 to 21,000 hectares), indicating intensified cultivation efforts.": {'sentiment': 'positive'},
        "These increases align with Qatar's post-2017 blockade strategy to enhance domestic food production and reduce import dependence.": {'sentiment': 'positive'},
        "The expansion of agriculture in Qatar's challenging desert environment demonstrates technological innovation in climate-adapted farming.": {'sentiment': 'positive'},
        "Qatar's agricultural productivity (~$10-11K per worker) exceeds regional peers like Oman (~$6K) but remains below advanced economies (>$50K per worker).": {'sentiment': 'neutral'},
    })
    
    # Human Development insights sentiments
    insight_sentiments.update({
        "Mean years of schooling increased significantly by 11.44% from 9.67 years in 2016 to 10.77 years in 2022, indicating substantial progress in Qatar's educational development.": {'sentiment': 'positive'},
        "Primary education completion rates have steadily improved from 87.03% in 2016 to 90.47% in 2022, moving closer to universal basic education.": {'sentiment': 'positive'},
        "The population with at least upper secondary education increased dramatically from 41.01% in 2016 to 51.43% in 2022, representing a 25.4% improvement.": {'sentiment': 'positive'},
        "The percentage of adults with at least a bachelor's degree saw remarkable growth of 60.95%, from 18.88% in 2016 to 30.39% in 2022, one of the most impressive gains among all indicators.": {'sentiment': 'positive'},
        "Qatar's tertiary attainment (~30%) is comparable to high-income countries (30-45%) but remains below leading nations like Canada and Korea (>55%).": {'sentiment': 'neutral'},
        
        "The learning gap (difference between expected and learning-adjusted years of schooling) decreased from 0.69 years in 2017 to 0.43 years in 2020, representing a reduction in learning loss from 5.31% to 3.24%.": {'sentiment': 'positive'},
        "Expected years of schooling increased from 12.46 years in 2016 to 13.26 years in 2020, reflecting expanded educational opportunities.": {'sentiment': 'positive'},
        "Learning-adjusted years of schooling improved from 12.31 years in 2017 to 12.83 years in 2020, indicating not just more education but better quality education.": {'sentiment': 'positive'},
        "Despite improvements, the persistence of a learning gap suggests ongoing challenges in education quality that need addressing.": {'sentiment': 'negative'},
        "Qatar's expected years of schooling (13.26) exceeds the global average (12) but remains below leading countries (15), while learning-adjusted years (12.83) significantly outperform the global average (7.8).": {'sentiment': 'positive'},
    
        "Qatar's Human Capital Index remained high and stable, changing only marginally from 0.992 in 2017 to 0.993 in 2020, indicating already strong human capital foundations.": {'sentiment': 'positive'},
        "Survival rates show positive trends, with the probability of survival to age 5 increasing from 94.05% in 2017 to 96.14% in 2020.": {'sentiment': 'positive'},
        "The survival rate from age 15-60 improved from 85.0% in 2017 to 87.8% in 2020, reflecting advancements in healthcare and quality of life.": {'sentiment': 'positive'},
        "A child born in Qatar today can expect to achieve 99.3% of their potential productivity as an adult, one of the highest rates globally.": {'sentiment': 'positive'},
        "Qatar's HCI (0.64) exceeds both the global average (0.56) and regional benchmarks (Saudi Arabia: 0.58) but remains below leading countries like Singapore (0.88) and Japan (0.80).": {'sentiment': 'positive'},
        
        "The pre-primary gender parity index consistently favors females, increasing from 0.979 in 2016 to 1.077 in 2020, indicating strong early educational opportunities for girls.": {'sentiment': 'positive'},
        "The trend shows an increasing female advantage in pre-primary enrollment, with the gender parity index growing by 10% from 2016 to 2020.": {'sentiment': 'positive'},
        "Strong female participation in early education creates a foundation for gender equality throughout the educational system.": {'sentiment': 'positive'},
        "The data suggests Qatar's educational policies have been particularly successful in promoting female participation in education from an early age.": {'sentiment': 'positive'},
        "Women comprise 51.6% of engineering students in Qatar, and Qatari women's enrollment in higher education is one of the highest in the region, even outnumbering men at public universities.": {'sentiment': 'positive'},
        
        "Qatar has made progress in developing its postgraduate education capacity, with modest increases in both master's and doctoral degree holders.": {'sentiment': 'positive'},
        "The percentage of adults with at least a master's degree is still relatively small but growing steadily as Qatar develops its knowledge economy workforce.": {'sentiment': 'neutral'},
        "Doctoral education remains at an early stage of development, with a very small percentage of the population holding PhDs.": {'sentiment': 'neutral'},
        "The OECD average tertiary attainment is approximately 39%, with Qatar aiming to reach similar levels for its citizen population.": {'sentiment': 'neutral'},
        "Qatar's investment in Education City branch campuses and international educational partnerships demonstrates its commitment to developing advanced education, with a goal of leading the Arab world in higher education outcomes by 2030.": {'sentiment': 'positive'},
        
        "Qatar's primary education completion rates have shown steady improvement, approaching universal completion (98-99%) for nationals.": {'sentiment': 'positive'},
        "Lower secondary completion rates have also improved but show greater room for growth compared to primary rates.": {'sentiment': 'neutral'},
        "Qatar outperforms the global average in both primary (89% globally) and secondary (75% globally) completion rates.": {'sentiment': 'positive'},
        "Completion rate improvements reflect both better retention of students and expanded access to education for all residents.": {'sentiment': 'positive'},
        "Qatar's investments in free public schooling and education scholarships have been key factors in maximizing completion rates.": {'sentiment': 'positive'},
    })
    
    # Social Development insights sentiments
    insight_sentiments.update({
        "Qatar has made remarkable progress in sanitation services, increasing coverage from 94.68% in 2016 to 99.94% in 2022 (5.55% improvement).": {'sentiment': 'positive'},
        "The data shows consistent year-on-year improvements, with approximately 0.9 percentage point gains annually.": {'sentiment': 'positive'},
        "Qatar has effectively achieved the UN Sustainable Development Goal target for universal access to safely managed sanitation.": {'sentiment': 'positive'},
        "Near-universal sanitation coverage represents a significant public health achievement that contributes to disease prevention and overall quality of life.": {'sentiment': 'positive'},
        "Qatar's sanitation access (99.94%) significantly exceeds the global average (75%) and is comparable to leading regions like North America and Europe (99%).": {'sentiment': 'positive'},
        
        "Qatar has achieved gender parity in primary education, with the Gender Parity Index (GPI) improving from 0.994 in 2016 to 1.030 in 2019, indicating a slight advantage for female students.": {'sentiment': 'positive'},
        "The 3.64% improvement in GPI reflects Qatar's commitment to equal educational opportunities regardless of gender.": {'sentiment': 'positive'},
        "By 2019, the GPI exceeded 1.0, indicating that girls slightly outnumber boys in primary education enrollment.": {'sentiment': 'positive'},
        "The data suggests Qatar's educational policies have been effective in eliminating gender-based barriers to basic education.": {'sentiment': 'positive'},
        "Women comprise 51.6% of engineering students in Qatar, and female enrollment in tertiary education is among the highest in the region, with women often outnumbering men in university enrollment.": {'sentiment': 'positive'},
        
        "The percentage of graduates from STEM programs has decreased dramatically by 39.96%, from 29.70% in 2016 to 17.83% in 2022.": {'sentiment': 'negative'},
        "The decline has been persistent across all years, indicating a systematic shift in student preferences away from STEM fields.": {'sentiment': 'negative'},
        "This trend poses a significant challenge to Qatar's ambition to develop a knowledge-based economy with strong scientific and technological foundations.": {'sentiment': 'negative'},
        "The consistent decline suggests an urgent need for interventions to increase interest and enrollment in STEM fields.": {'sentiment': 'negative'},
        "Qatar's current STEM graduate percentage (17.83%) is below both the global average (23%) and regional peer Saudi Arabia (32%), and significantly trails leading countries like Oman (43%) and Germany (37%).": {'sentiment': 'negative'},
        
        "Email skills have shown steady improvement, increasing from 56.55% in 2016 to 58.72% in 2020 (3.84% growth).": {'sentiment': 'positive'},
        "Programming skills have decreased from 5.51% in 2016 to 5.06% in 2019 (-8.25%), indicating challenges in developing advanced digital capabilities.": {'sentiment': 'negative'},
        "The divergence between improving basic skills and declining advanced skills suggests a digital skills gap that could impact innovation capacity.": {'sentiment': 'negative'},
        "While basic digital literacy is improving, the relatively low levels of advanced digital skills may limit Qatar's digital transformation ambitions.": {'sentiment': 'negative'},
        "Qatar's vision for a knowledge economy requires stronger development of advanced technical skills to support digitization initiatives and AI/robotics adoption.": {'sentiment': 'neutral'},
        
        "ICT (Information & Communication Technologies) graduates represent a relatively small percentage of Qatar's total tertiary graduates.": {'sentiment': 'negative'},
        "ICT graduate percentages have shown fluctuations without a clear upward trend, failing to match the growing importance of digital skills in the global economy.": {'sentiment': 'negative'},
        "The gap between Qatar's ICT graduate production and its digital economy ambitions poses a challenge for the country's knowledge economy transition.": {'sentiment': 'negative'},
        "Qatar's partnerships with technology companies (Microsoft, Google Cloud) are creating demand for ICT specialists that may exceed domestic graduate production.": {'sentiment': 'negative'},
        "Targeted programs to encourage ICT specialization will be crucial for Qatar to develop the skilled workforce needed for its digital future.": {'sentiment': 'neutral'},
    })
    
    # Key Indicators insights sentiments
    insight_sentiments.update({
        "Qatar maintained one of the world's highest GDP per capita levels throughout the period (over $100,000), but experienced a slight overall decline of 3.24% from 2016 to 2023.": {'sentiment': 'neutral'},
        "A significant drop occurred in 2020 (down to $103,061), representing a 14.2% decrease from 2016 levels, clearly showing the pandemic's impact.": {'sentiment': 'negative'},
        "The economy rebounded strongly in 2021 to $116,832, nearly returning to pre-pandemic levels, demonstrating economic resilience.": {'sentiment': 'positive'},
        "Qatar's GDP per capita is approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992).": {'sentiment': 'positive'},
    
        "The HCI data is only available for 2017, 2018, and 2020, which limits comprehensive trend analysis.": {'sentiment': 'neutral'},
        "There was a steady improvement in HCI from 0.615 in 2017 to 0.638 in 2020, representing a 3.7% increase.": {'sentiment': 'positive'},
        "A score of 0.638 means that a child born in Qatar today will be 63.8% as productive as they could be with complete education and full health.": {'sentiment': 'neutral'},
        "Qatar's HCI (0.64) is above the global average (0.56) and Middle East average, but remains below leading countries like Singapore (0.88) and Japan (0.80).": {'sentiment': 'positive'},
        
        "CO₂ emissions per capita increased by 15.54% from 2016 to 2023, reaching 38.84 tonnes per person in 2023.": {'sentiment': 'negative'},
        "Emissions showed significant year-to-year variability, suggesting changing energy usage patterns.": {'sentiment': 'neutral'},
        "The upward trend contradicts Qatar's environmental sustainability goals and presents a major challenge for Vision 2030's environmental pillar.": {'sentiment': 'negative'},
        "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes).": {'sentiment': 'negative'},
        
        "Renewable electricity production increased slightly from 0.13 TWh in 2016 to 0.15 TWh in 2023 (15.38% increase).": {'sentiment': 'positive'},
        "After increasing to 0.15 TWh in 2018, renewable electricity production has plateaued without further growth through 2023.": {'sentiment': 'negative'},
        "Given Qatar's climate, there's significant untapped potential for solar energy expansion.": {'sentiment': 'neutral'},
        "Qatar targets 20% of electricity from renewables by 2030, which would exceed the current Middle East average (4%) but remain below the global average (29%) and far behind leading countries like Brazil and Norway (80-95%).": {'sentiment': 'positive'},
        
        "Qatar's energy production is dominated by natural gas, with a significant focus on LNG exports where Qatar is a global leader.": {'sentiment': 'positive'},
        "Oil production experienced a decline from 582.57 TWh in 2016 to 511.54 TWh in 2020 (-12.2%), before rebounding to 616.21 TWh in 2023.": {'sentiment': 'neutral'},
        "Gas production has been more stable, reflecting Qatar's strategic emphasis on its vast North Field gas reserves.": {'sentiment': 'positive'},
        "Qatar plans to boost LNG output by 85% from current 77 million tons to 126-142 million tons by 2030, aiming to reclaim its position as the world's top LNG exporter.": {'sentiment': 'positive'},
        "This expansion will cement Qatar's position in global energy markets, targeting approximately 25% of global LNG trade by 2030.": {'sentiment': 'positive'},
        
        "Qatar has shown steady improvement in expected years of schooling, increasing from 12.46 years in 2016 to 13.26 years in 2020 (6.4% growth).": {'sentiment': 'positive'},
        "The Learning-Adjusted Years of School metric improved from 12.31 years in 2017 to 12.83 years in 2020, indicating enhanced education quality.": {'sentiment': 'positive'},
        "The gap between expected and learning-adjusted years decreased from 0.69 to 0.43 years, showing a reduction in learning loss from 5.31% to 3.24%.": {'sentiment': 'positive'},
        "Qatar's tertiary enrollment has grown substantially, from approximately 20% in the mid-2010s to over 40% recently, approaching the global average.": {'sentiment': 'positive'},
        "Qatar's education metrics now exceed global averages (12 expected years globally vs. 13.26 in Qatar; 7.8 learning-adjusted years globally vs. 12.83 in Qatar).": {'sentiment': 'positive'},
        
        "The percentage of graduates from STEM programs has declined dramatically from 29.70% in 2016 to 17.83% in 2022, representing a 39.96% decrease.": {'sentiment': 'negative'},
        "This consistent downward trend in STEM graduates contradicts Qatar's Vision 2030 goal of building a knowledge-based economy and innovation ecosystem.": {'sentiment': 'negative'},
        "At 17.83%, Qatar's STEM graduate percentage has fallen below the global average (23%) and significantly trails regional competitor Saudi Arabia (32%).": {'sentiment': 'negative'},
        "Leading countries in STEM education, such as Oman (43%) and Germany (37%), far outpace Qatar's current performance in this critical metric.": {'sentiment': 'negative'},
        "The decline in STEM graduates represents a major challenge for Qatar's economic diversification goals and may hinder the country's competitiveness in high-tech sectors.": {'sentiment': 'negative'},
    })
    
    # Overall insights sentiments for each tab
    insight_sentiments.update({
        "Economic Resilience: Despite fluctuations, Qatar maintains exceptionally high living standards (5.4x global average GDP per capita) while navigating energy transitions.": {'sentiment': 'positive'},
        "Environmental Challenges: Rising CO₂ emissions (8x global average) and limited renewable energy growth present the most significant challenges to Qatar Vision 2030 goals.": {'sentiment': 'negative'},
        "Human Development Progress: Education access is improving substantially, with Qatar's Human Capital Index (0.64) exceeding the global average (0.56), but quality metrics and STEM graduate percentages require attention.": {'sentiment': 'positive'},
        "Infrastructural Achievements: Near-universal sanitation (1.3x global average) and dramatic solar capacity expansion demonstrate Qatar's ability to rapidly develop infrastructure.": {'sentiment': 'positive'},
        
        "The data confirms Qatar's continued heavy reliance on oil and gas, despite diversification efforts under Vision 2030.": {'sentiment': 'negative'},
        "Qatar has demonstrated economic resilience, quickly recovering from the 2020 pandemic-induced downturn.": {'sentiment': 'positive'},
        "While educational reforms show progress, the economic structure remains heavily tilted toward energy production.": {'sentiment': 'neutral'},
        "Qatar is pursuing a careful balance between maximizing short-term revenue from its hydrocarbon resources while investing in long-term diversification.": {'sentiment': 'neutral'},
        "There remains an inherent tension between Qatar's role as a major hydrocarbon producer and its sustainability ambitions under Vision 2030.": {'sentiment': 'negative'},
        "Qatar's GDP per capita (5.4x global average) and per-worker agricultural value (higher than regional peers) demonstrate its economic efficiency.": {'sentiment': 'positive'},
        
        "The data reveals a significant disconnect between Qatar's Vision 2030 environmental sustainability goals and actual progress, particularly in emissions and energy transition.": {'sentiment': 'negative'},
        "While showing impressive progress in solar capacity expansion and agricultural development, Qatar has made limited headway in overall emissions reduction and renewable energy integration.": {'sentiment': 'neutral'},
        "With CO₂ emissions accelerating rather than decreasing, Qatar faces a critical decision point regarding its climate strategy credibility.": {'sentiment': 'negative'},
        "Despite significant investments in renewable capacity (particularly solar), the impact on the overall energy mix remains minimal.": {'sentiment': 'negative'},
        "The data highlights Qatar's complex sustainability challenge in balancing food security, water conservation, and energy transition in a desert environment.": {'sentiment': 'neutral'},
        "Qatar's per capita emissions (8x global average) and fossil-fuel dominated electricity mix (99.7%) contrast with its ambitious Vision 2030 sustainability goals.": {'sentiment': 'negative'},
        
        "The substantial increase in higher education attainment (especially bachelor's degrees) aligns with Qatar's Vision 2030 goal of transitioning to a knowledge-based economy.": {'sentiment': 'positive'},
        "The decreasing learning gap suggests a focus on quality of education, not just increased enrollment numbers.": {'sentiment': 'positive'},
        "Improvements across multiple indicators (educational attainment, expected years of schooling, survival rates) demonstrate Qatar's multifaceted approach to human development.": {'sentiment': 'positive'},
        "The strong performance in gender parity indicates attention to educational equity, though more comprehensive equity measures would be valuable.": {'sentiment': 'positive'},
        "The consistent improvements across indicators reflect sustained investment in Qatar's human capital, a core component of Vision 2030.": {'sentiment': 'positive'},
        "Qatar's human development metrics generally exceed global and regional averages but remain below those of leading countries, indicating both achievement and continued room for growth.": {'sentiment': 'neutral'},
        
        "Qatar shows impressive achievements in basic social infrastructure (sanitation) and gender equity in education, but concerning trends in STEM education and advanced digital skills.": {'sentiment': 'neutral'},
        "The data suggests that Qatar has successfully built social development foundations but faces challenges in developing the innovation capabilities needed for a knowledge economy.": {'sentiment': 'neutral'},
        "The achievement of gender parity in primary education represents a significant milestone in Qatar's social development journey.": {'sentiment': 'positive'},
        "The consistent decline in STEM and ICT graduates represents one of the most significant challenges to Qatar Vision 2030's knowledge economy objectives.": {'sentiment': 'negative'},
        "The data reveals a potential gap between Qatar's educational system outputs and its economic diversification requirements, particularly in technical fields.": {'sentiment': 'negative'},
        "Qatar's sanitation access (1.3x global average) is world-class, while its STEM graduate percentage (0.78x global average) indicates a critical area for improvement.": {'sentiment': 'neutral'},
    })
    
    # Default sentiment is neutral
    for insight in insights:
        if insight in insight_sentiments:
            sentiment = insight_sentiments[insight]['sentiment']
        else:
            sentiment = 'neutral'
            
        # Choose icon based on sentiment
        if sentiment == 'positive':
            icon_class = "fas fa-chart-line me-2"
            icon_color = colors['positive']
        elif sentiment == 'negative':
            icon_class = "fas fa-chart-line-down me-2"  # Note: This isn't a real FontAwesome icon, we'll fix it
            icon_color = colors['negative']
        else:
            icon_class = "fas fa-chart-line me-2"
            icon_color = colors['neutral']
        
        # Fix for negative icon (since fa-chart-line-down doesn't exist)
        if sentiment == 'negative':
            icon_class = "fas fa-arrow-down me-2"
        
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
        
        # Translate the insight if language is Arabic
        translated_insight = get_translation(insight, language)
        
        insight_elements.append(
            html.Div([
                html.I(className=icon_class, style={"color": icon_color}),
                html.Span(translated_insight, style={"color": colors['text']})
            ], className="mb-2")
        )
    
    # Translate the title
    translated_title = get_translation(title, language)
    
    return dbc.Card([
        dbc.CardHeader(html.H5(translated_title, className="mb-0", style={"color": colors['text']}), 
                     style={"borderLeft": f"4px solid {pillar_color}"}),
        dbc.CardBody(insight_elements)
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})

# Helper function to create benchmark comparison cards
def create_benchmark_card(title, benchmark_data, pillar_color, language='english'):
    if not benchmark_data:
        return None
    
    benchmark_items = []
    if 'global_avg' in benchmark_data:
        global_avg_text = f"Global average: {benchmark_data['global_avg']}"
        benchmark_items.append(
            html.Div([
                html.I(className="fas fa-globe me-2", style={"color": colors['global']}),
                html.Span(get_translation(global_avg_text, language),
                         style={"color": colors['text']})
            ], className="mb-2")
        )
    
    if 'regional' in benchmark_data:
        for region, value in benchmark_data['regional'].items():
            regional_text = f"{region}: {value}"
            benchmark_items.append(
                html.Div([
                    html.I(className="fas fa-map-marker-alt me-2", style={"color": colors['regional']}),
                    html.Span(get_translation(regional_text, language), style={"color": colors['text']})
                ], className="mb-2")
            )
    
    if 'leading' in benchmark_data:
        for leader, value in benchmark_data['leading'].items():
            leader_text = f"{leader}: {value}"
            benchmark_items.append(
                html.Div([
                    html.I(className="fas fa-trophy me-2", style={"color": colors['leading']}),
                    html.Span(get_translation(leader_text, language), style={"color": colors['text']})
                ], className="mb-2")
            )
    
    # Translate the title
    translated_title = get_translation(title, language)
    
    return dbc.Card([
        dbc.CardHeader(html.H5(translated_title, className="mb-0", style={"color": colors['text']}), 
                     style={"borderLeft": f"4px solid {pillar_color}"}),
        dbc.CardBody(benchmark_items)
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})

# Define benchmark data from second document
benchmarks = {
    "gdp_per_capita": {
        "global_avg": 22450,
        "regional": {"UAE": 83900, "Saudi Arabia": 54992},
        "leading": {"Luxembourg": 140000, "Singapore": 140000}
    },
    "human_capital_index": {
        "global_avg": 0.56,
        "regional": {"Saudi Arabia": 0.58, "Middle East Avg": 0.55},
        "leading": {"Singapore": 0.88, "Japan": 0.80}
    },
    "co2_per_capita": {
        "global_avg": 4.8,
        "regional": {"Kuwait": 25, "UAE": 20, "Saudi Arabia": 18},
        "leading": {"EU Average": 6.5}
    },
    "renewables_share": {
        "global_avg": 29,
        "regional": {"Middle East Avg": 4},
        "leading": {"Brazil": 85, "Norway": 90}
    },
    "stem_graduates": {
        "global_avg": 23,
        "regional": {"Saudi Arabia": 32},
        "leading": {"Oman": 43, "Germany": 37}
    },
    "sanitation": {
        "global_avg": 75,
        "regional": {"GCC Avg": 98},
        "leading": {"North America/Europe": 99}
    },
    "education_years": {
        "expected": {"global_avg": 12, "leading": 15},
        "learning_adjusted": {"global_avg": 7.8, "leading": 11}
    },
    "energy_production": {
        "lng_target": "85% increase by 2030 (126-142M tons)",
        "global_share": "Target 25% of global LNG trade"
    },
    "tertiary_enrollment": {
        "global_avg": 40,
        "qatar_growth": "From ~20% to >40% recently"
    },
    "agriculture_value": {
        "qatar": "10-11K per worker",
        "regional": {"Oman": "~6K per worker"},
        "leading": {"Advanced economies": ">50K per worker"}
    }
}

# Main layout with improved styling and structure and language support
app.layout = html.Div([
    # Store the current language
    dcc.Store(id='language-store', data='english'),
    
    # Header with language toggle
    dbc.Container([
        dbc.Row([
            dbc.Col([
                # Language toggle button in the upper right
                dbc.ButtonGroup(
                    [
                        dbc.Button("English", id="btn-english", color="primary"),
                        dbc.Button("العربية", id="btn-arabic", color="outline-primary"),
                    ],
                    className="mb-3"
                ),
            ], width=12, className="d-flex justify-content-end"),
        ]),
        dbc.Row([
            dbc.Col(html.Img(src='assets/qatar_vision_2030_logo.png', height='100px'), width=2, className="d-flex align-items-center"),
            dbc.Col([
                html.H1("Qatar Vision 2030 Dashboard", id="dashboard-title", className="mb-0", 
                       style={"color": colors['text'], "fontWeight": "bold"}),
                html.P("Monitoring Progress Across Economic, Environmental, Human, and Social Development Pillars", 
                      id="dashboard-subtitle", className="lead mb-0")
            ], width=10)
        ], className="py-4 border-bottom mb-4")
    ], fluid=True, style={"backgroundColor": colors['card']}),
    
    # Year slider
    dbc.Card(
        dbc.CardBody([
            html.H5("Select Year Range", id="year-range-title", className="card-title", style={"color": colors['text']}),
            dcc.RangeSlider(
                id='year-slider',
                min=min(key_indicators_df['Year']),
                max=max(key_indicators_df['Year']),
                step=1,
                marks={int(year): {"label": str(year), "style": {"transform": "rotate(45deg)", "color": colors['text']}} 
                       for year in key_indicators_df['Year'].unique()},
                value=[min(key_indicators_df['Year']), max(key_indicators_df['Year'])],
                className="mt-3"
            )
        ]), className="mb-4 shadow-sm", style={"backgroundColor": colors['card']}
    ),
    
    # Tabs
    dbc.Tabs([
        dbc.Tab(label="Key Indicators", tab_id="key-indicators", id="tab-key-indicators",
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label="Economic Development", tab_id="economic", id="tab-economic",
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label="Environmental Development", tab_id="environmental", id="tab-environmental",
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label="Human Development", tab_id="human", id="tab-human",
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
        dbc.Tab(label="Social Development", tab_id="social", id="tab-social",
               label_style={"fontWeight": "bold", "fontSize": "1.1rem"}),
    ], id="tabs", active_tab="key-indicators", className="mb-4"),
    
    # Tab content
    html.Div(id="tab-content", className="mt-4")
])

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

# update the button colors when the language changes
@app.callback(
    [Output('btn-english', 'color'),
     Output('btn-arabic', 'color')],
    [Input('language-store', 'data')]
)
def update_button_colors(language):
    if language == 'english':
        return "primary", "outline-primary"
    else:  # arabic
        return "outline-primary", "primary"

# Callback to update the main content based on language
@app.callback(
    Output('main-content', 'children'),
    [Input('language-store', 'data')]
)
def update_layout(language):
    # Apply RTL direction for Arabic
    direction = "rtl" if language == "arabic" else "ltr"
    
    return html.Div([
        # Header with language toggle
        create_header(language),
        
        # Main content with dynamic language and direction
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    create_year_slider(language),
                    create_tabs(language),
                    html.Div(id="tab-content", className="mt-4")
                ], width=12)
            ])
        ], fluid=True, style={"backgroundColor": colors['bg'], "minHeight": "100vh", "padding": "20px", "direction": direction})
    ])

# Callback to update the content based on active tab and language
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("year-slider", "value"),
     Input('language-store', 'data')]
)
def render_tab_content(active_tab, year_range, language):
    min_year, max_year = year_range
    
    if active_tab == "key-indicators":
        return render_key_indicators(min_year, max_year, language)
    elif active_tab == "economic":
        return render_economic(min_year, max_year, language)
    elif active_tab == "environmental":
        return render_environmental(min_year, max_year, language)
    elif active_tab == "human":
        return render_human(min_year, max_year, language)
    elif active_tab == "social":
        return render_social(min_year, max_year, language)
    
    return html.P(get_translation("This tab has no content.", language))

# Function to render Key Indicators tab with insights from PDF
def render_key_indicators(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = key_indicators_df[(key_indicators_df['Year'] >= min_year) & (key_indicators_df['Year'] <= max_year)]
    
    # Create GDP per capita chart with improved styling and benchmark comparisons
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
    max_year_data = int(filtered_df['Year'].max())
    gdp_fig.add_hline(y=benchmarks["gdp_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                     annotation_text=get_translation(f"Global Average: ${benchmarks['gdp_per_capita']['global_avg']:,}", language), 
                     annotation_position="bottom right")
    
    for region, value in benchmarks["gdp_per_capita"]["regional"].items():
        gdp_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                         annotation_text=get_translation(f"{region}: ${value:,}", language), 
                         annotation_position="bottom right")
    
    gdp_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Create Human Capital Index chart with improved styling and connected lines
    # Drop NaN values before creating chart
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
    
    hci_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    # Connect gaps between points for better trend visualization
    hci_fig.update_traces(connectgaps=True)
    
    # Create CO2 Emissions per capita chart with improved styling and better legend positioning
    co2_fig = px.line(
        filtered_df, 
        x='Year', 
        y='Annual CO₂ emissions (per capita)',
        title=get_translation('CO₂ Emissions per Capita', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
         labels={"Annual CO₂ emissions (per capita)":get_translation("Annual CO₂ emissions (per capita)", language), "variable": ""}
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
    
    co2_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),  # Increased top margin
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,  # Moved legend position up
            xanchor="center", 
            x=0.5   # Centered legend
        )
    )
    
    # Create Renewable Electricity chart with improved styling
    renewable_fig = px.line(
        filtered_df, 
        x='Year', 
        y='Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)',
        title=get_translation('Electricity from Renewables (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['key']],
         labels={"Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)":get_translation("Electricity from renewables - TWh", language), "variable": ""}
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
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    renewable_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Create Energy Production chart (Oil & Gas) with improved styling and better legend placement
    energy_fig = px.line(
        filtered_df, 
        x='Year', 
        y=['Oil production (TWh)','Gas production - TWh'],
        title=get_translation('Energy Production: Oil & Gas (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['key'], '#17becf'],
         labels={"value":get_translation("Oil production (TWh), Gas production - TWh", language), "variable": ""}
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
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    energy_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),  # Increased top margin
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,  # Moved legend position up
            xanchor="center", 
            x=0.5,   # Centered legend
            bgcolor='rgba(255,255,255,0.8)'  # Semi-transparent background
        )
    )
    # Ensure lines connect across missing data
    energy_fig.update_traces(connectgaps=True)
    
    # Create Education metrics chart with improved styling and better legend placement
    education_fig = px.line(
        filtered_df,
        x='Year',
        y=['Expected Years of School', 'Learning-Adjusted Years of School', 'School enrollment, tertiary (% gross)'],
        title=get_translation('Education Metrics', language),
        markers=True,
        color_discrete_sequence=[colors['key'], '#17becf', '#ff7f0e'],
         labels={"value":get_translation('Expected Years of School, Learning-Adjusted and enrollment', language), "variable": ""}
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
    
    education_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),  # Increased top margin
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.05,  # Moved legend position up
            xanchor="center", 
            x=0.5,   # Centered legend
            bgcolor='rgba(255,255,255,0.8)'  # Semi-transparent background
        )
    )
    # Ensure lines connect across missing data
    education_fig.update_traces(connectgaps=True)
    
    # Create STEM graduates percentage chart with improved styling
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
    
    stem_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Create cards for latest values with improved styling
    latest_year = filtered_df['Year'].max()
    latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
    
    # Safely extract values with fallbacks to handle NaN
    try:
        gdp_value = f"${latest_data['GDP per capita, PPP (constant 2021 international $)']:,.0f}"
        gdp_global_compare = get_translation(f"{latest_data['GDP per capita, PPP (constant 2021 international $)'] / benchmarks['gdp_per_capita']['global_avg']:.1f}x global average", language)
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
            hci_global_compare = get_translation(f"{latest_hci / benchmarks['human_capital_index']['global_avg']:.1f}x global average", language)
        else:
            hci_value = get_translation("Data unavailable", language)
            hci_global_compare = ""
    except (ValueError, KeyError, TypeError, IndexError):
        hci_value = get_translation("Data unavailable", language)
        hci_global_compare = ""
        
    try:
        co2_value = f"{latest_data['Annual CO₂ emissions (per capita)']:.1f} {get_translation("tonnes",language)}"
        co2_global_compare = get_translation(f"{latest_data['Annual CO₂ emissions (per capita)'] / benchmarks['co2_per_capita']['global_avg']:.1f}x global average", language)
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
            sanit_global_compare = get_translation(f"{latest_sanit / benchmarks['sanitation']['global_avg']:.1f}x global average", language)
        else:
            sanit_value = get_translation("Data unavailable", language)
            sanit_global_compare = ""
    except (ValueError, KeyError, TypeError, IndexError):
        sanit_value = get_translation("Data unavailable", language)
        sanit_global_compare = ""
    
    # Create more attractive key metric cards with icons and comparisons - with translations
    key_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("GDP per Capita (PPP)", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(155, 89, 182, 0.1)", "borderLeft": f"4px solid {colors['key']}"}),
            dbc.CardBody([
                html.I(className="fas fa-money-bill-wave fa-2x mb-2", style={"color": colors['key']}),
                html.H3(gdp_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(gdp_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Human Capital Index", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(155, 89, 182, 0.1)", "borderLeft": f"4px solid {colors['key']}"}),
            dbc.CardBody([
                html.I(className="fas fa-user-graduate fa-2x mb-2", style={"color": colors['key']}),
                html.H3(hci_value, className="mb-0"),
                html.P(get_translation("Scale: 0-1", language), className="text-muted"),
                html.P(hci_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("CO₂ Emissions per Capita", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(155, 89, 182, 0.1)", "borderLeft": f"4px solid {colors['key']}"}),
            dbc.CardBody([
                html.I(className="fas fa-smog fa-2x mb-2", style={"color": colors['key']}),
                html.H3(co2_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(co2_global_compare, className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Sanitation Access", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(155, 89, 182, 0.1)", "borderLeft": f"4px solid {colors['key']}"}),
            dbc.CardBody([
                html.I(className="fas fa-hands-wash fa-2x mb-2", style={"color": colors['key']}),
                html.H3(sanit_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(sanit_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
    ], className="mb-4 g-3")
    
    # Key Insights from the PDF with added benchmark comparisons
    gdp_insights = [
        "Qatar maintained one of the world's highest GDP per capita levels throughout the period (over $100,000), but experienced a slight overall decline of 3.24% from 2016 to 2023.",
        "A significant drop occurred in 2020 (down to $103,061), representing a 14.2% decrease from 2016 levels, clearly showing the pandemic's impact.",
        "The economy rebounded strongly in 2021 to $116,832, nearly returning to pre-pandemic levels, demonstrating economic resilience.",
        "Qatar's GDP per capita is approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992)."
    ]
    
    hci_insights = [
        "The HCI data is only available for 2017, 2018, and 2020, which limits comprehensive trend analysis.",
        "There was a steady improvement in HCI from 0.615 in 2017 to 0.638 in 2020, representing a 3.7% increase.",
        "A score of 0.638 means that a child born in Qatar today will be 63.8% as productive as they could be with complete education and full health.",
        "Qatar's HCI (0.64) is above the global average (0.56) and Middle East average, but remains below leading countries like Singapore (0.88) and Japan (0.80)."
    ]
    
    co2_insights = [
        "CO₂ emissions per capita increased by 15.54% from 2016 to 2023, reaching 38.84 tonnes per person in 2023.",
        "Emissions showed significant year-to-year variability, suggesting changing energy usage patterns.",
        "The upward trend contradicts Qatar's environmental sustainability goals and presents a major challenge for Vision 2030's environmental pillar.",
        "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes)."
    ]
    
    renewable_insights = [
        "Renewable electricity production increased slightly from 0.13 TWh in 2016 to 0.15 TWh in 2023 (15.38% increase).",
        "After increasing to 0.15 TWh in 2018, renewable electricity production has plateaued without further growth through 2023.",
        "Given Qatar's climate, there's significant untapped potential for solar energy expansion.",
        "Qatar targets 20% of electricity from renewables by 2030, which would exceed the current Middle East average (4%) but remain below the global average (29%) and far behind leading countries like Brazil and Norway (80-95%)."
    ]
    
    # New insights for energy production chart that was missing dedicated insights
    energy_production_insights = [
        "Qatar's energy production is dominated by natural gas, with a significant focus on LNG exports where Qatar is a global leader.",
        "Oil production experienced a decline from 582.57 TWh in 2016 to 511.54 TWh in 2020 (-12.2%), before rebounding to 616.21 TWh in 2023.",
        "Gas production has been more stable, reflecting Qatar's strategic emphasis on its vast North Field gas reserves.",
        "Qatar plans to boost LNG output by 85% from current 77 million tons to 126-142 million tons by 2030, aiming to reclaim its position as the world's top LNG exporter.",
        "This expansion will cement Qatar's position in global energy markets, targeting approximately 25% of global LNG trade by 2030."
    ]
    
    # New insights for education metrics chart that was missing dedicated insights
    education_metrics_insights = [
        "Qatar has shown steady improvement in expected years of schooling, increasing from 12.46 years in 2016 to 13.26 years in 2020 (6.4% growth).",
        "The Learning-Adjusted Years of School metric improved from 12.31 years in 2017 to 12.83 years in 2020, indicating enhanced education quality.",
        "The gap between expected and learning-adjusted years decreased from 0.69 to 0.43 years, showing a reduction in learning loss from 5.31% to 3.24%.",
        "Qatar's tertiary enrollment has grown substantially, from approximately 20% in the mid-2010s to over 40% recently, approaching the global average.",
        "Qatar's education metrics now exceed global averages (12 expected years globally vs. 13.26 in Qatar; 7.8 learning-adjusted years globally vs. 12.83 in Qatar)."
    ]
    
    # New insights for STEM graduates chart that was missing dedicated insights
    stem_graduates_insights = [
        "The percentage of graduates from STEM programs has declined dramatically from 29.70% in 2016 to 17.83% in 2022, representing a 39.96% decrease.",
        "This consistent downward trend in STEM graduates contradicts Qatar's Vision 2030 goal of building a knowledge-based economy and innovation ecosystem.",
        "At 17.83%, Qatar's STEM graduate percentage has fallen below the global average (23%) and significantly trails regional competitor Saudi Arabia (32%).",
        "Leading countries in STEM education, such as Oman (43%) and Germany (37%), far outpace Qatar's current performance in this critical metric.",
        "The decline in STEM graduates represents a major challenge for Qatar's economic diversification goals and may hinder the country's competitiveness in high-tech sectors."
    ]
    
    # Overall dashboard insights from the PDF with added benchmark context
    overall_insights = [
        "Economic Resilience: Despite fluctuations, Qatar maintains exceptionally high living standards (5.4x global average GDP per capita) while navigating energy transitions.",
        "Environmental Challenges: Rising CO₂ emissions (8x global average) and limited renewable energy growth present the most significant challenges to Qatar Vision 2030 goals.",
        "Human Development Progress: Education access is improving substantially, with Qatar's Human Capital Index (0.64) exceeding the global average (0.56), but quality metrics and STEM graduate percentages require attention.",
        "Infrastructural Achievements: Near-universal sanitation (1.3x global average) and dramatic solar capacity expansion demonstrate Qatar's ability to rapidly develop infrastructure."
    ]
    
    # Add connectgaps=True to all figures to ensure lines connect even with missing data points
    gdp_fig.update_traces(connectgaps=True)
    hci_fig.update_traces(connectgaps=True)
    co2_fig.update_traces(connectgaps=True)
    renewable_fig.update_traces(connectgaps=True)
    energy_fig.update_traces(connectgaps=True)
    education_fig.update_traces(connectgaps=True)
    stem_fig.update_traces(connectgaps=True)
    
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
        dbc.CardHeader(html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0"), 
                      style={"borderLeft": f"4px solid {colors['highlight']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-2"),
        ])
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})
    
    # Create layout with paired insights and charts
    layout = html.Div([
        key_cards,
        html.H4(get_translation("Key Indicators Analysis", language), className="mt-5 mb-4 text-center", style={"color": colors['text']}),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # GDP insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("GDP per Capita", gdp_insights, colors['key'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=gdp_fig),
                gdp_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # HCI insights and chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=hci_fig),
                hci_benchmark_card
            ], width=6, className="mb-4"),
            dbc.Col(create_insight_card("Human Capital Index", hci_insights, colors['key'], language), width=6, className="mb-4"),
        ]),
        
        # CO2 insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("CO₂ Emissions", co2_insights, colors['key'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=co2_fig),
                co2_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Renewable insights and chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=renewable_fig),
                renewables_benchmark_card
            ], width=6, className="mb-4"),
            dbc.Col(create_insight_card("Renewable Energy", renewable_insights, colors['key'], language), width=6, className="mb-4"),
        ]),
        
        # Energy production chart with added insights
        dbc.Row([
            dbc.Col(create_insight_card("Energy Production", energy_production_insights, colors['key'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=energy_fig),
            ], width=6, className="mb-4"),
        ]),
        
        # Education metrics chart with added insights
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=education_fig),
            ], width=6, className="mb-4"),
            dbc.Col(create_insight_card("Education Metrics", education_metrics_insights, colors['key'], language), width=6, className="mb-4"),
        ]),
        
        # STEM graduates chart with added insights
        dbc.Row([
            dbc.Col(create_insight_card("STEM Graduates", stem_graduates_insights, colors['key'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=stem_fig),
                stem_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Overall insights
        overall_insights_card,
    ])
    
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
         labels={"value":get_translation("GDP per capita, PPP (2021 international $)", language), "variable": ""}
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
    
    gdp_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Energy Production chart with improved styling and translations
    energy_production_fig = px.line(
        filtered_df,
        x='Year',
        y=['Oil production (TWh)', 'Gas production - TWh'],
        title=get_translation('Energy Production (TWh)', language),
        markers=True,
        color_discrete_sequence=[colors['economic'], '#17becf'],
         labels={"value":get_translation("Oil production and Gas production - TWh", language), "variable": ""}
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
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    energy_production_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    

    
    # Add coal consumption as a separate trace with secondary y-axis for better visibility
    coal_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add primary energy traces
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Primary energy consumption - TWh'],
            name=get_translation("Primary Energy", language),
            line=dict(color=colors['economic']),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Oil consumption - TWh'],
            name=get_translation("Oil Consumption", language),
            line=dict(color='#17becf'),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Gas consumption - TWh'],
            name=get_translation("Gas Consumption", language),
            line=dict(color='#ff7f0e'),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    # Add coal consumption on secondary y-axis
    coal_fig.add_trace(
        go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Coal consumption - TWh'],
            name=get_translation("Coal Consumption", language),
            line=dict(color='#d62728', dash='dot'),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    # Update layout with translations
    coal_fig.update_layout(
        title_text=get_translation("Energy Consumption", language),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    coal_fig.update_xaxes(title_text=get_translation("Year", language))
    coal_fig.update_yaxes(title_text=get_translation("Energy Consumption (TWh)", language), secondary_y=False)
    coal_fig.update_yaxes(title_text=get_translation("Coal Consumption (TWh)", language), secondary_y=True)
    
    # Connect gaps between points for better trend visualization
    coal_fig.update_traces(connectgaps=True)
    
    # Create Energy Growth chart with improved styling and translations
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
    
    # Add annotation with global comparison and translation
    energy_growth_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df[['Oil (% growth)', 'Gas (% growth)', 'Coal (% growth)']].max().max(),
        text=get_translation("Global energy demand growth: ~1-2% per year<br>Qatar targets: 2-3% growth by 2030<br>Past Qatar growth: ~6-7% annually", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    energy_growth_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Agriculture Value chart with improved styling and translations
    agriculture_fig = px.line(
        filtered_df,
        x='Year',
        y='Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)',
        title=get_translation('Agriculture, Forestry, and Fishing Value Added per Worker', language),
        markers=True,
        color_discrete_sequence=[colors['economic']],
         labels={"Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)":get_translation("Agriculture, forestry, and fishing, value per worker 2015 US$", language), "variable": ""}
    )

    if language == 'arabic':
        agriculture_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    agriculture_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Agriculture, forestry, and fishing, value added per worker (constant 2015 US$)'].max(),
        text=get_translation("Qatar's per-worker ag value: $10-11K<br>Regional peer (Oman): ~$6K<br>Advanced economies: >$50K", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    agriculture_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Create Business Graduates chart with improved styling and translations
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
    
    # Add annotations for business graduate percentage with translation
    business_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Percentage of graduates from tertiary education graduating from Business, Administration and Law programmes, (%)'].mean(),
        text=get_translation("Qatar 2018: ~26% business/law graduates<br>Regional comparison (Bahrain): ~50%<br>Vision 2030 aims to balance with STEM fields", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    business_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        yaxis_title=get_translation("Business & Law Graduates (%)", language)
    )
    
    # Extract latest values for KPI cards
    try:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
        
        gdp_value = f"${latest_data['GDP per capita, PPP (constant 2021 international $)']:,.0f}"
        gdp_global_compare = get_translation(f"{latest_data['GDP per capita, PPP (constant 2021 international $)'] / benchmarks['gdp_per_capita']['global_avg']:.1f}x global average", language)
        oil_prod = f"{latest_data['Oil production (TWh)']:,.1f} TWh"
        gas_prod = f"{latest_data['Gas production - TWh']:,.1f} TWh"
        energy_cons = f"{latest_data['Primary energy consumption - TWh']:,.1f} TWh"
    except:
        gdp_value = get_translation("N/A", language)
        gdp_global_compare = ""
        oil_prod = get_translation("N/A", language)
        gas_prod = get_translation("N/A", language)
        energy_cons = get_translation("N/A", language)
    
    # Key Insights from the PDF for Economic Development with added benchmark comparisons
    gdp_insights = [
        "Qatar's GDP per capita has shown notable volatility between 2016-2023, with a 3.24% overall decline.",
        "The most significant drop occurred in 2020 (to $103,062), representing a 14% decline from 2016 levels.",
        "The economy showed strong resilience with a rapid recovery to $116,833 in 2021.",
        "The stabilization around $115,000 in recent years suggests a 'new normal' that balances energy market realities with economic diversification efforts.",
        "Qatar's GDP per capita remains approximately 5.4x the global average ($22,450) and significantly higher than regional neighbors (UAE: $83,900, Saudi Arabia: $54,992)."
    ]
    
    oil_insights = [
        "Oil production declined from 582.57 TWh in 2016 to a low of 511.54 TWh in 2020 (-12.2%), but has since recovered to 616.21 TWh in 2023.",
        "The initial reduction reflects Qatar's strategic decision to focus more on natural gas, where it holds comparative advantage.",
        "The 20.5% increase from 2020 to 2023 shows Qatar's response to higher global energy demand and prices after the pandemic.",
        "The upward trend in recent years raises questions about alignment with climate commitments and sustainability goals.",
        "Qatar's oil output (~0.67 million barrels/day) is modest compared to other GCC producers, reflecting its strategic focus on natural gas production."
    ]
    
    gas_insights = [
        "Qatar has been investing heavily in liquefied natural gas (LNG) infrastructure, aiming to increase production capacity from 77 to 126 million tons annually by 2027.",
        "The focus on gas aligns with Qatar's positioning of natural gas as a 'transition fuel' with lower carbon emissions than oil or coal.",
        "Sustained gas production provides Qatar with economic stability as global demand for cleaner burning fuels increases.",
        "The vast majority of Qatar's gas production is destined for export markets, making it a critical component of the country's revenue stream.",
        "Qatar aims to maintain its position as one of the world's largest LNG exporters, competing with the U.S. which surpassed Qatar as the top LNG exporter in 2023."
    ]
    
    energy_consumption_insights = [
        "Energy consumption fluctuated significantly, from 168.92 TWh in 2016 to a low of 126.88 TWh in 2020 (-24.9%), before rebounding to 170.21 TWh in 2023.",
        "The consumption pattern closely mirrors GDP trends, with the 2020 pandemic-related drop and subsequent recovery.",
        "The data suggests limited progress in improving energy efficiency, as consumption has grown in line with economic recovery.",
        "Qatar has one of the world's highest per capita energy consumption rates, reflecting its energy-intensive industries and high standard of living.",
        "Global energy demand typically grows at 1-2% annually, while Qatar experienced 6-7% annual growth in the 2010s, though it targets moderating to 2-3% by the late 2020s."
    ]
    
    # New insights for Energy Growth Rates chart that was missing dedicated insights
    energy_growth_insights = [
        "Qatar's energy growth rates show significant volatility, reflecting both global energy market fluctuations and domestic economic changes.",
        "Growth rates were particularly negative during the 2020 pandemic period, with sharp contractions across all energy sources.",
        "Post-pandemic recovery shows positive growth rates, particularly in oil consumption, which may contradict Vision 2030's sustainability goals.",
        "Qatar's historical energy demand growth of 6-7% annually significantly exceeds the global average (1-2%), highlighting the challenge of energy-intensive development.",
        "Vision 2030 and the National Environment and Climate Strategy aim to reduce these high growth rates to a more sustainable 2-3% annually by 2030, still higher than typical OECD countries that have achieved near-zero growth through efficiency measures."
    ]
    
    # New insights for Agriculture Value chart that was missing dedicated insights
    agriculture_insights = [
        "Despite Qatar's challenging desert environment, agricultural productivity per worker is relatively high at $10,000-$11,000 (2015 US$) in value-added terms.",
        "Qatar's agricultural productivity exceeds regional peers like Oman (~$6,000) but remains well below advanced economies (>$50,000 per worker).",
        "The high per-worker value reflects Qatar's capital-intensive agricultural approach, utilizing advanced technologies like hydroponics and climate-controlled greenhouses.",
        "Following the 2017 blockade, Qatar has heavily invested in agricultural self-sufficiency, with arable land increasing by 14.75% (18,300 to 21,000 hectares).",
        "By 2030, Qatar aims to further improve agricultural efficiency through high-yield technology to enhance food security, even as the sector remains <1% of GDP."
    ]
    
    # New insights for Business Graduates chart that was missing dedicated insights
    business_graduates_insights = [
        "Business, administration, and law have historically been popular fields of study in Qatar, with approximately 26% of tertiary graduates specializing in these areas in 2018.",
        "This proportion is lower than in some other service-driven Gulf economies, such as Bahrain, where nearly 50% of graduates focus on business and law.",
        "Vision 2030 doesn't discourage these fields but seeks a better balance with STEM subjects to support innovation and knowledge economy development.",
        "The inverse relationship between business/law and STEM graduates represents a challenge for Qatar's diversification - as one increases, the other tends to decrease.",
        "Qatar aims to keep business/law graduates around or below one-third of total graduates while boosting STEM and technical fields to better align with labor market needs in a diversifying economy."
    ]
    
    overall_economic_insights = [
        "The data confirms Qatar's continued heavy reliance on oil and gas, despite diversification efforts under Vision 2030.",
        "Qatar has demonstrated economic resilience, quickly recovering from the 2020 pandemic-induced downturn.",
        "While educational reforms show progress, the economic structure remains heavily tilted toward energy production.",
        "Qatar is pursuing a careful balance between maximizing short-term revenue from its hydrocarbon resources while investing in long-term diversification.",
        "There remains an inherent tension between Qatar's role as a major hydrocarbon producer and its sustainability ambitions under Vision 2030.",
        "Qatar's GDP per capita (5.4x global average) and per-worker agricultural value (higher than regional peers) demonstrate its economic efficiency."
    ]
    
    # Create KPI cards for economic section with benchmark comparisons and translations
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("GDP per Capita (PPP)", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "borderLeft": f"4px solid {colors['economic']}"}),
            dbc.CardBody([
                html.I(className="fas fa-money-bill-wave fa-2x mb-2", style={"color": colors['economic']}),
                html.H3(gdp_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(gdp_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Oil Production", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "borderLeft": f"4px solid {colors['economic']}"}),
            dbc.CardBody([
                html.I(className="fas fa-oil-can fa-2x mb-2", style={"color": colors['economic']}),
                html.H3(oil_prod, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("0.67M barrels/day (modest for GCC)", language), className="small text-muted mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Gas Production", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "borderLeft": f"4px solid {colors['economic']}"}),
            dbc.CardBody([
                html.I(className="fas fa-burn fa-2x mb-2", style={"color": colors['economic']}),
                html.H3(gas_prod, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("177 billion m³ (globally significant)", language), className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Energy Consumption", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "borderLeft": f"4px solid {colors['economic']}"}),
            dbc.CardBody([
                html.I(className="fas fa-bolt fa-2x mb-2", style={"color": colors['economic']}),
                html.H3(energy_cons, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("Among GCC's highest per capita", language), className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
    ], className="mb-4 g-3")
    
    # Create benchmark comparison cards with translations
    gdp_benchmark_card = create_benchmark_card("GDP per Capita (PPP) Benchmarks", benchmarks["gdp_per_capita"], colors['economic'], language)
    agriculture_benchmark_card = create_benchmark_card("Agricultural Productivity", benchmarks["agriculture_value"], colors['economic'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader(html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0"), 
                      style={"borderLeft": f"4px solid {colors['highlight']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-2"),
        ])
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Economic Development Insights", overall_economic_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        
        html.H4(get_translation("Economic Development Analysis", language), className="mt-5 mb-4 text-center", style={"color": colors['text']}),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # GDP insights and chart
        dbc.Row([
            dbc.Col(create_insight_card("GDP per Capita Trends", gdp_insights, colors['economic'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=gdp_fig),
                gdp_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Oil production insights and chart
        dbc.Row([
            dbc.Col(dcc.Graph(figure=energy_production_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Energy Production", oil_insights, colors['economic'], language), width=6, className="mb-4"),
        ]),
        
        # Energy consumption chart and insights
        dbc.Row([
            dbc.Col(create_insight_card("Energy Consumption", energy_consumption_insights, colors['economic'], language), width=6, className="mb-4"),
            dbc.Col(dcc.Graph(figure=coal_fig), width=6, className="mb-4"),
        ]),
        
        # Energy growth chart and insights (newly added)
        dbc.Row([
            dbc.Col(dcc.Graph(figure=energy_growth_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Energy Growth Rates", energy_growth_insights, colors['economic'], language), width=6, className="mb-4"),
        ]),
        
        # Agriculture and business charts with insights (newly added)
        dbc.Row([
            dbc.Col(create_insight_card("Agricultural Productivity", agriculture_insights, colors['economic'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=agriculture_fig),
                agriculture_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col(dcc.Graph(figure=business_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Business, Administration and Law Graduates", business_graduates_insights, colors['economic'], language), width=6, className="mb-4"),
        ]),
        
        # Overall insights
        overall_insights_card,
    ])
    
    return layout

    # Function to render Environmental Development tab with insights from PDF
def render_environmental(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = environmental_df[(environmental_df['Year'] >= min_year) & (environmental_df['Year'] <= max_year)]
    
    # Create CO2 Emissions charts with improved styling and translations
    co2_fig = px.line(
        filtered_df,
        x='Year',
        y=['Annual CO₂ emissions', 'Annual CO₂ emissions from oil'],
        title=get_translation('Annual CO₂ Emissions (tonnes)', language),
        markers=True,
        color_discrete_sequence=[colors['environmental'], '#17becf'],
         labels={"value":get_translation("Annual CO₂ emissions and Annual CO₂ emissions from oil", language), "variable": ""}
    )

    if language == 'arabic':
        co2_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    co2_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Annual CO₂ emissions'].max(),
        text=get_translation("Qatar 2023: ~128M tonnes CO₂<br>Global total: 36.8B tonnes<br>Saudi Arabia: ~600M tonnes<br>UAE: ~230M tonnes", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    co2_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create CO2 Emissions per capita chart with improved styling and legend positioning
    co2_per_capita_fig = px.line(
    filtered_df,
    x='Year',
    y=['Annual CO₂ emissions (per capita)', 'Annual CO₂ emissions from oil (per capita)'],  # Original column names
    title=get_translation('Annual CO₂ Emissions per Capita', language),
    markers=True,
    color_discrete_sequence=[colors['environmental'], '#17becf'],
     labels={"value":get_translation("Annual CO₂ emissions and CO₂ emissions from oil per capita",language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        co2_per_capita_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))



    # Add benchmark lines for CO2 per capita with translations
    co2_per_capita_fig.add_hline(y=benchmarks["co2_per_capita"]["global_avg"], line_dash="dash", line_color=colors['global'],
                               annotation_text=get_translation(f"Global Average: {benchmarks['co2_per_capita']['global_avg']} tonnes", language), 
                               annotation_position="top right")
    
    for region, value in benchmarks["co2_per_capita"]["regional"].items():
        co2_per_capita_fig.add_hline(y=value, line_dash="dot", line_color=colors['regional'],
                                   annotation_text=get_translation(f"{region}: {value} tonnes", language), 
                                   annotation_position="bottom right")
    
    co2_per_capita_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),  # Increased top margin
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=0.95,  # Moved legend position up
            xanchor="center", 
            x=0.5,   # Centered legend
            bgcolor='rgba(255,255,255,0.8)'  # Semi-transparent background
        )
    )
    # Ensure lines connect across missing data
    co2_per_capita_fig.update_traces(connectgaps=True)
    
    # Create Energy Change chart with improved styling and translations
    energy_change_fig = px.bar(
    filtered_df,
    x='Year',
    y=['Annual change in primary energy consumption (%)'],  # Original column name
    title=get_translation('Annual Change in Primary Energy Consumption (%)', language),
    color_discrete_sequence=[colors['environmental']],
     labels={"value":get_translation("Annual change in primary energy consumption (%)", language), "variable": ""}
    )

# Translate trace names for Arabic
    if language == 'arabic':
        energy_change_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    energy_change_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Annual change in primary energy consumption (%)'].max(),
        text=get_translation("Global energy demand growth: ~1.9% (2022)<br>Qatar's historical growth: ~5-6% in 2010s<br>Qatar's 2030 target: <3% annually", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    energy_change_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Create Electricity Production chart with cleaner labels and log scale
    # First, create a copy of the dataframe with shorter column names
    elec_df = filtered_df.copy()
    elec_df['Fossil Fuels (TWh)'] = elec_df['Electricity from fossil fuels - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']
    elec_df['Nuclear (TWh)'] = elec_df['Electricity from nuclear - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']
    elec_df['Renewables (TWh)'] = elec_df['Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']

    electricity_fig = px.area(
        elec_df,
        x='Year',
        y=['Fossil Fuels (TWh)', 'Nuclear (TWh)', 'Renewables (TWh)'],  # Use actual column names
        title=get_translation('Electricity Production by Source (TWh)', language),
        color_discrete_sequence=['#636EFA', '#EF553B', colors['environmental']],
         labels={"Electricity Production (TWh) - Log Scale": "", "variable": ""}
    )

# Translate trace names for Arabic
    if language == 'arabic':
        electricity_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    electricity_fig.add_annotation(
        x=elec_df['Year'].median(),
        y=elec_df['Fossil Fuels (TWh)'].max(),
        text=get_translation("Qatar 2023: >99% fossil fuels<br>Global mix: 61% non-renewables<br>Qatar's 2030 target: 20% renewables", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    # Use log scale to better see smaller values like renewables
    electricity_fig.update_layout(
        yaxis_title=get_translation("Electricity Production (TWh)", language),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Renewable Electricity detail chart with cleaner labels
    renew_df = filtered_df.copy()
    renew_df['Solar (TWh)'] = renew_df['Electricity from solar - TWh (adapted for visualization of chart electricity-prod-source-stacked)']
    renew_df['Bioenergy (TWh)'] = renew_df['Electricity from bioenergy - TWh (adapted for visualization of chart electricity-prod-source-stacked)']

    renewable_detail_fig = px.area(
        renew_df,
        x='Year',
        y=['Solar (TWh)', 'Bioenergy (TWh)'],  # Use actual column names
        title=get_translation('Renewable Electricity Production Detail (TWh)', language),
        color_discrete_sequence=[colors['environmental'], '#17becf'],
         labels={"value":get_translation("Solar, Bioenergy (TWh)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        renewable_detail_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))

    # Add this after each plot creation if language is arabic
    if language == 'arabic':
        renewable_detail_fig.for_each_trace(lambda t: t.update(
        name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    renewable_detail_fig.add_annotation(
        x=renew_df['Year'].median(),
        y=renew_df['Solar (TWh)'].max() * 1.5,
        text=get_translation("Qatar renewable output: ~0.15 TWh<br>Global renewables: 7,858 TWh (2021)<br>Middle East renewables: 47 TWh (2022)", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    renewable_detail_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Solar capacity and growth chart
    solar_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    solar_fig.add_trace(
        go.Scatter(x=filtered_df['Year'], y=filtered_df['Solar capacity (total) (GW)'], 
                   name=get_translation("Solar Capacity (GW)", language), line=dict(color=colors['environmental'])),
        secondary_y=False,
    )
    
    solar_fig.add_trace(
        go.Scatter(x=filtered_df['Year'], y=filtered_df['Solar (% growth)'], 
                   name=get_translation("Solar Growth (%)", language), line=dict(color="#17becf", dash="dash")),
        secondary_y=True,
    )
    
    # Add annotation with target and translation
    solar_fig.add_annotation(
        x=filtered_df['Year'].max(),
        y=filtered_df['Solar capacity (total) (GW)'].max(),
        text=get_translation("Qatar 2023: 0.8 GW<br>Qatar target 2030: 4 GW<br>15,686% growth from 2016-2023", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    solar_fig.update_layout(
        title_text=get_translation("Solar Capacity and Growth", language),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    solar_fig.update_xaxes(title_text=get_translation("Year", language))
    solar_fig.update_yaxes(title_text=get_translation("Capacity (GW)", language), secondary_y=False)
    solar_fig.update_yaxes(title_text=get_translation("Growth (%)", language), secondary_y=True)
    
    # Extract latest values for KPI cards
    try:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year].iloc[0]
        
        co2_emissions = f"{latest_data['Annual CO₂ emissions']:,.1f} {get_translation('tonnes', language)}"
        co2_per_capita = f"{latest_data['Annual CO₂ emissions (per capita)']:,.1f} {get_translation('tonnes', language)}"
        co2_global_compare = get_translation(f"{latest_data['Annual CO₂ emissions (per capita)'] / benchmarks['co2_per_capita']['global_avg']:.1f}x global average", language)
        renewable_electricity = f"{latest_data['Electricity from renewables - TWh (adapted for visualization of chart elec-fossil-nuclear-renewables)']:,.2f} TWh"
        solar_capacity = f"{latest_data['Solar capacity (total) (GW)']:,.4f} GW"
    except:
        co2_emissions = get_translation("N/A", language)
        co2_per_capita = get_translation("N/A", language)
        co2_global_compare = ""
        renewable_electricity = get_translation("N/A", language)
        solar_capacity = get_translation("N/A", language)
    
    # Key Insights from the PDF for Environmental Development with added benchmark comparisons
    co2_insights = [
        "Total CO₂ emissions rose by 32.42% from 87.4 million tonnes in 2016 to 115.7 million tonnes in 2023, showing a concerning upward trajectory.",
        "CO₂ emissions per capita increased by 15.54% from 33.62 tonnes in 2016 to 38.84 tonnes in 2023, maintaining Qatar's position among the world's highest per capita emitters.",
        "The data shows an accelerating emissions trend, with the most significant jump occurring between 2022 and 2023 (9% increase in just one year).",
        "The rising emissions directly conflict with Qatar's environmental sustainability goals under Vision 2030 and its international climate commitments.",
        "Qatar's per capita emissions (38.84 tonnes) are approximately 8x the global average (4.8 tonnes) and higher than regional peers (Kuwait: 25 tonnes, UAE: 20 tonnes, Saudi Arabia: 18 tonnes)."
    ]
    
    electricity_insights = [
        "Fossil fuels generate over 99.7% of Qatar's electricity, with renewables contributing a minimal 0.28-0.31% throughout the period.",
        "Total electricity production increased by 28.2% from 42.44 TWh in 2016 to 54.39 TWh in 2023, driving up absolute emissions.",
        "Despite global renewable energy trends, Qatar's renewable electricity generation has plateaued at around 0.15 TWh since 2018.",
        "The data reveals a significant gap between Qatar's sustainability rhetoric and actual energy transformation progress.",
        "Global electricity mix shows 61% non-renewables vs 39% renewables, while Qatar targets 20% renewables by 2030, significantly above the Middle East average (4%) but below global average (29%)."
    ]
    
    solar_insights = [
        "Solar capacity experienced a remarkable 15,686% increase from 0.0051 GW in 2016 to 0.8051 GW in 2023.",
        "Almost all capacity growth occurred in a single year (2022), indicating a major infrastructure commissioning.",
        "Despite the capacity increase, the solar electricity generation data doesn't yet show a corresponding production increase, suggesting the new capacity may be at early operational stages.",
        "This dramatic solar expansion aligns with Qatar's National Development Strategy and preparations for hosting the 2022 FIFA World Cup.",
        "Qatar's 2030 target of 4 GW solar capacity would place it among the regional leaders in renewable capacity per capita, though still modest by global standards."
    ]
    
    # New insights for Energy Change chart that was missing dedicated insights
    energy_change_insights = [
        "Qatar's annual change in primary energy consumption shows significant volatility, with both substantial growth and contraction periods.",
        "The 2020 pandemic year saw the most dramatic energy consumption contraction, reflecting global economic slowdown and reduced industrial activity.",
        "Post-pandemic recovery shows a return to positive growth rates in energy consumption, potentially challenging sustainability targets.",
        "Qatar's typical annual energy consumption growth (5-6% in the 2010s) far exceeds the global average (1.9% in 2022), reflecting Qatar's rapid development and energy-intensive economy.",
        "Vision 2030 initiatives aim to moderate Qatar's energy consumption growth to below 3% annually by the late 2020s through efficiency improvements and renewable integration, though this would still exceed typical developed economy growth rates."
    ]
    
    # New insights for Renewable Electricity Production Detail chart that was missing dedicated insights
    renewable_detail_insights = [
        "Qatar's renewable electricity generation is dominated by solar power, accounting for nearly all renewable output since 2018.",
        "Bioenergy makes a minimal contribution to Qatar's renewable mix, with very limited growth over the monitoring period.",
        "Qatar's total renewable electricity production (0.15 TWh) is a fraction of the Middle East's already low renewable generation (47 TWh in 2022) and insignificant compared to global renewables (7,858 TWh in 2021).",
        "The dramatic increase in solar capacity in 2022-2023 has not yet translated to substantial increases in electricity generation, suggesting early operational stages or potential utilization challenges.",
        "Qatar's National Renewable Energy Strategy target of 4 GW solar capacity by 2030 would dramatically increase renewable electricity production, helping Qatar progress from its current 0.3% renewable share toward its 20% target."
    ]
    
    agricultural_insights = [
        "Agricultural land increased from 71,000 hectares in 2016 to 74,000 hectares in 2021 (4.23% growth), reflecting Qatar's food security strategy.",
        "Arable land saw more significant growth of 14.75% (18,300 to 21,000 hectares), indicating intensified cultivation efforts.",
        "These increases align with Qatar's post-2017 blockade strategy to enhance domestic food production and reduce import dependence.",
        "The expansion of agriculture in Qatar's challenging desert environment demonstrates technological innovation in climate-adapted farming.",
        "Qatar's agricultural productivity (~$10-11K per worker) exceeds regional peers like Oman (~$6K) but remains below advanced economies (>$50K per worker)."
    ]
    
    overall_environmental_insights = [
        "The data reveals a significant disconnect between Qatar's Vision 2030 environmental sustainability goals and actual progress, particularly in emissions and energy transition.",
        "While showing impressive progress in solar capacity expansion and agricultural development, Qatar has made limited headway in overall emissions reduction and renewable energy integration.",
        "With CO₂ emissions accelerating rather than decreasing, Qatar faces a critical decision point regarding its climate strategy credibility.",
        "Despite significant investments in renewable capacity (particularly solar), the impact on the overall energy mix remains minimal.",
        "The data highlights Qatar's complex sustainability challenge in balancing food security, water conservation, and energy transition in a desert environment.",
        "Qatar's per capita emissions (8x global average) and fossil-fuel dominated electricity mix (99.7%) contrast with its ambitious Vision 2030 sustainability goals."
    ]
    
    # Create KPI cards for environmental section with benchmark comparisons and translations
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("CO₂ Emissions", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(46, 204, 113, 0.1)", "borderLeft": f"4px solid {colors['environmental']}"}),
            dbc.CardBody([
                html.I(className="fas fa-smog fa-2x mb-2", style={"color": colors['environmental']}),
                html.H3(co2_emissions, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("Small share of global total", language), className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("CO₂ per Capita", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(46, 204, 113, 0.1)", "borderLeft": f"4px solid {colors['environmental']}"}),
            dbc.CardBody([
                html.I(className="fas fa-user-alt fa-2x mb-2", style={"color": colors['environmental']}),
                html.H3(co2_per_capita, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(co2_global_compare, className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Renewable Electricity", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(46, 204, 113, 0.1)", "borderLeft": f"4px solid {colors['environmental']}"}),
            dbc.CardBody([
                html.I(className="fas fa-solar-panel fa-2x mb-2", style={"color": colors['environmental']}),
                html.H3(renewable_electricity, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("0.3% of electricity mix", language), className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Solar Capacity", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(46, 204, 113, 0.1)", "borderLeft": f"4px solid {colors['environmental']}"}),
            dbc.CardBody([
                html.I(className="fas fa-sun fa-2x mb-2", style={"color": colors['environmental']}),
                html.H3(solar_capacity, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(get_translation("Target: 4GW by 2030", language), className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
    ], className="mb-4 g-3")
    
    # Create benchmark comparison cards with translations
    co2_benchmark_card = create_benchmark_card("CO₂ Emissions per Capita Benchmarks", benchmarks["co2_per_capita"], colors['environmental'], language)
    renewables_benchmark_card = create_benchmark_card("Renewables Share Benchmarks", benchmarks["renewables_share"], colors['environmental'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader(html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0"), 
                      style={"borderLeft": f"4px solid {colors['highlight']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-2"),
        ])
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Environmental Development Insights", overall_environmental_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        html.H4(get_translation("Environmental Development Analysis", language), className="mt-5 mb-4 text-center", style={"color": colors['text']}),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # CO2 emissions insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("CO₂ Emissions", co2_insights, colors['environmental'], language), width=6, className="mb-4"),
            dbc.Col(dcc.Graph(figure=co2_fig), width=6, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=co2_per_capita_fig),
                co2_benchmark_card
            ], width=6, className="mb-4"),
            dbc.Col(dcc.Graph(figure=energy_change_fig), width=6, className="mb-4"),
        ]),
        
        # Energy Change insights and card (newly added)
        dbc.Row([
            dbc.Col(create_insight_card("Energy Consumption Change", energy_change_insights, colors['environmental'], language), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Agricultural Development", agricultural_insights, colors['environmental'], language), width=6, className="mb-4"),
        ]),
        
        # Electricity production insights and charts
        dbc.Row([
            dbc.Col(dcc.Graph(figure=electricity_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Electricity Production", electricity_insights, colors['environmental'], language), width=6, className="mb-4"),
        ]),
        
        # Renewable and solar insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Solar Energy Development", solar_insights, colors['environmental'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=solar_fig),
                renewables_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Renewable detail chart with newly added insights
        dbc.Row([
            dbc.Col(dcc.Graph(figure=renewable_detail_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Renewable Energy Detail", renewable_detail_insights, colors['environmental'], language), width=6, className="mb-4"),
        ]),
        
        # Overall insights
        overall_insights_card,
    ])
    
    return layout

# Function to render Human Development tab with insights from PDF
def render_human(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = human_df[(human_df['Year'] >= min_year) & (human_df['Year'] <= max_year)]
    
    # Create Education Level charts with shortened labels and improved layout
    # Create a copy of the dataframe with shorter column names
    edu_df = filtered_df.copy()
    edu_df['Primary Education (%)'] = edu_df['UIS: Percentage of population age 25+ with at least completed primary education (ISCED 1 or higher). Total']
    edu_df['Secondary Education (%)'] = edu_df['UIS: Percentage of population age 25+ with at least completed upper secondary education (ISCED 3 or higher). Total'] 
    edu_df['Bachelor Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with at least a completed bachelor\'s or equivalent degree (ISCED 6 or higher). Total']

    education_level_fig = px.line(
        edu_df,
        x='Year',
        y=['Primary Education (%)', 'Secondary Education (%)', 'Bachelor Degree (%)'],  # Use actual column names
        title=get_translation('Population Education Levels (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf', '#ff7f0e'],
         labels={"value":get_translation("Primary Education, Secondary Education and Bachelor Degree (%)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        education_level_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    education_level_fig.add_annotation(
        x=edu_df['Year'].median(),
        y=edu_df['Bachelor Degree (%)'].max(),
        text=get_translation("Qatar tertiary attainment: ~30%<br>High-income countries: 30-45%<br>Leading countries (Canada/Korea): >55%", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    # Improve layout by setting higher minimum height
    education_level_fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Advanced education with shortened labels and improved layout
    edu_df['Master Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with at least a completed master\'s degree or equivalent (ISCED 7 or higher). Total']
    edu_df['Doctoral Degree (%)'] = edu_df['UIS: Percentage of population age 25+ with a doctoral degree or equivalent (ISCED 8). Total']

    advanced_edu_fig = px.line(
        edu_df,
        x='Year',
        y=['Master Degree (%)', 'Doctoral Degree (%)'],  # Use actual column names
        title=get_translation('Advanced Education Levels (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf'],
         labels={"value":get_translation("Master Degree and Doctoral Degree (%)", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        advanced_edu_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with OECD comparison and translation
    advanced_edu_fig.add_annotation(
        x=edu_df['Year'].median(),
        y=edu_df['Master Degree (%)'].max(),
        text=get_translation("OECD tertiary attainment: ~39%<br>Qatar aims to lead Arab world<br>in higher education outcomes", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    # Improve layout by setting higher minimum height
    advanced_edu_fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Completion Rate charts with improved styling and translations
    completion_rate_fig = px.line(
        filtered_df,
        x='Year',
        y=['Primary completion rate, total (% of relevant age group)',
       'Lower secondary completion rate, total (% of relevant age group)'],  # Original column names
        title=get_translation('Education Completion Rates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf'],
         labels={"value":get_translation("Primary and Lower secondary completion rate total", language), "variable": ""}
    )

    # Translate trace names for Arabic
    if language == 'arabic':
        completion_rate_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation with global comparison and translation
    completion_rate_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Primary completion rate, total (% of relevant age group)'].max(),
        text=get_translation("Qatar primary: ~98-99%<br>Global average: ~89%<br>Global secondary: ~75%", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    completion_rate_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create School Life Expectancy chart with improved styling and spacing
    school_life_fig = px.line(
        filtered_df,
        x='Year',
        y=['School life expectancy, primary to tertiary, both sexes (years)',
       'Expected Years of School',
       'Learning-Adjusted Years of School'],  # Original column names
        title=get_translation('School Life Expectancy and Learning Years', language),
        markers=True,
        color_discrete_sequence=[colors['human'], '#17becf', '#ff7f0e'],
         labels={"value":get_translation("'School life expectancy, primary to tertiary and Learning-Adjusted", language), "variable": ""}
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
    
    school_life_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=70, b=40),  # Increased top margin
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=0.95,  # Moved legend position up
            xanchor="center", 
            x=0.5,   # Centered legend
            bgcolor='rgba(255,255,255,0.8)'  # Semi-transparent background
        )
    )
    # Ensure lines connect across missing data
    school_life_fig.update_traces(connectgaps=True)
    
    # Extract latest values for KPI cards
    try:
        # Find years with non-null values for each metric
        bachelor_years = edu_df.dropna(subset=['Bachelor Degree (%)']).sort_values('Year')
        if not bachelor_years.empty:
            latest_bachelor_year = bachelor_years['Year'].max()
            latest_bachelor = bachelor_years[bachelor_years['Year'] == latest_bachelor_year]['Bachelor Degree (%)'].iloc[0]
            bachelor_value = f"{latest_bachelor:.1f}%"
            # Compare to global benchmarks
            bachelor_global_compare = get_translation("Above global average, below leading countries", language)
        else:
            bachelor_value = get_translation("N/A", language)
            bachelor_global_compare = ""
            
        hci_years = filtered_df.dropna(subset=['Human Capital Index (HCI) (scale 0-1)']).sort_values('Year')
        if not hci_years.empty:
            latest_hci_year = hci_years['Year'].max()
            latest_hci = hci_years[hci_years['Year'] == latest_hci_year]['Human Capital Index (HCI) (scale 0-1)'].iloc[0]
            hci_value = f"{latest_hci:.3f}"
            hci_global_compare = get_translation(f"{latest_hci / benchmarks['human_capital_index']['global_avg']:.1f}x global average", language)
        else:
            hci_value = get_translation("N/A", language)
            hci_global_compare = ""
            
        school_years = filtered_df.dropna(subset=['Expected Years of School']).sort_values('Year')
        if not school_years.empty:
            latest_school_year = school_years['Year'].max()
            latest_expected = school_years[school_years['Year'] == latest_school_year]['Expected Years of School'].iloc[0]
            expected_value = f"{latest_expected:.1f} {get_translation('years', language)}"
            expected_global_compare = get_translation(f"{latest_expected / benchmarks['education_years']['expected']['global_avg']:.1f}x global average", language)
        else:
            expected_value = get_translation("N/A", language)
            expected_global_compare = ""
            
        learning_years = filtered_df.dropna(subset=['Learning-Adjusted Years of School']).sort_values('Year')
        if not learning_years.empty:
            latest_learning_year = learning_years['Year'].max()
            latest_learning = learning_years[learning_years['Year'] == latest_learning_year]['Learning-Adjusted Years of School'].iloc[0]
            learning_value = f"{latest_learning:.1f} {get_translation('years', language)}"
            learning_global_compare = get_translation(f"{latest_learning / benchmarks['education_years']['learning_adjusted']['global_avg']:.1f}x global average", language)
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
    
    # Key Insights from the PDF for Human Development with added benchmark comparisons
    educational_attainment_insights = [
        "Mean years of schooling increased significantly by 11.44% from 9.67 years in 2016 to 10.77 years in 2022, indicating substantial progress in Qatar's educational development.",
        "Primary education completion rates have steadily improved from 87.03% in 2016 to 90.47% in 2022, moving closer to universal basic education.",
        "The population with at least upper secondary education increased dramatically from 41.01% in 2016 to 51.43% in 2022, representing a 25.4% improvement.",
        "The percentage of adults with at least a bachelor's degree saw remarkable growth of 60.95%, from 18.88% in 2016 to 30.39% in 2022, one of the most impressive gains among all indicators.",
        "Qatar's tertiary attainment (~30%) is comparable to high-income countries (30-45%) but remains below leading nations like Canada and Korea (>55%)."
    ]
    
    education_quality_insights = [
        "The learning gap (difference between expected and learning-adjusted years of schooling) decreased from 0.69 years in 2017 to 0.43 years in 2020, representing a reduction in learning loss from 5.31% to 3.24%.",
        "Expected years of schooling increased from 12.46 years in 2016 to 13.26 years in 2020, reflecting expanded educational opportunities.",
        "Learning-adjusted years of schooling improved from 12.31 years in 2017 to 12.83 years in 2020, indicating not just more education but better quality education.",
        "Despite improvements, the persistence of a learning gap suggests ongoing challenges in education quality that need addressing.",
        "Qatar's expected years of schooling (13.26) exceeds the global average (12) but remains below leading countries (15), while learning-adjusted years (12.83) significantly outperform the global average (7.8)."
    ]
    
    human_capital_insights = [
        "Qatar's Human Capital Index remained high and stable, changing only marginally from 0.992 in 2017 to 0.993 in 2020, indicating already strong human capital foundations.",
        "Survival rates show positive trends, with the probability of survival to age 5 increasing from 94.05% in 2017 to 96.14% in 2020.",
        "The survival rate from age 15-60 improved from 85.0% in 2017 to 87.8% in 2020, reflecting advancements in healthcare and quality of life.",
        "A child born in Qatar today can expect to achieve 99.3% of their potential productivity as an adult, one of the highest rates globally.",
        "Qatar's HCI (0.64) exceeds both the global average (0.56) and regional benchmarks (Saudi Arabia: 0.58) but remains below leading countries like Singapore (0.88) and Japan (0.80)."
    ]
    
    gender_equity_insights = [
        "The pre-primary gender parity index consistently favors females, increasing from 0.979 in 2016 to 1.077 in 2020, indicating strong early educational opportunities for girls.",
        "The trend shows an increasing female advantage in pre-primary enrollment, with the gender parity index growing by 10% from 2016 to 2020.",
        "Strong female participation in early education creates a foundation for gender equality throughout the educational system.",
        "The data suggests Qatar's educational policies have been particularly successful in promoting female participation in education from an early age.",
        "Women comprise 51.6% of engineering students in Qatar, and Qatari women's enrollment in higher education is one of the highest in the region, even outnumbering men at public universities."
    ]
    
    # New insights for Advanced Education Levels chart that was missing dedicated insights
    advanced_education_insights = [
        "Qatar has made progress in developing its postgraduate education capacity, with modest increases in both master's and doctoral degree holders.",
        "The percentage of adults with at least a master's degree is still relatively small but growing steadily as Qatar develops its knowledge economy workforce.",
        "Doctoral education remains at an early stage of development, with a very small percentage of the population holding PhDs.",
        "The OECD average tertiary attainment is approximately 39%, with Qatar aiming to reach similar levels for its citizen population.",
        "Qatar's investment in Education City branch campuses and international educational partnerships demonstrates its commitment to developing advanced education, with a goal of leading the Arab world in higher education outcomes by 2030."
    ]
    
    # New insights for Education Completion Rates chart that was missing dedicated insights
    completion_rates_insights = [
        "Qatar's primary education completion rates have shown steady improvement, approaching universal completion (98-99%) for nationals.",
        "Lower secondary completion rates have also improved but show greater room for growth compared to primary rates.",
        "Qatar outperforms the global average in both primary (89% globally) and secondary (75% globally) completion rates.",
        "Completion rate improvements reflect both better retention of students and expanded access to education for all residents.",
        "Qatar's investments in free public schooling and education scholarships have been key factors in maximizing completion rates."
    ]
    
    overall_human_development_insights = [
        "The substantial increase in higher education attainment (especially bachelor's degrees) aligns with Qatar's Vision 2030 goal of transitioning to a knowledge-based economy.",
        "The decreasing learning gap suggests a focus on quality of education, not just increased enrollment numbers.",
        "Improvements across multiple indicators (educational attainment, expected years of schooling, survival rates) demonstrate Qatar's multifaceted approach to human development.",
        "The strong performance in gender parity indicates attention to educational equity, though more comprehensive equity measures would be valuable.",
        "The consistent improvements across indicators reflect sustained investment in Qatar's human capital, a core component of Vision 2030.",
        "Qatar's human development metrics generally exceed global and regional averages but remain below those of leading countries, indicating both achievement and continued room for growth."
    ]
    
    # Create KPI cards for human development section with benchmark comparisons and translations
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Bachelor's Degree or Higher", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(243, 156, 18, 0.1)", "borderLeft": f"4px solid {colors['human']}"}),
            dbc.CardBody([
                html.I(className="fas fa-user-graduate fa-2x mb-2", style={"color": colors['human']}),
                html.H3(bachelor_value, className="mb-0"),
                html.P(get_translation("of adult population", language), className="text-muted"),
                html.P(bachelor_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Human Capital Index", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(243, 156, 18, 0.1)", "borderLeft": f"4px solid {colors['human']}"}),
            dbc.CardBody([
                html.I(className="fas fa-brain fa-2x mb-2", style={"color": colors['human']}),
                html.H3(hci_value, className="mb-0"),
                html.P(get_translation("Scale: 0-1", language), className="text-muted"),
                html.P(hci_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Expected Years of School", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(243, 156, 18, 0.1)", "borderLeft": f"4px solid {colors['human']}"}),
            dbc.CardBody([
                html.I(className="fas fa-school fa-2x mb-2", style={"color": colors['human']}),
                html.H3(expected_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(expected_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Learning-Adjusted Years", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(243, 156, 18, 0.1)", "borderLeft": f"4px solid {colors['human']}"}),
            dbc.CardBody([
                html.I(className="fas fa-book-reader fa-2x mb-2", style={"color": colors['human']}),
                html.H3(learning_value, className="mb-0"),
                html.P(get_translation("Latest value", language), className="text-muted"),
                html.P(learning_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
    ], className="mb-4 g-3")
    
    # Create benchmark comparison cards with translations
    hci_benchmark_card = create_benchmark_card("Human Capital Index Benchmarks", benchmarks["human_capital_index"], colors['human'], language)
    tertiary_benchmark_card = create_benchmark_card("Tertiary Education", benchmarks["tertiary_enrollment"], colors['human'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader(html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0"), 
                      style={"borderLeft": f"4px solid {colors['highlight']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-2"),
        ])
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Human Development Insights", overall_human_development_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        html.H4(get_translation("Human Development Analysis", language), className="mt-5 mb-4 text-center", style={"color": colors['text']}),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # Educational attainment insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Educational Attainment", educational_attainment_insights, colors['human'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=education_level_fig),
                tertiary_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Advanced education levels with newly added insights
        dbc.Row([
            dbc.Col(dcc.Graph(figure=advanced_edu_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Advanced Education", advanced_education_insights, colors['human'], language), width=6, className="mb-4"),
        ]),
        
        # Education quality insights
        dbc.Row([
            dbc.Col(create_insight_card("Education Quality", education_quality_insights, colors['human'], language), width=6, className="mb-4"),
            dbc.Col(dcc.Graph(figure=school_life_fig), width=6, className="mb-4"),
        ]),
        
        # School completion and human capital development
        dbc.Row([
            dbc.Col(dcc.Graph(figure=completion_rate_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Completion Rates", completion_rates_insights, colors['human'], language), width=6, className="mb-4"),
        ]),
        
        # Human capital and gender equity
        dbc.Row([
            dbc.Col([
                create_insight_card("Human Capital Development", human_capital_insights, colors['human'], language),
                hci_benchmark_card
            ], width=6, className="mb-4"),
            dbc.Col(create_insight_card("Gender Equity in Education", gender_equity_insights, colors['human'], language), width=6, className="mb-4"),
        ]),
        
        # Overall insights
        overall_insights_card,
    ])
    
    return layout

    # Function to render Social Development tab with insights from PDF
def render_social(min_year, max_year, language='english'):
    # Filter data by year range
    filtered_df = social_df[(social_df['Year'] >= min_year) & (social_df['Year'] <= max_year)]
    
    # Create Sanitation Services chart with handling for NaN values and connected gaps
    # Drop NaN values before creating chart
    sanitation_df = filtered_df.dropna(subset=['Share of the population using safely managed sanitation services'])
    
    if not sanitation_df.empty:
        sanitation_fig = px.line(
        sanitation_df,
        x='Year',
        y='Share of the population using safely managed sanitation services',  # Original column name
        title=get_translation('Population with Safely Managed Sanitation Services (%)', language),
        markers=True,
        color_discrete_sequence=[colors['social']],
         labels={"Share of the population using safely managed sanitation services":get_translation("Share of the population using safely managed sanitation services"), "variable": ""}
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
        
        # Ensure lines connect across missing data points
        sanitation_fig.update_traces(connectgaps=True)
        
        # Improve styling
        sanitation_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode="x unified",
            xaxis_title=get_translation("Year", language)
        )
    else:
        # Create an empty figure with a message if no data is available
        sanitation_fig = go.Figure()
        sanitation_fig.update_layout(
            title=get_translation("Population with Safely Managed Sanitation Services (%)", language),
            annotations=[dict(
                text=get_translation("No data available for sanitation services", language),
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text']),
            margin=dict(l=40, r=40, t=40, b=40),
        )
    
    # Create Gender Parity charts with shortened labels and improved layout
    gpi_df = filtered_df.copy()
    gpi_df['Primary Education GPI'] = gpi_df['School enrollment, primary (gross), gender parity index (GPI)']
    gpi_df['Tertiary Education GPI'] = gpi_df['Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, gender parity index (GPI)']

    gender_parity_fig = px.line(
        gpi_df,
        x='Year',
        y=['Primary Education GPI', 'Tertiary Education GPI'],  # Use actual column names
        title=get_translation('Gender Parity Indices in Education', language),
        markers=True,
        color_discrete_sequence=[colors['social'], '#17becf'],
         labels={"value":get_translation("Primary and Tertiary Education GPI", language), "variable": ""}
    )

    if language == 'arabic':
        gender_parity_fig.for_each_trace(lambda t: t.update(
        name=get_translation(t.name, language)
    ))
    
    # Add annotation for gender parity (GPI = 1.0 line) with translation
    gender_parity_fig.add_hline(y=1.0, line_dash="dash", line_color="#888888",
                               annotation_text=get_translation("Gender Parity (GPI = 1.0)", language), 
                               annotation_position="bottom right")
    
    # Add annotation for Qatar's gender equity in education with translation
    gender_parity_fig.add_annotation(
        x=gpi_df['Year'].median(),
        y=gpi_df['Primary Education GPI'].max(),
        text=get_translation("Qatar 2019: GPI >1.0 indicates slight<br>advantage for female students<br>Women: 51.6% of engineering students", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    # Improve layout
    gender_parity_fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create STEM & ICT graduates chart with shortened labels
    grad_df = filtered_df.copy()
    grad_df['STEM Graduates (%)'] = grad_df['Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, (%)']
    grad_df['ICT Graduates (%)'] = grad_df['Percentage of graduates from tertiary education graduating from Information and Communication Technologies programmes, (%)']

    stem_ict_fig = px.line(
        grad_df,
        x='Year',
        y=['STEM Graduates (%)', 'ICT Graduates (%)'],  # Use actual column names
        title=get_translation('STEM & ICT Graduates (%)', language),
        markers=True,
        color_discrete_sequence=[colors['social'], '#17becf'],
         labels={"value":get_translation("STEM and ICT Graduates (%)", language), "variable": ""}
    )

    if language == 'arabic':
        stem_ict_fig.for_each_trace(lambda t: t.update(
        name=get_translation(t.name, language)
    ))
    
    # Add benchmark lines for STEM graduates with translations
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
    
    # Improve layout
    stem_ict_fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Create Programming Skills chart with improved styling
    programming_fig = px.line(
        filtered_df,
        x='Year',
        y='Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)',  # Original column name
        title=get_translation('Programming Skills (%)', language),
        markers=True,
        color_discrete_sequence=[colors['social']],
         labels={"Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)":get_translation("Proportion of youth and adults who wrote a computer program", language), "variable": ""}
    )
    if language == 'arabic':
        programming_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))

    # Translate trace names for Arabic
    if language == 'arabic':
        programming_fig.for_each_trace(lambda t: t.update(
            name=get_translation(t.name, language)
    ))
    
    # Add annotation for digital skills context with translation
    programming_fig.add_annotation(
        x=filtered_df['Year'].median(),
        y=filtered_df['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)'].max(),
        text=get_translation("Qatar's divergent digital skills:<br>Improving basic skills (email: 58.72%)<br>Declining advanced skills (programming: 5.06%)", language),
        showarrow=True,
        arrowhead=1,
        font=dict(size=10),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#c7c7c7",
        borderwidth=1
    )
    
    programming_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text']),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        xaxis_title=get_translation("Year", language)
    )
    
    # Extract latest values for KPI cards
    try:
        # Find years with non-null values for each metric
        sanitation_years = filtered_df.dropna(subset=['Share of the population using safely managed sanitation services']).sort_values('Year')
        if not sanitation_years.empty:
            latest_sanitation_year = sanitation_years['Year'].max()
            latest_sanitation = sanitation_years[sanitation_years['Year'] == latest_sanitation_year]['Share of the population using safely managed sanitation services'].iloc[0]
            sanitation_value = f"{latest_sanitation:.1f}%"
            sanitation_global_compare = get_translation(f"{latest_sanitation / benchmarks['sanitation']['global_avg']:.1f}x global average", language)
        else:
            sanitation_value = get_translation("N/A", language)
            sanitation_global_compare = ""
            
        stem_years = grad_df.dropna(subset=['STEM Graduates (%)']).sort_values('Year')
        if not stem_years.empty:
            latest_stem_year = stem_years['Year'].max()
            latest_stem = stem_years[stem_years['Year'] == latest_stem_year]['STEM Graduates (%)'].iloc[0]
            stem_value = f"{latest_stem:.1f}%"
            if latest_stem < benchmarks["stem_graduates"]["global_avg"]:
                stem_global_compare = get_translation(f"{latest_stem / benchmarks['stem_graduates']['global_avg']:.1f}x global average (below avg)", language)
            else:
                stem_global_compare = get_translation(f"{latest_stem / benchmarks['stem_graduates']['global_avg']:.1f}x global average", language)
        else:
            stem_value = get_translation("N/A", language)
            stem_global_compare = ""
            
        gpi_years = gpi_df.dropna(subset=['Primary Education GPI']).sort_values('Year')
        if not gpi_years.empty:
            latest_gpi_year = gpi_years['Year'].max()
            latest_gpi = gpi_years[gpi_years['Year'] == latest_gpi_year]['Primary Education GPI'].iloc[0]
            gpi_value = f"{latest_gpi:.2f}"
            if latest_gpi > 1:
                gpi_global_compare = get_translation("Favors female students", language)
            elif latest_gpi < 1:
                gpi_global_compare = get_translation("Favors male students", language)
            else:
                gpi_global_compare = get_translation("Perfect gender parity", language)
        else:
            gpi_value = get_translation("N/A", language)
            gpi_global_compare = ""
            
        prog_years = filtered_df.dropna(subset=['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)']).sort_values('Year')
        if not prog_years.empty:
            latest_prog_year = prog_years['Year'].max()
            latest_prog = prog_years[prog_years['Year'] == latest_prog_year]['Proportion of youth and adults who have wrote a computer program using a specialised programming language, (%)'].iloc[0]
            prog_value = f"{latest_prog:.1f}%"
            prog_global_compare = get_translation("8.25% decline from 2016", language)
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
    
    # Key Insights from the PDF for Social Development with added benchmark comparisons
    sanitation_insights = [
        "Qatar has made remarkable progress in sanitation services, increasing coverage from 94.68% in 2016 to 99.94% in 2022 (5.55% improvement).",
        "The data shows consistent year-on-year improvements, with approximately 0.9 percentage point gains annually.",
        "Qatar has effectively achieved the UN Sustainable Development Goal target for universal access to safely managed sanitation.",
        "Near-universal sanitation coverage represents a significant public health achievement that contributes to disease prevention and overall quality of life.",
        "Qatar's sanitation access (99.94%) significantly exceeds the global average (75%) and is comparable to leading regions like North America and Europe (99%)."
    ]
    
    gender_equality_insights = [
        "Qatar has achieved gender parity in primary education, with the Gender Parity Index (GPI) improving from 0.994 in 2016 to 1.030 in 2019, indicating a slight advantage for female students.",
        "The 3.64% improvement in GPI reflects Qatar's commitment to equal educational opportunities regardless of gender.",
        "By 2019, the GPI exceeded 1.0, indicating that girls slightly outnumber boys in primary education enrollment.",
        "The data suggests Qatar's educational policies have been effective in eliminating gender-based barriers to basic education.",
        "Women comprise 51.6% of engineering students in Qatar, and female enrollment in tertiary education is among the highest in the region, with women often outnumbering men in university enrollment."
    ]
    
    stem_insights = [
        "The percentage of graduates from STEM programs has decreased dramatically by 39.96%, from 29.70% in 2016 to 17.83% in 2022.",
        "The decline has been persistent across all years, indicating a systematic shift in student preferences away from STEM fields.",
        "This trend poses a significant challenge to Qatar's ambition to develop a knowledge-based economy with strong scientific and technological foundations.",
        "The consistent decline suggests an urgent need for interventions to increase interest and enrollment in STEM fields.",
        "Qatar's current STEM graduate percentage (17.83%) is below both the global average (23%) and regional peer Saudi Arabia (32%), and significantly trails leading countries like Oman (43%) and Germany (37%)."
    ]
    
    digital_skills_insights = [
        "Email skills have shown steady improvement, increasing from 56.55% in 2016 to 58.72% in 2020 (3.84% growth).",
        "Programming skills have decreased from 5.51% in 2016 to 5.06% in 2019 (-8.25%), indicating challenges in developing advanced digital capabilities.",
        "The divergence between improving basic skills and declining advanced skills suggests a digital skills gap that could impact innovation capacity.",
        "While basic digital literacy is improving, the relatively low levels of advanced digital skills may limit Qatar's digital transformation ambitions.",
        "Qatar's vision for a knowledge economy requires stronger development of advanced technical skills to support digitization initiatives and AI/robotics adoption."
    ]
    
    # New insights for ICT graduates that was missing dedicated insights
    ict_graduates_insights = [
        "ICT (Information & Communication Technologies) graduates represent a relatively small percentage of Qatar's total tertiary graduates.",
        "ICT graduate percentages have shown fluctuations without a clear upward trend, failing to match the growing importance of digital skills in the global economy.",
        "The gap between Qatar's ICT graduate production and its digital economy ambitions poses a challenge for the country's knowledge economy transition.",
        "Qatar's partnerships with technology companies (Microsoft, Google Cloud) are creating demand for ICT specialists that may exceed domestic graduate production.",
        "Targeted programs to encourage ICT specialization will be crucial for Qatar to develop the skilled workforce needed for its digital future."
    ]
    
    overall_social_insights = [
        "Qatar shows impressive achievements in basic social infrastructure (sanitation) and gender equity in education, but concerning trends in STEM education and advanced digital skills.",
        "The data suggests that Qatar has successfully built social development foundations but faces challenges in developing the innovation capabilities needed for a knowledge economy.",
        "The achievement of gender parity in primary education represents a significant milestone in Qatar's social development journey.",
        "The consistent decline in STEM and ICT graduates represents one of the most significant challenges to Qatar Vision 2030's knowledge economy objectives.",
        "The data reveals a potential gap between Qatar's educational system outputs and its economic diversification requirements, particularly in technical fields.",
        "Qatar's sanitation access (1.3x global average) is world-class, while its STEM graduate percentage (0.78x global average) indicates a critical area for improvement."
    ]
    
    # Create KPI cards for social development section with benchmark comparisons and translations
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Sanitation Access", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(231, 76, 60, 0.1)", "borderLeft": f"4px solid {colors['social']}"}),
            dbc.CardBody([
                html.I(className="fas fa-hands-wash fa-2x mb-2", style={"color": colors['social']}),
                html.H3(sanitation_value, className="mb-0"),
                html.P(get_translation("of population", language), className="text-muted"),
                html.P(sanitation_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("STEM Graduates", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(231, 76, 60, 0.1)", "borderLeft": f"4px solid {colors['social']}"}),
            dbc.CardBody([
                html.I(className="fas fa-microscope fa-2x mb-2", style={"color": colors['social']}),
                html.H3(stem_value, className="mb-0"),
                html.P(get_translation("of all graduates", language), className="text-muted"),
                html.P(stem_global_compare, className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Gender Parity Index", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(231, 76, 60, 0.1)", "borderLeft": f"4px solid {colors['social']}"}),
            dbc.CardBody([
                html.I(className="fas fa-venus-mars fa-2x mb-2", style={"color": colors['social']}),
                html.H3(gpi_value, className="mb-0"),
                html.P(get_translation("Primary education", language), className="text-muted"),
                html.P(gpi_global_compare, className="small text-success mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H6(get_translation("Programming Skills", language), className="mb-0"), 
                          style={"backgroundColor": "rgba(231, 76, 60, 0.1)", "borderLeft": f"4px solid {colors['social']}"}),
            dbc.CardBody([
                html.I(className="fas fa-laptop-code fa-2x mb-2", style={"color": colors['social']}),
                html.H3(prog_value, className="mb-0"),
                html.P(get_translation("of population", language), className="text-muted"),
                html.P(prog_global_compare, className="small text-warning mt-2")
            ], className="text-center")
        ], className="h-100 shadow-sm"), width=3),
    ], className="mb-4 g-3")
    
    # Create benchmark comparison cards with translations
    sanitation_benchmark_card = create_benchmark_card("Sanitation Access Benchmarks", benchmarks["sanitation"], colors['social'], language)
    stem_benchmark_card = create_benchmark_card("STEM Graduates Benchmarks", benchmarks["stem_graduates"], colors['social'], language)
    
    # Create legend for benchmark lines with translations
    benchmark_legend = dbc.Card([
        dbc.CardHeader(html.H5(get_translation("Benchmark Comparison Legend", language), className="mb-0"), 
                      style={"borderLeft": f"4px solid {colors['highlight']}"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['global']}),
                html.Span(get_translation("Global Average", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['regional']}),
                html.Span(get_translation("Regional Comparison", language), style={"color": colors['text']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-minus me-2", style={"color": colors['leading']}),
                html.Span(get_translation("Leading Country", language), style={"color": colors['text']})
            ], className="mb-2"),
        ])
    ], className="mb-4 shadow-sm", style={"backgroundColor": colors['card']})
    
    # Overall insights card with translations
    overall_insights_card = dbc.Row([
        dbc.Col([
            create_insight_card("Overall Social Development Insights", overall_social_insights, colors['highlight'], language),
        ], width=12)
    ])
    
    # Create layout with paired insights and charts
    layout = html.Div([
        kpi_cards,
        html.H4(get_translation("Social Development Analysis", language), className="mt-5 mb-4 text-center", style={"color": colors['text']}),
        
        dbc.Row([
            dbc.Col(benchmark_legend, width=12, className="mb-4"),
        ]),
        
        # Sanitation insights and charts
        dbc.Row([
            dbc.Col(create_insight_card("Sanitation Services", sanitation_insights, colors['social'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=sanitation_fig),
                sanitation_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # Gender parity insights and charts
        dbc.Row([
            dbc.Col(dcc.Graph(figure=gender_parity_fig), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Gender Equality in Education", gender_equality_insights, colors['social'], language), width=6, className="mb-4"),
        ]),
        
        # STEM and ICT graduates insights and charts (with newly added ICT insights)
        dbc.Row([
            dbc.Col(create_insight_card("STEM Education", stem_insights, colors['social'], language), width=6, className="mb-4"),
            dbc.Col([
                dcc.Graph(figure=stem_ict_fig),
                stem_benchmark_card
            ], width=6, className="mb-4"),
        ]),
        
        # ICT graduates and digital skills
        dbc.Row([
            dbc.Col(create_insight_card("ICT Graduates", ict_graduates_insights, colors['social'], language), width=6, className="mb-4"),
            dbc.Col(create_insight_card("Digital Skills", digital_skills_insights, colors['social'], language), width=6, className="mb-4"),
        ]),
        
        # Programming skills chart
        dbc.Row([
            dbc.Col(dcc.Graph(figure=programming_fig), width=12, className="mb-4"),
        ]),
        
        # Overall insights
        overall_insights_card,
    ])
    
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
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
            }
            .card {
                border-radius: 8px;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
            }
            .chart-container {
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .nav-tabs .nav-link.active {
                font-weight: bold;
                border-bottom: 3px solid #18bc9c;
            }
            /* RTL Support for Arabic */
            [dir="rtl"] {
                font-family: 'Amiri', 'Traditional Arabic', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: right;
            }
            [dir="rtl"] .fa-arrow-right:before {
                content: "\\f060"; /* FontAwesome arrow left */
            }
            [dir="rtl"] .fa-arrow-left:before {
                content: "\\f061"; /* FontAwesome arrow right */
            }
            /* Set larger font size for Arabic */
            [dir="rtl"] body {
                font-size: 1.1rem;
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