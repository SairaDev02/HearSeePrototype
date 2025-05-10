# Data Flow Diagram for HearSee Application

## Introduction

This document presents a comprehensive Data Flow Diagram (DFD) for the HearSee web application following the Structured Systems Analysis and Design Method (SSADM). The DFD illustrates how data moves through the system, showing the interactions between processes, external entities, and data stores.

## SSADM DFD Notation Legend

The diagram uses standard SSADM notation:

| Symbol | Description | Visual Representation |
|--------|-------------|------------------------|
| Process | A function or transformation that processes data | Circle |
| External Entity | An external system or person that interacts with the system | Rectangle |
| Data Store | A repository where data is stored | Open-ended rectangle or parallel lines |
| Data Flow | Movement of data between elements | Labeled arrow |

## Level 1 DFD

```plantuml
@startuml HearSee Level 1 DFD
!define PROCESS circle
!define ENTITY rectangle
!define DATASTORE database

' Styling
skinparam backgroundColor white
skinparam roundCorner 15
skinparam ArrowColor black
skinparam ArrowThickness 1.5

skinparam process {
  BackgroundColor #FFA07A
  BorderColor #333333
  FontColor black
}

skinparam rectangle {
  BackgroundColor white
  BorderColor #333333
  FontColor black
}

skinparam database {
  BackgroundColor white
  BorderColor #333333
  FontColor black
}

' External Entities
ENTITY "User" as User
ENTITY "Replicate API" as ReplicateAPI

' Processes
PROCESS "1. User Interface\nManagement" as P1
PROCESS "2. Image\nProcessing" as P2
PROCESS "3. Chat\nProcessing" as P3
PROCESS "4. Vision Model\nIntegration" as P4
PROCESS "5. Text-to-Speech\nProcessing" as P5
PROCESS "6. System\nConfiguration" as P6

' Data Stores
DATASTORE "D1: Temporary Files" as DS1
DATASTORE "D2: Session State" as DS2

' Data Flows - User to System
User --> P1 : Image Upload
User --> P1 : Text Input
User --> P1 : TTS Settings
User --> P1 : UI Commands

' Data Flows - System to User
P1 --> User : Image Display
P1 --> User : Text Response
P1 --> User : Audio Playback
P1 --> User : Status Updates

' Data Flows - Internal Processes
P1 --> P2 : Image Data
P1 --> P3 : User Message
P1 --> P5 : Voice Type, Speed
P1 --> P2 : Command Type
P1 --> P3 : Command Type

P2 --> P4 : Processed Image
P2 --> P3 : Image Metadata

P3 --> P4 : Prompt + Context
P3 --> P1 : Response Text
P3 --> P5 : Text for TTS

P4 --> ReplicateAPI : Vision API Request
ReplicateAPI --> P4 : Vision API Response
P4 --> P3 : Model Response

P5 --> ReplicateAPI : TTS API Request
ReplicateAPI --> P5 : TTS Audio URL
P5 --> P1 : Audio File Path

' Data Flows - Data Stores
P5 --> DS1 : Store Audio File
DS1 --> P5 : Retrieve Audio File

P1 --> DS2 : Update State
P2 --> DS2 : Update State
P3 --> DS2 : Update State
DS2 --> P1 : Retrieve State
DS2 --> P3 : Retrieve State

P6 --> P1 : Config Parameters
P6 --> P2 : Config Parameters
P6 --> P3 : Config Parameters
P6 --> P4 : Config Parameters
P6 --> P5 : Config Parameters
@enduml
```

### Process Descriptions

The Level 1 DFD breaks down the HearSee system into six major processes:

1. **User Interface Management**
   - Handles all user interactions through the Gradio web interface
   - Displays images, text responses, and status updates
   - Manages audio playback
   - Routes commands to appropriate processes

2. **Image Processing**
   - Validates and processes uploaded images
   - Converts images to appropriate formats (base64)
   - Extracts image metadata
   - Prepares images for AI model processing

3. **Chat Processing**
   - Manages conversation context and history
   - Formats prompts for the vision model
   - Processes model responses
   - Prepares text for TTS conversion

4. **Vision Model Integration**
   - Handles communication with Replicate API for vision models
   - Sends formatted requests with images and prompts
   - Receives and processes model responses
   - Handles API errors and retries

5. **Text-to-Speech Processing**
   - Validates TTS parameters (voice type, speed)
   - Sends TTS requests to Replicate API
   - Downloads and manages audio files
   - Provides audio files for playback

6. **System Configuration**
   - Manages application settings and parameters
   - Provides configuration values to all processes
   - Handles environment variables and defaults

### Data Store Descriptions

The data stores in the system include:

- **D1: Temporary Files**
  - Purpose: Stores downloaded audio files temporarily
  - Content: WAV audio files from TTS processing
  - Persistence: Files are deleted after use

- **D2: Session State**
  - Purpose: Maintains the current application state
  - Content: Conversation history, uploaded images, UI state
  - Persistence: In-memory during the application session

### Data Flow Descriptions

The diagram illustrates several key data flows through the system:

1. **Image Processing Flow**:
   - User uploads an image → UI Management → Image Processing → Vision Model Integration → Replicate API → Vision Model Integration → Chat Processing → UI Management → User

2. **Text Input Flow**:
   - User enters text → UI Management → Chat Processing → Vision Model Integration → Replicate API → Vision Model Integration → Chat Processing → UI Management → User

3. **TTS Processing Flow**:
   - Chat Processing provides text → TTS Processing → Replicate API → TTS Processing → Temporary Files → TTS Processing → UI Management → User

4. **Configuration Flow**:
   - System Configuration → All processes → Affects all data processing

This SSADM-compliant DFD provides a comprehensive view of how data flows through the HearSee application, from user input to external API interactions and back to user output.