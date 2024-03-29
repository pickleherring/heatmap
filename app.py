"""The heatmap app.
"""

import plotnine
import streamlit

import heatmap


DEFAULT_WINDOW_SIZE = 300

MAX_WINDOW_SIZE = 1000

N_HOTSPOTS = 1

CONTEXT_SIZE = 10

with open('sex_terms.txt', encoding='utf-8') as f:
    TERMS = f.read().split()


# %% helper functions

@streamlit.cache
def load_explanation_text(filename):
    
    return open(filename, encoding='utf-8').read()


def read_uploaded_file(file):
    
    contents = file.read()
    
    try:
        text = contents.decode('utf-8')
    except UnicodeDecodeError:
        text = contents.decode('latin-1')
        
    return text


# %% preloads

intro = load_explanation_text('intro.md')
explanation = load_explanation_text('explanation.md')
faq = load_explanation_text('FAQ.md')


# %% user data - file upload

uploaded_file = streamlit.sidebar.file_uploader(
    'upload your story as text files:',
    help='pick a plain text file on your computer (.txt)'
)


# %% user data - text field

pasted_text = streamlit.sidebar.text_area(
    'or paste your text here:',
    help='paste text into the box',
    disabled=bool(uploaded_file)
)


# %% user config - window size

window_size = streamlit.sidebar.slider(
    'adjust the smoothness of your heatmap',
    min_value=3,
    max_value=MAX_WINDOW_SIZE,
    value=DEFAULT_WINDOW_SIZE,
    help="slide left for a more detailed but more 'jagged' map,\nslide right for a 'smoother' map"
)


# %% process user data

if uploaded_file:
    text = read_uploaded_file(uploaded_file)
else:
    text = pasted_text

if text:
    n_sentences = len(heatmap.split_sentences(text))
    df = heatmap.process_text(text, terms=TERMS, window=min(n_sentences // 2, window_size))
    hotspots = df.nlargest(N_HOTSPOTS, 'smoothed')


# %% explanation

streamlit.title('erotica heatmap')
streamlit.markdown(intro)


# %% confirm text

if text:
    streamlit.subheader('your text')
    streamlit.text(text[:100] + '[...]')


# %% figure

streamlit.subheader('your results')

if text:
    
    if n_sentences >= 3:
    
        fig = (
            plotnine.ggplot(
                df,
                plotnine.aes(
                    x='pos',
                    y='smoothed'
                )
            )
            + plotnine.labs(
                x='sentence',
                y='heat'
            )
            + plotnine.geom_line()
            + plotnine.geom_point(
                data=hotspots,
                color='red'
            )
        )

        streamlit.pyplot(fig.draw())

        streamlit.markdown(explanation)

        for row in hotspots.index:
            context_start = row - (CONTEXT_SIZE // 2)
            context_stop = row + (CONTEXT_SIZE // 2)
            context = ''.join(df['sentence'][context_start:context_stop])
            streamlit.text('[...] ' + context + ' [...]')
        
    else:
        
        streamlit.markdown('text is too short (try at least 3 sentences)')

else:
    
    streamlit.markdown('← *upload or paste your story*')


# %% FAQs

streamlit.subheader('FAQs')
streamlit.markdown(faq)
