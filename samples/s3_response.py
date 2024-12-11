{
    "query": 'Generate use case for this sequence diagram without any comments:\n@startuml\n\nactor Client\nparticipant Envoy\nparticipant "Authorization Server"\nparticipant "Authorization Provider"\nparticipant "Application Server"\n\nClient -> Envoy: HTTP request\nactivate Envoy\n\nEnvoy -> "Authorization Server": Check request\nactivate "Authorization Server"\n\n"Authorization Server" -> "Authorization Provider": Authorization request\nactivate "Authorization Provider"\n"Authorization Provider" -> "Authorization Provider": Authorize request\n"Authorization Provider" -> "Authorization Server": Authorization response (approved)\ndeactivate "Authorization Provider"\n\n"Authorization Server" -> Envoy: Check response (approved)\ndeactivate "Authorization Server"\n\nEnvoy -> "Application Server": HTTP request\nactivate "Application Server"\n"Application Server" -> "Application Server": Process request\n"Application Server" -> Envoy: HTTP response\ndeactivate "Application Server"\n\nEnvoy -> Client: HTTP response\ndeactivate Envoy\n\n@enduml',
    "response": ChatCompletion(
        id="chatcmpl-AdFHFkYPsdaVQL6bLiadk30lJsWSv",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                logprobs=None,
                message=ChatCompletionMessage(
                    content='<useCase id="1">\n   <description>Client requests access to application through Envoy</description>\n   <mainSequence>\n      <step>Envoy forwards HTTP request to Authorization Server</step>\n      <step>Authorization Server checks request</step>\n      <step>Authorization Server sends authorization request to Authorization Provider</step>\n      <step>Authorization Provider authorizes request and sends approval to Authorization Server</step>\n      <step>Authorization Server verifies approval and sends response to Envoy</step>\n      <step>Envoy forwards HTTP request to Application Server</step>\n      <step>Application Server processes request and sends HTTP response to Envoy</step>\n      <step>Envoy returns HTTP response to Client</step>\n   </mainSequence>\n</useCase>',
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
            )
        ],
        created=1733916881,
        model="gpt-3.5-turbo-0125",
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=159,
            prompt_tokens=338,
            total_tokens=497,
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
