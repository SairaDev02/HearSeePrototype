# HearSee Application - UML Activity Diagrams

This document contains UML activity diagrams for the key workflows in the HearSee application, a multimodal chat application with vision and voice capabilities.

## Table of Contents

1. [Image Upload Workflow](#image-upload-workflow)
2. [Chat Interaction Workflow](#chat-interaction-workflow)
3. [Text Extraction Workflow](#text-extraction-workflow)
4. [Image Captioning Workflow](#image-captioning-workflow)
5. [Image Summarization Workflow](#image-summarization-workflow)
6. [Text-to-Speech Conversion Workflow](#text-to-speech-conversion-workflow)
7. [Regenerate Response Workflow](#regenerate-response-workflow)
8. [Clear History Workflow](#clear-history-workflow)
9. [Exception Handling Workflow](#exception-handling-workflow)
10. [System Startup Workflow](#system-startup-workflow)

## Image Upload Workflow

This diagram illustrates the process of uploading an image to the HearSee application, which is the initial step required for all image-based interactions. It shows how the system validates the uploaded image, stores it in memory, and updates the UI to enable further interaction options. This workflow is critical as it establishes the foundation for all subsequent image analysis operations in the application.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ClickUpload[Click 'Upload Image' button]
        SelectImage[Select image file] --> WaitForProcessing[Wait for processing]
    end
    
    subgraph UI
        ClickUpload --> ShowFileDialog[Show file selection dialog]
        ShowFileDialog --> SelectImage
        WaitForProcessing --> DisplayImage[Display image in gallery]
        DisplayImage --> EnableButtons[Enable interaction buttons]
    end
    
    subgraph System
        EnableButtons --> ValidateImage{Validate image}
        ValidateImage -->|Valid| StoreImage[Store image in memory]
        ValidateImage -->|Invalid| ShowError[Show error message]
        StoreImage --> UpdateUIState[Update UI state]
        ShowError --> End([End])
    end
    
    UpdateUIState --> End
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Upload limited to 10MB]:::note
    Note2[Buttons enabled: Send, Extract Text, Caption, Summarize]:::note
    
    ValidateImage -.-> Note1
    EnableButtons -.-> Note2
```

## Chat Interaction Workflow

This diagram depicts the core conversational functionality of the HearSee application, showing how users can interact with the AI vision model after uploading an image. It demonstrates the complete flow from user input to AI response generation, including validation steps, API communication, and UI updates. This workflow represents the primary way users engage with the system to get information about uploaded images through natural language conversation.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| EnterMessage[Enter message in text field]
        EnterMessage --> SendMessage[Click 'Send' or press Enter]
        WaitForResponse[Wait for AI response] --> ViewResponse[View AI response]
        ViewResponse --> Decision{Continue conversation?}
        Decision -->|Yes| EnterMessage
        Decision -->|No| End([End])
    end
    
    subgraph UI
        SendMessage --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayResponse[Display response in chat]
        DisplayResponse --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateInputs{Validate inputs}
        ValidateInputs -->|Invalid| ShowError[Show error message]
        ValidateInputs -->|Valid| CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| ProcessMessage[Process message with vision model]
        ProcessMessage --> GenerateResponse[Generate AI response]
        GenerateResponse --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForResponse
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Send button disabled until image uploaded]:::note
    Note2[Uses Qwen VL model via Replicate API]:::note
    Note3[Metrics include latency and word count]:::note
    
    ImageUploaded -.-> Note1
    ProcessMessage -.-> Note2
    UpdateMetrics -.-> Note3
```

## Text Extraction Workflow

This diagram outlines the specialized workflow for extracting text from images (OCR functionality) in the HearSee application. It shows how the system processes an uploaded image specifically for text recognition, sends it to the vision model with specialized OCR prompts, and returns the extracted text to the user. This workflow is particularly useful for documents, signs, or any image containing textual information that users want to convert to editable text.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickExtract[Click 'Extract Text' button]
        WaitForProcessing[Wait for processing] --> ViewResults[View extracted text]
        ViewResults --> End([End])
    end
    
    subgraph UI
        ClickExtract --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayResults[Display extracted text in chat]
        DisplayResults --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with OCR prompt]
        CallVisionModel --> ExtractText[Extract text from image]
        ExtractText --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Extract Text button disabled until image uploaded]:::note
    Note2[Uses specialized prompt for OCR functionality]:::note
    Note3[Handles various text formats and layouts]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    ExtractText -.-> Note3
```

## Image Captioning Workflow

This diagram illustrates the process of generating descriptive captions for uploaded images. It shows how the system uses the vision model with specialized prompting to create detailed descriptions focusing on objects, people, scenery, colors, and composition. This workflow provides users with concise, objective descriptions of image content, serving as a quick way to get factual information about what appears in an image.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickCaption[Click 'Caption Image' button]
        WaitForProcessing[Wait for processing] --> ViewCaption[View image caption]
        ViewCaption --> End([End])
    end
    
    subgraph UI
        ClickCaption --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayCaption[Display caption in chat]
        DisplayCaption --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with caption prompt]
        CallVisionModel --> GenerateCaption[Generate detailed image description]
        GenerateCaption --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Caption button disabled until image uploaded]:::note
    Note2[Uses specialized prompt for detailed description]:::note
    Note3[Focuses on objects, people, scenery, colors, and composition]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    GenerateCaption -.-> Note3
```

## Image Summarization Workflow

This diagram presents the workflow for generating comprehensive contextual summaries of uploaded images. Unlike the captioning workflow which focuses on objective description, this process creates more in-depth analysis including context, interpretation, and significance of image elements. This workflow helps users understand not just what appears in an image, but also its broader meaning and implications, providing deeper insights than simple captioning.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickSummarize[Click 'Summarize Image' button]
        WaitForProcessing[Wait for processing] --> ViewSummary[View image summary]
        ViewSummary --> End([End])
    end
    
    subgraph UI
        ClickSummarize --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplaySummary[Display summary in chat]
        DisplaySummary --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with summary prompt]
        CallVisionModel --> GenerateSummary[Generate comprehensive contextual summary]
        GenerateSummary --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Summarize button disabled until image uploaded]:::note
    Note2[More comprehensive than caption]:::note
    Note3[Includes context, analysis, and interpretation]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    GenerateSummary -.-> Note3
```

## Text-to-Speech Conversion Workflow

This diagram details the process of converting AI-generated text responses into spoken audio. It shows how users can select voice types and adjust speech speed before the system processes the text through a TTS model and delivers playable audio. This workflow enhances accessibility by providing an auditory alternative to reading text responses, making the application more inclusive for users with visual impairments or those who prefer audio content.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ChatHistory{Chat history exists?}
        ChatHistory -->|No| NoAction[No action possible]
        ChatHistory -->|Yes| SelectVoice[Select voice type]
        SelectVoice --> AdjustSpeed[Adjust speech speed]
        AdjustSpeed --> ClickTTS[Click 'Play Last Response' button]
        WaitForProcessing[Wait for processing] --> ListenAudio[Listen to audio]
        ListenAudio --> End([End])
    end
    
    subgraph UI
        ClickTTS --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayAudio[Display audio player]
        DisplayAudio --> UpdateStatus[Update TTS status]
    end
    
    subgraph System
        DisableInteraction --> ValidateText{Validate text}
        ValidateText -->|Invalid| ShowError[Show error message]
        ValidateText -->|Valid| ValidateVoice[Validate voice type]
        ValidateVoice --> ValidateSpeed[Validate speed]
        ValidateSpeed --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallTTSModel[Call TTS model]
        CallTTSModel --> GenerateAudio[Generate audio file]
        GenerateAudio --> DownloadAudio[Download audio file]
        DownloadAudio --> CreateTempFile[Create temporary audio file]
        CreateTempFile --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    NoAction --> End([End])
    UpdateStatus --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Voice options: Male/Female with different accents]:::note
    Note2[Speed range: 0.5x to 2.0x]:::note
    Note3[Uses Kokoro TTS model via Replicate API]:::note
    Note4[Temporary audio file created for playback]:::note
    
    SelectVoice -.-> Note1
    AdjustSpeed -.-> Note2
    CallTTSModel -.-> Note3
    CreateTempFile -.-> Note4
```

## Regenerate Response Workflow

This diagram illustrates the process of regenerating an AI response to the last user message. It shows how the system extracts the previous user message, removes the last conversation pair, and processes the message again to generate a new response. This workflow provides users with the ability to get alternative perspectives or answers when they're not satisfied with the initial AI response, enhancing the interactive experience without requiring users to rephrase their questions.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ChatHistory{Chat history exists?}
        ChatHistory -->|No| NoAction[No action possible]
        ChatHistory -->|Yes| ClickRegenerate[Click 'Regenerate' button]
        WaitForProcessing[Wait for processing] --> ViewNewResponse[View new AI response]
        ViewNewResponse --> End([End])
    end
    
    subgraph UI
        ClickRegenerate --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayNewResponse[Display new response in chat]
        DisplayNewResponse --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ExtractLastMessage[Extract last user message]
        ExtractLastMessage --> RemoveLastPair[Remove last conversation pair]
        RemoveLastPair --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| ProcessMessage[Process message with vision model]
        ProcessMessage --> GenerateNewResponse[Generate new AI response]
        GenerateNewResponse --> ProcessingComplete
        APIError --> EnableInteraction
    end
    
    NoAction --> End([End])
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Regenerates response to the last user message]:::note
    Note2[Uses same image but may produce different response]:::note
    Note3[Preserves conversation history except last pair]:::note
    
    ClickRegenerate -.-> Note1
    ProcessMessage -.-> Note2
    RemoveLastPair -.-> Note3
```

## Clear History Workflow

This diagram outlines the process of resetting the application to its initial state. It shows how the system clears the chat history, image gallery, and performance metrics, effectively starting a fresh session. This workflow is essential for privacy and usability, allowing users to quickly remove all traces of previous interactions and start new conversations with different images without having to reload the application.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ClickClear[Click 'Clear History' button]
        ViewReset[View reset interface] --> End([End])
    end
    
    subgraph UI
        ClickClear --> ResetChatbot[Reset chatbot to initial state]
        ResetChatbot --> ClearGallery[Clear image gallery]
        ClearGallery --> ResetMetrics[Reset performance metrics]
        ResetMetrics --> DisableButtons[Disable interaction buttons]
        DisableButtons --> ShowInstruction[Show image upload instruction]
    end
    
    subgraph System
        ShowInstruction --> ResetImageState[Reset image uploaded state]
        ResetImageState --> ClearImageData[Clear image data from memory]
        ClearImageData --> ResetProcessingState[Reset processing state]
    end
    
    ResetProcessingState --> ViewReset
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Completely resets the application state]:::note
    Note2[User must upload a new image to continue]:::note
    
    ClickClear -.-> Note1
    ShowInstruction -.-> Note2
```

## Exception Handling Workflow

This diagram details the system's approach to handling various types of errors that may occur during operation. It illustrates how exceptions are caught, logged, categorized by type, and presented to users with appropriate messages. This workflow is crucial for maintaining system stability and providing a smooth user experience even when problems occur, ensuring that users understand what went wrong and can take appropriate action to resolve issues.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> UserAction[Perform any action]
        ViewError[View error message] --> RetryOption{Retry?}
        RetryOption -->|Yes| UserAction
        RetryOption -->|No| End([End])
    end
    
    subgraph System
        UserAction --> ProcessAction[Process user action]
        ProcessAction --> ExceptionOccurs{Exception occurs?}
        ExceptionOccurs -->|No| CompleteAction[Complete action normally]
        ExceptionOccurs -->|Yes| LogError[Log error details]
        LogError --> DetermineErrorType{Determine error type}
    end
    
    subgraph ErrorHandling
        DetermineErrorType -->|API Error| HandleAPIError[Handle API unavailability]
        DetermineErrorType -->|Image Error| HandleImageError[Handle image processing error]
        DetermineErrorType -->|Model Error| HandleModelError[Handle model execution error]
        DetermineErrorType -->|Other Error| HandleGenericError[Handle generic error]
        
        HandleAPIError --> FormatAPIError[Format API error message]
        HandleImageError --> FormatImageError[Format image error message]
        HandleModelError --> FormatModelError[Format model error message]
        HandleGenericError --> FormatGenericError[Format generic error message]
        
        FormatAPIError --> DisplayError[Display error to user]
        FormatImageError --> DisplayError
        FormatModelError --> DisplayError
        FormatGenericError --> DisplayError
    end
    
    CompleteAction --> End([End])
    DisplayError --> ViewError
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[All errors are logged with details]:::note
    Note2[User-friendly messages hide technical details]:::note
    Note3[System remains in usable state after errors]:::note
    
    LogError -.-> Note1
    DisplayError -.-> Note2
    DisplayError -.-> Note3
```

## System Startup Workflow

This diagram depicts the initialization sequence when the HearSee application is launched. It shows how the system loads environment variables, configures logging, creates the UI theme, initializes components, and sets up event handlers before launching the application. This workflow provides insight into the application's architecture and startup process, illustrating how the various components are initialized and connected to create a cohesive user experience from the moment the application starts.

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph System
        Start([Start]) --> LoadEnvironment[Load environment variables]
        LoadEnvironment --> ConfigureLogging[Configure logging]
        ConfigureLogging --> CreateTheme[Create custom UI theme]
        CreateTheme --> InitializeBlocks[Initialize Gradio Blocks]
        InitializeBlocks --> CreateTabs[Create Chat and Guide tabs]
    end
    
    subgraph ChatTab
        CreateTabs --> CreateChatInterface[Create chat interface components]
        CreateChatInterface --> SetupEventHandlers[Setup event handlers]
        SetupEventHandlers --> ConnectComponents[Connect UI components]
    end
    
    subgraph GuideTab
        CreateTabs --> CreateGuideInterface[Create guide interface]
    end
    
    subgraph Initialization
        ConnectComponents --> ReturnApp[Return app instance]
        CreateGuideInterface --> ReturnApp
        ReturnApp --> LaunchApp[Launch Gradio app]
        LaunchApp --> End([End])
    end
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Loads API keys from .env file]:::note
    Note2[Sets up error logging and monitoring]:::note
    Note3[Creates responsive UI with light theme]:::note
    Note4[Launches in browser automatically]:::note
    
    LoadEnvironment -.-> Note1
    ConfigureLogging -.-> Note2
    CreateTheme -.-> Note3
    LaunchApp -.-> Note4
```

These activity diagrams provide a comprehensive visualization of all key workflows in the HearSee application, including both happy paths and exception handling. The diagrams use consistent notation throughout and clearly represent the system boundaries and actor responsibilities through swimlanes.