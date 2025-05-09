## uc\00015_uc.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<useCase id="dronology-SC10">
    <name>Lease Airspace for Planned Flight Path</name>
    <description>All UAVs must receive airspace authorization prior to commencing flight to a waypoint. Collisions are prevented through a multi-faceted approach of collision avoidance for unplanned violations of minimum separation distance, and just-in-time airspace reservations from the UAVs current coordinates to a target coordinate.</description>

    <actors>
        <actor>Semi-Autonomous UAV</actor>
        <actor>Air Traffic Control</actor>
    </actors>

    <preconditions>
        <precondition>The UAV is either armed and ready-to-fly or already in the air.</precondition>
    </preconditions>

    <successEndConditions>
        <condition>UAVs always receive permission from ATC before commencing flight to a waypoint.</condition>
    </successEndConditions>

    <failureEndConditions>
        <condition>UAVs fly to a waypoint without authorization creating the potential for a mid-air collision.</condition>
    </failureEndConditions>

    <trigger>The UAV needs to fly to a waypoint or needs some space to perform an action.</trigger>

    <mainSequence>
        <step id="S1">The UAV calculates the airspace needed for its next action.</step>
        <step id="S2">The UAV requests permission from ATC to reserve the airspace identified.</step>
        <step id="S3">ATC determines that the airspace can be reserved.</step>
        <step id="S4">ATC reserves the airspace.</step>
        <step id="S5">ATC releases any airspace reservations previously held by the UAV.</step>
        <step id="S6">ATC grants the UAV an exclusive lease of the airspace.</step>
        <step id="S7">The UAV completes its action and goes to step 1.</step>
    </mainSequence>

    <errorSteps>
        <esteps id="E1" start="S3">
            <description>ATC determines that the airspace is not currently available.</description>
            <step id="E1S1">ATC finds all reservations held by other UAVs that share some altitude with the requested airspace.</step>
            <step id="E1S2">ATC finds all restricted airspace that shares some altitude and is less than 1000 meters from the requested airspace.</step>
            <step id="E1S3">ATC denies the request for airspace and attaches both the list of other reservations and the list of restricted airspaces.</step>
            <step id="E1S4">The UAV analyzes the attached lists and selects an alternative action among:</step>
            <step id="E1S5">If the action is impossible because of restricted airspace:</step>
            <step id="E1S6">If the next action is to fly to a waypoint, and the UAV determines that meaningful progress is possible then:</step>
            <step id="E1S7">The UAV picks a new waypoint that moves it closer to the target.</step>
            <step id="E1S8">The use case continues at step 1.</step>
            <step id="E1S9">If progress on the next action is possible, then:</step>
            <step id="E1S10">The UAV decides on a new next action.</step>
            <step id="E1S11">The use case continues at step 1.</step>
            <step id="E1S12">If progress is not possible, and the UAV is in the air, then:</step>
            <step id="E1S13">The UAV requests a small amount of airspace to wait within. This new airspace must fit inside the airspace that the UAV has already reserved. The UAV is guaranteed to get a lease on the new airspace in case it fits within its current airspace.</step>
            <step id="E1S14">The UAV waits for a random time interval (&lt; 5 seconds) and repeats its request for airspace.</step>
            <step id="E1S15">The use case continues at step 3.</step>
            <step id="E1S16">If the UAV is on the ground, awaiting takeoff, and progress is not possible, then:</step>
            <step id="E1S17">The UAV waits for a random time interval (&lt; 5 seconds) and repeats its request for airspace.</step>
            <step id="E1S18">The use case continues at step 3.</step>
        </esteps>
    </errorSteps>
</useCase>

```
## uc\00015_uc.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<useCase id="dronology-SC10">
    <name>Lease Airspace for Planned Flight Path</name>
    <description>All UAVs must receive airspace authorization prior to commencing flight to a waypoint. Collisions are prevented through a multi-faceted approach of collision avoidance for unplanned violations of minimum separation distance, and just-in-time airspace reservations from the UAVs current coordinates to a target coordinate.</description>

    <actors>
        <actor>Semi-Autonomous UAV</actor>
        <actor>Air Traffic Control</actor>
    </actors>

    <preconditions>
        <precondition>The UAV is either armed and ready-to-fly or already in the air.</precondition>
    </preconditions>

    <successEndConditions>
        <condition>UAVs always receive permission from ATC before commencing flight to a waypoint.</condition>
    </successEndConditions>

    <failureEndConditions>
        <condition>UAVs fly to a waypoint without authorization creating the potential for a mid-air collision.</condition>
    </failureEndConditions>

    <trigger>The UAV needs to fly to a waypoint or needs some space to perform an action.</trigger>

    <mainSequence>
        <step id="S1">The UAV calculates the airspace needed for its next action.</step>
        <step id="S2">The UAV requests permission from ATC to reserve the airspace identified.</step>
        <step id="S3">ATC determines that the airspace can be reserved.</step>
        <step id="S4">ATC reserves the airspace.</step>
        <step id="S5">ATC releases any airspace reservations previously held by the UAV.</step>
        <step id="S6">ATC grants the UAV an exclusive lease of the airspace.</step>
        <step id="S7">The UAV completes its action and goes to step 1.</step>
    </mainSequence>

    <errorSteps>
        <esteps id="E1" start="S3">
            <description>ATC determines that the airspace is not currently available.</description>
            <step id="E1S1">ATC finds all reservations held by other UAVs that share some altitude with the requested airspace.</step>
            <step id="E1S2">ATC finds all restricted airspace that shares some altitude and is less than 1000 meters from the requested airspace.</step>
            <step id="E1S3">ATC denies the request for airspace and attaches both the list of other reservations and the list of restricted airspaces.</step>
            <step id="E1S4">The UAV analyzes the attached lists and selects an alternative action among:</step>
            <step id="E1S5">If the action is impossible because of restricted airspace:</step>
            <step id="E1S6">If the next action is to fly to a waypoint, and the UAV determines that meaningful progress is possible then:</step>
            <step id="E1S7">The UAV picks a new waypoint that moves it closer to the target.</step>
            <step id="E1S8">The use case continues at step 1.</step>
            <step id="E1S9">If progress on the next action is possible, then:</step>
            <step id="E1S10">The UAV decides on a new next action.</step>
            <step id="E1S11">The use case continues at step 1.</step>
            <step id="E1S12">If progress is not possible, and the UAV is in the air, then:</step>
            <step id="E1S13">The UAV requests a small amount of airspace to wait within. This new airspace must fit inside the airspace that the UAV has already reserved. The UAV is guaranteed to get a lease on the new airspace in case it fits within its current airspace.</step>
            <step id="E1S14">The UAV waits for a random time interval (&lt; 5 seconds) and repeats its request for airspace.</step>
            <step id="E1S15">The use case continues at step 3.</step>
            <step id="E1S16">If the UAV is on the ground, awaiting takeoff, and progress is not possible, then:</step>
            <step id="E1S17">The UAV waits for a random time interval (&lt; 5 seconds) and repeats its request for airspace.</step>
            <step id="E1S18">The use case continues at step 3.</step>
        </esteps>
    </errorSteps>
</useCase>

```
seq ![](00130_seq_gen.png)
seq ![](00015_uc.png)
## uc\00018_uc.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<useCase id="dronology-EC1">
    <name>Loss of Signal</name>
    <description>Without an onboard pilot, there is a significant reliance on the command and control link, and a greater emphasis on the loss of functionality associated with lost of signal. This exception case occurs when such a loss of signal occurs. Most UAVs have some degree of onboard autonomy - varying between the ability to continue flight to the currently assigned waypoint, execute failsafe mechanisms, and/or complete an entire mission autonomously.</description>

    <actors>
        <actor>Ground Control System</actor>
        <actor>RPIC</actor>
        <actor>Unmanned Aerial Vehicle</actor>
        <actor>Air Traffic Control</actor>
    </actors>

    <preconditions>
        <precondition>The UAV is in the air and has a command and control link to one or more ground control stations.</precondition>
        <precondition>A [failsafe] action has been established to activate RTL (Return to Launch) at a predefined altitude in case of loss-of-signal.</precondition>
    </preconditions>

    <successEndConditions>
        <condition>Signal is re-established and the flight continues.</condition>
        <condition>The UAV is landed safely despite the loss of signal.</condition>
        <condition>The UAV completes its mission autonomously despite loss of signal (currently not authorized by FAA).</condition>
    </successEndConditions>
    <failureEndConditions>
        <condition>The UAV is lost and/or crashes.</condition>
    </failureEndConditions>

    <trigger>The UAV is in flight and experiences a loss-of-signal event for greater than [loss_of_signal_threshold_seconds].</trigger>

    <mainSequence>
        <step id="S1">The UAV detects and responds to loss-of-signal.</step>
        <step id="S1.1">The UAV detects that it has lost communication with the ground control station.</step>
        <step id="S1.2">The failsafe mechanism is activated, and the UAV autonomously returns to launch (RTL) at its designated RTL altitude.</step>

        <step id="S2">DroneResponse responds to the loss-of-signal event.</step>
        <step id="S2.1">The runtime monitoring system detects the loss of signal event for the UAV.</step>
        <step id="S2.2">The runtime monitoring system raises an alert.</step>
        <step id="S2.3">The alert is displayed in the UI to notify the RPIC of the loss-of-signal event.</step>

        <step id="S3">The RPIC maintains visual line of sight with the UAV and observes that it has transitioned to RTL mode.</step>
        <step id="S4">If necessary, the UAV suspends the remainder of its mission or moves other UAVs out of the way of the returning UAV.</step>
    </mainSequence>

    <errorSteps>
        <esteps id="E1" start="S1">
            <description>No failsafe mechanism has been established onboard the UAV.</description>
            <step id="E1S1">If the UAV flies outside an established Geofence, the Geofence_failsafe is activated.</step>
        </esteps>
        <esteps id="E2" start="S2">
            <description>Multiple UAVs experience a simultaneous loss of signal and activate RTL simultaneously.</description>
            <step id="E2S1">Each UAV has a unique altitude assigned and returns home safely, avoiding collisions during RTL (optimistic scenario).</step>
            <step id="E2S2">Each UAV does not have a unique altitude assigned, increasing the risk of collisions during simultaneous RTL events.</step>
        </esteps>
        <esteps id="E3" start="S1.2">
            <description>Signal is re-established during RTL.</description>
            <step id="E3S1">ATC runs a diagnostic of each UAV's flight path and attempts to reserve airspace for the entire RTL route.</step>
            <step id="E3S2">When airspace cannot be reserved for the entire route, the UAV reserves airspace for as much of the route as available. The UAV mode is reset to FLYING.</step>
            <step id="E3S3">When the UAV reaches an intermediate waypoint, it attempts to reserve airspace for the remainder of the flight.</step>
            <step id="E3S4">Steps 4.2 and 4.3 are repeated until the UAV receives clearance to return home.</step>
        </esteps>
    </errorSteps>
</useCase>

```
seq ![](00155_seq_gen.png)
seq ![](00018_uc.png)
## uc_gen\00185_uc_gen.xml
```xml
<useCase id="1">
 <name>Add New Material Information</name>
 <actors>
  <actor>Manager</actor>
 </actors>
 <mainSequence>
  <step id="S1">Manager adds new material information</step>
  <step id="S2">ManagerPage invokes ManagerMaterialController to add new material information by calling addMaterial method with newMaterialInfo parameter</step>
  <step id="S3">ManagerMaterialController calls MaterialService to add new material information by invoking addMaterial method with newMaterialInfo parameter</step>
  <step id="S4">MaterialService requests MaterialRepository to save new material information by calling save method with newMaterialInfo parameter</step>
  <step id="S5">MaterialRepository executes insert query in the Database to save new material information</step>
  <step id="S6">Database confirms successful insertion of new material information</step>
  <step id="S7">MaterialRepository confirms successful insert to MaterialService</step>
  <step id="S8">MaterialService confirms successful insert to ManagerMaterialController</step>
  <step id="S9">ManagerMaterialController confirms successful insert to ManagerPage</step>
  <step id="S10">ManagerPage displays confirmation of successful addition</step>
 </mainSequence>
</useCase>
```
seq ![](00023_seq.png)
seq ![](00185_uc_gen.png)
## uc_gen\00243_uc_gen.xml
```xml
<useCase id="UC1">
    <name>Manage Game Instructions</name>
    <actors>
        <actor>Player</actor>
    </actors>
    <preconditions>
        <precondition>The game interface is open.</precondition>
    </preconditions>
    <successEndConditions>
        <condition>The player successfully adds and edits game instructions.</condition>
    </successEndConditions>
    <failureEndConditions>
        <condition>The player fails to add or edit game instructions.</condition>
    </failureEndConditions>
    <mainSequence>
        <step id="S1">Player opens the game interface.</step>
        <step id="S2">Game interface loads the map and robot positions.</step>
        <step id="S3">Game controller initializes the game state.</step>
        <step id="S4">Game controller displays the initial map and robot positions.</step>
        <step id="S5">Player clicks on the edit instructions button.</step>
        <step id="S6">Game interface enters the instruction editing interface.</step>
        <step id="S7">Player selects an instruction.</step>
        <step id="S8">Game interface adds the selected instruction.</step>
        <step id="S9">Player continues selecting and adding instructions.</step>
        <step id="S10">Game interface requests to continue selecting and adding instructions.</step>
        <step id="S11">Player selects an instruction.</step>
        <step id="S12">Game interface adds the selected instruction.</step>
        <step id="S13">Player continues selecting and adding instructions.</step>
        <step id="S14">Game interface completes the instruction editing.</step>
        <step id="S15">Player clicks on the start button.</step>
        <step id="S16">Game interface starts the game.</step>
        <step id="S17">Game logic begins executing the instruction sequence.</step>
        <step id="S18">Game controller updates the game status.</step>
        <step id="S19">Player exits the game.</step>
        <step id="S20">Game interface handles the game exit.</step>
    </mainSequence>
</useCase>
```
