"""
GEON Quick Start - GEO Integration
Simple script to add GEO features to your existing platform
Run this to test GEO functionality immediately
"""

import streamlit as st
import sys
from pathlib import Path

# Add repo root to path
sys.path.append(str(Path(__file__).parent))

# Import GEO modules
try:
    from geo.analyzer import GEOAnalyzer
    from geo.optimizer import GEOOptimizer, Industry
    GEO_AVAILABLE = True
except ImportError as e:
    GEO_AVAILABLE = False
    st.error(f"⚠️ GEO modules not found / import failed: {e}")

def main():
    st.set_page_config(
        page_title="GEON - GEO Quick Start",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 GEON - Generative Engine Optimization")
    st.caption("Transform your content for AI search visibility")
    
    if not GEO_AVAILABLE:
        st.error("Please install GEO modules first.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Industry selection
        industry = st.selectbox(
            "Industry",
            options=[
                "general", "science_tech", "business_finance",
                "arts_humanities", "health_medical", "legal",
                "ecommerce", "education"
            ],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        st.divider()
        
        st.subheader("About GEON")
        st.info("""
        **GEON** analyzes and optimizes content for:
        - ChatGPT
        - Claude
        - Gemini
        - Perplexity
        - AI Overviews
        """)
        
        st.metric("GEO Methods", "8+")
        st.metric("Avg Improvement", "22-37%")
    
    # Main content area - Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Analyze Content",
        "🚀 Get Recommendations",
        "📚 Learn GEO"
    ])
    
    # Tab 1: Analyze
    with tab1:
        st.header("Analyze Content for GEO")
        
        content_input_method = st.radio(
            "How do you want to provide content?",
            ["Paste Text", "Enter URL"],
            horizontal=True
        )
        
        content = None
        url = None
        
        if content_input_method == "Paste Text":
            content = st.text_area(
                "Paste your content here",
                height=250,
                placeholder="Paste HTML or plain text content to analyze..."
            )
        else:
            url = st.text_input(
                "Enter URL",
                placeholder="https://example.com/article"
            )
            if url:
                st.warning("⚠️ URL scraping requires your existing scraper integration")
                content = None
        
        if st.button("🔍 Analyze for GEO", type="primary", disabled=not content):
            if content:
                with st.spinner("Analyzing content..."):
                    analyzer = GEOAnalyzer()
                    results = analyzer.analyze_content(content, url)
                    
                    if 'error' in results:
                        st.error(results['error'])
                    else:
                        display_analysis_results(results)
    
    # Tab 2: Recommendations
    with tab2:
        st.header("Get GEO Optimization Recommendations")
        st.info("💡 Get specific, actionable recommendations to improve your content's AI visibility")
        
        content = st.text_area(
            "Content to optimize",
            height=200,
            placeholder="Enter content to get optimization recommendations..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            current_score = st.slider(
                "Current GEO Score (if known)",
                0, 100, 50,
                help="If you've analyzed this content, enter its score"
            )
        
        if st.button("🎯 Generate Optimization Plan", type="primary", disabled=not content):
            if content:
                with st.spinner("Creating optimization plan..."):
                    optimizer = GEOOptimizer()
                    industry_enum = Industry[industry.upper()]
                    
                    plan = optimizer.generate_optimization_plan(
                        content=content,
                        industry=industry_enum,
                        current_scores={'overall_score': current_score}
                    )
                    
                    display_optimization_plan(plan)
    
    # Tab 3: Learn
    with tab3:
        st.header("Learn About GEO")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 What is GEO?")
            st.write("""
            **Generative Engine Optimization (GEO)** is the practice of optimizing 
            content to improve visibility in AI-generated responses.
            
            Unlike traditional SEO which focuses on ranking in search results, 
            GEO ensures your content is:
            - **Cited** by AI engines
            - **Quoted** in AI responses
            - **Recommended** to users
            """)
            
            st.subheader("📈 Why GEO Matters")
            st.write("""
            - **40%+** of searches now use AI tools
            - AI engines bypass traditional search results
            - Direct answers = higher user trust
            - Early adopters gain competitive advantage
            """)
        
        with col2:
            st.subheader("🔧 GEO Methods")
            
            methods = [
                ("Statistics Addition", "22%", "Add data points and metrics"),
                ("Quotation Addition", "37%", "Include expert quotes"),
                ("Cite Sources", "115%", "Proper attribution"),
                ("Authoritative Writing", "20%", "Expert tone"),
                ("Technical Terms", "18%", "Industry terminology"),
                ("EEAT Enhancement", "25%", "Expertise signals")
            ]
            
            for method, improvement, desc in methods:
                with st.expander(f"{method} - {improvement} improvement"):
                    st.write(f"**{desc}**")
                    st.caption(f"Expected improvement: {improvement}")
        
        st.divider()
        
        st.subheader("🎓 GEO Best Practices")
        
        practices = {
            "Content Structure": [
                "Start with direct answers (50-100 words)",
                "Use FAQ format for common questions",
                "Add clear headings and sections",
                "Include bulleted lists"
            ],
            "Authority Building": [
                "Add author credentials",
                "Include expert quotes",
                "Cite authoritative sources",
                "Display certifications"
            ],
            "Technical Optimization": [
                "Implement Schema.org markup",
                "Add JSON-LD structured data",
                "Use semantic HTML",
                "Optimize meta tags"
            ],
            "Content Quality": [
                "High vocabulary diversity",
                "Industry-specific terminology",
                "Data and statistics",
                "Unique insights"
            ]
        }
        
        for category, items in practices.items():
            with st.expander(f"📋 {category}"):
                for item in items:
                    st.write(f"✓ {item}")

def display_analysis_results(results):
    st.success("✅ Analysis Complete!")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = results['scores']['overall_score']
        grade = results['overall_grade']
        st.metric("Overall GEO Score", f"{score:.1f}/100", delta=grade, delta_color="off")
    
    with col2:
        st.metric("Word Count", results['detailed_analysis']['word_count'])
    
    with col3:
        st.metric("Paragraphs", results['detailed_analysis']['paragraph_count'])
    
    with col4:
        has_schema = results['detailed_analysis']['has_structured_data']
        st.metric("Schema Markup", "✅" if has_schema else "❌")
    
    st.divider()
    
    st.subheader("📊 Score Breakdown")
    
    scores = results['scores']
    score_items = [
        ("Entity Recognition", scores['entity_recognition'], "🏷️"),
        ("Answer Format", scores['answer_optimization'], "❓"),
        ("Semantic Depth", scores['semantic_depth'], "🧠"),
        ("Structured Data", scores['structured_data'], "🏗️"),
        ("Authority Signals", scores['authority_signals'], "⭐"),
        ("Citation Worthiness", scores['citation_worthiness'], "📚")
    ]
    
    col1, col2, col3 = st.columns(3)
    
    for i, (name, score, emoji) in enumerate(score_items):
        col = [col1, col2, col3][i % 3]
        with col:
            st.metric(
                f"{emoji} {name}",
                f"{score:.1f}/100",
                delta=get_score_assessment(score),
                delta_color="normal" if score >= 60 else "inverse"
            )
    
    st.divider()
    st.subheader("🎯 Recommendations")
    
    if results['recommendations']:
        for i, rec in enumerate(results['recommendations'][:5], 1):
            priority_color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
            
            with st.expander(f"{priority_color[rec['priority']]} Priority {i}: {rec['category']}", expanded=(i == 1)):
                st.write(f"**Action Required:** {rec['action']}")
                st.write(f"**Impact:** {rec['impact']}")
                
                st.write("**Examples:**")
                for example in rec['examples']:
                    st.write(f"  • {example}")
    else:
        st.info("Great job! Your content is well-optimized for GEO.")
    
    st.divider()
    
    if results['opportunities']['quick_wins']:
        st.subheader("⚡ Quick Wins")
        
        for opp in results['opportunities']['quick_wins']:
            st.success(f"**{opp['opportunity']}**  \n⏱️ {opp['estimated_time']} | 📈 {opp['impact']}")

def display_optimization_plan(plan):
    st.success("✅ Optimization Plan Generated!")
    st.info(f"**Expected Improvement:** {plan.estimated_improvement}")
    
    st.subheader("🎯 Primary Optimization Methods")
    
    for i, method in enumerate(plan.primary_methods, 1):
        with st.expander(
            f"{i}. {method['method'].replace('_', ' ').title()} - {method['improvement']}% improvement potential",
            expanded=(i == 1)
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Difficulty:** {method['difficulty']}")
            with col2:
                st.write(f"**Time:** {method['time_investment']}")
            
            st.write(f"**Description:** {method['details']['description']}")
            
            st.write("**Implementation Steps:**")
            for step in method['details']['implementation']:
                st.write(f"  {step}")
            
            if method['details'].get('examples'):
                st.write("**Examples:**")
                for example in method['details']['examples']:
                    st.code(example, language=None)
    
    st.subheader("➕ Specific Content to Add")
    for addition in plan.content_additions:
        st.write(addition)
    
    st.subheader("🏗️ Schema Markup Recommendations")
    for schema in plan.schema_recommendations:
        with st.expander(f"{schema['type']} Schema - {schema['priority']} Priority"):
            st.write("**Fields to complete:**")
            for field in schema['fields_to_complete']:
                st.write(f"  • {field}")
            
            st.write("**JSON-LD Template:**")
            st.json(schema['template'])

def get_score_assessment(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Work"
    else:
        return "Critical"

if __name__ == "__main__":
    main()
