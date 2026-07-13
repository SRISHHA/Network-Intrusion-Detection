import os
import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image
from dotenv import load_dotenv

import google.generativeai as genai

from src.config import *
from src.roi import compute_roi, decision
from src.pipelines.inference_pipeline import run_inference


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = None

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    llm = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.title("🤖 AI Dashboard")

    st.markdown("---")

    st.success("CatBoost X-Learner")

    st.write("### Navigation")

    page = st.radio(
    "",
    [
        "Dashboard",
        "Customer Explorer",
        "Campaign Insights",
        "Ask AI"
    ]
  )

    st.markdown("---")

    ai_enabled = st.toggle(
        "Enable AI Insights",
        value=True
    )

    st.markdown("---")

    st.caption(
        "AI-powered customer retention decision support system."
    )












# -------------------------------
# CACHE DATA
# -------------------------------

@st.cache_data(show_spinner=False)
def load_predictions():

    df = run_inference(
        input_path=DATA_PATH,
        model_path=MODEL_PATH,
        feature_path=FEATURE_PATH
    )

    return df


@st.cache_resource(show_spinner=False)
def load_shap_image():

    try:
        return Image.open("images/shap.png")

    except FileNotFoundError:

        return None


try:

    df = load_predictions()
    if "selected_customer" not in st.session_state:
      st.session_state.selected_customer = None

except Exception as e:

    st.error(f"Unable to load predictions: {e}")

    st.stop()


# -------------------------------
# UTILITY FUNCTIONS
# -------------------------------

def get_customer(customer_id):

    customer = df[df["customerID"] == customer_id]

    if customer.empty:
        return None

    return customer.iloc[0]


def dataframe_summary():

    return {

        "customers": len(df),

        "average_uplift": round(
            df["uplift_pred"].mean(),
            3
        ),

        "average_roi": round(
            df["roi"].mean(),
            2
        ),

        "segment_distribution":
            df["segment"].value_counts().to_dict(),

        "best_segment":
            df.groupby("segment")["roi"].mean().idxmax()

    }

# -------------------------------
# AI HELPER
# -------------------------------

def ask_ai(prompt):

    if llm is None:

        return (
            "⚠️ Gemini API key not configured."
        )

    try:

        response = llm.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {e}"


def build_customer_prompt(customer):

    uplift = float(customer["uplift_pred"])

    roi = compute_roi(uplift)

    recommendation = decision(uplift)

    return f"""
You are an experienced Customer Retention Consultant.

Below is a customer predicted by a Causal Uplift Model.

Customer Data

{customer.to_dict()}

Predicted Uplift:
{uplift:.3f}

Estimated ROI:
{roi:.2f}

Recommended Action:
{recommendation}

Write a concise executive report using the following headings:

## Customer Summary

## Why the model recommends this action

## Business Risks

## Recommended Marketing Action

## Expected Business Impact

Keep the explanation under 250 words.

Avoid technical ML terminology.

Write for marketing executives.
"""


st.title("🤖 AI Customer Retention Dashboard")

st.caption(
    "Causal Uplift Modeling + Explainable AI + Generative AI for smarter retention decisions."
)
if page == "Dashboard":
  st.header("📊 Dashboard Overview")
  summary = dataframe_summary()

  segment_summary = (
    df.groupby("segment")
      .agg(
          customers=("segment", "count"),
          avg_roi=("roi", "mean"),
          avg_uplift=("uplift_pred", "mean")
      )
      .round(3)
  )

  roi_segment = (
      df.groupby("segment")["roi"]
        .mean()
        .sort_values(ascending=False)
  )
  
  segment_counts = df["segment"].value_counts()

  st.header("🤖 AI Executive Summary")
  
  if ai_enabled:
  
      if st.button("Generate Executive Summary"):
  
          with st.spinner("Generating AI summary..."):
  
              prompt = f"""
  You are a Chief Marketing Analytics Consultant.
  
  Summarize the following uplift campaign results.
  
  Total Customers: {summary['customers']}
  
  Average Uplift: {summary['average_uplift']}
  
  Average ROI: {summary['average_roi']}
  
  Segment Distribution:
  
  {summary['segment_distribution']}
  
  Best Performing Segment:
  
  {summary['best_segment']}
  
  Write:
  
  - Executive Summary
  - Key Findings
  - Business Risks
  - Recommended Next Steps
  
  Keep it under 250 words.
  """
  
              response = ask_ai(prompt)
  
              st.markdown(
                  f"""
  <div class="ai-box">
  
  {response}
  
  </div>
  """,
                  unsafe_allow_html=True,
              )
  
  st.divider()
 
  uplift = 0.0
  roi = 0.0
  
  col1, col2, col3 = st.columns(3)
  
  with col1:
  
      st.info(
          f"""
  ### Priority
  
  {"High" if uplift > 0.20 else "Medium" if uplift > 0 else "Low"}
  """
      )
  
  with col2:
  
      st.info(
          """
  ### Suggested Channel
  
  📧 Email Campaign
  """
      )
  
  with col3:
  
      st.info(
          f"""
  ### Estimated ROI
  
  ${roi:.2f}
  """
      )
  
  best_roi = (
      df.groupby("segment")["roi"]
      .mean()
      .max()
  )
  col1, col2, col3, col4 = st.columns(4)
  
  col1.metric(
      "Customers",
      f"{summary['customers']:,}"
  )
  
  col2.metric(
      "Average Uplift",
      f"{summary['average_uplift']:.3f}"
  )
  
  col3.metric(
      "Average ROI",
      f"${summary['average_roi']:.2f}"
  )
  
  col4.metric(
      "Best Segment ROI",
      f"${best_roi:.2f}"
  )
  
  st.progress(
      min(max((uplift + 1) / 2, 0), 1)
  )
  
  st.caption(
      "Higher values indicate stronger expected response to treatment."
  )
elif page == "Customer Explorer":

    st.header("📈 Campaign Performance")

    left, right = st.columns(2)

    with left:

        st.subheader("Customer Segments")

        segment_counts = (
            df["segment"]
            .value_counts()
        )

        st.bar_chart(segment_counts)

    with right:

        st.subheader("Average ROI by Segment")

        roi_segment = (
            df.groupby("segment")["roi"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(roi_segment)

    st.header("🔍 Customer Explorer")

    customer_id = st.text_input("Enter Customer ID")

    if st.button("Analyze Customer"):

        customer = get_customer(customer_id)

       

        if customer is None:

            st.error("Customer ID not found")

        else:

            st.dataframe(
                customer.to_frame().T,
                use_container_width=True
            )

            st.session_state.selected_customer = customer

            uplift = float(st.session_state.selected_customer["uplift_pred"])

            roi = compute_roi(uplift)

            st.success(f"Recommended Action: {decision(uplift)}")

            st.write(f"ROI: ${roi:.2f}")

            if ai_enabled:

                prompt = build_customer_prompt(customer)

                response = ask_ai(prompt)

                st.markdown(response)

    st.header("🧠 Why This Prediction?")

    if st.button("Explain Uplift Model"):

        image = load_shap_image()

        if image:

            st.image(
                image,
                caption="SHAP Summary Plot",
                use_container_width=True
            )

        else:

            st.warning("SHAP image not found.")

        st.markdown("""
### Interpretation

This SHAP summary plot explains how each feature influences the **predicted treatment effect (uplift)**.

- **Each dot represents one customer.**
- **X-axis (SHAP Value):**
  - Positive → increases predicted uplift.
  - Negative → decreases predicted uplift.
- **Color of dots:**
  - 🔴 High feature value
  - 🔵 Low feature value

#### Key Insights

- **TreatmentEffect** is the strongest driver of uplift.
- **Electronic Check** payment method tends to increase uplift.
- **Tenure** has a mixed impact depending on customer history.
- **Monthly Charges** influence whether a customer is likely to respond to treatment.
- Lower-ranked features have relatively little impact on the uplift prediction.

This visualization helps identify **which customer characteristics contribute most to the estimated treatment effect**, enabling more targeted marketing interventions.
        """)

    st.header("📈 Uplift Distribution")

    st.subheader("Predicted Uplift Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(df["uplift_pred"], bins=30)

    ax.set_xlabel("Predicted Uplift")
    ax.set_ylabel("Customers")
    ax.set_title("Distribution of Predicted Uplift")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    st.pyplot(fig)

elif page == "Campaign Insights":
  st.header("🎯 AI Campaign Insights")
  
  if ai_enabled:
  
      if st.button("Generate Campaign Strategy"):
  
          with st.spinner("Analyzing campaign..."):
  
              segment_summary = (
                  df.groupby("segment")
                  .agg(
                      customers=("segment","count"),
                      avg_roi=("roi","mean"),
                      avg_uplift=("uplift_pred","mean")
                  )
                  .round(3)
              )
  
              prompt = f"""
  You are a senior CRM strategist.
  
  Campaign Results
  
  {segment_summary.to_string()}
  
  Provide
  
  1. Which segment should be targeted first.
  
  2. Which customers should not receive offers.
  
  3. Budget recommendations.
  
  4. Expected ROI considerations.
  
  5. Three actionable recommendations.
  
  Keep it concise.
  """
  
              response = ask_ai(prompt)
  
              st.markdown(
                  f"""
  <div class="report-box">
  
  {response}
  
  </div>
  """,
                  unsafe_allow_html=True
              )

elif page == "Ask AI":

    st.header("💬 Ask AI")

    user_prompt = st.text_area("Ask a marketing question")

    if st.button("Ask"):

        response = ask_ai(user_prompt)

        st.markdown(response) 
