### basic
<useCase id="001">
   <description>Register Resource</description>
   <mainSequence>
      <step id="1">RegisterResourceRequest(type, name, inputs, options)</step>
      <step id="2">RegisterResourceEvent(type, name, inputs, options)</step>
      <step id="3">CheckRequest(type, inputs, old inputs)</step>
      <step id="4">CheckResponse(inputs', failures)</step>
      <step id="5">DiffRequest(type, inputs', old state)</step>
      <step id="6">DiffResponse(diffs)</step>
      <step id="7">SameStep(inputs', old state, options)</step>
      <step id="8">done(old state)</step>
      <step id="9">RegisterResourceResponse(urn, ID, old state)</step>
   </mainSequence>
</useCase>

======================
### Suggest a better version of the question in quotes to use instead and show it at beggining of response.

"Create a use case based on the following sequence diagram without any comments:"

<useCase id="1">
  <mainSequence>
    <step id="1">RegisterResourceRequest(type, name, inputs, options) from Language SDK to Resource Monitor</step>
    <step id="2">RegisterResourceEvent(type, name, inputs, options) from Resource Monitor to Step Generator</step>
    <step id="3">CheckRequest(type, inputs, old inputs) from Step Generator to Resource Provider</step>
    <step id="4">CheckResponse(inputs', failures) from Resource Provider to Step Generator</step>
    <step id="5">DiffRequest(type, inputs', old state) from Step Generator to Resource Provider</step>
    <step id="6">DiffResponse(diffs) from Resource Provider to Step Generator</step>
    <step id="7">SameStep(inputs', old state, options) from Step Generator to Step Executor</step>
    <step id="8">done(old state) from Step Executor to Resource Monitor</step>
    <step id="9">RegisterResourceResponse(urn, ID, old state) from Resource Monitor to Language SDK</step>
  </mainSequence>
</useCase>

=======================
example_use_case = ""
with open(r"C:\Users\Jakub\SoftEn-datasets\data\usecases\01.xml", "r") as file:
    example_use_case = file.read()
    
dtd = ""
with open(dtd_scheme_path, "r") as file:
    dtd = file.read()

promt_ctx = [{"role": "user", "content": f"Here is example of sequence diagram: {example_diagam}"},
             {"role": "user", "content": f"Here is dtd scheme for usecase: {dtd}"},
             {"role": "user", "content": "How whould you formulate prompt to get sequence diagram in format as example from usecase in dtd scheme?"}]

result = context.execute_query("a", promt_ctx)[0]
print(f"Tokens used:\tprompt_tokens: {result["usage"]["prompt_tokens"]} + completion_tokens: {result["usage"]["completion_tokens"]} = {result["usage"]["total_tokens"]}")
print(result["choices"][0]["message"]["content"])

# response

To prompt for a sequence diagram in the format specified in the usecase DTD scheme, you can create a structured prompt that includes all the necessary elements. Here is how you could formulate the prompt:

"Please provide a sequence diagram that follows the structure outlined in the usecase DTD scheme. The sequence diagram should include the following elements:

1. Actor: The actor initiating the sequence.
2. System: The system being interacted with.
3. Database: The database being queried.
4. Request Data: The action of requesting data.
5. Query Data: The action of querying data from the database.
6. Process Data: The action of processing the data.
7. Return Data: The data returned.
8. Display Data: The data being displayed.
9. Error: Handling of errors if data is not found.

Please ensure that the sequence diagram clearly shows the flow of actions between the actor, system, and database, as well as any error handling steps that may be required. Thank you."

==============

promt_ctx = [{"role": "user", "content": f"Here is example of sequence diagram: {example_diagam}"},
             {"role": "user", "content": f"Here is dtd scheme for usecase: {dtd}"},
             {"role": "user", "content": "How whould you formulate prompt to get sequence diagram in format plantuml as example from usecase in dtd scheme? Expected behaviour: I would provide usecase, prompt and you reply only with sequence diagram in plantuml"}]

To generate a sequence diagram in PlantUML format based on the provided use case defined in the DTD scheme, the prompt could be formulated as follows:

---

**Prompt:**
Please provide the use case details according to the DTD scheme. Include the name, description, actors, preconditions, success end conditions, failure end conditions, trigger, main sequence steps, alternative steps, and error steps.

---

By providing the use case information as requested in the prompt, a sequence diagram in PlantUML format can then be created based on the input. Let me know if you have a specific use case to work on.

================
promt_ctx = [{"role": "user", "content": f"Here is example of sequence diagram: {example_diagam}"},
             {"role": "user", "content": f"Here is dtd scheme for usecase: {dtd}"},
             {"role": "user", "content": "How whould you formulate prompt to get sequence diagram in format plantuml as example from usecase in dtd scheme? Expected behaviour: I would provide usecase, prompt and you reply only with sequence diagram in plantuml"},
             {"role": "assistant", "content": """
              To generate a sequence diagram in PlantUML format based on the provided use case defined in the DTD scheme, the prompt could be formulated as follows:

---

**Prompt:**
Please provide the use case details according to the DTD scheme. Include the name, description, actors, preconditions, success end conditions, failure end conditions, trigger, main sequence steps, alternative steps, and error steps.

---

By providing the use case information as requested in the prompt, a sequence diagram in PlantUML format can then be created based on the input. Let me know if you have a specific use case to work on."""},
             {"role": "user", "content": "No, I expect prompt similar to this: Create a use case based on the following sequence diagram without any comments"}
            ]

I'm sorry for misunderstanding. Here is the prompt tailored to your requirements:

---

**Prompt:**
Based on the following sequence diagram, create a use case without any comments.

---

Please provide the sequence diagram, and I will proceed to create the corresponding use case based on the diagram.
====================

Based on the following use case, create a sequence diagram any comments.
Based on the following use case, create a sequence diagram in plantuml without any comments.
Based on the following use case, create a sequence diagram in plantuml without any comments and last line is domain of usecase.
Based on the following use case, create a sequence diagram in plantuml without any comments and last line is domain of usecase inside {{}}.
Based on the following use case, create a sequence diagram in plantuml without any comments and response last line is domain of usecase inside {{}}

In sequence diagram if name is multiple words, put it in quotation marks
In sequence diagram if name is multiple words, put it in quotation marks and give diagram title
In sequence diagram if name of participant is multiple words, put it in quotation marks and give diagram title
In sequence diagram if name of element is multiple words, put it in quotation marks and give diagram title