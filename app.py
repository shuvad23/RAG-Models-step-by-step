# Use %%writefile to create a file with your code

import streamlit as st
import os
from google import genai
import getpass
# from diffusers import AutoPipelineForText2Image
import torch
from huggingface_hub import login # Import the login function
import time
from dotenv import load_dotenv



def app_file():
    load_dotenv()
    YOUR_HUGGINGFACE_TOKEN = os.getenv("YOUR_HUGGINGFACE_TOKEN")
    google_gemini_api_key = os.getenv("google_gemini_api_key")  
    # google_gemini_api_key  = getpass.getpass("Enter your Gemini API key: ")

    # api's autherization -------
    # YOUR_HUGGINGFACE_TOKEN= userdata.get('YOUR_HUGGINGFACE_TOKEN')
    # google_gemini_api_key = userdata.get('google_gemini_api_key')
    os.environ["GEMINI_API_KEY"] = google_gemini_api_key
    client = genai.Client(api_key=google_gemini_api_key)

    # generate article --------
    def generate(prompt,model_name):
        response = client.models.generate_content(
            model = model_name,
            contents = prompt
        )
        return response.text

    # improve content -----
    def improve_content(text,model_name,tone):
        token = "Clear Compelling Title, Hook in the Indroduction, Know my Audience, Well-structured Content, SEO Optimization, Value-Packed Information, Engaging and Conversational Tone, Call to Action, Profreading and Editing, Consistency and Authenticity"
        prompt = f"Improve this blog post base on your previous result: {text}."+ token+f"Tone like :{tone}"
        response = generate(prompt,model_name)
        return response


    # smart analysis for title generation
    def smart_analysis(text,tone,lan):
        title= f"\"{text}\": this is the user topic. Generate beautiful, cute, and engaging blog title , i give you same example : "
        suggessted_title = {
            "💖 Heartwarming & Cute Blog Titles":
                          ["Little Joys That Make Life Sparkle ✨",

                          "Sweet & Simple: Finding Happiness in Small Moments 🍯",

                          "Cuddles, Coffee & Comfort: My Cozy Life Diary ☕🐾",

                          "Bloom Where You’re Planted 🌸🌿",

                          "Sunshine & Smiles: A Happy Soul’s Guide ☀️😊"
                          ],
            "🌟 Inspirational & Uplifting Titles":
                        ["Dare to Dream: How to Chase Your Wildest Goals 🌠",

                        "Rise & Shine: Morning Habits for a Brighter Day 🌄✨",

                        "You Are Enough: A Reminder for Your Soul 💖",

                        "Turning Stumbles into Strength 💪🌈",

                        "The Magic of Believing in Yourself ✨🔮"
                        ],
            "📚 Bookish & Creative Titles":
                        [
                            "Lost in Pages: My Love Affair with Books 📖❤️",

                            "Wanderlust & Words: Travel Stories from My Bookshelf 🌍📚",

                            "Writing My Heart Out: A Writer’s Journey ✍️💭",

                            "Bookworm Diaries: Cozy Nights & Fictional Lives 🛋️🐛",

                            "Poetry in Motion: Words That Dance on Paper 🩰📜"
                        ],
            "🍃 Wellness & Self-Care Titles":
                        [
                            "Breathe In, Bliss Out: A Guide to Inner Peace 🧘‍♀️🌸",

                            "Soulful Sundays: Slow Living for a Happy Heart 🕯️🍵",

                            "Glow Up Inside Out: Self-Love Rituals 💖✨",

                            "Calm Mind, Happy Life: Anxiety-Busting Tips 🧠🌊",

                            "Tea, Tranquility & Tiny Joys 🫖🌼"
                        ],
            "✈️ Travel & Adventure Titles":
                          [
                              "Wander Often, Wonder Always 🌎✈️",

                              "Roaming with a Heart Full of Dreams 🗺️💫",

                              "Sunsets, Souvenirs & Serendipity 🌅🛍️",

                              "Getting Lost to Find Myself 🧭❤️",

                              "Jet Lag & Joy: My Travel Confessions ✈️😂"
                          ],


                  "🍽️ Food & Cooking Titles":
                        [
                            "Butter, Sugar & Love: Baking My Way to Happiness 🧁💕",

                            "Kitchen Chronicles: Messy Aprons & Happy Hearts 👩‍🍳❤️",

                            "Sip, Savor & Smile: My Coffee Adventures ☕📓",

                            "From My Kitchen to Yours: Homemade Happiness �🍪",

                            "Food for the Soul: Recipes That Heal 🥘💖"
                        ],


                  "🎨 Creative & Artistic Titles":
                        [
                          "Painting My Dreams in Color 🎨🌈",

                          "Doodles, Daydreams & Divine Chaos ✏️🌀",

                          "Creating Magic with My Hands ✂️✨",

                          "Art Heals: My Journey Through Creativity 🖌️❤️",

                          "Ink & Imagination: Stories Behind My Sketches 📓✍️",
                        ],

                    "💡Funny & Relatable Titles":
                                  [
                                      "Adulting is Hard, But Coffee Helps ☕😅",

                                      "Napping Like It’s My Job 😴💼",

                                      "My Plants Are Alive… Barely 🌱⚰️",

                                      "Procrastination Level: Expert 📺⏳",

                                      "SOS: Send Snacks & Motivation 🍕🔥"
                                  ]

                    }
        how_to_use = """ How to Use These Titles:
                              Personal Blogs → Mix heartfelt + cute emojis (e.g., "Finding Light in the Little Things 🌟🍃")

                              Lifestyle Guides → Use action-driven titles (e.g., "10 Ways to Turn Your Day Around 🔄💖")

                              Travel Diaries → Add wanderlust emojis (e.g., "Soul-Searching in Santorini 🌊🤍")

                                      """
        final_prompt= title + str(suggessted_title) + how_to_use+ f"Tone: \"{tone}\".Now Generate atlist five blog title like this suggestion, base on user topic.keyNote: selected language {lan} "
        response = generate(final_prompt,'gemini-2.5-flash')
        return response


    # smart analysis full blog content
    def smart_analysis_full_blog(text,keywords,tone,lan):
        token_prompt = f"""
        You are a smart, creative, and SEO-optimized AI blog assistant. Your job is to help users generate engaging, informative, and well-structured blog posts on any topic they provide. Always follow the best blogging practices, including:

                1. A compelling title

                2. A catchy introduction

                3. Proper headings and subheadings (H1, H2, H3)

                4. SEO keywords naturally embedded

                5. Human-like tone (friendly, clear, and helpful)

                6. Use bullet points, short paragraphs, and call-to-action when needed

                7. Add FAQs, summary, or conclusion if applicable

        Given a blog topic, your output should be a full blog post in markdown format. Be original and avoid generic or repetitive content.

        Input:
        Topic: \"{text}\"
        Keywords: \"{keywords}\"
        user tone: \"{tone}\",
        user language: \"{lan}\"
        tone:
        Conversational: Write as if you're talking to a curious friend. Avoid robotic or overly formal language.

        Clear & Friendly: Be approachable and supportive, like a mentor guiding the reader.

        Confident & Helpful: Present facts and suggestions with clarity and authority, but without sounding pushy.

        Human-like: Use natural phrasing, contractions (like "you’re" instead of "you are"), and occasional rhetorical questions to engage the reader.

        SEO-Aware: Embed keywords naturally without keyword stuffing.

        Professional but Relaxed: Maintain professionalism while being warm and welcoming.

        Output:
        (A complete, high-quality blog post with all the elements listed above.)"
        """
        response = generate(token_prompt,'gemini-2.5-flash')
        return response

    # text classification (base on user given text)
    def text_classification_blog(blog_text):
        from transformers import pipeline
        # Load a zero-shot classification model
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        candidate_labels = [
                          "Technology",
                          "Health & Wellness",
                          "Finance & Investing",
                          "Education",
                          "Lifestyle",
                          "Travel",
                          "Food & Recipes",
                          "Business & Entrepreneurship",
                          "Marketing & SEO",
                          "Entertainment & Pop Culture",
                          "Sports & Fitness",
                          "Science & Environment",
                          "Personal Development",
                          "DIY & Crafts",
                          "Parenting & Family",
                          "Fashion & Beauty",
                          "News & Politics",
                          "Gaming & eSports",
                          "Art & Design",
                          "Automotive & Transportation"
                      ]
        result = classifier(blog_text, candidate_labels=candidate_labels)
        return result['labels'][0]

    # smart blog generator ( using text classification )
    def smart_blog_gernerator(prompt,model_name):
        tones = """
        Note:   generate engaging, informative, and well-structured blog posts on this topic . Always follow the best blogging practices, including:
                1. A compelling title

                2. A catchy introduction

                3. Proper headings and subheadings (H1, H2, H3)

                4. SEO keywords naturally embedded

                5. Human-like tone (friendly, clear, and helpful)

                6. Use bullet points, short paragraphs, and call-to-action when needed

                7. Add FAQs, summary, or conclusion if applicable
        provide him with top suggested five links:
        """
        final_prompt = prompt + tones
        response = generate(final_prompt,model_name)
        return response

    def translate_to_english(text,lang):
        # translate this using googletrans

        # from googletrans import Translator
        # translator = Translator()
        # translated_text = translator.translate(text, src='auto', dest='en').text
        # return translated_text


        # using Hugging face api
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        from langdetect import detect
        # Load model and tokenizer
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        # Language map (ISO 639-1 → NLLB)
        lang_code_map = {
            "bn": "ben_Beng",
            "hi": "hin_Deva",
            "fr": "fra_Latn",
            "es": "spa_Latn",
            "de": "deu_Latn",
            "ar": "arb_Arab",
            "ta": "tam_Taml",
            "en": "eng_Latn",
            "ru": "rus_Cyrl",
            "zh": "cmn_Hans",
            "ja": "jpn_Jpan",
            "ko": "kor_Hang",
            "it": "ita_Latn",
            "tr": "tur_Latn",
            "pt": "por_Latn",
        }



        src_lang = lang_code_map.get(lang)

        if not src_lang:
            raise ValueError(f"Language '{lang}' not supported")

        tokenizer.src_lang = src_lang

        encoded = tokenizer(text, return_tensors="pt")

        # Use convert_tokens_to_ids to get the token ID for the target language
        # The NLLB target language code needs to be prefixed with '__' and suffixed with '__'
        encoded["forced_bos_token_id"] = tokenizer.convert_tokens_to_ids(f"__{lang_code_map['en']}__")

        output = model.generate(**encoded)
        return tokenizer.decode(output[0], skip_special_tokens=True)
    # --------------------------------------------------------Body structure -----------------------------------
    # Title
    st.title("🐰ྀི Hey - This is Rabbit.")
    # subheader
    st.subheader("➤ I Am Your - AI Blog Assistant.😊")
    # horizontal line
    st.markdown(
    "<hr style='border:1px solid #ccc; width:100%; margin:20px 0;'>",
    unsafe_allow_html=True
    )

    # sidebar for user input
    with st.sidebar:


        # sidebar title and subheader
        st.title("🐰ྀི AI Blog Assistant Application")
        st.subheader("Enter Details of the Blog You Want to write")


        # blog title
        blog_title = st.text_input("Blog Title")
        # keywords
        keywords = st.text_area("Keywords( For Better Feedback )")
        # number of words
        number_words = st.number_input("Number of Words",min_value = 100,max_value=1000, step=100)

        # Tone selector
        tones = st.selectbox(
                "Choose Your Tone",
                        [
                        'Conversational',
                        'Clear & Friendly',
                        'Confident & Helpful',
                        'Human-like',
                        'SEO-Aware',
                        'Professional but Relaxed',
                        'Expert/Informative',
                        'Witty/Humorous',
                        'Inspirational/Motivational',
                        'Neutral/Objectively',
                        'Calm/Empathetic',
                        'Assertive/Opinionated'
                        ]
        )


        # Models
        gemini_models = st.selectbox(
                "Choose Your Gemini Models",
                        [
                        'gemini-2.5-flash',
                        'gemini-2.5-flash-lite-preview-06-17',
                        'gemini-2.5-flash-lite-preview-06-17',
                        ]
        )

        # language selection:
        language = st.selectbox(
                "Choose Your Language",
                    [
                        "English",
                        "Hindi",
                        "Bangla",
                        "Japanese",
                        "Korean",
                        "Spanish",
                        "French",
                        "German",
                        "Italian",
                        "Russian",
                        "Chinese",
                        "Arabic",
                    ]
        )

        # buttons( Horizontaliy )
        submit_button1,submit_button2 = st.columns(2)


        # button 1 generate content
        prompt1 = f"""Generate a comprehensive and engaging blog post relevant to the given title \"{blog_title}\".
              Use the provided keywords:\"{keywords}\".The blog post should be approximately {number_words} words in length with H1,H2 heading,
              suitable for an online audience. Ensure the content is original, informative,tone:{tones}, and beautiful structured and Add few quotes of {blog_title}. KeyNote: Selected Language:{language}"""
        with submit_button1:
            submit_button1 = st.button("✨Generate Blog")

        # button 2 (Content Improvements)
        with submit_button2:
            submit_button2 = st.button("🧠Improve Article")

        # button 3,4 (Analysis smartly)
        submit_button3,submit_button4 = st.columns(2)
        with submit_button3:
          submit_button3 = st.button("🌈 Smartly Analysis(Title)")
        with submit_button4:
          submit_button4 = st.button("🌈 Smartly Analysis(Full Blog)")

        # button 5(Thinking smartly base on user given input )
        user_pasted_text = st.text_area("Paste your text/articles here")
        submit_button5 = st.button("Smartly Thinking (Your interest)")

    # click button 1
    if submit_button1:
        try:
            if blog_title == "" or keywords == "":
                raise NameError
            else:
                with st.spinner("🤖 Thinking..."):
                    # print("Please Wait for Processing image.....")
                    response = generate(prompt1,gemini_models)
                    st.session_state['generated_response'] = response # Store it safely in session
                    time.sleep(1)  # Simulate a delay (e.g., calling an AI model)
                st.success("Done!")
                st.write(response)

        except:
            st.write("⚠️ Please enter the blog title and keywords first.")
    # click button 2
    if submit_button2:
        try:
            with st.spinner("🤖 Thinking..."):
                response2 = improve_content(st.session_state['generated_response'],gemini_models,tones)
                time.sleep(1)  # Simulate a delay (e.g., calling an AI model)
            st.success("Done!")
            st.write(response2)
        except NameError:
            st.write("⚠️ Please generate the blog first before improving it.")

    #click button 3
    if submit_button3:

        try:
          if blog_title == "":
            raise NameError
          else:
            with st.spinner("🤖 Thinking..."):
                response3 = smart_analysis(blog_title,tones,language)
                time.sleep(1)  # Simulate a delay (e.g., calling an AI model)
            st.success("Done!")
            st.write(response3)
        except NameError:
            st.write("⚠️ Please generate the blog first before Smart Analysis.⋆˚✿˖°")

    # click button 4
    if submit_button4:

        try:
          if blog_title == "":
            raise NameError
          else:
            with st.spinner("🤖 Thinking..."):
                response4 = smart_analysis_full_blog(blog_title,keywords,tones,language)
                time.sleep(1)  # Simulate a delay (e.g., calling an AI model)
            st.success("Done!")
            st.write(response4)
        except NameError:
            st.write("⚠️ Please generate the blog first before Smart Analysis.⋆˚✿")

    # click button 5
    if submit_button5:

        try:
          if user_pasted_text == "":
            raise NameError
          else:
            with st.spinner("🤖 Thinking..."):
                from langdetect import detect
                lang = detect(user_pasted_text)
                if lang != "en":
                    user_pasted_text = translate_to_english(user_pasted_text,lang)

                # text classification section
                response_label = text_classification_blog(user_pasted_text)
                token = f"Awesome! Since you're interested in {response_label}, I’ll go ahead and generate a blog post on one of the best, most trending, and top-rated topics related to it."
                st.write(token)

                # main generation section
                response5 = smart_blog_gernerator(token,gemini_models)
                time.sleep(1)  # Simulate a delay (e.g., calling an AI model)

            st.success("Done!")
            st.write(response5)

        except NameError:
            st.write("⚠️ Please paste the text first before Smart Analysis.⋆˚✿")

# call the main function
if __name__ == "__main__":
  app_file()

#---------------------------------