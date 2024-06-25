import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import traceable
from dotenv import load_dotenv

load_dotenv()

feedbacks = {
    "positive": [
        "WidgetWorld exceeded my expectations with their top-notch widgets! Our machines run smoother than ever before.",
        "Impressed by WidgetWorld's attention to detail and commitment to quality. Their widgets are a game-changer for our business.",
        "WidgetWorld's widgets are reliable and durable, making them an essential component in our manufacturing process."
    ],
    "neutral": [
        "WidgetWorld's widgets are decent, but nothing exceptional. They get the job done adequately.",
        "Average experience with WidgetWorld. Their widgets function as expected, but nothing to write home about.",
        "WidgetWorld's widgets are alright, but there's room for improvement in terms of durability."
    ],
    "negative": [
        "Avoid WidgetWorld at all costs! Their widgets are cheaply made and constantly malfunction.",
        "Terrible experience with WidgetWorld. Their widgets broke down within weeks of installation.",
        "WidgetWorld's widgets are a nightmare. We've had nothing but problems since day one."
    ]
}

template = ChatPromptTemplate.from_messages([
    ("system", "You are a customer service representative for WidgetWorld, a company that manufactures widgets. A customer has left feedback about their experience with WidgetWorld's widgets. Please respond to the feedback. Be polite and professional, even if the customer sounds unhappy or angry. Empathise with the customer. Keep your response concise and to the point."),
    ("human", "{feedback}"),
])


@traceable
def respond_to_customer_feedback():
    responses = []
    openai_client = template | ChatOpenAI(model="gpt-3.5-turbo")
    for feedback_type, feedback_list in feedbacks.items():
        for feedback in feedback_list:
            ai_cx_response = openai_client.invoke({"feedback": feedback})
            print(ai_cx_response.content)
            responses.append({
                "feedback": feedback,
                "ai_response": ai_cx_response.content,
                "annotation": "",  # Leaving it empty for now, we'll edit straight into json
            })

    with open("ai-responses-raw.json", "w") as f:
        json.dump(responses, f, indent=4)


# # Step 1: Generate responses to customer feedback by AI
# respond_to_customer_feedback()


def load_annotated_responses(file_path="ai-responses-annotated.json"):
    with open(file_path, "r") as file:
        return json.load(file)


def generate_refined_responses():
    annotated_responses = load_annotated_responses()
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{feedback_input}"),
            ("ai", "{response_output}"),
        ]
    )
    few_shots_examples = []
    for response in annotated_responses:
        if response["annotation"] == "good":  # Filter or use all depending on your strategy
            few_shots_examples.append(
                {
                    "feedback_input": response["feedback"],
                    "response_output": response["ai_response"],
                }
            )

    few_shot_template = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=few_shots_examples
    )
    final_template = ChatPromptTemplate.from_messages([
        ("system", "You are a customer service representative for WidgetWorld, a company that manufactures widgets. A customer has left feedback about their experience with WidgetWorld's widgets. Please respond to the feedback. Be polite and professional, even if the customer sounds unhappy or angry. Empathise with the customer. Keep your response concise and to the point."),
        few_shot_template,
        ("human", "{feedback}"),
    ])

    openai_client = final_template | ChatOpenAI(model="gpt-3.5-turbo")

    # In the annotated responses, we have removed the boring first line "Thank you for your kind words!" or "Thank you for feedback" from for positive review response. So it should not generate that kinda line anymore for a positive feedback.
    test_feedback = "Impressed by WidgetWorld's attention to detail and overall UX. Their widgets are a such a time saver."
    ai_cx_response = openai_client.invoke({"feedback": test_feedback})
    print(f"Feedback: {test_feedback}")
    print(f"Refined AI Response: {ai_cx_response.content}")


# Step 2: Load annotated responses from json file and test refined response
generate_refined_responses()
