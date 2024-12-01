import streamlit as st
from utils import LinkedInPostGenerator


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English"]

# Main app layout
def main():
    # Page configuration
    st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

    # Sidebar configuration
    with st.sidebar:
        st.markdown(
            """<h2 style='color: #4CAF50;'>Options</h2>""",
            unsafe_allow_html=True,
        )

        post_generator = LinkedInPostGenerator()
        tags = post_generator.get_tags()

        selected_tag = st.selectbox("Select Topic:", options=tags, help="Choose the topic for your LinkedIn post.")
        selected_length = st.selectbox("Post Length:", options=length_options, help="Choose the desired length of your post.")
        selected_language = st.selectbox("Language:", options=language_options, help="Currently, only English is supported.")

        generate_button = st.button("Generate Post")

    # Main content area
    st.markdown(
        """<h1 style='text-align: center; color: #4CAF50;'>LinkedIn Post Generator</h1>
        <h4 style='text-align: center; color: #555;'>Generate tailored LinkedIn posts effortlessly</h4>""",
        unsafe_allow_html=True,
    )

    st.write("\n")  # Add spacing

    if generate_button:
        with st.spinner("Generating your LinkedIn post..."):
            post = post_generator.generate_post(selected_length, selected_language, selected_tag)

        # Display the generated post
        st.markdown("### Your Generated Post:")
        st.text_area("Generated Post", post, height=300, help="Copy and use this post for your LinkedIn.")

    # Footer
    st.write("\n\n")  # Add spacing
    st.markdown(
        """<footer style='text-align: center; font-size: 12px; color: #888;'>
        Developed with ❤️ by MD Abdur Rahim | Powered by <a href="https://www.rahim.com.bd" target="_blank" style="color: #4CAF50; text-decoration: none;">RAHIM.COM.BD</a>
        </footer>""",
        unsafe_allow_html=True,
    )

# Run the app
if __name__ == "__main__":
    main()
