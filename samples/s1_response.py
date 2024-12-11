{
    "query": 'Generate use case for this sequence diagram without any comments:\n    @startuml\nparticipant "Language SDK" order 10\nbox "Engine"\nparticipant "Resource Monitor" order 15\nparticipant "Step Generator" order 20\nparticipant "Step Executor" order 25\nend box\nparticipant "Resource Provider" order 30\n\n"Language SDK" -> "Resource Monitor" ++ : RegisterResourceRequest(type, name, inputs, options)\n"Resource Monitor" -> "Step Generator" ++ : RegisterResourceEvent(type, name, inputs, options)\n"Step Generator" -> "Resource Provider" ++ : CheckRequest(type, inputs, old inputs)\n"Step Generator" <- "Resource Provider" -- : CheckResponse(inputs\', failures)\n"Step Generator" -> "Resource Provider" ++ : DiffRequest(type, inputs\', old state)\n"Step Generator" <- "Resource Provider" -- : DiffResponse(diffs)\n"Step Generator" -> "Step Executor" --++ : SameStep(inputs\', old state, options)\nnote left\n\tThis is fire-and-forget on the part of the step generator.\n\tThe step will run in parallel with steps for other resources.\nend note\n"Resource Monitor" <- "Step Executor" -- : done(old state)\n"Language SDK" <- "Resource Monitor" -- : RegisterResourceResponse(urn, ID, old tate)\n@enduml',
    "response": ChatCompletion(
        id="chatcmpl-AdEmwW9xNMCZ9ILwoikSRJh2caIvQ",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                logprobs=None,
                message=ChatCompletionMessage(
                    content='<useCase id="1">\n    <description>Registering a Resource and Executing Steps</description>\n    <mainSequence>\n        <step id="1">Language SDK registers a resource request with Resource Monitor</step>\n        <step id="2">Resource Monitor registers a resource event with Step Generator</step>\n        <step id="3">Step Generator checks the resource request with Resource Provider</step>\n        <step id="4">Resource Provider responds to Step Generator with check results</step>\n        <step id="5">Step Generator requests differences from Resource Provider</step>\n        <step id="6">Resource Provider responds to Step Generator with differences</step>\n        <step id="7">Step Generator initiates the step execution with Step Executor</step>\n        <step id="8">Step Executor completes the step execution and informs Resource Monitor</step>\n        <step id="9">Resource Monitor informs Language SDK about registration completion</step>\n    </mainSequence>\n</useCase>',
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
            )
        ],
        created=1733915002,
        model="gpt-3.5-turbo-0125",
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=205,
            prompt_tokens=424,
            total_tokens=629,
            prompt_tokens_details={"cached_tokens": 0, "audio_tokens": 0},
            completion_tokens_details={
                "reasoning_tokens": 0,
                "audio_tokens": 0,
                "accepted_prediction_tokens": 0,
                "rejected_prediction_tokens": 0,
            },
        ),
    ),
}
