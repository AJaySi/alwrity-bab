import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)


def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def sidebar():
    st.sidebar.markdown(
            "**Other AI Apps by [Alwrity](https://alwrity.netlify.app)**"
        )
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")



def title_and_description():
    st.title("✍️ Alwrity - AI Generator for CopyWriting BAB Formula")
    with st.expander("What is **Copywriting BAB formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's BAB copywriting Formula, How to use this AI generator 🗣️
            ---
            #### BAB Copywriting Formula

            BAB stands for Before-After-Bridge. It's a copywriting formula that involves:

            1. **Before**: Presenting the current undesirable situation or problem faced by the audience.
            2. **After**: Describing the desired state or outcome the audience wants to achieve.
            3. **Bridge**: Introducing your product or service as the solution that bridges the gap between the before and after states.

            The BAB formula is effective in capturing attention, creating desire for change, and presenting your solution as the means to achieve it.

            #### BAB Copywriting Formula: Simple Example

            - **Before**: Are you tired of waking up tired every morning?
            - **After**: Imagine feeling energized and refreshed, ready to tackle the day with enthusiasm.
            - **Bridge**: Our energy-boosting supplement provides the vitality you need to start each day feeling invigorated and full of life.

            ---
        ''')

def input_section():
    with st.expander("**PRO-TIP** - Campaign's Key features and benefits to build **Interest & Desire**", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('**Enter Brand/Company Name**')
        with col2:
            description = st.text_input(f'**Describe What {brand_name} Does ?** (In 5-6 words)')

        before = st.text_input('**What\'s the Problem?**', 
                       help="For example: 'People can't find a good taxi.'",
                       placeholder="Describe the problem...")
        after = st.text_input('**What\'s the Solution?**', 
                      help="Guide: 'Describe what people want instead.'",
                      placeholder="Describe the ideal outcome...")
        bridge = st.text_input('**How Does Your Solution Help?**', 
                       help="Guide: 'Explain how your solution fixes the problem.'",
                       placeholder="Describe how you solve it...")

        if st.button('**Get BAB Copy**'):
            if before.strip() and after.strip() and bridge.strip():
                with st.spinner("Generating BAB Copy..."):
                    bab_copy = generate_bab_copy(brand_name, description, before, after, bridge)
                    if bab_copy:
                        st.subheader('**👩🔬👩🔬 Your BAB marketing Copy**')
                        st.markdown(bab_copy)
                    else:
                        st.error("💥 **Failed to generate BAB copy. Please try again!**")
            else:
                st.error("Before, After, and Bridge fields are required!")

    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_bab_copy(brand_name, description, before, after, bridge):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name},
        which is a {description}. Your task is to use the BAB (Before-After-Bridge) formula to craft compelling copywrite.
        Here's the breakdown:
        - Before: {before}
        - After: {after}
        - Bridge: {bridge}
        Do not provide explanations in your response, provide the final marketing copy.
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """ """
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using BAB formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Problem:
    Are you struggling to create compelling marketing campaigns that grab your audience's attention and drive them to take action?

    ### Agitate:
    Imagine spending hours crafting a message, only to find it doesn't resonate with your audience or compel them to engage with your brand. Your campaigns may lack the attention-grabbing headlines, compelling details, and persuasive calls-to-action needed to stand out in today's crowded digital landscape.

    ### Bridge:
    Introducing Alwrity - Your AI Generator for Copywriting BAB Formula.
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()

