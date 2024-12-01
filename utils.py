import pandas as pd
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


class LinkedInPostGenerator:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.llm = None
        self.load_environment()
        self.load_posts(file_path)
        self.initialize_llm()

    def load_environment(self):
        load_dotenv()

    def initialize_llm(self):
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.2-90b-vision-preview")

    def load_posts(self, file_path):
        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
                self.df = pd.json_normalize(posts)
                self.df['length'] = self.df['line_count'].apply(self.categorize_length)
                all_tags = self.df['tags'].apply(lambda x: x).sum()
                self.unique_tags = list(set(all_tags))
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the provided file.")

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length, language, tag):
        if self.df is None:
            raise ValueError("Data not loaded. Please load the data first.")
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    def get_tags(self):
        return self.unique_tags

    def get_length_str(self, length):
        return {
            "Short": "1 to 5 lines",
            "Medium": "6 to 10 lines",
            "Long": "11 to 15 lines"
        }.get(length, "Unknown")

    def get_prompt(self, length, language, tag):
        length_str = self.get_length_str(length)

        prompt = f'''
        You are tasked with generating a professional LinkedIn post using the information provided below. Your response must be in English and structured into four distinct sections:

        1. Post Title/Image Thumbnail Title: Create a catchy, professional, and relevant title that grabs attention and effectively conveys the main focus of the post. It should be concise, engaging, and tailored to the topic.

        2. Post Content: Craft the main body of the post in a professional, persuasive marketing and outreach style designed to engage the target audience and drive leads. The content should highlight your unique expertise, showcase your ability to solve challenges, and communicate your value proposition. Use actionable insights, success stories, or practical tips that resonate with potential clients. Ensure the tone is confident, enthusiastic, and inspiring, with a clear call to action that encourages readers to connect, inquire, or hire you for freelance projects. Include relevant details that make the post informative and compelling, reinforcing why you are the right choice for potential clients.

        3. Portfolio Link: Provide a link to your personal portfolio or professional website (e.g., https://yourportfolio.com) to showcase your work, skills, and successful projects. This helps build trust and credibility with your audience.

        4. Popular Targeted Tags: Suggest a list of popular and relevant LinkedIn hashtags that align with the topic, such as #Python, #GenerativeAI, #FreelancingTips, #TechInnovation, or other relevant tags to expand reach and engagement.

        Input Parameters:
        - Topic: {tag}
        - Length: {length_str} (Short, Medium, or Long)
        - Language: {language} (Always craft the response in English)

        Output Format:
        - Post Title: 
        - Post Content: 
        - Portfolio Link: (e.g., https://yourportfolio.com)
        - Popular Targeted Tags: 

        *Note*: Ensure there is no extra formatting, such as additional ** for the output format. Make sure the post is impactful, engaging, and aligns with the interests of professionals in freelancing, AI, software development, and tech innovation. The final post should encourage readers to take action and see you as a trusted, knowledgeable professional in your field.
        '''


        # Add examples if available
        examples = self.get_filtered_posts(length, language, tag)
        if examples:
            prompt += "4) Use the writing style as per the following examples."
            for i, post in enumerate(examples[:2]):  # Limit to max 2 examples for brevity
                post_text = post['text']
                prompt += f'\n\n Example {i+1}: \n\n {post_text}'
                if i == 1:
                    break

        return prompt

    def generate_post(self, length, language, tag):
        prompt = self.get_prompt(length, language, tag)
        response = self.llm.invoke(prompt)
        return response.content


# Example usage
# if __name__ == "__main__":
#     post_generator = LinkedInPostGenerator()
#     length = "Short"  # Sample input
#     language = "English"
#     tag = "#GenerativeAI"

#     # Generate post
#     post = post_generator.generate_post(length, language, tag)
#     print(post)
