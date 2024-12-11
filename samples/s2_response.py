{
    "query": 'Generate use case for this sequence diagram without any comments:\n    @startuml\n\nparticipant WorkflowKernel order 1\nparticipant Model order 2\ncollections Plugin order 50\ncollections Service order 99\n\nbox "Workflow Engine" #White\n\tparticipant WorkflowKernel \n\tparticipant Model\n\tparticipant Plugin\n\nend box\n\nbox "Microservice" #LightBlue\n\tparticipant Service\nend box\n\nhide footbox\n\nactivate WorkflowKernel\n\nWorkflowKernel -> WorkflowKernel: register Plug-In \n\nWorkflowKernel -> Model: load BPMN Event\nactivate Model\nModel --> WorkflowKernel:\ndeactivate Model\n\n\n\nWorkflowKernel -> Plugin: init Plug-In\nactivate Plugin\nWorkflowKernel -> Plugin: run Plug-In\n\nPlugin -->o Service: external API Call\nactivate Service\nService --> Plugin\ndeactivate Service\n\nWorkflowKernel -> Plugin: close Plug-In\ndeactivate Plugin\n\n\n\ndeactivate WorkflowKernel\n\n@enduml',
    "response": ChatCompletion(
        id="chatcmpl-AdFFaSQ6OgaWfkEPeWU0w7CH0ayNo",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                logprobs=None,
                message=ChatCompletionMessage(
                    content='<useCase id="1">\n   <mainSequence>\n      <step id="1">Register Plug-In</step>\n      <step id="2">Load BPMN Event</step>\n      <step id="3">Initialize Plug-In</step>\n      <step id="4">Run Plug-In</step>\n      <step id="5">Close Plug-In</step>\n   </mainSequence>\n   <alternativeSteps>\n      <astep id="6">N/A</astep>\n   </alternativeSteps>\n   <errorSteps>\n      <estep id="7">External API Call</estep>\n   </errorSteps>\n</useCase>',
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
            )
        ],
        created=1733916778,
        model="gpt-3.5-turbo-0125",
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=136,
            prompt_tokens=328,
            total_tokens=464,
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
