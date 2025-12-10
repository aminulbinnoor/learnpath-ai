# app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
import json
import time

# Page configuration
st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        color: #4f46e5;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: 600;
    }
    .resource-link {
        display: block;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: white;
        border-radius: 5px;
        text-decoration: none;
        color: #4f46e5;
        border-left: 4px solid #4f46e5;
    }
    .resource-link:hover {
        background: #f0f0ff;
    }
</style>
""", unsafe_allow_html=True)

# Mock AI function
def generate_learning_path(topic, level, hours_per_week, goal):
    """Generate a personalized learning path"""
    
    # Define available topics and their resources
    topics_data = {
        "Data Science": {
            "beginner": ["Python Basics", "Pandas & NumPy", "Data Visualization", "Statistics Fundamentals"],
            "intermediate": ["Machine Learning Basics", "SQL for Data Science", "Data Cleaning", "EDA Techniques"],
            "advanced": ["Deep Learning", "Big Data Tools", "MLOps", "Advanced Statistics"]
        },
        "Web Development": {
            "beginner": ["HTML/CSS", "JavaScript Basics", "Responsive Design", "Git Basics"],
            "intermediate": ["React/Vue.js", "Node.js", "API Development", "Database Design"],
            "advanced": ["Performance Optimization", "Testing", "DevOps", "System Design"]
        },
        "Machine Learning": {
            "beginner": ["Python for ML", "Linear Algebra", "Basic Algorithms", "Scikit-learn"],
            "intermediate": ["Neural Networks", "TensorFlow/PyTorch", "Feature Engineering", "Model Evaluation"],
            "advanced": ["Deep Learning", "NLP/CV", "Reinforcement Learning", "Research Papers"]
        },
        "Mobile Development": {
            "beginner": ["Swift/Kotlin", "UI Design", "Basic Apps", "Mobile Patterns"],
            "intermediate": ["Advanced UI", "API Integration", "State Management", "Testing"],
            "advanced": ["Performance", "Native Modules", "CI/CD", "App Store Optimization"]
        }
    }
    
    # Calculate timeline based on hours per week
    hours_map = {"light (3-5 hours)": 12, "moderate (6-10 hours)": 8, "intensive (10+ hours)": 4}
    weeks = hours_map.get(hours_per_week, 8)
    
    # Generate timeline
    start_date = datetime.now()
    timeline = []
    resources = topics_data.get(topic, {}).get(level, [])
    
    if not resources:
        # Default resources if topic not found
        resources = ["Foundation", "Core Concepts", "Projects", "Advanced Topics"]
    
    for i, resource in enumerate(resources[:4]):  # Limit to 4 weeks for demo
        week_num = i + 1
        due_date = start_date + timedelta(weeks=week_num)
        
        # Generate subtasks for each resource
        subtasks = []
        if level == "beginner":
            subtasks = ["Watch introductory videos", "Complete exercises", "Build small project"]
        elif level == "intermediate":
            subtasks = ["Study documentation", "Complete tutorial", "Contribute to open source"]
        else:
            subtasks = ["Read research papers", "Implement from scratch", "Optimize performance"]
        
        timeline.append({
            "week": week_num,
            "topic": resource,
            "due_date": due_date.strftime("%b %d, %Y"),
            "subtasks": subtasks,
            "resources": [
                f"Course: {resource} Fundamentals",
                f"Book: Mastering {resource}",
                f"Project: Build a {resource} Application"
            ],
            "completed": random.choice([True, False]) if week_num == 1 else False
        })
    
    # Generate motivational quote
    quotes = [
        "The journey of a thousand miles begins with one step.",
        "Learning is not attained by chance, it must be sought for with ardor.",
        "The expert in anything was once a beginner.",
        "Education is the most powerful weapon which you can use to change the world."
    ]
    
    return {
        "topic": topic,
        "level": level,
        "goal": goal,
        "timeline": timeline,
        "total_weeks": weeks,
        "motivational_quote": random.choice(quotes),
        "generated_date": datetime.now().strftime("%Y-%m-%d")
    }

def create_roadmap_visualization(timeline):
    """Create a Gantt chart visualization of the learning path"""
    df = pd.DataFrame(timeline)
    
    # Create dates for visualization
    dates = []
    for i, week in enumerate(timeline):
        start_date = datetime.now() + timedelta(weeks=i*7)
        end_date = start_date + timedelta(days=6)
        dates.append({
            "Task": week["topic"],
            "Start": start_date,
            "Finish": end_date,
            "Week": f"Week {week['week']}"
        })
    
    df_viz = pd.DataFrame(dates)
    
    fig = px.timeline(
        df_viz, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Week",
        title="Learning Path Timeline",
        labels={"Task": "Learning Topic", "Week": "Week"},
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    return fig

def create_skill_radar_chart(level):
    """Create a radar chart for skill progression"""
    categories = ['Theory', 'Practice', 'Projects', 'Community', 'Innovation']
    
    if level == "beginner":
        values = [3, 2, 1, 2, 1]
    elif level == "intermediate":
        values = [4, 4, 3, 3, 2]
    else:
        values = [5, 5, 5, 4, 4]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line_color='rgb(102, 126, 234)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        height=300,
        title="Skill Progression Radar"
    )
    return fig

def display_resource_links():
    """Display resource links in sidebar"""
    st.markdown("### 🔗 Useful Resources")
    
    resources = [
        ("📁 GitHub Repository", "https://github.com"),
        ("📚 Streamlit Docs", "https://docs.streamlit.io"),
        ("🎓 FreeCodeCamp", "https://www.freecodecamp.org"),
        ("📊 Kaggle", "https://www.kaggle.com"),
        ("🧠 Coursera", "https://www.coursera.org")
    ]
    
    for name, url in resources:
        st.markdown(f'<a href="{url}" target="_blank" class="resource-link">{name}</a>', unsafe_allow_html=True)

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 LearnPath AI</h1>', unsafe_allow_html=True)
    st.markdown("### Your Personalized Learning Journey Generator")
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown("### 🎯 Configure Your Path")
        
        topic = st.selectbox(
            "Choose your learning topic:",
            ["Data Science", "Web Development", "Machine Learning", "Mobile Development", "Cybersecurity", "Cloud Computing"]
        )
        
        level = st.select_slider(
            "Current skill level:",
            options=["beginner", "intermediate", "advanced"]
        )
        
        hours_per_week = st.radio(
            "Weekly commitment:",
            ["light (3-5 hours)", "moderate (6-10 hours)", "intensive (10+ hours)"]
        )
        
        goal = st.text_area(
            "Your learning goal:",
            placeholder="e.g., Build a portfolio project, Prepare for job interview, Learn for fun..."
        )
        
        generate_btn = st.button("✨ Generate Learning Path", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 Progress Tracker")
        
        if 'learning_path' in st.session_state:
            completed_weeks = sum(1 for week in st.session_state.learning_path["timeline"] if week.get('completed', False))
            total_weeks = len(st.session_state.learning_path["timeline"])
            progress = (completed_weeks / total_weeks) * 100 if total_weeks > 0 else 0
            st.progress(int(progress))
            st.caption(f"Overall Progress: {int(progress)}%")
        else:
            st.progress(0)
            st.caption("Overall Progress: 0%")
        
        display_resource_links()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if generate_btn and topic and goal:
            with st.spinner("🤖 AI is generating your personalized learning path..."):
                time.sleep(1.5)  # Simulate AI processing
                
                # Generate learning path
                learning_path = generate_learning_path(topic, level, hours_per_week, goal)
                
                # Store in session state
                st.session_state.learning_path = learning_path
                
                # Display success message
                st.success("✅ Learning path generated successfully!")
                
                # Show overview
                st.markdown(f'<h3 class="sub-header">📚 Your {topic} Learning Path</h3>', unsafe_allow_html=True)
                
                # Display roadmap visualization
                st.plotly_chart(create_roadmap_visualization(learning_path["timeline"]), use_container_width=True)
                
                # Display weekly breakdown
                st.markdown(f'<h3 class="sub-header">🗓️ Weekly Breakdown</h3>', unsafe_allow_html=True)
                
                for week in learning_path["timeline"]:
                    with st.expander(f"Week {week['week']}: {week['topic']} (Due: {week['due_date']})", expanded=False):
                        col_a, col_b = st.columns([1, 2])
                        
                        with col_a:
                            status = "✅ Completed" if week.get('completed', False) else "🔄 In Progress"
                            st.markdown(f"**Status:** {status}")
                            
                            if not week.get('completed', False):
                                if st.button(f"Mark Complete", key=f"complete_{week['week']}"):
                                    st.session_state.learning_path["timeline"][week['week']-1]["completed"] = True
                                    st.success(f"Week {week['week']} marked as complete!")
                                    st.rerun()
                        
                        with col_b:
                            st.markdown("**Tasks:**")
                            for task in week['subtasks']:
                                st.markdown(f"• {task}")
                            
                            st.markdown("**Resources:**")
                            for i, resource in enumerate(week['resources']):
                                st.markdown(f"{i+1}. {resource}")
        
        elif 'learning_path' in st.session_state:
            # Display existing learning path
            learning_path = st.session_state.learning_path
            
            st.markdown(f'<h3 class="sub-header">📚 Your {learning_path["topic"]} Learning Path</h3>', unsafe_allow_html=True)
            st.plotly_chart(create_roadmap_visualization(learning_path["timeline"]), use_container_width=True)
            
            # Display weekly breakdown
            st.markdown(f'<h3 class="sub-header">🗓️ Weekly Breakdown</h3>', unsafe_allow_html=True)
            
            for week in learning_path["timeline"]:
                with st.expander(f"Week {week['week']}: {week['topic']} (Due: {week['due_date']})", expanded=False):
                    col_a, col_b = st.columns([1, 2])
                    
                    with col_a:
                        status = "✅ Completed" if week.get('completed', False) else "🔄 In Progress"
                        st.markdown(f"**Status:** {status}")
                        
                        if not week.get('completed', False):
                            if st.button(f"Mark Complete", key=f"complete_{week['week']}"):
                                st.session_state.learning_path["timeline"][week['week']-1]["completed"] = True
                                st.success(f"Week {week['week']} marked as complete!")
                                st.rerun()
                    
                    with col_b:
                        st.markdown("**Tasks:**")
                        for task in week['subtasks']:
                            st.markdown(f"• {task}")
                        
                        st.markdown("**Resources:**")
                        for i, resource in enumerate(week['resources']):
                            st.markdown(f"{i+1}. {resource}")
        
        else:
            # Initial state - show instructions
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("""
            ### Welcome to LearnPath AI! 🤖
            
            **How it works:**
            1. Select your learning topic and skill level from the sidebar
            2. Choose your weekly time commitment
            3. Describe your learning goal
            4. Click "Generate Learning Path" to get your personalized plan
            
            **Features:**
            - 📅 Interactive timeline with deadlines
            - 🎯 Weekly tasks and resources
            - 📊 Progress tracking
            - 🔄 Adjustable based on your pace
            - 💾 Save and export your learning path
            
            Get started by configuring your path in the sidebar!
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show sample topics
            st.markdown(f'<h3 class="sub-header">🎯 Popular Learning Paths</h3>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Data Science**")
                st.markdown("*6-month path*")
                st.markdown("👥 24,500 learners")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Web Development**")
                st.markdown("*4-month path*")
                st.markdown("👥 18,200 learners")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Machine Learning**")
                st.markdown("*8-month path*")
                st.markdown("👥 12,800 learners")
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'learning_path' in st.session_state:
            learning_path = st.session_state.learning_path
            
            # Display motivational quote
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### 💭 Inspiration")
            st.markdown(f'*"{learning_path["motivational_quote"]}"*')
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display skill radar chart
            st.plotly_chart(create_skill_radar_chart(learning_path["level"]), use_container_width=True)
            
            # Progress statistics
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📈 Progress Statistics")
            
            total_weeks = len(learning_path["timeline"])
            completed_weeks = sum(1 for week in learning_path["timeline"] if week.get('completed', False))
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Weeks Completed", f"{completed_weeks}/{total_weeks}")
            with col_stat2:
                st.metric("Success Rate", "92%")
            
            st.metric("Total Duration", f"{learning_path['total_weeks']} weeks")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options
            st.markdown("### 💾 Export Options")
            
            if st.button("Save as JSON", use_container_width=True):
                json_data = json.dumps(learning_path, indent=2)
                st.download_button(
                    label="Download JSON File",
                    data=json_data,
                    file_name=f"learning_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            if st.button("Reset Learning Path", use_container_width=True):
                if 'learning_path' in st.session_state:
                    del st.session_state.learning_path
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Made with ❤️ using Streamlit</p>
        <p>⚡ Add this to your GitHub portfolio!</p>
        </div>
        """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()