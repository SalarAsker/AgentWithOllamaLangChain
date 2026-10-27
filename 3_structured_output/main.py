from pydantic_example import FeedbackAnalysis

result = FeedbackAnalysis(
    summary = "This is a sample feedback summary.",
    sentiment="positive",
    problems=["Issue 1", "Issue 2"],
    follow_up_required=True
)

if __name__ == "__main__":
    print(result)
    print(result.summary)
    print(result.sentiment)
    print(result.problems)
    print(result.follow_up_required)