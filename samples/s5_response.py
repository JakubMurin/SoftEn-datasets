{
    "query": 'Generate use case for this sequence diagram without any comments:\n@startuml\n\nparticipant controller as "RouteController"\nparticipant template as "Template"\nparticipant view as "MapView"\nparticipant trip as "Trip"\nparticipant location as "Location"\nparticipant service as "Service"\nparticipant google as "GoogleService"\n\n\ncreate trip\nview -> trip: currentTrip\ncreate location\ntrip -> location\n\ncontroller -> service: getActiveTrips\ncontroller -> service: getStops\ncontroller -> view: trip\ncontroller -> template: data(currentTrip, activeTrips, stops)\n\n[-> template: rendered\nactivate template\n  template -> view: showMap\n  template -> google: addAutocomplete(input, view.setCurrentTripTo)\ndeactivate template\n\ntemplate -\\ view: data\nactivate view\n  template \\-- view: trip\ndeactivate view\ntemplate -> trip: getFromAddress\n\nalt Set from location from browser\n  [-> view: setCurrentTripFrom(latlng, null)\n  activate view\n  view -> view: clarifyLocation(latlng, null)\n  activate view\n  view -\\ google: geocode(latlng, trip.from.setAddress)\n  alt reactive\n    view -> location: setLatLng\n    template -> location: getLatLng\n  end\n  deactivate view\n  deactivate view\n  alt reactive\n    location \\-- google: setAddress\n    activate location\n    template -> location: getAddress\n    deactivate location\n  end\nend\n\nalt Autocomplete address\n  [-> google: typeahead toAddress\n  view <- google: setCurrentTripTo(latlng, address)\n  activate view\n  view -> view: clarifyLocation(latlng, address)\n  activate view\n  view -> location: setLatLng\n  view -> location: address\n  deactivate view\n  deactivate view\nend\n\nalt Drop marker\n  view -> view: setCurrentTripTo(latlng, null)\n  note left: when to update address?\n  activate view\n  view -> view: clarifyLocation(latlng, null)\n  activate view\n  view -\\ google: geocode(latlng, trip.to.setAddress)\n  alt reactive\n    view -> location: setLatLng\n    template -> location: getLatLng\n  end\n  deactivate view\n  deactivate view\n  alt reactive\n    location \\-- google: setAddress\n    activate location\n    template -> location: getAddress\n    deactivate location\n  end\nend\n\n[-> template: click .saveTrip\ntemplate -> service: saveTrip(trip)\nservice -> service: Are to / from locations set?\n\n@enduml',
    "response": ChatCompletion(
        id="chatcmpl-AdFKa9KCqTB8urXQ2LkZeElwqinpF",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                logprobs=None,
                message=ChatCompletionMessage(
                    content='<useCase id="1">\n   <mainSequence>\n      <step>create trip</step>\n      <step>view -> trip: currentTrip</step>\n      <step>create location</step>\n      <step>trip -> location</step>\n      <step>controller -> service: getActiveTrips</step>\n      <step>controller -> service: getStops</step>\n      <step>controller -> view: trip</step>\n      <step>controller -> template: data(currentTrip, activeTrips, stops)</step>\n   </mainSequence>\n   <alternativeSteps>\n      <astep>[-> template: rendered</astep>\n      <astep>template -> view: showMap</astep>\n      <astep>template -> google: addAutocomplete(input, view.setCurrentTripTo)</astep>\n      <astep>[-> view: setCurrentTripFrom(latlng, null)</astep>\n      <astep>view -> view: clarifyLocation(latlng, null)</astep>\n      <astep>view -\\ google: geocode(latlng, trip.from.setAddress)</astep>\n      <astep>location \\-- google: setAddress</astep>\n      <astep>[-> google: typeahead toAddress</astep>\n      <astep>view <- google: setCurrentTripTo(latlng, address)</astep>\n      <astep>view -> view: clarifyLocation(latlng, address)</astep>\n      <astep>view -> location: setLatLng</astep>\n      <astep>view -> location: address</astep>\n      <astep>view -> view: setCurrentTripTo(latlng, null)</astep>\n      <astep>view -> view: clarifyLocation(latlng, null)</astep>\n      <astep>view -\\ google: geocode(latlng, trip.to.setAddress)</astep>\n   </alternativeSteps>\n</useCase>',
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
            )
        ],
        created=1733917088,
        model="gpt-3.5-turbo-0125",
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=405,
            prompt_tokens=673,
            total_tokens=1078,
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
