# C4 Architecture Diagrams for HearSee Application

## Introduction

This document presents a comprehensive C4 architecture visualization for the HearSee web application. The C4 model provides a hierarchical approach to describing software architecture at different levels of abstraction, making it easier to communicate and understand the system structure.

The diagrams follow the standard C4 notation:
- **Person**: End users of the system (represented as stick figures)
- **System**: A high-level software system (represented as a box)
- **Container**: An application or data store (represented as a box within the system)
- **Component**: A grouping of related functionality (represented as a box within a container)
- **Code**: Classes, interfaces, and their relationships (represented as UML-style diagrams - not included in this document)

## Level 1: System Context Diagram

The System Context diagram shows HearSee and its relationships with users and external systems.

```mermaid
graph TD
    User[User<br/>A person using the HearSee application] -- Uses --> HearSee[HearSee<br/>Multimodal Chat Application]
    HearSee -- Uses --> ReplicateAPI[Replicate API<br/>Provides AI model inference]
    
    %% Styling
    classDef person fill:#08427B,stroke:#052E56,color:#fff
    classDef system fill:#1168BD,stroke:#0B4884,color:#fff
    classDef external fill:#999999,stroke:#6B6B6B,color:#fff
    
    class User person
    class HearSee system
    class ReplicateAPI external
```

### Description

The System Context diagram illustrates:

- **Users** interact directly with the HearSee application through a web interface
- **HearSee** is the core system providing multimodal chat capabilities with vision and voice features
- **Replicate API** is an external service that provides AI model inference for:
  - Vision-language understanding (Qwen VL model)
  - Text-to-speech conversion (Kokoro TTS model)

## Level 2: Container Diagram

The Container diagram shows the high-level technical building blocks of the HearSee system.

```mermaid
graph TD
    User[User<br/>A person using the HearSee application] -- Uses --> WebUI[Web UI<br/>Gradio-based interactive interface]
    
    subgraph HearSee[HearSee Application]
        WebUI -- Sends requests to --> AppCore[Application Core<br/>Main application logic]
        AppCore -- Uses --> Services[Services<br/>Modular service components]
        AppCore -- Uses --> Utils[Utilities<br/>Helper functions and tools]
        Services -- Uses --> Config[Configuration<br/>Application settings]
        Utils -- Uses --> Config
    end
    
    Services -- Makes API calls to --> ReplicateAPI[Replicate API<br/>Provides AI model inference]
    
    %% Styling
    classDef person fill:#08427B,stroke:#052E56,color:#fff
    classDef container fill:#438DD5,stroke:#2E6295,color:#fff
    classDef external fill:#999999,stroke:#6B6B6B,color:#fff
    
    class User person
    class WebUI,AppCore,Services,Utils,Config container
    class ReplicateAPI external
```

### Description

The Container diagram shows:

- **Web UI**: A Gradio-based web interface that provides interactive components for users
- **Application Core**: The main application logic that coordinates between UI and services
- **Services**: Modular components that handle specific functionality:
  - Image processing
  - AI model integration via Replicate
  - Text-to-speech conversion
- **Utilities**: Helper functions for image processing, logging, and validation
- **Configuration**: Centralized application settings and constants
- **Replicate API**: External service providing AI model inference capabilities

## Level 3: Component Diagram

The Component diagram breaks down the containers into their principal structural elements.

```mermaid
graph TD
    User[User<br/>A person using the HearSee application] -- Uses --> WebUI[Web UI]
    
    subgraph WebUI[Web UI Container]
        ChatInterface[Chat Interface<br/>Main chat UI components]
        GuideInterface[Guide Interface<br/>Help documentation]
        UIComponents[UI Components<br/>Reusable UI elements]
        
        ChatInterface -- Uses --> UIComponents
        GuideInterface -- Uses --> UIComponents
    end
    
    subgraph AppCore[Application Core Container]
        AppMain[App Main<br/>Entry point and orchestration]
        EventHandlers[Event Handlers<br/>UI event processing]
        
        AppMain -- Configures --> EventHandlers
    end
    
    subgraph Services[Services Container]
        ImageService[Image Service<br/>Image processing operations]
        ReplicateService[Replicate Service<br/>AI model integration]
        TTSService[TTS Service<br/>Text-to-speech operations]
        
        TTSService -- Uses --> ReplicateService
    end
    
    subgraph Utils[Utilities Container]
        ImageUtils[Image Utils<br/>Image processing utilities]
        Validators[Validators<br/>Input validation]
        Logger[Logger<br/>Logging utilities]
        
        ImageUtils -- Uses --> ImageService
        ImageUtils -- Uses --> ReplicateService
    end
    
    subgraph Config[Configuration Container]
        Settings[Settings<br/>Application constants]
        LoggingConfig[Logging Config<br/>Logger configuration]
    end
    
    ChatInterface -- Sends events to --> EventHandlers
    GuideInterface -- Provides help for --> ChatInterface
    
    EventHandlers -- Uses --> ImageService
    EventHandlers -- Uses --> ReplicateService
    EventHandlers -- Uses --> TTSService
    EventHandlers -- Uses --> ImageUtils
    EventHandlers -- Uses --> Validators
    
    ImageService -- Uses --> Settings
    ReplicateService -- Uses --> Settings
    TTSService -- Uses --> Settings
    Logger -- Configured by --> LoggingConfig
    
    ReplicateService -- Makes API calls to --> ReplicateAPI[Replicate API]
    
    %% Styling
    classDef person fill:#08427B,stroke:#052E56,color:#fff
    classDef component fill:#85BBF0,stroke:#5D82A8,color:#000
    classDef external fill:#999999,stroke:#6B6B6B,color:#fff
    
    class User person
    class ChatInterface,GuideInterface,UIComponents,AppMain,EventHandlers,ImageService,ReplicateService,TTSService,ImageUtils,Validators,Logger,Settings,LoggingConfig component
    class ReplicateAPI external
```

### Description

The Component diagram details:

- **Web UI Container**:
  - **Chat Interface**: Main chat UI components and layout
  - **Guide Interface**: Help documentation and user guidance
  - **UI Components**: Reusable UI elements shared across interfaces

- **Application Core Container**:
  - **App Main**: Entry point and application orchestration
  - **Event Handlers**: Processing of UI events and coordination of services

- **Services Container**:
  - **Image Service**: Image processing operations (conversion, validation)
  - **Replicate Service**: Integration with Replicate API for AI models
  - **TTS Service**: Text-to-speech operations and audio handling

- **Utilities Container**:
  - **Image Utils**: Higher-level image processing utilities
  - **Validators**: Input validation functions
  - **Logger**: Logging utilities for application monitoring

- **Configuration Container**:
  - **Settings**: Application constants and configuration values
  - **Logging Config**: Logger configuration settings



## Conclusion

These C4 architecture diagrams provide a comprehensive view of the HearSee application from different levels of abstraction:

1. **System Context**: Shows the application in relation to its users and external systems
2. **Container**: Illustrates the high-level technical building blocks
3. **Component**: Details the principal structural elements within each container
4. **Code**: Presents key classes and their relationships (not shown in this diagram file)